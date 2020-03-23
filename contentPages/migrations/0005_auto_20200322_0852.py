# Generated by Django 2.2.11 on 2020-03-22 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0004_resourceitempage_link_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resourceitempage',
            name='link_url',
        ),
        migrations.AddField(
            model_name='resourcespage',
            name='signup_message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='resourceitempage',
            name='link_document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtaildocs.Document', verbose_name='Upload document'),
        ),
    ]