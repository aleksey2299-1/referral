# flake8: noqa
import pytest
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


@pytest.fixture(scope="function")
def create_users(db):
    for i in range(1, 6):
        User.objects.create(
            id=i,
            phone=f"+7999999999{i}",
        )


@pytest.fixture(scope="function")
def create_referrals(create_users):
    parent_user = User.objects.get(id=1)
    for i in range(2, 5):
        user = User.objects.get(id=i)
        user.used_referral_code = parent_user
        user.save()


@pytest.fixture(scope="function")
def get_token(create_users, request):
    id = request.param
    token = RefreshToken.for_user(User.objects.get(id=id))
    return str(token.access_token)
