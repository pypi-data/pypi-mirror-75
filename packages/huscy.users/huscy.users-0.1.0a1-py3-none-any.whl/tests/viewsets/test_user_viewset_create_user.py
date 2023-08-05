from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from django.contrib.auth.models import Permission


def test_admin_user_can_create_users(admin_client):
    response = create_user(admin_client)

    assert response.status_code == HTTP_201_CREATED


def test_user_with_permission_cannot_create_users(client, user):
    add_permission = Permission.objects.get(codename='add_user')
    user.user_permissions.add(add_permission)

    response = create_user(client)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_user_without_permission_cannot_create_users(client):
    response = create_user(client)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_create_users(anonymous_client):
    response = create_user(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def create_user(client):
    return client.post(reverse('user-list'), data=dict(username='username', password='password'))
