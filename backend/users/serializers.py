from django.contrib.auth import get_user_model

from djoser.serializers import UserCreateSerializer

User = get_user_model()


class UserCreateExtendedSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            'first_name',
            'last_name',
            'password',
        )
