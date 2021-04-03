from rest_framework import status
from rest_framework.response import Response
from ..models import Account, PasswordResetToken
from ..serializers import AccountDetailsSerializer, AccountLifecycleSerializer
from password_strength import PasswordPolicy
from rest_framework.decorators import api_view, permission_classes

import django.utils.timezone as time
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db import DatabaseError

from rest_framework.authtoken.models import Token
from random import getrandbits
from hashlib import sha256
from smtplib import SMTPException


password_policy = PasswordPolicy.from_names(
    length=8,
    uppercase=1,
    nonletters=1
)


def _password_secure(password: str):
    if not len(password_policy.test(password)):
        return True
    else:
        return False


def send_confirmation_mail(account: Account, server_address):
    send_mail(
        subject='Email confirmation',
        message='This is an automated email confirmation message from Musicly.\n\n'
                'Go to the link below to confirm your email address for Musicly account.'
                f'{server_address}/api/confirmEmail/{account.id}/{sha256(account.email.encode()).hexdigest()}\n',
        html_message=render_to_string('email_confirm_mail.html', {'server_address': server_address,
                                                                  'account_id': account.id,
                                                                  'token': sha256(account.email.encode()).hexdigest()}),
        from_email='"noreply@musicly.com" <noreply@musicly.com>',
        recipient_list=[account.email],
        fail_silently=False
    )


@api_view(['GET'])
def resend_confirmation_mail(request):
    server_address = 'http://' + request.get_host()
    try:
        send_confirmation_mail(request.user, server_address)
    except SMTPException:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'details': 'could not send a mail.'})
    return Response(status=status.HTTP_200_OK, data={'details': 'email has been sent.'})


@api_view(['POST'])
@permission_classes([])
def register(request):
    server_address = 'http://' + request.get_host()
    account_info = request.data
    serializer = AccountLifecycleSerializer(data=account_info)

    restricted_chars = '@\/\'"'
    for char in restricted_chars:
        if char in account_info['username']:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={'details': f'username cannot contain this set of characters: {restricted_chars}'})

    if not _password_secure(account_info['password']):
        return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'password is too weak.'})

    if serializer.is_valid():
        account = Account.objects.create(username=account_info['username'],
                                         email=account_info['email'])
        account.set_password(account_info['password'])
        try:
            account.save()
            token = {"token": Token.objects.get(user=account).key}
        except DatabaseError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            send_confirmation_mail(account, server_address)
        except SMTPException:
            return Response(status=status.HTTP_201_CREATED, data={'details': 'account created',
                                                                  'errors': 'could not send confirmation email'})
        return Response(status=status.HTTP_201_CREATED, data=token)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN, data=serializer.errors)


@api_view(['GET'])
@permission_classes([])
def confirm_email(request, pk, token):
    try:
        user = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'details': 'user with this id does not exist.'})
    confirmation_token = sha256(user.email.encode()).hexdigest()
    if token == confirmation_token:
        user.email_confirmed = True
        try:
            user.save()
            return Response(status=status.HTTP_200_OK, data={'details': 'email address confirmed.'})
        except DatabaseError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data={'details': 'server error, could not confirm email.'})
    else:
        return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'incorrect token provided.'})


@api_view(['POST'])
@permission_classes([])
def create_reset_token(request):
    account_info = request.data
    try:
        account = Account.objects.get(username=account_info['username_or_email'])
    except Account.DoesNotExist:
        try:
            account = Account.objects.get(email=account_info['username_or_email'])
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'details': 'wrong account identifier'})

    try:
        old_token = PasswordResetToken.objects.get(account=account)
        old_token.delete()
    except PasswordResetToken.DoesNotExist:
        pass

    token = '%032x' % getrandbits(256)
    reset_token = PasswordResetToken(account=account, token=token, expires_at=time.now() + time.timedelta(hours=48))

    try:
        reset_token.save()
    except DatabaseError:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'details': 'could not create a token.'})

    # TODO: implement possibility for password change when you are logged in
    send_mail(
        subject='Musicly password reset',
        message='This is an automated password reset message from Musicly.\n'
                'Ignore it if you did not start the password reset procedure.\n\n'
                'Copy and paste the token below into your application.'
                f'{reset_token.token}\n',
        html_message=render_to_string('password_reset_mail.html', {'token': reset_token.token}),
        from_email='"noreply@musicly.com" <noreply@musicly.com>',
        recipient_list=['waclawiak.pawel@wp.pl'],
        fail_silently=False
    )
    return Response(status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([])
def change_password(request):
    data = request.data

    missing_data = {}
    for argument in ['password_reset_token', 'new_password']:
        if argument not in data.keys():
            missing_data[argument] = ['value has not been provided.']
    if len(missing_data.keys()):
        return Response(status=400, data=missing_data)

    reset_token = data['password_reset_token']
    password = data['new_password']

    try:
        password_reset_token = PasswordResetToken.objects.get(token=reset_token)
        if time.now() > password_reset_token.expires_at:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'password reset token has expired.'})
    except PasswordResetToken.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'password reset token does not exist.'})

    try:
        account = password_reset_token.account
    except Account.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'reset token not assigned to any account.'})

    if _password_secure(password):
        account.set_password(password)
        account.save()
        password_reset_token.delete()
    else:
        return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'password does not meet security criteria.'})

    return Response(status=status.HTTP_200_OK, data={'details': 'password changed successfully.'})


@api_view(['GET'])
def account_details(request):
    account = request.user
    serializer = AccountDetailsSerializer(account)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@api_view(['DELETE'])
def delete_account(request):

    try:
        account = Account.objects.get(pk=request.user.id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'details': 'account does not exist.'})

    if account.delete():
        return Response(status=status.HTTP_200_OK, data={'details': 'account deleted.'})
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        data={'details': 'server error, could not delete the account.'})


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
