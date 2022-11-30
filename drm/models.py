from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
import uuid

from drm.models_utils import URN_NAMESPACE, URNField

User = get_user_model()


class Asset(models.Model):
    asset_urn = URNField(primary_key=True, editable=False, namespace=URN_NAMESPACE, typename="asset")
    # asset_urn = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    license = models.ForeignKey("License", on_delete=models.CASCADE, related_name="assets")

    def __str__(self) -> str:
        return self.name


class Policy(models.Model):
    policy_urn = URNField(primary_key=True, editable=False, namespace=URN_NAMESPACE, typename="policy")
    # policy_urn = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=64)
    statements = models.CharField(max_length=256)
    # organization = models.ForeignKey(
    #     "Organization", related_name="policies", null=True, blank=True, on_delete=models.CASCADE, db_index=True
    # )

    def __str__(self):
        return f"{self.policy_urn} -> {self.display_name}"

    __repr__ = __str__


class Attachment(models.Model):
    attachment_urn = URNField(primary_key=True, editable=False, namespace=URN_NAMESPACE, typename="attachment")
    # attachment_urn = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # content_type
    entity_urn = URNField()  # object_id
    # entity_urn = models.UUIDField()  # object_id
    entity = GenericForeignKey("entity_type", "entity_urn")  # tagged_object

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey("content_type", "object_id")

    policy = models.ForeignKey("Policy", related_name="attachments", on_delete=models.CASCADE)  # tag_name

    class Meta:
        unique_together = ("policy", "entity_type", "entity_urn")

    def __str__(self) -> str:
        return str(self.entity_type) + str(self.policy)

    @property
    def attachment_ok(self):
        return "ok " + str(self.attachment_urn)


class License(models.Model):
    license_urn = URNField(primary_key=True, editable=False, namespace=URN_NAMESPACE, typename="license")
    # license_urn = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    attachments = GenericRelation("Attachment", "entity_urn", "entity_type")

    def __str__(self) -> str:
        return self.name


class HasLicense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self) -> str:
        return self.organization.name + " -> " + self.license.name


class Organization(models.Model):
    organization_urn = URNField(primary_key=True, editable=False, namespace=URN_NAMESPACE, typename="organization")
    # organization_urn = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    licenses = models.ManyToManyField(
        License,
        through=HasLicense,
        through_fields=["organization", "license"],
        related_name="organizations",
    )
    attachments = GenericRelation("Attachment", "entity_urn", "entity_type")

    def __str__(self) -> str:
        return self.name


class Role(models.Model):
    role_urn = URNField(primary_key=True, editable=False, namespace=URN_NAMESPACE, typename="role")
    # role_urn = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=200)
    attachments = GenericRelation("Attachment", "entity_urn", "entity_type")

    def __str__(self) -> str:
        return self.display_name


class Membership(models.Model):
    membership_urn = URNField(primary_key=True, editable=False, namespace=URN_NAMESPACE, typename="membership")
    # membership_urn = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name="memberships", on_delete=models.CASCADE)
    roles = models.ManyToManyField(to="Role", related_name="memberships")
    organization = models.ForeignKey("Organization", related_name="members", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.display_name
