from django.contrib.contenttypes.models import ContentType
from contentPages.models import HomePage, LandingPage, OverviewPage, ResourcesPage


class CreateForm:
    def __init__(self, request):
        self.page_title = request.get('page-title')

    def is_valid(self):
        if self.page_title:
            return True
        return False

    def save(self):
        homepage = HomePage.objects.all()[0]
        print(homepage.path)
        landing_page_content_type = ContentType.objects.get_for_model(
            LandingPage
        )
        landing_page = LandingPage(
            title=self.page_title,
            heading=self.page_title,
            draft_title=self.page_title,
            slug=self.page_title.replace(' ', '-'),
            content_type=landing_page_content_type,
            show_in_menus=True
        )

        overview_content_type = ContentType.objects.get_for_model(
            OverviewPage
        )
        overview_page = OverviewPage(
            title='Overview',
            heading=self.page_title,
            draft_title='Overview',
            slug='overview',
            content_type=overview_content_type,
            show_in_menus=True,
        )

        resources_content_type = ContentType.objects.get_for_model(
            ResourcesPage
        )
        resources_page = ResourcesPage(
            title='Resources',
            heading=self.page_title,
            draft_title='Resources',
            slug='resources',
            content_type=resources_content_type,
            show_in_menus=True
        )

        homepage.add_child(instance=landing_page)
        landing_page.save_revision()
        landing_page.save()
        landing_page.add_child(instance=overview_page)
        landing_page.add_child(instance=resources_page)
        overview_page.save_revision()
        overview_page.save()
        resources_page.save_revision()
        resources_page.save()
