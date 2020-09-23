# -*- coding: utf-8 -*-
"""
This module contains all models for the user app.

Full list of declared models:
    1. UserSource
"""

from django.db import models
from django.contrib.auth.models import User

from article.models import Source


class UserSource(models.Model):
    """
    Model for storing User Sources.

    Password is encrypted using crypto-algorithm from top_news.helper module
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return 'Source "{}" for user "{}"'.format(self.source.name, self.user.username)
