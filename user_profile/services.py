from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError

from department.models import Department
from user_profile.errors import DuplicateUserError
from user_profile.models import UserProfile

User = get_user_model()


class UserService:
    @classmethod
    @transaction.atomic
    def create_user_with_profile(cls, data: dict, user: User) -> User:
        try:
            user = User.objects.create_user(email=data['email'],
                                            password=data['password'], )
        except User.DoesNotExist:
            raise ObjectDoesNotExist('user does not exist')
        except IntegrityError:
            raise DuplicateUserError()

        UserProfile.objects.create(user=user, name=data['name'], phone=data['phone'],
                                   department=Department.objects.get(id=data['department']),
                                   telegram=data['telegram'], status=data['status'], congestion=data['congestion'],
                                   resume=data['resume'])

        return user
