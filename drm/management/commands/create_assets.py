from drm.factories import AssetsFactory, LicensesFactory
from drm.management.commands.base import CreateDataBaseCommand


class Command(CreateDataBaseCommand):

    help = "Create assets"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f"Creating {self.number} assets ...")
        AssetsFactory.create_batch(size=self.number)
