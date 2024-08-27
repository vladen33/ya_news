from django.test import TestCase

from news.models import News


class TestNews(TestCase):
    TITLE = 'Заголовок новости'
    TEXT = 'Тестовый текст'

    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(
            title=cls.TITLE,
            text='Тестовый текст'
        )

    def test_cuccessful_creation(self):
        news_count = News.objects.count()
        self.assertEqual(news_count, 1, 'Ошибка при создании объекта')

    def test_title(self):
        self.assertEqual(self.news.title, self.TITLE)