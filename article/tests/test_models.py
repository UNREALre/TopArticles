from django.test import TestCase
from ..models import Source


class SourceTest(TestCase):

    """ Test module for Sources model """

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
