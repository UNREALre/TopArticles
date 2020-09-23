# -*- coding: utf-8 -*-
"""
This module contains all models for the article app.

Full list of declared models:
    1. Source
    2. Article
"""

import re
from django.db import models
from django.contrib.auth.models import User


class Source(models.Model):
    """Here will be stored base info about feed: its name, feed url to parse and label ('VC', 'HABR', etc)"""

    name = models.CharField(max_length=255)
    feed_url = models.CharField(max_length=255)
    label = models.CharField(max_length=50)  # used within parser factories

    def __repr__(self):
        return '<Source {}>'.format(self.name)

    def __str__(self):
        return 'Source "{}"'.format(self.name)

    def get_info(self):
        return 'Source {} with the feed URL {}'.format(self.name, self.feed_url)


class Article(models.Model):
    """
    Model for storing Articles from parsed sources.

    source - links to Source of the article
    url - full url of the article within its source
    header - header of the article
    text - full text of the article
    added - auto generated field with value equals to the date when article was parsed and added to the database
    users - list of users that subscribed to the source with this article
    """

    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    header = models.CharField(max_length=255)
    text = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name='articles')

    @property
    def short_description(self):
        """This property is used in list API call, to return not full text, but only first 700 chars."""

        clean_text = re.sub('[^A-Za-zа-яА-Я0-9 ]+', '', self.text)
        return clean_text[:700]

    def __str__(self):
        return self.header

    class Meta:
        """URL and header fields has to be indexed, because of many searches using them during parser process"""

        indexes = [
            models.Index(fields=['url', ]),
            models.Index(fields=['header', ]),
        ]
