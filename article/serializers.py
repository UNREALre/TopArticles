# -*- coding: utf-8 -*-
"""
This module contains all serializers for the article app.
"""

from rest_framework import serializers
from .models import Source, Article


class SourceSerializer(serializers.ModelSerializer):
    """Serializer for the article sources."""

    class Meta:
        model = Source
        fields = ('id', 'name', 'feed_url', 'label')


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for the articles."""

    class Meta:
        model = Article
        fields = ('id', 'header', 'text', 'url', 'source_id')


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Serializer for the article detail API call."""

    class Meta:
        model = Article
        fields = ('header', 'text', 'url')


class ArticleListSerializer(serializers.ModelSerializer):
    """Serializer for the articles list API call."""

    class Meta:
        model = Article
        fields = ('id', 'header', 'short_description')
