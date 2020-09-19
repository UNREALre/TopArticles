import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Source
from ..serializers import SourceSerializer


# Initialize the API Client
client = Client()
