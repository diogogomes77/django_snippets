from drm.factories import LicensesFactory, PolicyFactory
from drm.management.commands.base import CreateDataBaseCommand


class Command(CreateDataBaseCommand):

    help = "Create policies"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f"Creating {self.number} policies ...")
        PolicyFactory.create_batch(size=self.number)
