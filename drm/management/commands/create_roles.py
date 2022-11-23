from drm.factories import LicensesFactory, PolicyFactory, RoleFactory
from drm.management.commands.base import CreateDataBaseCommand


class Command(CreateDataBaseCommand):

    help = "Create roles"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f"Creating {self.number} roles ...")
        RoleFactory.create_batch(size=self.number)
