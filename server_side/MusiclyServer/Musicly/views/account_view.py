from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from json import loads as load_json
from ..models import Account, PasswordResetToken
from ..serializers import AccountSerializer, AccountDetailsSerializer, AccountLifecycleSerializer
from password_strength import PasswordPolicy
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail


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


@api_view(['GET'])
@permission_classes([])
def send_mail(request):
    placeholder = 'sike! it\'s a wrong number!'
    send_mail(
        subject='Musicly password reset',
        message='Click the link below to reset your Musicly password.'
                'Ignore this message if you did not started the password reset procedure.'
                f'{placeholder}',
        from_mail='noreply@musicly.com',
        recipient_list=['waclawiak.pawel@wp.pl']
    )


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

    token = '%032x' % getrandbits(256)
    print(token)
    reset_token = PasswordResetToken(account=account, token=token, expires_at=now()+timedelta(hours=48))
    try:
        reset_token.save()
    except Exception as e:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'details': 'could not create a token.'})

    # TODO: finish sending mail, take care of backend and probably connection
    # implement possibility for password change when you are logged in
    send_mail(
        subject='Musicly password reset',
        message='Click the link below to reset your Musicly password.'
                'Ignore this message if you did not started the password reset procedure.'
                f'{reset_token}',
        from_mail='noreply@musicly.com',
        recipient_list=[account.email]
    )
    return Response(status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def change_password(request):
    data = load_json(request.body)

    missing_data = {}
    for argument in ['password_reset_token', 'password']:
        if argument not in data.keys():
            missing_data[argument] = ['value has not been provided.']
    if len(missing_data.keys()):
        return Response(status=400, data=missing_data)

    reset_token = data['password_reset_token']
    password = data['password']
    account = request.user

    try:
        password_reset_token = PasswordResetToken.objects.get(account=account)
    except PasswordResetToken.DoesNotExist:
        return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'password reset token does not exist.'})

    if reset_token != password_reset_token.token:
        return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'incorrect password reset token provided.'})
    if now() > reset_token.expires_at:
        return Response(status=status.HTTP_403_FORBIDDEN, data={'details': 'password reset token has expired.'})

    if _password_secure(password):
        account.set_password(password)
        password_reset_token.delete()

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

        # account_template = load_json(request.body)
        # print(account_template)
        # serializer = AccountDetailsSerializer(data=account_template)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(True)
        # else:
        #     return Response(serializer.errors)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
