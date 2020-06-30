from django.db import migrations

from django.contrib.contenttypes.models import ContentType

from contentPages.models import OverviewPage, ResourcesPage, HomePage


def remove_landing_pages(apps, schema_editor):
    overview_pages = OverviewPage.objects.all()
    resource_content_type = ContentType.objects.get_for_model(ResourcesPage).id
    home_page = HomePage.objects.get()
    for overview_page in overview_pages:
        landing_page = overview_page.get_parent()
        campaign_item = home_page.campaign_items.filter(campaign_landing_page=landing_page).first()
        if campaign_item:
            campaign_item.campaign_landing_page = overview_page
            campaign_item.save()
        campaign_slug = landing_page.slug
        landing_page.slug = campaign_slug + '-deprecated'
        landing_page.save()
        landing_page.save_revision()
        if landing_page.live:
            landing_page.unpublish()
        resource_page = overview_page.get_siblings().filter(content_type_id=resource_content_type).first()
        resource_page.move(overview_page, 'first-child')
        overview_page.move(landing_page)
        new_overview_page = OverviewPage.objects.get(id=overview_page.id)
        new_overview_page.slug = campaign_slug
        new_overview_page.save()
        overview_revision = new_overview_page.save_revision()
        if new_overview_page.live:
            overview_revision.publish()
    home_page.save()
    new_revision = home_page.save_revision()
    new_revision.publish()


class Migration(migrations.Migration):

    dependencies = [
        ('contentPages', '0042_auto_20200529_1010'),
    ]

    operations = [
        migrations.RunPython(remove_landing_pages),
    ]
