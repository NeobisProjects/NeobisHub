from django.contrib.auth import authenticate, login, get_user_model
from rest_framework import generics
from rest_framework import permissions, status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.constants import UserNotActive, BadAuthorization, \
    WrongValidationCode, UserDoesNotExist, SuccessfulValidation
from user_profile.errors import DuplicateUserError
from user_profile.models import UserProfile
from user_profile.permissions import IsOwnerOrAdmin
from user_profile.serializers import UserCreateSerializer, UserSerializer, \
    UserProfileSerializer, UserProfileUpdateSerializer
from user_profile.services import UserService, ValidateUserService
from user_profile.utils import Validate

User = get_user_model()


class UserCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
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
    def post(request):
        data = request.data

        username = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            profile = ValidateUserService.get_user_profile_by_id(user_id=user.id)
            if user.is_active:
                login(request, user)
                token = Token.objects.get_or_create(user=user)
                data = {
                    'user_id': user.id,
                    'surname': profile.surname,
                    'name': profile.name,
                    'patronymic': profile.patronymic,
                    'status': profile.status,
                    'token': str(token[0])
                }

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(UserNotActive, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(BadAuthorization, status=status.HTTP_404_NOT_FOUND)


class UserProfileUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileUpdateSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    # IsOwnerOrAdmin

    # def permission_by_id(self):
    #     return bool(self.request.user.id is self.kwargs.get('pk'))
    # TODO: как передать d изменяемого профиля?


class UserProfileRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserProfileListByNameView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().order_by('name')
    filter_backends = (SearchFilter,)
    search_fields = ('surname', 'name', 'patronymic')


class UserProfileListByDepartmentView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().order_by('department')
    filter_backends = (SearchFilter,)
    search_fields = ('surname', 'name', 'patronymic')


class UserProfileListByCongestionView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().order_by('congestion')
    filter_backends = (SearchFilter,)
    search_fields = ('surname', 'name', 'patronymic')


class CodeValidationView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        try:
            data_to_validate = request.data['validate_field']
            user_id = request.data['user_id']
            user_profile = ValidateUserService.get_user_profile_by_id(user_id=user_id)

            if data_to_validate == user_profile.validation_code:
                user = ValidateUserService.change_user_status(user_id=user_id)

                ValidateUserService.get_user_token(user=user)

                return Response(SuccessfulValidation, status=status.HTTP_200_OK)
            else:
                return Response(WrongValidationCode, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(UserDoesNotExist, status=status.HTTP_404_NOT_FOUND)


# TODO: написаать отправку сообщения и подтверждение статуса HQ пользователя


class UserForgotPassword(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            email = request.data['email']
            user = User.objects.get(email=email)
            user_profile = UserProfile.objects.get(user=user.id)
            if user_profile:
                code = Validate.create_validation_code()
                user_profile.validation_code = code
                user_profile.save()
                Validate.send_email_with_code(user, code)

            return Response({"user_id": user.id}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(UserDoesNotExist, status=status.HTTP_404_NOT_FOUND)


class PasswordRecovery(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        try:
            code = request.data['code']
            user_id = request.data['user_id']
            password = request.data['password']
            user = User.objects.get(id=user_id)
            user_profile = ValidateUserService.get_user_profile_by_id(user_id=user_id)

            if code == user_profile.validation_code:
                if password == request.data['password_repeat']:

                    user.password = password
                    user.set_password(user.password)
                    user.save()
                else:
                    raise serializers.ValidationError(detail='Ваши пароли не совпадают')

                return Response({"Message": 'Success'}, status=status.HTTP_200_OK)
            else:
                return Response({"Message": 'Wrong Code'}, status=status.HTTP_400_BAD_REQUEST)

        except UserProfile.DoesNotExist:
            return Response(UserDoesNotExist, status=status.HTTP_404_NOT_FOUND)
