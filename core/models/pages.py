from django.core.management import call_command
from django.db import transaction

from wagtail.core.models import Page

from CMS.enums import enums
from core.models.nav import Menu, Footer
from core.utils import parse_menu_item, find_subscription_page_url


class MethodsBasePage(Page):
    class Meta:
        abstract = True

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

    def get_context(self, request):
        context = super().get_context(request)
        context['page'] = self
        context['subscription_url'] = find_subscription_page_url()
        return context
