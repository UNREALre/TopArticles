# -*- coding: utf-8 -*-
"""
This module contains base automated tests for article models: Source, Article.
"""

from django.test import TestCase
from ..models import Source, Article


class SourceTest(TestCase):
    """ Test class for Sources model """

    def setUp(self):
        Source.objects.create(
            name='Habr',
            feed_url='https://habr.com/ru/feed/'
        )
        Source.objects.create(
            name='VC',
            feed_url='https://vc.ru/'
        )

    def test_get_info(self):
        source_habr = Source.objects.get(name='Habr')
        source_vc = Source.objects.get(name='VC')
        self.assertEqual(source_habr.get_info(), "Source Habr with the feed URL https://habr.com/ru/feed/")
        self.assertEqual(source_vc.get_info(), "Source VC with the feed URL https://vc.ru/")


class ArticleTest(TestCase):
    """ Test class for Article model """

    def setUp(self):
        source = Source.objects.create(
            name='Habr',
            feed_url='https://habr.com/ru/feed/'
        )
        Article.objects.create(
            source=source,
            url="https://site.com/123",
            header="Article #1",
            text="Text of the article #1"
        )
        Article.objects.create(
            source=source,
            url="https://site.com/321",
            header="Article #2",
            text="Text of the article #2"
        )

    def test_get_info(self):
        article_1 = Article.objects.get(url='https://site.com/123')
        article_2 = Article.objects.get(url='https://site.com/321')
        self.assertEqual(article_1.header, "Article #1")
        self.assertEqual(article_2.header, "Article #2")
