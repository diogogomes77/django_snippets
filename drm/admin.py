from django.contrib import admin

from drm.models import Asset, HasLicense, License, Organization


class HasLicenseInline(admin.TabularInline):
    model = HasLicense
    extra = 1


class AssetsInline(admin.TabularInline):
    model = Asset
    extra = 1


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [HasLicenseInline]
    # prepopulated_fields = {"slug": ("course",)}


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [AssetsInline]


@admin.register(HasLicense)
class HasLicenseAdmin(admin.ModelAdmin):
    list_display = ("pk", "organization", "license")
