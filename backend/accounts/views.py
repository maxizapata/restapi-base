from django.contrib.auth import get_user_model
from random import randrange
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


from .serializers import (
    UserSerializer,
    UpdateUserSerializer,
    MobileTokenSerializer)


from .tasks import send_mobile_token

from .models import MobileToken


class SignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': 'request'})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        user_data = {
            'id': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'mobile': user.get_mobile(),
            'role': user.role,
        }
        return Response(user_data, status=status.HTTP_201_CREATED)


class LogOutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserInfoView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UpdateUserSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_204_NO_CONTENT)


class MobileTokenView(APIView):
    def post(self, request, format=None):
        token = randrange(000000, 999999)
        user_id = request.user.id
        serializer = MobileTokenSerializer(data={
            'user': user_id,
            'token': token
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_mobile_token.delay(serializer.data['id'])
        return Response('Patch OK', status=status.HTTP_201_CREATED)

    def patch(self, request, format=None):
        # DB token is created when call MobileTokenView
        db_token = MobileToken.objects\
            .filter(user=request.user.id).latest('created_at')
        if db_token.is_expired:
            return Response(
                "Token is expired",
                status=status.HTTP_400_BAD_REQUEST
            )
        # request_token is the incoming request token
        request_token = request.data['token']
        if db_token.token == request_token:
            request.user.verified_mobile = True
            request.user.save()
            db_token.is_expired = True
            db_token.save()
            return Response(
                'Mobile phone has been verified',
                status=status.HTTP_200_OK)
        return Response(
            "Token do not match", status=status.HTTP_400_BAD_REQUEST)
