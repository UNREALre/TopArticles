from django.db import models
from django.contrib.auth.models import User


class Source(models.Model):
    name = models.CharField(max_length=255)
    feed_url = models.CharField(max_length=255)

    def __repr__(self):
        return '<Source {}>'.format(self.name)

    def __str__(self):
        return 'Source "{}"'.format(self.name)

    def get_info(self):
        return 'Source {} with the feed URL {}'.format(self.name, self.feed_url)


class Article(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    header = models.CharField(max_length=255)
    text = models.CharField(max_length=700)
    date = models.DateTimeField()
    added = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name='articles')
