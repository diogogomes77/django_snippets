from rest_framework import serializers

from drm.models import HasLicense, License, Organization, Asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["id", "name"]


class LicenseSerializer(serializers.ModelSerializer):
    assets = AssetSerializer(many=True, read_only=True)

    class Meta:
        model = License
        fields = [
            "id",
            "name",
            "assets",
        ]


class HasLicenseModelSerializer(serializers.ModelSerializer):
    license = LicenseSerializer()

    class Meta:
        model = HasLicense
        fields = ["license", "start", "end"]


class HasLicenseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    # license_name = serializers.CharField(source="name")
    license = LicenseSerializer()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()


class OrganizationSerializer(serializers.ModelSerializer):
    licenses = HasLicenseModelSerializer(many=True, source="haslicense_set", read_only=True)
    # licenses = HasLicenseSerializer(many=True, source="haslicense_set", read_only=True)
    # licenses = LicenseSerializer(many=True)

    class Meta:
        model = Organization
        fields = ["name", "licenses"]
