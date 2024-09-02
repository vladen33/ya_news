from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import News, Comment
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


COUNT_COMMENTS_ON_NEWS_PAGE = 10


@pytest.fixture
def url_home():
    return reverse('news:home')


@pytest.fixture
def url_detail(news):
    return reverse('news:detail', kwargs={'pk': news.pk})


@pytest.fixture
def url_comment(comment):
    return reverse('news:detail', kwargs={'pk': comment.news.pk})


@pytest.fixture
def url_edit(comment):
    return reverse('news:edit', kwargs={'pk': comment.pk})


@pytest.fixture
def url_delete(comment):
    return reverse('news:delete', kwargs={'pk': comment.pk})


@pytest.fixture
def url_login():
    return reverse('users:login')


@pytest.fixture
def url_signup():
    return reverse('users:signup')


@pytest.fixture
def url_logout():
    return reverse('users:logout')


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def anonymous_client():
    return Client()


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def news_array():
    today = datetime.today()
    all_news = [
        News(
            title=f'Заголовок #{index}',
            text=f'Текст новости #{index}',
            date=today - timedelta(days=index)
        ) for index in range(NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария')
    return comment


@pytest.fixture
def comments_array(news, author):
    now = timezone.now()
    for index in range(COUNT_COMMENTS_ON_NEWS_PAGE):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Текст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
