# -*- coding: utf-8 -*-

from django.db import models
from rest_framework import serializers

from jnt_django_graphene_toolbox.serializers.fields.char import CharField


class ModelSerializer(serializers.ModelSerializer):
    """Base model serializer."""

    def __init__(self, *args, **kwargs):
        """Init base model serializer, override fields."""
        self.serializer_field_mapping[models.CharField] = CharField
        self.serializer_field_mapping[models.TextField] = CharField
        super().__init__(*args, **kwargs)
