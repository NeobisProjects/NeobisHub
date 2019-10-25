from django.contrib.auth import authenticate, login
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from user_profile.errors import DuplicateUserError
from user_profile.models import UserProfile
from user_profile.serializers import UserCreateSerializer, UserSerializer, UserProfileSerializer, UserUpdateSerializer
from user_profile.services import UserService


class UserCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data=serializer.errors, status=400)
        try:
            user = UserService.create_user_with_profile(serializer.validated_data, request.user)
        except DuplicateUserError as e:
            return Response(data=e.message, status=400)

        return Response(UserSerializer(instance=user).data, status=200)


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data

        username = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                token = Token.objects.get_or_create(user=user)
                data = {
                    'user_id': user.id,
                    'token': str(token[0])
                }

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'Message': 'User Not Activate'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'Message': 'Bad Authorization'}, status=status.HTTP_404_NOT_FOUND)


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = UserProfile.objects.all()


# class CodeValidationView(APIView): # TODO: восстановление пароля или регистрация :страница ввода кода
# class UserForgotPassword(APIView): # TODO: восстановление пароля:страница ввода имейла и отправки кода валидации
# class
