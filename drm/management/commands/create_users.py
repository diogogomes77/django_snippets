from drm.factories import LicensesFactory, UserFactory
from drm.management.commands.base import CreateDataBaseCommand


class Command(CreateDataBaseCommand):

    help = "Create users"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f"Creating {self.number} licenses ...")
        UserFactory.create_batch(size=self.number)
