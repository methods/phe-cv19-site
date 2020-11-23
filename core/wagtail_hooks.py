from axes.models import AccessAttempt

from wagtail.contrib.modeladmin.options import (ModelAdmin, modeladmin_register)
from wagtail.core import hooks
from wagtail.admin import widgets as wagtailadmin_widgets

from .models.nav import Menu, Footer
from contentPages.models import HomePage, CreateNewResourceType
from .models.config import MethodsRedirect


class MenuAdmin(ModelAdmin):

    model = Menu
    menu_label = 'Menu'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class FooterAdmin(ModelAdmin):

    model = Footer
    menu_label = 'Footer'  # ditch this to use verbose_name_plural from model
    menu_icon = 'form'  # change as required
    menu_order = 300  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = True  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class AccessAttemptAdmin(ModelAdmin):
    model = AccessAttempt
    menu_label = 'Access'
    menu_icon = 'code'
    menu_order = 5
    add_to_settings_menu = True


class MethodsRedirectAdmin(ModelAdmin):
    model = MethodsRedirect
    menu_label = 'Redirects'
    menu_icon = 'redirect'
    menu_order = 1000
    add_to_settings_menu = True


class CreateNewResourceTypeAdmin(ModelAdmin):
    model = CreateNewResourceType
    menu_label = 'Resource Types'
    menu_icon = 'form'
    menu_order = 400
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('resource_type',)
    list_filter = ('resource_type',)
    search_fields = ('resource_type',)


modeladmin_register(MenuAdmin)
modeladmin_register(FooterAdmin)
modeladmin_register(AccessAttemptAdmin)
modeladmin_register(CreateNewResourceTypeAdmin)
modeladmin_register(MethodsRedirectAdmin)


@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):
    if isinstance(page, HomePage):
        yield wagtailadmin_widgets.PageListingButton(
            'Create Campaign',
            '/admin/create-campaign/',
            priority=60
        )


@hooks.register('register_rich_text_features')
def unregister_document_feature(features):
    features.default_features.remove('document-link')

# Remove the default wagtail redirect object
for item in hooks._hooks['register_settings_menu_item']:
    if (item[0].__name__ == 'register_redirects_menu_item'):
        hooks._hooks['register_settings_menu_item'].remove(item)


