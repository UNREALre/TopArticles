# -*- coding: utf-8 -*-
"""
This module contains all urls routes of the app.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserCreate, UserUpdate, UserSourceViewSet


app_name = 'user'

router = DefaultRouter()
router.register(r'sources', UserSourceViewSet, basename='user_source')

urlpatterns = [
    path('get-token/', obtain_auth_token, name='get_token'),
    path('create/', UserCreate.as_view(), name='create_user'),
    path('update/', UserUpdate.as_view(), name='update_user'),
] + router.urls
