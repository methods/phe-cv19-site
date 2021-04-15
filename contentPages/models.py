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

from core.models.pages import MethodsBasePage


@register_snippet
class CreateNewResourceType(models.Model):
    resource_type = CharField(max_length=500, default='', blank=True, null=True)

    panels = [
            FieldPanel('resource_type'),
    ]

    @classmethod
    def get_resource_type_choices(cls):
        resource_types = []
        try:
            all_resource_types = CreateNewResourceType.objects.all().values_list('resource_type', flat=True)
            for resource_type in all_resource_types:
                resource_type_value = resource_type.lower().replace(' ', '_')
                resource_types.append((resource_type_value, resource_type))
        except:

            print('Resource types not present')
        return resource_types

    def __str__(self):
        return self.resource_type

    class Meta:
        verbose_name = "Resource Type"


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
    external_link = TextField(blank=True)

    page = ParentalKey("HomePage", related_name="campaign_items")

    panels = [
        FieldPanel('caption'),
        ImageChooserPanel('thumbnail_image'),
        PageChooserPanel('campaign_landing_page'),
        FieldPanel('external_link'),
    ]

    @property
    def show_tile(self):
        if self.campaign_landing_page:
            return self.campaign_landing_page.live
        return True
    

class HomePage(MethodsBasePage):
    subpage_types = [
        'contentPages.LandingPage',
        'contentPages.OverviewPage',
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
    overview_subpage_text = RichTextField(default='', blank=True)
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
    resources_subpage_text = RichTextField(default='', blank=True)
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
        FieldPanel('overview_subpage_text'),
        # SnippetChooserPanel('overview_subpage_body'),
        FieldPanel('resources_subpage_heading'),
        FieldPanel('resources_subpage_text'),
        # SnippetChooserPanel('resources_subpage_body'),
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
    subpage_types = [
        'contentPages.ResourcesPage'
    ]

    parent_page_type = [
        'contentPages.LandingPage',
        'contentPages.HomePage'
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


class ExternalResource(Orderable):
    caption = TextField(blank=True)
    thumbnail_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    external_link = TextField(blank=False)

    page = ParentalKey("ResourcesPage", related_name="external_resources")

    panels = [
        FieldPanel('caption'),
        ImageChooserPanel('thumbnail_image'),
        FieldPanel('external_link'),
    ]


class ResourcesPage(MethodsBasePage):
    subpage_types = ['contentPages.ResourceItemPage']

    parent_page_type = [
        'contentPages.LandingPage',
        'contentPages.OverviewPage'
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

    signup_message = RichTextField(blank=True, null=True)

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        ImageChooserPanel('banner_image'),
        FieldPanel('signup_message'),
        MultiFieldPanel(
            [
                ImageChooserPanel('sidebar_image'),
                FieldPanel('sidebar_screenreader_text'),
                FieldPanel('sidebar_note'),
            ], 'Side bar'),
        InlinePanel('external_resources', label="External resources")
    ]

    @property
    def site_heading(self):
        parent = self.get_parent()
        return parent.landingpage.heading

    @property
    def resource_count(self):
        resource_item_page_count = ResourceItemPage.objects.live().descendant_of(self).count()
        external_resource_count = self.external_resources.count()
        return resource_item_page_count + external_resource_count

    @property
    def resource_list(self):
        return ResourceItemPage.objects.live().descendant_of(self)

    @property
    def ordered_resource_list(self):
        resource_pages = ResourceItemPage.objects.live().descendant_of(self)
        return resource_pages.order_by('-last_published_at')

    @property
    def campaign_slug(self):
        parent = self.get_parent()
        return parent.landingpage.slug

    @property
    def campaign_name(self):
        parent = self.get_parent()
        return parent.specific.heading


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

    document_type = models.ForeignKey(
        'contentPages.CreateNewResourceType',
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL,
    )

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

    @property
    def campaign_name(self):
        grandparent = self.get_parent().get_parent()
        return grandparent.specific.heading

    @property
    def campaign_live(self):
        try:
            grandparent = self.get_parent().get_parent()
            return grandparent.live
        except Exception:
            return False


# @register_snippet
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
    caption = models.ForeignKey(
        'contentPages.CreateNewResourceType',
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL,
    )

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

    document_type = models.ForeignKey(
        'contentPages.CreateNewResourceType',
        null=True,
        blank=False,
        related_name='+',
        on_delete=models.SET_NULL,
    )

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        FieldPanel('subtitle'),
        ImageChooserPanel('banner_image'),
        FieldPanel('signup_intro'),
        FieldPanel('asset_type_header'),
        FieldPanel('document_type')
    ]

    def resource_item_pages(self):
        live_pages = []
        resource_pages = ResourceItemPage.objects.live().filter(document_type=self.document_type)
        for page in resource_pages:
            if page.campaign_live:
                live_pages.append(page)
        return live_pages

    def ordered_resource_item_pages(self):
        live_pages = []
        resource_pages = ResourceItemPage.objects.live().filter(document_type=self.document_type)
        resource_pages = resource_pages.order_by('-last_published_at')
        for page in resource_pages:
            if page.campaign_live:
                live_pages.append(page)
        return live_pages

    def asset_count(self):
        live_pages = []
        resource_pages = ResourceItemPage.objects.live().filter(document_type=self.document_type)
        for page in resource_pages:
            if page.campaign_live:
                live_pages.append(page)
        resource_count = len(live_pages)
        return resource_count





