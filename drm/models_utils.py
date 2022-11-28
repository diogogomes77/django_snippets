from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
import uuid
from typing import Type
from uuid import UUID
from django import forms
from django.core.exceptions import ValidationError


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


class URNField(models.UUIDField):
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

    @property
    def urn_prefix(self):
        """Constructs a URN prefix `<prefix>:<namespace>:<typename>:`"""
        return ":".join([URN_PREFIX, self._namespace, self._typename or self.model.__name__.lower(), ""])

    def get_validator(self):
        """Return a validator for this URN field"""

        def validates(value, *args, **kwargs):
            validator = urn_validator_factory(typename=self._typename, namespace=self._namespace)(ValidationError)
            validator(urn_string=value)

        return validates

    def deconstruct(self):
        """Prepares this object instance for pickling"""
        name, path, args, kwargs = super().deconstruct()
        kwargs["set_default"] = self._set_default
        kwargs["typename"] = self._typename
        kwargs["namespace"] = self._namespace
        return name, path, args, kwargs

    def validate(self, value, model_instance):
        """Validates prefix, and the UUID superclass validates the integrity of the UID part of the URN"""
        self.get_validator()(value)
        super().validate(value, model_instance)

    def to_python(self, value) -> str:
        """Converts the value to the expected python type"""
        if isinstance(value, uuid.UUID):
            return f"{self.urn_prefix}{value.hex}"
        if not self._strict:
            if isinstance(value, str):
                if value.startswith(self.urn_prefix):
                    return value
                return f"{self.urn_prefix}{value[-32:]}"
        return value

    def get_prep_value(self, value):
        """preps the value for writing to the database"""
        value = super().get_prep_value(value)
        value = self.to_python(value)
        try:
            return uuid.UUID(value.rsplit(":", 1)[-1])
        except (ValueError, AttributeError):
            pass
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        """Prepares the value for database read/write"""
        if not prepared:
            value = self.get_prep_value(value)
        return super().get_db_prep_value(value, connection, prepared)

    def from_db_value(self, value, expression, connection):
        """Will pass a UUID object OR a CHAR(32) hex string"""
        return self.to_python(value)

    def pre_save(self, model_instance, add):
        """Generates a default URN if `set_default` was passed"""
        if not getattr(model_instance, self.attname):
            if add and self._set_default:
                value = self.to_python(uuid.uuid4())
                setattr(model_instance, self.attname, value)
                return value
        return super().pre_save(model_instance, add)

    def formfield(self, **kwargs):
        """Use a CharField as the form input in the admin app"""
        field = type("URNField", (forms.CharField,), {"default_validators": [self.get_validator()]})
        kwargs.setdefault("form_class", field)
        return super().formfield(**kwargs)
