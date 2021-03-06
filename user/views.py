# -*- coding: utf-8 -*-
"""
This module contains all views for the user app.
"""

from rest_framework.generics import get_object_or_404
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer, UserSourceSerializer
from .models import UserSource, Source


class UserCreate(CreateAPIView):
    """View for create user API"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class UserUpdate(UpdateAPIView):
    """View for update user API"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class UserSourceViewSet(viewsets.ModelViewSet):
    """View for user source API"""

    serializer_class = UserSourceSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """Restricting queryset to contain only user related sources"""

        return UserSource.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        source = get_object_or_404(Source, id=self.request.data.get('source_id'))
        user = self.request.user
        return serializer.save(source=source, user=user)

    def perform_update(self, serializer):
        source = get_object_or_404(Source, id=self.request.data.get('source_id'))
        user = self.request.user
        return serializer.save(source=source, user=user)
