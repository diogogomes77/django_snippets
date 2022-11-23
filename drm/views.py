from rest_framework import viewsets

from drm.models import Asset, HasLicense, License, Membership, Organization
from drm.serializers import (
    LicenseSerializer,
    MembershipSerializer,
    OrganizationSerializer,
    UserSerializer,
)
from django.db.models import F
from django.db.models import Prefetch
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response


class OrganizationsViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        qs = self.queryset
        qs = (
            qs.prefetch_related(
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
            )
            .prefetch_related("attachments", "attachments__policy")
            .prefetch_related(
                "licenses",
                "licenses__assets",
                "licenses__attachments",
                "licenses__attachments__policy",
            )
        )

        return qs


class LicensesViewSet(viewsets.ModelViewSet):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer


User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related(
        "memberships",
        "memberships__roles",
        "memberships__roles__attachments",
        "memberships__roles__attachments__policy",
    )
    serializer_class = UserSerializer

    obj_name = "User"
    lookup_field = "id"
    lookup_url_kwarg = "id"
    uri_field = lookup_field
    detail_url_name = "user-detail"

    @action(detail=True)
    def memberships(self, request, id=None):
        print("memberships: ", request)
        obj = self.get_object()
        print("--obj: ", obj)
        qs = Membership.objects.filter(user=obj).prefetch_related(
            "roles",
            "roles__attachments",
            "roles__attachments__policy",
        )
        # qs = qs.select_related("user", "organization")

        serializer = MembershipSerializer(
            qs,
            many=True,
            read_only=True,
            context={"request": request},
        )

        return Response(serializer.data)
