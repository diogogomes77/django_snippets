from django.db import models


class License(models.Model):
    name = models.CharField(max_length=200)

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

    def __str__(self) -> str:
        return self.name
