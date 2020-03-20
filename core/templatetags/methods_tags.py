import string
import json

from urllib.parse import urlencode

from django import template

from CMS.enums import enums

register = template.Library()

@register.simple_tag
def queryparams(*_, **kwargs):
    safe_args = {key: value for key, value in kwargs.items() if value is not None}
    if safe_args:
        return '?{}'.format(urlencode(safe_args))
    return ''


@register.simple_tag
def create_list(*args):
    return args


@register.simple_tag
def title_to_id(title):
    return title.replace(' ', '_').lower()

