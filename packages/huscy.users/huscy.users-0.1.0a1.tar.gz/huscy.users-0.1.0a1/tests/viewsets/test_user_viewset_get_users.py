from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


def test_admin_user_can_list_users(admin_client):
    response = list_users(admin_client)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_list_users(client):
    response = list_users(client)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_list_users(anonymous_client):
    response = list_users(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def list_users(client):
    return client.get(reverse('user-list'))
