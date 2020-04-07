from django.db import models
from django.db.models.fields import TextField

from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import  RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel

from core.models.pages import MethodsBasePage

class ErrorPage(MethodsBasePage):
    subpage_types = []

    parent_page_type = [
        'contentPages.HomePage'
    ]

    error_message = TextField(blank=True)
    error_message_details = TextField(blank=True)

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('error_message'),
    ]
