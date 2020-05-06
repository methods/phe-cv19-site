# Generated by Django 2.2.12 on 2020-05-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('contentPages', '0032_resource_item_page_document_type'),
    ]

    operations = [
        migrations.RunSQL('CREATE TABLE "contentPages_assettype" (ID INT PRIMARY KEY NOT NULL,"page_id" INT, "thumbnail_image_id" INT)'),
        migrations.RunSQL('CREATE TABLE "contentPages_allresources" (ID INT PRIMARY KEY NOT NULL)'),
        migrations.RemoveField(
            model_name='assettype',
            name='page',
        ),
        migrations.RemoveField(
            model_name='assettype',
            name='thumbnail_image',
        ),
        migrations.AlterField(
            model_name='allresourcestile',
            name='caption',
            field=models.CharField(choices=[('posters', 'Poster'), ('digital_screens', 'Digital Screen'), ('alternative_formats', 'Alternative Format'), ('digital_out_of_home', 'Digital out-of-home'), ('email_signatures', 'Email Signature'), ('fact_sheets', 'Fact Sheet'), ('leaflet', 'Leaflet'), ('lockup', 'Lockup'), ('pm_letter', 'PM Letter'), ('press_release', 'Press Release')], default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='assettypepage',
            name='document_type',
            field=models.CharField(choices=[('posters', 'Poster'), ('digital_screens', 'Digital Screen'), ('alternative_formats', 'Alternative Format'), ('digital_out_of_home', 'Digital out-of-home'), ('email_signatures', 'Email Signature'), ('fact_sheets', 'Fact Sheet'), ('leaflet', 'Leaflet'), ('lockup', 'Lockup'), ('pm_letter', 'PM Letter'), ('press_release', 'Press Release')], default='posters', max_length=25),
        ),
        migrations.AlterField(
            model_name='resourceitempage',
            name='document_type',
            field=models.CharField(choices=[('posters', 'Poster'), ('digital_screens', 'Digital Screen'), ('alternative_formats', 'Alternative Format'), ('digital_out_of_home', 'Digital out-of-home'), ('email_signatures', 'Email Signature'), ('fact_sheets', 'Fact Sheet'), ('leaflet', 'Leaflet'), ('lockup', 'Lockup'), ('pm_letter', 'PM Letter'), ('press_release', 'Press Release')], default='posters', max_length=25),
        ),
        migrations.DeleteModel(
            name='AllResources',
        ),
        migrations.DeleteModel(
            name='AssetType',
        ),
    ]
