from rest_framework import serializers
from .models import Source, Article


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('id', 'name', 'feed_url', 'label')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'header', 'text', 'url', 'source_id')


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('header', 'text', 'url')


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('header', 'short_description')
