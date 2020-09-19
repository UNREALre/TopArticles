from django.test import TestCase
from ..models import Sources


class SourcesTest(TestCase):

    """ Test module for Sources model """

    def setUp(self):
        Sources.objects.create(
            name='Habr',
            feed_url='https://habr.com/ru/feed/'
        )
        Sources.objects.create(
            name='VC',
            feed_url='https://vc.ru/'
        )

    def test_get_info(self):
        source_habr = Sources.objects.get(name='Habr')
        source_vc = Sources.objects.get(name='VC')
        self.assertEqual(source_habr.get_info(), "Source Habr with the feed URL https://habr.com/ru/feed/")
        self.assertEqual(source_vc.get_info(), "Source VC with the feed URL https://vc.ru/")
