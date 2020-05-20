# Generated by Django 2.2.11 on 2020-05-20 10:19

from django.db import migrations, models
from CMS.enums import enums


def convert_existing_resource_types(apps, schema_editor):
    CreateNewResourceTypes = apps.get_model("contentPages", "CreateNewResourceTypes")
    for asset_type in enums.asset_types:
        new_resource_type = CreateNewResourceTypes(resource_type_value=asset_type[0], resource_type=asset_type[1])
        new_resource_type.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0037_auto_20200519_1616'),
    ]

    operations = [
        migrations.RunPython(convert_existing_resource_types),

        migrations.RemoveField(
            model_name='createnewresourcetype',
            name='available_resource_types',
        ),
        migrations.AlterField(
            model_name='allresourcestile',
            name='caption',
            field=models.CharField(choices=[('web_banners', 'Web banners')], default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='assettypepage',
            name='document_type',
            field=models.CharField(choices=[('web_banners', 'Web banners')], default='posters', max_length=25),
        ),
        migrations.AlterField(
            model_name='resourceitempage',
            name='document_type',
            field=models.CharField(choices=[('web_banners', 'Web banners')], default='posters', max_length=25),
        ),
    ]
