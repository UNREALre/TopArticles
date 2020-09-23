# -*- coding: utf-8 -*-
"""
This module contains all serializers for the user app.
"""

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import UserSource
from top_news.helpers import AESCipher


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user model."""

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSourceSerializer(serializers.ModelSerializer):
    """Serializer for the user source model."""

    class Meta:
        model = UserSource
        fields = ('id', 'user_id', 'source_id', 'login', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        """If update API contains password we have to encrypt it first."""

        password = validated_data.get('password', None)
        if password is not None:
            validated_data['password'] = AESCipher(password, self.context['request'].user.password).encrypt()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        """If create API contains password we have to encrypt it first."""

        password = validated_data.get('password', None)
        if password is not None:
            validated_data['password'] = AESCipher(password, self.context['request'].user.password).encrypt()
        return super().create(validated_data)
