from django.db import models
from django.db.models.fields import TextField, CharField
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
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
        on_delete=models.SET_NULL,
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


class OverviewPage(MethodsBasePage):
    heading = TextField(blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = RichTextField(null=True, blank=True)

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        ImageChooserPanel('banner_image'),
        FieldPanel('body'),
    ]


class ResourceItemPreview(Orderable):
    page = ParentalKey("contentPages.ResourcesPage", related_name="resource_items")

    heading = TextField(blank=True)
    description = TextField(blank=True)
    preview_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    resource_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('heading'),
        FieldPanel('description'),
        ImageChooserPanel('preview_image'),
        PageChooserPanel('resource_page'),
    ]


class ResourcesPage(MethodsBasePage):
    heading = TextField(blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        ImageChooserPanel('banner_image'),
        MultiFieldPanel([
            InlinePanel('resource_items')
        ], heading='Resource Items'),
    ]


class ResourceItemPage(MethodsBasePage):
    heading = TextField(blank=True)
    description = TextField(blank=True)
    preview_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    preview_image_screen_reader_text = TextField(blank=True)

    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.CASCADE,
        verbose_name='Upload document'
    )

    product_code = CharField(max_length=256, blank=True, null=True)
    overview = RichTextField()
    format = CharField(max_length=256, blank=True, null=True)
    file_size = CharField(max_length=256, blank=True, null=True)
    link_url = CharField(max_length=2048, blank=True)

    content_panels = MethodsBasePage.content_panels + [

        MultiFieldPanel([
            FieldPanel('heading'),
            FieldPanel('description'),
            DocumentChooserPanel('link_document'),
            ImageChooserPanel('preview_image'),
            FieldPanel('preview_image_screen_reader_text'),
        ], heading='Header section'),
        MultiFieldPanel([
            FieldPanel('product_code'),
            FieldPanel('overview'),
            FieldPanel('format'),
            FieldPanel('file_size'),
        ], heading='Details'),
    ]
