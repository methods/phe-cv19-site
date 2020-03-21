# Generated by Django 2.2.11 on 2020-03-21 11:42

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('contentPages', '0002_overviewpage_resourceitempreview_resourcespage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceItemPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('heading', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('preview_image_screen_reader_text', models.TextField(blank=True)),
                ('product_code', models.CharField(blank=True, max_length=256, null=True)),
                ('overview', wagtail.core.fields.RichTextField()),
                ('format', models.CharField(blank=True, max_length=256, null=True)),
                ('file_size', models.CharField(blank=True, max_length=256, null=True)),
                ('link_url', models.CharField(blank=True, max_length=2048)),
                ('preview_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
