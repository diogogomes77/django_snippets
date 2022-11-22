from rest_framework import viewsets

from drm.models import Asset, HasLicense, License, Organization
from drm.serializers import LicenseSerializer, OrganizationSerializer
from django.db.models import F
from django.db.models import Prefetch


class OrganizationsViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        qs = self.queryset
        qs = qs.prefetch_related(
            Prefetch(
                "haslicense_set",
                queryset=HasLicense.objects.select_related(
                    "license",
                    "organization",
                )
                .prefetch_related(
                    Prefetch(
                        "license",
                        queryset=License.objects.all(),
                    ),
                )
                .prefetch_related(
                    Prefetch(
                        "license__assets",
                        queryset=Asset.objects.all(),
                    ),
                )
                .prefetch_related(
                    "license__attachments",
                    "license__attachments__policy",
                ),
            ),
        ).prefetch_related("attachments", "attachments__policy")

        return qs


class LicensesViewSet(viewsets.ModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
