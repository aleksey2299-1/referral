from http import HTTPStatus

import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.mark.django_db
def test_login(client: APIClient):
    url = "/api/v1/login/"

    data = {
        "phone": "+3 (333) 333-33-33",
        "send_code": True,
    }

    response = client.post(url, data, content_type="application/json")
    print(response.json())
    assert response.status_code == HTTPStatus.OK
    assert "confirmation_code" in response.json()

    data["confirmation_code"] = response.json()["confirmation_code"]
    data.pop("send_code")

    response = client.post(url, data, content_type="application/json")
    assert response.status_code == HTTPStatus.OK
    assert "token" in response.json()
    token = response.json()["token"]

    url = "/api/v1/profile/"

    response = client.get(url, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_invalid_phone_login(client: APIClient):
    url = "/api/v1/login/"

    data = {
        "phone": "3 (333) 333-33-33",
        "send_code": True,
    }

    response = client.post(url, data, content_type="application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST

    data = {
        "phone": "+7 (333) 333-33-33",
        "send_code": True,
    }

    response = client.post(url, data, content_type="application/json")
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.parametrize("get_token", [1], indirect=True)
def test_use_refferal_code(client: APIClient, create_users, get_token):
    client.force_login(User.objects.get(id=1))

    url = "/api/v1/profile/"
    referral_code = User.objects.get(id=2).referral_code

    print(get_token)

    response = client.patch(
        url,
        {"used_referral_code": referral_code},
        content_type="application/json",
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()["used_referral_code"] == referral_code


@pytest.mark.django_db
@pytest.mark.parametrize("get_token", [1], indirect=True)
def test_use_invalid_refferal_code(client: APIClient, create_users, get_token):
    client.force_login(User.objects.get(id=1))

    url = "/api/v1/profile/"
    referral_code = User.objects.get(id=1).referral_code

    response = client.patch(
        url,
        {"used_referral_code": referral_code},
        content_type="application/json",
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST

    referral_code = "hi_man"
    response = client.patch(
        url,
        {"used_referral_code": referral_code},
        content_type="application/json",
        headers={"Authorization": f"Bearer {get_token}"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
