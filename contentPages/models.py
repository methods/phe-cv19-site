from django.conf import settings
from django.db import models
from django.db.models.fields import TextField, CharField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from CMS.enums import enums

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

    @property
    def show_tile(self):
        if self.campaign_landing_page:
            return self.campaign_landing_page.live
        return True
    


class HomePage(MethodsBasePage):
    subpage_types = [
        'contentPages.LandingPage',
        'subscription.SubscriptionPage',
        'errors.ErrorPage',
        'contentPages.AllResourcesPage'
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
    signup_intro = RichTextField(null=True, blank=True)
    campaign_list_header = RichTextField(null=True, blank=True)

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
    OVERVIEW_HEADING = 'Overview'
    overview_subpage_heading = TextField(default=OVERVIEW_HEADING)
    overview_subpage_body = models.ForeignKey(
        'contentPages.SharedContent',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    overview_subpage = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    RESOURCES_HEADING = 'Resources'
    resources_subpage_heading = TextField(default=RESOURCES_HEADING)
    resources_subpage_body = models.ForeignKey(
        'contentPages.SharedContent',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
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
        SnippetChooserPanel('overview_subpage_body'),
        FieldPanel('resources_subpage_heading'),
        SnippetChooserPanel('resources_subpage_body'),
        FieldPanel('body'),
    ]

    def get_resources_subpage(self):
        children = self.get_children().specific()
        for child in children:
            if type(child) == ResourcesPage:
                return child

    def get_overview_subpage(self):
        children = self.get_children().specific()
        for child in children:
            if type(child) == OverviewPage:
                return child


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

    document_type = models.CharField(max_length=25, choices=enums.asset_types, default='posters')

    upload_link = TextField(blank=True, default='')

    product_code = CharField(max_length=256, blank=True, null=True, default='')
    overview = RichTextField(blank=True, default='')
    format = CharField(max_length=256, blank=True, null=True, default='')
    file_size = CharField(max_length=256, blank=True, null=True, default='')

    content_panels = MethodsBasePage.content_panels + [

        MultiFieldPanel([
            FieldPanel('heading'),
            FieldPanel('description'),
            FieldPanel('upload_link'),
            DocumentChooserPanel('link_document'),
            FieldPanel('document_type'),
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
        return settings.FINAL_SITE_DOMAIN + self.url


@register_snippet
class SharedContent(models.Model):

    title = CharField(max_length=500, default='', blank=True)
    content_body = RichTextField(default='', blank=True)

    panels = [

        MultiFieldPanel([
                FieldPanel("title"),
                FieldPanel("content_body")
            ], heading='Shared Content')
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Shared Content Snippet"


class AllResourcesTile(Orderable):
    caption = models.CharField(max_length=25, choices=enums.asset_types, default='')
    thumbnail_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    page = ParentalKey("AllResourcesPage", related_name="asset_types")

    panels = [
        FieldPanel('caption'),
        ImageChooserPanel('thumbnail_image')
    ]

    def get_asset_string(self):
        for asset_type in enums.asset_types:
            if asset_type[0] == self.caption:
                return asset_type[1]


class AllResourcesPage(MethodsBasePage):
    subpage_types = [
        'contentPages.AssetTypePage',
    ]

    parent_page_type = [
        'contentPages.HomePage'
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

    ASSET_LIST_HEADER = 'Resources List'
    signup_intro = TextField(blank=True)
    asset_list_header = TextField(default=ASSET_LIST_HEADER)

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        FieldPanel('subtitle'),
        ImageChooserPanel('banner_image'),
        FieldPanel('signup_intro'),
        FieldPanel('asset_list_header'),
        InlinePanel('asset_types', label='Asset Types')
    ]

    def get_child_of_type(self, asset_type):
        children = self.get_children()
        for child in children:
            if child.specific.document_type == asset_type:
                return child


class AssetTypePage(MethodsBasePage):
    subpage_types = []

    parent_page_type = ['contentPages.AllResourcesPage']

    heading = TextField(blank=True)
    subtitle = TextField(blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    ASSET_TYPE_HEADER = 'Type Resources'
    signup_intro = TextField(blank=True)
    asset_type_header = TextField(default=ASSET_TYPE_HEADER)
    document_type = models.CharField(max_length=25, choices=enums.asset_types, default='posters')

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        FieldPanel('subtitle'),
        ImageChooserPanel('banner_image'),
        FieldPanel('signup_intro'),
        FieldPanel('asset_type_header'),
        FieldPanel('document_type')
    ]

    def resource_item_pages(self):
        return ResourceItemPage.objects.filter(document_type=self.document_type)

    def asset_count(self):
        resource_count = len(ResourceItemPage.objects.filter(document_type=self.document_type))
        return resource_count


