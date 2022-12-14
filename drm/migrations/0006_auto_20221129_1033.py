# Generated by Django 3.2.16 on 2022-11-29 10:33

from django.db import migrations
import drm.models_utils


class Migration(migrations.Migration):

    dependencies = [
        ('drm', '0005_alter_attachment_entity_urn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='asset_urn',
            field=drm.models_utils.URNField(editable=False, namespace='snippet', primary_key=True, serialize=False, set_default=True, typename='asset'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='attachment_urn',
            field=drm.models_utils.URNField(editable=False, namespace='snippet', primary_key=True, serialize=False, set_default=True, typename='attachment'),
        ),
        migrations.AlterField(
            model_name='license',
            name='license_urn',
            field=drm.models_utils.URNField(editable=False, namespace='snippet', primary_key=True, serialize=False, set_default=True, typename='license'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='membership_urn',
            field=drm.models_utils.URNField(editable=False, namespace='snippet', primary_key=True, serialize=False, set_default=True, typename='membership'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='organization_urn',
            field=drm.models_utils.URNField(editable=False, namespace='snippet', primary_key=True, serialize=False, set_default=True, typename='organization'),
        ),
        migrations.AlterField(
            model_name='policy',
            name='policy_urn',
            field=drm.models_utils.URNField(editable=False, namespace='snippet', primary_key=True, serialize=False, set_default=True, typename='policy'),
        ),
        migrations.AlterField(
            model_name='role',
            name='role_urn',
            field=drm.models_utils.URNField(editable=False, namespace='snippet', primary_key=True, serialize=False, set_default=True, typename='role'),
        ),
    ]
