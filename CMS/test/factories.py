from wagtail.core.models import Site

from core.models.pages import MethodsBasePage


class PageFactory:

    @classmethod
    def create_home_page(cls, title='Test home page', path='1', depth=0):
        root_page = cls.get_root_page()
        home_page = MethodsBasePage(title=title, path=path, depth=depth)
        root_page.add_child(instance=home_page)
        home_page.save()
        return home_page

    @classmethod
    def get_root_page(cls):
        return cls.get_site().root_page

    @classmethod
    def get_site(cls):
        site = Site.objects.first()
        if not site.site_name:
            site.site_name = 'methodstest'
            site.save()
        return site
