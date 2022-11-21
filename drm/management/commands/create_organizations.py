from drm.factories import OrganizationsFactory
from drm.management.commands.base import CreateDataBaseCommand


class Command(CreateDataBaseCommand):

    help = "Create organizations"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f"Creating {self.number} organizations ...")
        OrganizationsFactory.create_batch(size=self.number)
