# Generated by Django 2.2.11 on 2020-03-22 21:41

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0008_auto_20200322_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourceitempage',
            name='overview',
            field=wagtail.core.fields.RichTextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='resourceitempage',
            name='preview_image_screen_reader_text',
            field=models.TextField(blank=True, default=''),
        ),
    ]
