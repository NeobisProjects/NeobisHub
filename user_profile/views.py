from django.contrib.auth import authenticate, login, get_user_model
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from user_profile.constants import UserNotActive, BadAuthorization, WrongValidationCode, UserDoesNotExist, \
    SuccessfulValidation
from user_profile.errors import DuplicateUserError
from user_profile.models import UserProfile
from user_profile.serializers import UserCreateSerializer, UserSerializer, UserProfileSerializer, UserUpdateSerializer
from user_profile.services import UserService, ValidateUserService

User = get_user_model()


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

    @staticmethod
    def post(request, *args, **kwargs):
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
                return Response(UserNotActive, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(BadAuthorization, status=status.HTTP_404_NOT_FOUND)


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = UserProfile.objects.all()


class UserProfileRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class CodeValidationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            data_to_validate = self.request.data['validate_field']
            user_id = self.request.data['user_id']
            user_profile = ValidateUserService.get_user_profile(user_id=user_id)

            if data_to_validate == user_profile.validation_code:
                user = ValidateUserService.change_user_status(user_id=user_id)

                ValidateUserService.get_user_token(user=user)

                return Response(SuccessfulValidation, status=status.HTTP_200_OK)
            else:
                return Response(WrongValidationCode, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(UserDoesNotExist, status=status.HTTP_404_NOT_FOUND)

# TODO: восстановление пароля или регистрация :страница ввода кода
# class UserForgotPassword(APIView): # TODO: восстановление пароля:страница ввода имейла и отправки кода валидации
# class
