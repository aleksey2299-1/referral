from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password


class MyUserManager(BaseUserManager):
    """
    Кастомный менеджер для модели User.
    """

    def _create_user(
        self, phone: str, password: str, **extra_fields: Any
    ) -> AbstractBaseUser:
        """
        Создает и сохраняет пользователя с телефоном.
        """
        user = self.model(phone=phone, **extra_fields)
        user.password = make_password(password)
        user.save()

    def create_user(self, phone: str, **extra_fields: Any) -> AbstractBaseUser:
        """
        Создает пользователя.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            phone, self.make_random_password, **extra_fields
        )

    def create_superuser(
        self, phone: str, password: str, **extra_fields: Any
    ) -> AbstractBaseUser:
        """
        Создает суперюзера.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(phone, password, **extra_fields)
