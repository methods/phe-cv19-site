# Generated by Django 2.2.11 on 2020-04-14 13:32

from django.db import migrations, models
import django.db.models.deletion


def create_revisions(apps, schema_editor):
    LandingPage = apps.get_model("contentPages", "LandingPage")
    landing_pages = LandingPage.objects.filter(live=False)
    for landing_page in landing_pages:
        landing_page.save_revision()


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0034_merge_20200512_2155'),
    ]

    operations = [
        migrations.RunPython(create_revisions),
    ]
