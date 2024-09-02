import pytest

from news.forms import CommentForm
from news.models import Comment
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_count_on_main_page(client, news_array, url_home):
    response = client.get(url_home)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news_array, url_home):
    response = client.get(url_home)
    object_list = response.context['object_list']
    all_dates = [news_object.date for news_object in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_order(comments_array, news):
    comment_set = Comment.objects.filter(news__pk=news.pk)
    all_timestamps = [comm.created for comm in comment_set]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, url_detail):
    response = client.get(url_detail)
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, url_detail):
    response = author_client.get(url_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
