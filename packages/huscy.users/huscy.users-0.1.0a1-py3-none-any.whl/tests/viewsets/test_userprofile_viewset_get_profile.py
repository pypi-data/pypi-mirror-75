from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


def test_admin_user_can_retrieve_profile(admin_client):
    response = retrieve_profile(admin_client)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_retrieve_profile(client):
    response = retrieve_profile(client)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_retrieve_profile(anonymous_client):
    response = retrieve_profile(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_profile_created(django_db_reset_sequences, client, user):
    response = retrieve_profile(client)

    expected_json = dict(id=1, prefered_language='en', user=user.id)

    assert expected_json == response.json()


def retrieve_profile(client):
    return client.get(reverse('userprofile-detail', kwargs=dict(pk='any_value')))
