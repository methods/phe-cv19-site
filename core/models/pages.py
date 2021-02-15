from django.conf import settings

from wagtail.core.models import Page

from core.models.nav import Menu, Footer
from core.utils import parse_menu_item, find_subscription_page_url


class MethodsBasePage(Page):
    class Meta:
        abstract = True

    def unpublish(self, set_expired=False, commit=True):
        super(MethodsBasePage, self).unpublish(set_expired, commit)
        for child in self.get_children():
            child.specific.unpublish(set_expired, commit)

    @property
    def menu(self):
        menu_data = Menu.objects.first()
        menu = []
        if menu_data:
            for item in menu_data.menu_items:
                menu.append(parse_menu_item(item))
        return menu

    @property
    def footer(self):
        footer_data = Footer.objects.filter(name=footer_name).first()
        footer = []
        if footer_data:
            for item in footer_data.footer_items:
                footer.append(parse_menu_item(item))
        return footer

    @property
    def breadcrumbs(self):
        return self.get_ancestors().live()[1:]

    def get_context(self, request):
        context = super().get_context(request)
        context['page'] = self
        context['subscription_url'] = find_subscription_page_url()
        context['usage_url'] = settings.USAGE_URL
        return context
