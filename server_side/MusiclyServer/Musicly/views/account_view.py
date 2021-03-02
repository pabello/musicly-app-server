from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from json import loads as load_json
from ..models import Account, PasswordResetToken
from ..serializers import AccountSerializer, AccountDetailsSerializer, AccountLifecycleSerializer
from hashlib import sha256
from datetime import datetime


class AccountViewSet(viewsets.ViewSet):
    @staticmethod
    def retrieve(request, pk):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountDetailsSerializer(account)
        return Response(serializer.data)

    @staticmethod
    def create(request):
        account_info = load_json(request.body)
        password_hash = sha256(account_info['password'].encode()).hexdigest()

        account_template = {
            'username': account_info['username'],
            'email': account_info['email'],
            'password_hash': password_hash,
            'confirmed': False,
            'last_login_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        serializer = AccountLifecycleSerializer(data=account_template)
        if serializer.is_valid():
            serializer.save()
            return Response(status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

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