# Generated by Django 2.2.11 on 2020-03-22 20:02

from django.db import migrations, models
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0007_delete_resourceitempreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourceitempage',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='resourceitempage',
            name='file_size',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='resourceitempage',
            name='format',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='resourceitempage',
            name='product_code',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
    ]