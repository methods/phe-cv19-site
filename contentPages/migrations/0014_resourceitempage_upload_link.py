# Generated by Django 2.2.11 on 2020-03-26 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0013_resourcespage_sidebar_screenreader_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourceitempage',
            name='upload_link',
            field=models.TextField(blank=True, default=''),
        ),
    ]