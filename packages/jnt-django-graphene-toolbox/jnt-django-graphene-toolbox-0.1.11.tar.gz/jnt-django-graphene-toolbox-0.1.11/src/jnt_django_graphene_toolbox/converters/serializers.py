# -*- coding: utf-8 -*-

import graphene
from graphene_django.registry import get_global_registry
from graphene_django.rest_framework.serializer_converter import (
    convert_serializer_field_to_enum as base_convert_serializer_field_to_enum,
)
from graphene_django.rest_framework.serializer_converter import (
    get_graphene_type_from_serializer_field,
)
from graphene_file_upload.scalars import Upload
from rest_framework import serializers

from jnt_django_graphene_toolbox.serializers.fields import EnumField


@get_graphene_type_from_serializer_field.register(serializers.ManyRelatedField)
def convert_list_serializer_to_field(field):
    """Defines graphql field type for serializers.ManyRelatedField."""
    return (graphene.List, graphene.ID)


@get_graphene_type_from_serializer_field.register(
    serializers.PrimaryKeyRelatedField,
)
def convert_serializer_field_to_id(field):
    """Defines graphql field type for serializers.PrimaryKeyRelatedField."""
    return graphene.ID


@get_graphene_type_from_serializer_field.register(serializers.ImageField)
def convert_serializer_field_to_image(field):
    """Defines graphql field type for serializers.ImageField."""
    return Upload


@get_graphene_type_from_serializer_field.register(serializers.ChoiceField)
def convert_serializer_field_to_enum(field):
    """Convert serializers enum fields to rigth type."""
    if isinstance(field, EnumField):
        global_registry = get_global_registry()

        registered = next(
            (
                converted
                for converted in global_registry._field_registry.values()  # noqa:  WPS437
                if getattr(converted, "django_enum", None) == field.enum
            ),
            None,
        )

        if registered:
            return registered._meta.class_type  # noqa: WPS437

    return base_convert_serializer_field_to_enum(field)
