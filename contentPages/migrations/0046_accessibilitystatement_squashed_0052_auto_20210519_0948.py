# Generated by Django 2.2.20 on 2021-05-19 13:10

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    replaces = [('contentPages', '0046_accessibilitystatement'), ('contentPages', '0047_delete_accessibilitystatement'), ('contentPages', '0048_accessibilitystatement'), ('contentPages', '0049_flexpage'), ('contentPages', '0050_delete_flexpage'), ('contentPages', '0051_auto_20210518_1611'), ('contentPages', '0052_auto_20210519_0948')]

    dependencies = [
        ('wagtailcore', '0045_assign_unlock_grouppagepermission'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('contentPages', '0045_auto_20201123_1103'),
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailimages', '0022_uploadedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessibilityStatement',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('heading', models.TextField()),
                ('subtitle', models.TextField(default='Accessibility Statement')),
                ('content', wagtail.core.fields.StreamField([('title_and_paragraph', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.TextBlock(required=True)), ('paragraph', wagtail.core.blocks.RichTextBlock(required=True))]))], blank=True, null=True)),
                ('banner_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('intro', wagtail.core.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]