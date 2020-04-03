import string
import json

from urllib.parse import urlencode

from django import template
from django.conf import settings

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


def restructure_s3_link(s3_link, new_bucket_name=None):
    if s3_link is None:
        return None

    if s3_link.startswith('https://s3.amazonaws.com'):
        converted = s3_link[len('https://s3.amazonaws.com') + 1:]
        query_position = converted.find('?')
        if query_position >= 0:
            converted = converted[0:query_position]

        bucket_name_length = converted.find('/')
        bucket_name = converted[0:bucket_name_length]
        key = converted[bucket_name_length + 1:]

        if new_bucket_name:
            converted = 'https://' + new_bucket_name + '/' + key
        else:
            converted = 'https://' + bucket_name + '.s3.amazonaws.com/' + key

        return converted
    else:
        query_position = s3_link.find('?')
        if query_position >= 0:
            return s3_link[0:query_position]

        return s3_link


@register.simple_tag
def convert_s3_link(s3_link):
    if settings.DOWNLOADS_BUCKET_NAME:
        return restructure_s3_link(s3_link, settings.DOWNLOADS_BUCKET_NAME)
    else:
        return restructure_s3_link(s3_link)


@register.simple_tag
def convert_s3_document_link(s3_link):
    converted = convert_s3_link(s3_link)

    documents_position = converted.find('/documents/')
    if documents_position < 0:
        return converted

    documents_end_position = documents_position + len('/documents/')
    start_path = converted[:documents_end_position]
    end_path = converted[documents_end_position:]

    slash_position = end_path.find('/')
    if slash_position > 0:
        return start_path + end_path[slash_position + 1:]
    else:
        return start_path + end_path
