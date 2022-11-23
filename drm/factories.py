from random import choice
import datetime
import factory
from faker import Faker
from django.contrib.auth import get_user_model
from drm.management.commands.add_licenses import get_random_license

from . import models

fake = Faker()
User = get_user_model()


def get_fake_filepath():
    return fake.file_path(depth=2, category="video")


class AssetsFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(get_fake_filepath)
    license = factory.LazyFunction(get_random_license)

    class Meta:
        model = models.Asset


class LicensesFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(fake.color_name)

    class Meta:
        model = models.License


class OrganizationsFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(fake.company)

    class Meta:
        model = models.Organization


class PolicyFactory(factory.django.DjangoModelFactory):
    display_name = factory.LazyFunction(fake.domain_name)
    statements = factory.LazyFunction(fake.hostname)

    class Meta:
        model = models.Policy


class RoleFactory(factory.django.DjangoModelFactory):
    display_name = factory.LazyFunction(fake.cryptocurrency_name)

    class Meta:
        model = models.Role


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.LazyFunction(fake.user_name)
    email = factory.LazyFunction(fake.ascii_email)
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)

    class Meta:
        model = User
