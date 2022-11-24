from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Create test data"

    def handle(self, *args, **options):
        management.call_command("create_organizations", number=500)
        management.call_command("create_licenses", number=10)
        management.call_command("create_assets", number=100)
        management.call_command("add_licenses", number=5)
        management.call_command("create_policies", number=10)

        management.call_command("create_roles", number=10)
        management.call_command("create_users", number=10)
        management.call_command("create_memberships", number=500)

        management.call_command("add_policies", number=5)
