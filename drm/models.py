from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Asset(models.Model):
    name = models.CharField(max_length=200)
    license = models.ForeignKey("License", on_delete=models.CASCADE, related_name="assets")

    def __str__(self) -> str:
        return self.name


class Policy(models.Model):
    display_name = models.CharField(max_length=64)
    statements = models.CharField(max_length=256)
    # organization = models.ForeignKey(
    #     "Organization", related_name="policies", null=True, blank=True, on_delete=models.CASCADE, db_index=True
    # )

    def __str__(self):
        return f"{self.id} -> {self.display_name}"

    __repr__ = __str__


class Attachment(models.Model):
    entity_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # content_type
    entity_urn = models.PositiveIntegerField()  # object_id
    entity = GenericForeignKey("entity_type", "entity_urn")  # tagged_object

    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey("content_type", "object_id")

    policy = models.ForeignKey("Policy", related_name="attachments", on_delete=models.CASCADE)  # tag_name

    class Meta:
        unique_together = ("policy", "entity_type", "entity_urn")

    def __str__(self) -> str:
        return str(self.entity_type) + str(self.policy)


class License(models.Model):
    name = models.CharField(max_length=200)
    attachments = GenericRelation("Attachment", "entity_urn", "entity_type")

    def __str__(self) -> str:
        return self.name


class HasLicense(models.Model):
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    organization = models.ForeignKey("Organization", on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self) -> str:
        return self.organization.name + " -> " + self.license.name


class Organization(models.Model):
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
