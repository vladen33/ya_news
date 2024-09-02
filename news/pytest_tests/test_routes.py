from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

LAZY___EDIT = pytest.lazy_fixture('url_edit')
LAZY_DELETE = pytest.lazy_fixture('url_delete')
LAZY___HOME = pytest.lazy_fixture('url_home')
LAZY_SIGNUP = pytest.lazy_fixture('url_signup')
LAZY__LOGIN = pytest.lazy_fixture('url_login')
LAZY_LOGOUT = pytest.lazy_fixture('url_logout')
LAZY_DETAIL = pytest.lazy_fixture('url_detail')
LAZY_AUTHOR_____CLIENT = pytest.lazy_fixture('author_client')
LAZY_NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')
LAZY_ANONYMOUS__CLIENT = pytest.lazy_fixture('anonymous_client')


@pytest.mark.parametrize('url', (LAZY___EDIT, LAZY_DELETE))
@pytest.mark.django_db
def test_redirect_for_anonymous_client(url, client, url_login):
    response = client.get(url)
    assertRedirects(response, f'{url_login}?next={url}')


@pytest.mark.parametrize(
    'url, client, status', (
        (LAZY___EDIT, LAZY_AUTHOR_____CLIENT, HTTPStatus.OK),
        (LAZY_DELETE, LAZY_AUTHOR_____CLIENT, HTTPStatus.OK),
        (LAZY___EDIT, LAZY_NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (LAZY_DELETE, LAZY_NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (LAZY___HOME, LAZY_ANONYMOUS__CLIENT, HTTPStatus.OK),
        (LAZY_SIGNUP, LAZY_ANONYMOUS__CLIENT, HTTPStatus.OK),
        (LAZY__LOGIN, LAZY_ANONYMOUS__CLIENT, HTTPStatus.OK),
        (LAZY_LOGOUT, LAZY_ANONYMOUS__CLIENT, HTTPStatus.OK),
        (LAZY_DETAIL, LAZY_ANONYMOUS__CLIENT, HTTPStatus.OK),
    )
)
@pytest.mark.django_db
def test_pages_availability_for_author(url, client, status):
    response = client.get(url)
    assert response.status_code == status
