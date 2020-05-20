
from django.db import migrations
from CMS.enums import enums


def convert_existing_resource_types(apps, schema_editor):
    CreateNewResourceTypes = apps.get_model("contentPages", "CreateNewResourceType")
    for asset_type in enums.asset_types:
        new_resource_type = CreateNewResourceTypes(resource_type=asset_type[1])
        new_resource_type.save()


class Migration(migrations.Migration):

    dependencies = [
        ("contentPages", "0037_auto_20200519_1616")
    ]

    operations = [
        migrations.RunPython(convert_existing_resource_types)
    ]
