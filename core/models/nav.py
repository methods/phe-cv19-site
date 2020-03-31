from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.snippets.models import register_snippet


class SimpleMenuItem(blocks.StructBlock):
    label = blocks.CharBlock(required=False, help_text='Leave blank to use the page name')
    link_page = blocks.PageChooserBlock(required=False, help_text='Link to an internal page')
    link_url = blocks.CharBlock(required=False, help_text='Link to an external page')

    class Meta:
        icon = 'link'


class MultiMenuItem(blocks.StructBlock):
    label = blocks.CharBlock(required=True)
    menu_items = blocks.StreamBlock([
        ('simple_menu_item', SimpleMenuItem())
    ], icon='arrow-left', label='Items')


@register_snippet
class Menu(models.Model):
    name = models.CharField(max_length=255)
    menu_items = StreamField([
        ('simple_menu_item', SimpleMenuItem()),
    ])

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('menu_items')
    ]

    def __str__(self):
        return self.name


@register_snippet
class Footer(models.Model):
    name = models.CharField(max_length=255)
    footer_items = StreamField([
        ('footer_item', SimpleMenuItem()),
    ])

    panels = [
        FieldPanel('name'),
        StreamFieldPanel('footer_items')
    ]

    def __str__(self):
        return self.name
