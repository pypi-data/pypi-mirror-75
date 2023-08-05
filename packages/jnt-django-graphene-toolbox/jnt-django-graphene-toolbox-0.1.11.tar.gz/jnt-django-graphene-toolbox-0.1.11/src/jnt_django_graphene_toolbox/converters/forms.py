# -*- coding: utf-8 -*-

import graphene
from graphene_django.forms.converter import convert_form_field

from jnt_django_graphene_toolbox.filters.integers_array import (
    IntegersArrayField,
)


@convert_form_field.register(IntegersArrayField)
def convert_integers_array_field(field):
    """Convert form field."""
    return graphene.List(graphene.ID)
