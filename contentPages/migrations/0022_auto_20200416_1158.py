# Generated by Django 2.2.11 on 2020-04-16 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0021_auto_20200416_1100'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ResourcesSharedContent',
        ),
        migrations.AlterModelOptions(
            name='sharedcontent',
            options={'verbose_name': 'Shared Content Snippet'},
        ),
    ]
