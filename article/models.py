from django.db import models


class Sources(models.Model):
    name = models.CharField(max_length=255)
    feed_url = models.CharField(max_length=255)

    def __repr__(self):
        return '<Source {}>'.format(self.name)

    def get_info(self):
        return 'Source {} with the feed URL {}'.format(self.name, self.feed_url)
