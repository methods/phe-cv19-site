# Generated by Django 2.2.12 on 2020-05-07 11:47

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0016_auto_20200506_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='campaign_list_header',
            field=wagtail.core.fields.RichTextField(blank=True, null=True),
        ),
    ]
