from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.errors import DuplicateUserError
from user_profile.serializers import UserCreateSerializer, UserSerializer
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
