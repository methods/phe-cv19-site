from django.db import models
from django.db.models.fields import TextField, CharField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from core.models.pages import MethodsBasePage


class HomePageCampaign(Orderable):
    caption = TextField(blank=True)
    thumbnail_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    campaign_landing_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    page = ParentalKey("HomePage", related_name="campaign_items")

    panels = [
        FieldPanel('caption'),
        ImageChooserPanel('thumbnail_image'),
        PageChooserPanel('campaign_landing_page'),
    ]


class HomePage(MethodsBasePage):
    subpage_types = [
        'contentPages.LandingPage',
        'subscription.SubscriptionPage',
    ]

    parent_page_type = [
        'wagtailcore.Page'
    ]

    heading = TextField(blank=True)
    subtitle = TextField(blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    signup_intro = TextField(blank=True)
    campaign_list_header = TextField(blank=True)

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        FieldPanel('subtitle'),
        ImageChooserPanel('banner_image'),
        FieldPanel('signup_intro'),
        FieldPanel('campaign_list_header'),
        InlinePanel('campaign_items', label="Campaign list")
    ]


class LandingPage(MethodsBasePage):
    subpage_types = [
        'contentPages.OverviewPage',  # appname.ModelName
        'contentPages.ResourcesPage',  # appname.ModelName
    ]

    parent_page_type = [
        'wagtailcore.HomePage'  # appname.ModelName
    ]

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
    body = RichTextField(null=True, blank=True)

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        ImageChooserPanel('banner_image'),
        FieldPanel('body'),
    ]

    @property
    def site_heading(self):
        parent = self.get_parent()
        return parent.landingpage.heading

    @property
    def campaign_slug(self):
        parent = self.get_parent()
        return parent.landingpage.slug


class ResourcesPage(MethodsBasePage):
    subpage_types = ['contentPages.ResourceItemPage']

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
    sidebar_note = TextField(blank=True, null=True)
    sidebar_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    sidebar_screenreader_text = TextField(blank=True, null=True)

    signup_message = TextField(blank=True, null=True)

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        ImageChooserPanel('banner_image'),
        FieldPanel('signup_message'),
        MultiFieldPanel(
            [
                ImageChooserPanel('sidebar_image'),
                FieldPanel('sidebar_screenreader_text'),
                FieldPanel('sidebar_note'),
            ], 'Side bar')
    ]

    @property
    def site_heading(self):
        parent = self.get_parent()
        return parent.landingpage.heading

    @property
    def resource_count(self):
        return ResourceItemPage.objects.live().descendant_of(self).count()

    @property
    def resource_list(self):
        return ResourceItemPage.objects.live().descendant_of(self)

    @property
    def campaign_slug(self):
        parent = self.get_parent()
        return parent.landingpage.slug


class ResourceItemPage(MethodsBasePage):
    subpage_types = []

    parent_page_type = ['contentPages.ResourcesPage']

    heading = TextField(blank=True)
    description = RichTextField(blank=True, null=True, default='')
    preview_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    preview_image_screen_reader_text = TextField(blank=True, default='')

    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name='Upload document'
    )

    product_code = CharField(max_length=256, blank=True, null=True, default='')
    overview = RichTextField(blank=True, default='')
    format = CharField(max_length=256, blank=True, null=True, default='')
    file_size = CharField(max_length=256, blank=True, null=True, default='')

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

    @property
    def link_url(self):
        return self.get_site().hostname + self.url_path
