from rest_framework import serializers

from drm.models import Attachment, HasLicense, License, Membership, Organization, Asset, Policy, Role
from django.contrib.auth import get_user_model

User = get_user_model()


class NestedRelationField(serializers.PrimaryKeyRelatedField):
    def __init__(self, related_serializer_class, *args, **kwargs):
        self.related_serializer_class = related_serializer_class
        super().__init__(*args, **kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        return self.related_serializer_class(instance=value).data


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["asset_urn", "name"]


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ["policy_urn", "display_name", "statements"]


class AttachmentSerializer(serializers.ModelSerializer):
    # policy = NestedRelationField(PolicySerializer, queryset=Policy.objects.all())
    # attachment_urn = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            "attachment_urn",
            # "policy",
        ]
        # fields = "__all__"

    def get_attachment_urn(self, instance):
        return instance.attachment_ok


class LicenseSerializer(serializers.ModelSerializer):
    assets = AssetSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = License
        fields = [
            "id",
            "name",
            "attachments",
            "assets",
        ]
        # fields = "__all__"


class HasLicenseModelSerializer(serializers.ModelSerializer):
    license = LicenseSerializer()

    class Meta:
        model = HasLicense
        fields = [
            "start",
            "end",
            "license",
        ]


class HasLicenseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    # license_name = serializers.CharField(source="name")
    license = LicenseSerializer()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()


class OrganizationSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    # has_licenses = HasLicenseModelSerializer(many=True, source="haslicense_set", read_only=True)
    # has_licenses = HasLicenseSerializer(many=True, source="haslicense_set", read_only=True)
    # licenses = LicenseSerializer(many=True)

    class Meta:
        model = Organization
        fields = [
            "name",
            "attachments",
            # "has_licenses",
            # "licenses",
        ]
        # fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):

    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = [
            "display_name",
            "attachments",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "url",
            "username",
            "email",
            "is_staff",
        ]


class MembershipSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True)
    # user = UserSerializer()
    # organization = OrganizationSerializer()

    class Meta:
        model = Membership
        fields = fields = [
            "membership_urn",
            "display_name",
            "user",
            # "organization",
            "roles",
        ]
