import datetime as dt

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import permissions, serializers, status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    throttle_classes,
)
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserLoginSerializer, UserSerializer
from users.throttles import CodeRequestThrottle
from users.utils import generate_confirmation_code


def create_confirmation_code(user: User) -> int:
    """Создание кода подтверждения."""
    code = generate_confirmation_code()
    user.code_request_date = timezone.now()
    user.confirmation_code = code
    user.save()
    return code


def check_confirmation_code(user: User, code: int) -> Response | None:
    """Проверка кода подтверждения."""
    if user.code_request_date < timezone.now() - dt.timedelta(minutes=5):
        raise ValidationError(
            _("Срок действия кода подтверждения истёк."),
            status.HTTP_400_BAD_REQUEST,
        )
    if user.confirmation_code != code:
        raise ValidationError(
            _("Неправильные данные."), status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    request=UserLoginSerializer(),
    responses={
        200: inline_serializer("token", {"token": serializers.CharField()})
    },
)
@api_view(("POST",))
@permission_classes((permissions.AllowAny,))
@throttle_classes((CodeRequestThrottle,))
def user_login(request: Request) -> Response:
    """View для авторизации."""
    data = request.data
    user = User.objects.filter(phone=data.get("phone")).first()
    if not user:
        serializer = UserLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
    if data.get("send_code") is True:
        code = create_confirmation_code(user)
        return Response(
            {
                "detail": _("Чтобы войти введите код подтверждения."),
                "confirmation_code": code,
            },
            status.HTTP_200_OK,
        )
    check_confirmation_code(user, data.get("confirmation_code"))
    token = RefreshToken.for_user(user)
    return Response(
        data={"token": str(token.access_token)}, status=status.HTTP_200_OK
    )


@extend_schema_view(
    get=extend_schema(responses=UserSerializer()),
    patch=extend_schema(request=UserSerializer(), responses=UserSerializer()),
)
class RetriveUser(APIView):
    """View для профиля пользователя."""

    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ("get", "patch")

    def get(self, request: Request) -> Response:
        """Возвращает профиль пользователя."""
        user = request.user
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request) -> Response:
        """Изменяет информацию о пользователе."""
        user = request.user
        data = request.data
        serializer = UserSerializer(user, data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
