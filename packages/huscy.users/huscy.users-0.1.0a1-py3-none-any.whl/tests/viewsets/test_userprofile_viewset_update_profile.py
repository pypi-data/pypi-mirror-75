from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


def test_admin_user_can_update_profile(admin_client):
    response = update_profile(admin_client)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_update_profile(client):
    response = update_profile(client)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_update_profile(anonymous_client):
    response = update_profile(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_profile_updated(django_db_reset_sequences, client, user):
    response = update_profile(client)

    expected_json = dict(id=1, prefered_language='de', user=user.id)

    assert expected_json == response.json()


def update_profile(client):
    return client.put(
        reverse('userprofile-detail', kwargs=dict(pk='any_value')),
        data=dict(prefered_language='de'),
    )
