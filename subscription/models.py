from django.db import models
from django.db.models.fields import TextField

from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import  RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel

from core.models.pages import MethodsBasePage

class SubscriptionPage(MethodsBasePage):
    subpage_types = []

    parent_page_type = [
        'contentPages.LandingPage'  # appname.ModelName
    ]

    heading = TextField(blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    sub_heading = TextField(blank=True)
    intro = TextField(blank=True)
    signup_details = RichTextField(blank=True)
    terms_agreement = RichTextField(blank=True)

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        ImageChooserPanel('banner_image'),
        FieldPanel('sub_heading'),
        FieldPanel('intro'),
        FieldPanel('signup_details'),
        FieldPanel('terms_agreement'),
    ]
