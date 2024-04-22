from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.mark.django_db
@pytest.mark.parametrize("get_token", [1], indirect=True)
def test_user_profile(client: APIClient, create_referrals, get_token):
    client.force_login(User.objects.get(id=1))

    url = "/api/v1/profile/"

    response = client.get(
        url, headers={"Authorization": f"Bearer {get_token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["phone"] == "+79999999991"
    assert response.json()["used_referral_code"] is None
    assert isinstance(response.json()["referral_code"], str)
    assert len(response.json()["referrals"]) == 3


@pytest.mark.django_db
def test_anonim_profile(client: APIClient, create_users):
    url = "/api/v1/profile/"

    response = client.get(url)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
