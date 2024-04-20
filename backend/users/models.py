import random
import string

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from users.manager import MyUserManager
from users.utils import generate_confirmation_code


def generate_unique_referral_code() -> str:
    """Создаем уникальный реферальный код."""
    # Создаем список из символов латинского алфавита и цифр
    characters = string.ascii_letters + string.digits
    while True:
        # Генерируем случайную строку заданной длины
        random_string = "".join(random.choice(characters) for _ in range(6))
        # Проверяем, уникальна ли строка
        if not User.objects.filter(referral_code=random_string).exists():
            return random_string


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя."""

    USERNAME_FIELD = "phone"

    phone = models.CharField(
        verbose_name="Номер телефона",
        max_length=20,
        blank=False,
        unique=True,
    )
    is_staff = models.BooleanField(
        "Является модератором",
        default=False,
    )
    is_superuser = models.BooleanField(
        "Является админом",
        default=False,
    )
    confirmation_code = models.IntegerField(
        "Код подтверждения",
        default=generate_confirmation_code,
    )
    code_request_date = models.DateTimeField(
        "Дата запроса кода подтверждения",
        default=timezone.now,
    )
    referral_code = models.CharField(
        "Реферральный код",
        max_length=6,
        unique=True,
        default="FIRST1",
    )
    used_referral_code = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        to_field="referral_code",
        db_column="referral_by",
        related_name="referrals",
        verbose_name="Введенный реферальный код",
        blank=True,
        null=True,
    )

    objects = MyUserManager()

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.phone


@receiver(pre_save, sender=User)
def set_referral_code(sender, instance: User, **kwargs) -> None:
    """Присваеваем реферальный код перед созданием модели."""
    if instance.referral_code == "FIRST1":
        instance.referral_code = generate_unique_referral_code()
