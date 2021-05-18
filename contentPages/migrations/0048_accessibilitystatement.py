# Generated by Django 2.2.20 on 2021-05-18 07:48

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('contentPages', '0047_delete_accessibilitystatement'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessibilityStatement',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('heading', models.TextField(blank=True)),
                ('subtitle', models.TextField(blank=True)),
                ('content', wagtail.core.fields.StreamField([('title_and_paragraph', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.TextBlock(required=True)), ('paragraph', wagtail.core.blocks.RichTextBlock(required=True))]))], blank=True, null=True)),
                ('banner_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]