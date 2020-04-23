# Generated by Django 2.2.11 on 2020-04-16 10:42

from django.db import migrations, models
import django.db.models.deletion

def convert_resources_subpage_body_to_snippet(apps, schema_editor):
    LandingPage = apps.get_model("contentPages", "LandingPage")
    SharedContent = apps.get_model("contentPages", "SharedContent")
    landing_page_objects = LandingPage.objects.all()
    for landing_page_object in landing_page_objects:
        resources_body = landing_page_object.resources_subpage_body
        resources_title = landing_page_object.resources_subpage_heading
        snippet = SharedContent(content_body=resources_body, title=resources_title)
        snippet.save()
        landing_page_object.resources_subpage_body = snippet.id
        landing_page_object.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0019_merge_20200416_1038'),
    ]

    operations = [
        migrations.RunPython(convert_resources_subpage_body_to_snippet),
        migrations.AlterField(
            model_name='landingpage',
            name='resources_subpage_body',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='contentPages.SharedContent'),
        ),
    ]