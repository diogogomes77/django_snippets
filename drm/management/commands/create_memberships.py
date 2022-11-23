from random import choice
from drm.factories import LicensesFactory, PolicyFactory, RoleFactory
from drm.management.commands.base import CreateDataBaseCommand
from django.contrib.auth import get_user_model
from drm import models
from faker import Faker
import datetime

fake = Faker()


def get_random_role():
    pks = models.Role.objects.values_list("pk", flat=True)
    random_pk = choice(pks)
    random_object = models.Role.objects.get(pk=random_pk)
    return random_object


def get_random_organization():
    pks = models.Organization.objects.values_list("pk", flat=True)
    random_pk = choice(pks)
    random_object = models.Organization.objects.get(pk=random_pk)
    return random_object


class Command(CreateDataBaseCommand):

    help = "Create memberships"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f"Creating {self.number} memberships ...")

        User = get_user_model()
        for user in User.objects.all():
            for n in range(1, self.number):

                organization = get_random_organization()
                print("organization: ", organization)
                membership = models.Membership.objects.create(
                    display_name=user.username + "-" + organization.name,
                    user=user,
                    organization=organization,
                )
                for n in range(1, 5):
                    role = get_random_role()
                    print("role: ", role)
                    membership.roles.add(role)
