from django.db import models
from django.db.models.fields import TextField

from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel

from core.models.pages import MethodsBasePage


class LandingPage(MethodsBasePage):
    heading = TextField(blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    signup_intro = TextField(blank=True)
    subpages_background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    overview_subpage_heading = TextField(blank=True)
    overview_subpage_body = TextField(blank=True)
    overview_subpage = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    resources_subpage_heading = TextField(blank=True)
    resources_subpage_body = TextField(blank=True)
    resources_subpage = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET`_NULL,
        related_name='+'
    )

    body = RichTextField(null=True, blank=True)

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        ImageChooserPanel('banner_image'),
        FieldPanel('signup_intro'),
        ImageChooserPanel('subpages_background_image'),
        FieldPanel('overview_subpage_heading'),
        FieldPanel('overview_subpage_body'),
        PageChooserPanel('overview_subpage'),
        FieldPanel('resources_subpage_heading'),
        FieldPanel('resources_subpage_body'),
        PageChooserPanel('resources_subpage'),
        FieldPanel('body'),
    ]
