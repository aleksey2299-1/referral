from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User


class RefferalSerializer(serializers.ModelSerializer):
    """Класс сериализатора для рефералов."""

    class Meta:
        model = User
        fields = ("phone",)


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора для профиля пользователя."""

    referrals = RefferalSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("phone", "referral_code", "used_referral_code", "referrals")
        read_only_fields = ("phone", "referral_code")

    def update(self, instance: User, validated_data: dict):
        if instance.used_referral_code:
            raise ValidationError("You can use only one referral code")
        if instance == validated_data["used_referral_code"]:
            raise ValidationError("You cant use your referral code")
        return super().update(instance, validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """Класс сериализатора для авторизации."""

    send_code = serializers.BooleanField(required=False)
    confirmation_code = serializers.IntegerField(
        required=False, write_only=True
    )

    class Meta:
        model = User
        fields = ("phone", "send_code", "confirmation_code")
