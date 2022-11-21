from random import choice
from drm import models
from drm.factories import LicensesFactory
from drm.management.commands.base import CreateDataBaseCommand
from drm.models import Organization
import factory
from faker import Faker
import datetime

fake = Faker()


def get_random_license():
    pks = models.License.objects.values_list("pk", flat=True)
    random_pk = choice(pks)
    random_object = models.License.objects.get(pk=random_pk)
    return random_object


class Command(CreateDataBaseCommand):

    help = "Add licenses"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f"Adding {self.number} licenses ...")

        for org in Organization.objects.all():
            for n in range(1, self.number):
                license = get_random_license()
                print("license: ", license)
                start = fake.date_between_dates(
                    date_start=datetime.datetime(2015, 1, 1), date_end=datetime.datetime(2021, 12, 31)
                )
                end = fake.date_between_dates(
                    date_start=start + datetime.timedelta(weeks=4),
                    date_end=start + datetime.timedelta(weeks=60),
                )
                models.HasLicense.objects.create(
                    license=license,
                    organization=org,
                    start=start,
                    end=end,
                )
