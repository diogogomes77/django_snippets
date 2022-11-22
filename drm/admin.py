from django.contrib import admin
from django.contrib.contenttypes import admin as cadmin
from drm.models import Asset, Attachment, HasLicense, License, Organization, Policy


class HasLicenseInline(admin.TabularInline):
    model = HasLicense
    extra = 1


class AssetsInline(admin.TabularInline):
    model = Asset
    extra = 1


class AttachmentInline(cadmin.GenericTabularInline):
    model = Attachment
    ct_field = "entity_type"
    ct_fk_field = "entity_urn"


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "entity_type", "policy")


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ("display_name",)
    inlines = []


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [HasLicenseInline, AttachmentInline]
    # prepopulated_fields = {"slug": ("course",)}


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [AssetsInline, AttachmentInline]


@admin.register(HasLicense)
class HasLicenseAdmin(admin.ModelAdmin):
    list_display = ("pk", "organization", "license")
