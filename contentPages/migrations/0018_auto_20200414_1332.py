# Generated by Django 2.2.11 on 2020-04-14 13:32

from django.db import migrations, models
import django.db.models.deletion


def convert_subpage_body_to_snippet(apps, schema_editor):
    LandingPage = apps.get_model("contentPages", "LandingPage")
    SharedContent = apps.get_model("contentPages", "SharedContent")
    landing_pages = LandingPage.objects.all()
    for landing_page in landing_pages:
        overview_body = landing_page.overview_subpage_body
        overview_title = "{0} - {1}".format(landing_page.title, landing_page.overview_subpage_heading)
        snippet = SharedContent(content_body=overview_body, title=overview_title)
        snippet.save()
        landing_page.overview_subpage_body = snippet.id
        landing_page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0017_auto_20200409_1424'),
    ]

    operations = [
        migrations.RunPython(convert_subpage_body_to_snippet),
        migrations.AlterModelOptions(
            name='sharedcontent',
            options={'verbose_name': 'Shared Content Snippet'},
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='overview_subpage_body',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='contentPages.SharedContent'),
        ),
        migrations.AlterField(
            model_name='sharedcontent',
            name='title',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
