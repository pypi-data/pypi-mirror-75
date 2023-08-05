# -*- coding: utf-8 -*-

import graphene


class BitField(graphene.Scalar):
    """Bit field."""

    @staticmethod
    def serialize(bit):  # noqa: WPS602
        """Serialize."""
        return [key for key, setted in bit if setted]
