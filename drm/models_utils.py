from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
import uuid
from typing import Type
from uuid import UUID
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core import checks, exceptions, validators

URN_PREFIX = "urn"
URN_NAMESPACE = "snippet"
URN_INVALID_MESSAGE = "Invalid URN string"  # type: str


def urn_validator_factory(
    typename: str, id_type: Type = UUID, prefix: str = URN_PREFIX, namespace: str = URN_NAMESPACE
):
    """Configures an URN validator"""

    def inner(error_class: Type = ValidationError):
        """Takes the class of error to raise when the urn is invalid"""

        def validate_urn(urn_string: str):
            """Runs validation"""

            try:
                prefix_, namespace_, typename_, identifier_ = urn_string.split(":")
            except ValueError:
                raise error_class(URN_INVALID_MESSAGE)
            if not all([prefix_ == prefix, typename_ == typename, namespace_ == namespace]):
                raise error_class(URN_INVALID_MESSAGE)
            try:
                id_type(identifier_)
            except Exception:
                raise error_class(URN_INVALID_MESSAGE)

        return validate_urn

    return inner


class MyUUIDField(models.Field):
    _default_error_messages = {
        "invalid": _("“%(value)s” is not a valid UUID."),
    }
    _description = _("Universally unique identifier")
    _empty_strings_allowed = False

    def ___init__(self, verbose_name=None, **kwargs):
        kwargs["max_length"] = 32
        super().__init__(verbose_name, **kwargs)

    def _get_internal_type(self):
        return "UUIDField"

    def _get_db_prep_value(self, value, connection, prepared=False):
        print("--- UUIDField get_db_prep_value: ", value)
        return value.hex


class URNField(models.Field):
    """Universal resource name database field"""

    _DEFAULT_NAMESPACE = URN_NAMESPACE
    default_error_messages = {"invalid": URN_INVALID_MESSAGE}

    def __init__(
        self, verbose_name=None, namespace=_DEFAULT_NAMESPACE, typename=None, set_default=True, strict=True, **kwargs
    ):
        super().__init__(verbose_name, **kwargs)
        self._namespace = namespace
        self._typename = typename
        self._set_default = set_default
        self._strict = strict

    def get_internal_type(self):
        return "UUIDField"

    @property
    def urn_prefix(self):
        """Constructs a URN prefix `<prefix>:<namespace>:<typename>:`"""
        return ":".join([URN_PREFIX, self._namespace, self._typename or self.model.__name__.lower(), ""])

    def get_db_prep_value(self, value, connection, prepared=False):
        print("--- UUIDField get_db_prep_value: ", value)
        return value.hex

    def _value_from_object(self, obj):
        value = super().value_from_object(obj)
        ret = None
        if isinstance(value, uuid.UUID):
            ret = f"{self.urn_prefix}{value.hex}"
            print("--- 1 to_python: ", ret)
            return ret
        if not self._strict:
            if isinstance(value, str):
                if value.startswith(self.urn_prefix):
                    ret = value
                    print("--- 2 to_python: ", ret)
                    return ret
                ret = f"{self.urn_prefix}{value[-32:]}"
                print("--- 3 to_python: ", ret)
                return ret
        ret = value
        print("--- 4 to_python: ", ret)
        return ret

    def value_to_string(self, obj):
        print("--- *** value_to_string obj: ", obj)
        value = self.value_from_object(obj)

        ret = None
        if isinstance(value, uuid.UUID):
            ret = f"{self.urn_prefix}{value.hex}"
            print("--- 1 to_python: ", ret)
            return ret
        if not self._strict:
            if isinstance(value, str):
                if value.startswith(self.urn_prefix):
                    ret = value
                    print("--- 2 to_python: ", ret)
                    return ret
                ret = f"{self.urn_prefix}{value[-32:]}"
                print("--- 3 to_python: ", ret)
                return ret
        ret = value
        print("--- 4 to_python: ", ret)
        return ret

        return self.get_prep_value(value)
