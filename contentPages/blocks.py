from wagtail.core import blocks

class TitleAndParagraphBlock(blocks.StructBlock):
    title = blocks.TextBlock(required=True)
    paragraph = blocks.RichTextBlock(required=True)

