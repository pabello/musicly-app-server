from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from json import loads as load_json
from ..models import Account, PasswordResetToken
from ..serializers import AccountSerializer, AccountDetailsSerializer, AccountLifecycleSerializer
from password_strength import PasswordPolicy
from rest_framework.decorators import api_view, permission_classes

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import django.utils.timezone as time
from django.core.mail import send_mail
from django.template.loader import render_to_string


from rest_framework.authtoken.models import Token
from random import getrandbits


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


@api_view(['POST'])
@permission_classes([])
def register(request):
    account_info = load_json(request.body)
    serializer = AccountLifecycleSerializer(data=account_info)

    if serializer.is_valid():
        account = Account.objects.create(username=account_info['username'],
                                         email=account_info['email'])
        account.set_password(account_info['password'])
        try:
            account.save()
            token = {"token": Token.objects.get(user=account).key}
        except ValueError:
            pass
        return Response(status=status.HTTP_201_CREATED, data=token)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([])
def create_reset_token(request):
    account_info = load_json(request.body)
    try:
        account = Account.objects.get(username=account_info['username'])
    except Account.DoesNotExist:
        try:
            account = Account.objects.get(email=account_info['email'])
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'details': 'wrong account identifier'})

    try:
        old_token = PasswordResetToken.objects.get(account=account)
        old_token.delete()
    except PasswordResetToken.DoesNotExist:
        pass

    token = '%032x' % getrandbits(256)
    print(token)
    reset_token = PasswordResetToken(account=account, token=token, expires_at=time.now() + time.timedelta(hours=48))

    try:
        reset_token.save()
    except Exception as e:
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
    data = load_json(request.body)

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

    return Response(status=status.HTTP_204_NO_CONTENT)


class AccountViewSet(viewsets.ViewSet):
    @staticmethod
    def retrieve(request, pk):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountDetailsSerializer(account)
        return Response(serializer.data)

    @staticmethod
    def destroy(request, pk):
        try:
            account = Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

        # TODO: validation if the deleter owns the account

        if account.delete():
            return Response(status.HTTP_204_NO_CONTENT)
        else:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
