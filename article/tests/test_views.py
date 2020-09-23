# -*- coding: utf-8 -*-
"""
This module contains examples of how API methods can be tested inside Django.

For now, all tests are created within Postman collection (reed README.md for actual Postman collection URL).
"""

from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from ..models import Source
from ..serializers import SourceSerializer


class GetAllSourcesTest(TestCase):
    """ Test module for GET all sources API """

    def setUp(self):
        self.client = APIClient()
        Source.objects.create(name='Source1', feed_url='https://site1.com')
        Source.objects.create(name='Source2', feed_url='https://site2.com')
        Source.objects.create(name='Source3', feed_url='https://site3.com')

    def test_get_all_sources(self):
        response = self.client.get(reverse('article:sources_list'))
        sources = Source.objects.all()
        serializer = SourceSerializer(sources, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleSourceTest(TestCase):
    """ Test module for GET single source API """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)

        self.src1 = Source.objects.create(name='Source1', feed_url='https://site1.com')
        self.src2 = Source.objects.create(name='Source2', feed_url='https://site2.com')
        self.src3 = Source.objects.create(name='Source3', feed_url='https://site3.com')

    def test_get_valid_single_source(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('article:source_view_update_delete', kwargs={'pk': self.src1.pk}))
        source = Source.objects.get(pk=self.src1.pk)
        serializer = SourceSerializer(source)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
