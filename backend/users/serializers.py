from django.contrib.auth import get_user_model

from djoser.conf import settings as djoser_settings
from djoser.serializers import UserSerializer

from rest_framework import serializers, validators
from rest_framework.fields import CurrentUserDefault

from recipes.models import Recipe
from .models import Subscription
from .validators import UniqueValuesValidator

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            djoser_settings.USER_ID_FIELD,
            djoser_settings.LOGIN_FIELD,
            'is_subscribed',
        )
        read_only_fields = (djoser_settings.LOGIN_FIELD,)


class SubscriptionSerializer(serializers.ModelSerializer):
    from_user = serializers.HiddenField(default=CurrentUserDefault())
    to_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Subscription
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                Subscription.objects.all(),
                fields=('from_user', 'to_user'),
                message='You are already subscribed to the user.',
            ),
            UniqueValuesValidator(
                fields=('from_user', 'to_user'),
                message='You cannot subscribe to yourself.',
            ),
        ]


class BaseRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserRecipesSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            djoser_settings.USER_ID_FIELD,
            djoser_settings.LOGIN_FIELD,
            'is_subscribed',
            'recipes',
        )
        read_only_fields = (djoser_settings.LOGIN_FIELD,)

    def get_recipes(self, obj):
        request = self.context.get('request')
        queryset = obj.recipes.all()
        if request is not None:
            recipes_limit = request.query_params.get('recipes_limit')
            if recipes_limit is not None:
                try:
                    queryset = queryset[:int(recipes_limit)]
                except ValueError:
                    pass
        return BaseRecipeSerializer(queryset, many=True).data
