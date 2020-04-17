# Generated by Django 2.2.11 on 2020-04-16 11:00

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0020_auto_20200416_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourcesSharedContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=500)),
                ('content_body', wagtail.core.fields.RichTextField(blank=True, default='')),
            ],
            options={
                'verbose_name': 'Resources Shared Content',
            },
        ),
        migrations.AlterModelOptions(
            name='sharedcontent',
            options={'verbose_name': 'Overview Shared Content'},
        ),
    ]
