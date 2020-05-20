# Generated by Django 2.2.12 on 2020-05-20 19:41

from django.db import migrations, models
import django.db.models.deletion

def convert_resource_types_to_keys(apps, schema_editor):
    CreateNewResourceType = apps.get_model("contentPages", "CreateNewResourceType")
    AllResourcesTile = apps.get_model("contentPages", "AllResourcesTile")
    AssetTypePage = apps.get_model("contentPages", "AssetTypePage")
    ResourceItemPage = apps.get_model("contentPages", "ResourceItemPage")

    all_types = CreateNewResourceType.objects.all()

    resource_tiles = AllResourcesTile.objects.all()
    for resource_tile in resource_tiles:
        for resource_type in all_types:
            if resource_type.resource_type.lower().replace(' ', '_') == resource_tile.caption:
                resource_tile.caption = resource_type.id
        resource_tile.save()

    asset_type_pages = AssetTypePage.objects.all()
    for asset_type_page in asset_type_pages:
        if asset_type_page.document_type == "":
            asset_type_page.document_type = '1'
        else:
            for resource_type in all_types:
                if resource_type.resource_type.lower().replace(' ', '_') == asset_type_page.document_type:
                    asset_type_page.document_type = resource_type.id
        asset_type_page.save()

    resource_items = ResourceItemPage.objects.all()
    for resource_item in resource_items:
        for resource_type in all_types:
            if resource_type.resource_type.lower().replace(' ', '_') == resource_item.document_type:
                resource_item.document_type = resource_type.id
        resource_item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0038_convert_existing_asset_types'),
    ]

    operations = [
        migrations.RunPython(convert_resource_types_to_keys),
        migrations.AlterField(
            model_name='allresourcestile',
            name='caption',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='contentPages.CreateNewResourceType'),
        ),
        migrations.AlterField(
            model_name='assettypepage',
            name='document_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='contentPages.CreateNewResourceType'),
        ),
        migrations.AlterField(
            model_name='resourceitempage',
            name='document_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='contentPages.CreateNewResourceType'),
        ),
    ]