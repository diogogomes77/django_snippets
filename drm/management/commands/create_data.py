from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Create test data"

    def handle(self, *args, **options):
        management.call_command("create_organizations", number=100)
        management.call_command("create_licenses", number=10)
        management.call_command("add_licenses", number=5)
