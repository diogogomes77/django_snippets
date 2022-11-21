from drm.factories import LicensesFactory
from drm.management.commands.base import CreateDataBaseCommand


class Command(CreateDataBaseCommand):

    help = "Create licenses"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f"Creating {self.number} licenses ...")
        LicensesFactory.create_batch(size=self.number)
