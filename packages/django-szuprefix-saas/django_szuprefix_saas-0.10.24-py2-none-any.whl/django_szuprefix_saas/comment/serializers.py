# -*- coding:utf-8 -*-
from django_szuprefix.api.mixins import IDAndStrFieldSerializerMixin
from django_szuprefix_saas.saas.mixins import PartySerializerMixin
from rest_framework import serializers
from . import models


class CommentSerializer(IDAndStrFieldSerializerMixin, PartySerializerMixin, serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", label='用户名', read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            'content_type',
            'object_id',
            'object_name',
            'user',
            'user_name',
            'content',
            'context',
            'anchor',
            'is_active',
            'create_time',
            'reply_count'
        )
        read_only_fields = ('user', 'create_time', 'object_name')


class FavoriteSerializer(IDAndStrFieldSerializerMixin, PartySerializerMixin, serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", label='用户名', read_only=True)

    class Meta:
        model = models.Favorite
        fields = (
            'content_type',
            'object_id',
            'object_name',
            'user',
            'user_name',
            'notes',
            'is_active',
            'create_time',
            'notes_count'
        )
        read_only_fields = ('user', 'create_time', 'object_name')


class RatingSerializer(IDAndStrFieldSerializerMixin, PartySerializerMixin, serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", label='用户名', read_only=True)

    class Meta:
        model = models.Rating
        fields = ('content_type', 'object_id', 'object_name', 'user', 'user_name', 'score', 'create_time')
        read_only_fields = ('user', 'create_time', 'object_name')
