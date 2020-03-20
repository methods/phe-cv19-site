from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import  RichTextField
from django.db.models.fields import TextField

from core.models.pages import MethodsBasePage

class DemoPage(MethodsBasePage):
    heading = TextField(blank=True)
    intro = RichTextField(blank=True)

    content_panels = MethodsBasePage.content_panels + [
        FieldPanel('heading'),
        FieldPanel('intro'),
    ]
