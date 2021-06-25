from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import (CreateAPIView, RetrieveAPIView)
# from configs.backends import JWTAuthentication
from .serializers import RegisterSerializer, LoginSerializer, CustomerSerializer


class RegisterUserView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUserView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthMeView(RetrieveAPIView):
    # authentication_classes = [JWTAuthentication,]
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)