from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
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
        if not validated_data.get("used_referral_code"):
            raise ValidationError(
                _("Некорректный реферальный код."), status.HTTP_400_BAD_REQUEST
            )
        if instance.used_referral_code:
            raise ValidationError(
                _("Вы уже использовали реферальный код."),
                status.HTTP_400_BAD_REQUEST,
            )
        if instance == validated_data.get("used_referral_code"):
            raise ValidationError(
                _("Вы не можете использовать свой реферальный код."),
                status.HTTP_400_BAD_REQUEST,
            )
        return super().update(instance, validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    """Класс сериализатора для авторизации."""

    send_code = serializers.BooleanField(required=False)
    confirmation_code = serializers.IntegerField(
        required=False, write_only=True
    )
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields = ("phone", "send_code", "confirmation_code")

    def create(self, validated_data: dict):
        validated_data.pop("send_code")
        return super().create(validated_data)
