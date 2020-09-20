from django.db import models
from django.contrib.auth.models import User

from article.models import Source


class UserSource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    label = models.CharField(max_length=50)  # used within parser factories

    def __str__(self):
        return 'Source "{}" for user "{}"'.format(self.source.name, self.user.username)
