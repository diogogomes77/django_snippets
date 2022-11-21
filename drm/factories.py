from random import choice
import datetime
import factory
from faker import Faker

from . import models

fake = Faker()


class LicensesFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(fake.color_name)

    class Meta:
        model = models.License


class OrganizationsFactory(factory.django.DjangoModelFactory):
    name = factory.LazyFunction(fake.company)

    class Meta:
        model = models.Organization


# class HasLicenseFactory(factory.django.DjangoModelFactory):
#     license = factory.LazyFunction(get_random_object(models.License))
#     organization = factory.LazyFunction(get_random_object(models.Organization))
#     start = factory.LazyFunction(
#         lambda: fake.date_between_dates(
#             date_start=datetime.datetime(2015, 1, 1), date_end=datetime.datetime(2021, 12, 31)
#         )
#     )
#     end = factory.LazyAttribute(
#         lambda o: fake.date_between_dates(
#             date_start=o.started_at + datetime.timedelta(weeks=4), date_end=o.started_at + datetime.timedelta(weeks=60)
#         )
#     )

#     class Meta:
#         models.HasLicense
