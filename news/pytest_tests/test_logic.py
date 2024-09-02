from http import HTTPStatus
from random import choice

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Текст комментария'}
NEW_COMMENT_TEXT = 'Обновленный текст комментария'


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, url_detail):
    count_before = Comment.objects.count()
    client.post(url_detail, data=FORM_DATA)
    count_after = Comment.objects.count()
    assert count_after - count_before == 0


@pytest.mark.django_db
def test_authorised_user_can_create_comment(author_client, url_detail):
    count_before = Comment.objects.count()
    response = author_client.post(url_detail, data=FORM_DATA)
    count_after = Comment.objects.count()
    assert count_after - count_before == 1
    assertRedirects(response, f'{url_detail}#comments')
    comm = Comment.objects.get()
    assert comm.text == FORM_DATA['text']


def test_user_cants_use_badwords(author_client, url_detail):
    random_bad_word = choice(BAD_WORDS)
    bad_words_data = {'text': f'Мой комментарий: {random_bad_word}'}
    count_before = Comment.objects.count()
    response = author_client.post(url_detail, data=bad_words_data)
    count_after = Comment.objects.count()
    assert count_after - count_before == 0
    assertFormError(response, 'form', 'text', errors=WARNING)


def test_author_can_edit_comment(author_client, url_comment,
                                 url_edit, comment):
    response = author_client.post(url_edit, data={'text': NEW_COMMENT_TEXT})
    assertRedirects(response, url_comment + '#comments')
    comment.refresh_from_db()
    assert comment.text == NEW_COMMENT_TEXT


def test_user_cant_edit_comment_of_another_user(not_author_client,
                                                url_edit, comment):
    original_comment_text = comment.text
    response = not_author_client.post(url_edit,
                                      data={'text': NEW_COMMENT_TEXT})
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == original_comment_text


def test_author_can_delete_comment(author_client, url_comment, url_delete):
    count_before = Comment.objects.count()
    response = author_client.delete(url_delete)
    count_after = Comment.objects.count()
    assert count_after - count_before == -1
    assertRedirects(response, url_comment + '#comments')


def test_user_cant_delete_comment_of_another_user(not_author_client,
                                                  url_delete):
    count_before = Comment.objects.count()
    response = not_author_client.delete(url_delete)
    count_after = Comment.objects.count()
    assert count_after - count_before == 0
    assert response.status_code == HTTPStatus.NOT_FOUND
