import pyclamd

import boto3

from django.core.management import call_command
from django.conf import settings

from os import listdir
from os.path import isfile, join

from wagtail.core.signals import page_published, page_unpublished

from errors.models import VirusException


def fallback_to(value, default_value):
    return value if value is not None else default_value


def parse_menu_item(menu_item):
    label = menu_item.value.get('label') if menu_item.value.get('label') else menu_item.value.get('link_page').title
    item_dict = {'label': label}
    if 'menu_items' in menu_item.value:
        sub_items = []
        for item in menu_item.value.get('menu_items'):
            sub_items.append(parse_menu_item(item))
        item_dict['sub_items'] = sub_items
    else:
        item_dict['sub_items'] = None
        item_dict['url'] = menu_item.value.get('link_page').url

    return item_dict


def find_subscription_page_url():
    from subscription.models import SubscriptionPage
    page = SubscriptionPage.objects.first()
    if page is None:
        return '#'
    return page.full_url


def check_for_virus(instance):
    if instance.file.closed:
        with open(instance.file.path, 'rb') as file:
            file_content = file.read()
    else:
        file_content = instance.file.read()

    has_virus, name = is_infected(file_content)

    if has_virus:
        raise VirusException(_('Virus "{}" was detected').format(name))

    return instance


def is_infected(stream):
    clam = get_clam()
    if not settings.CLAMAV_ACTIVE or clam is None:
        return None, ''

    result = clam.scan_stream(stream)
    if result:
        return True, result['stream'][1]

    return False, ''


def get_clam():
    try:
        clam = pyclamd.ClamdUnixSocket()

        # test if server is reachable
        clam.ping()

        return clam
    except pyclamd.ConnectionError:
        # if failed, test for network socket
        try:
            cd = pyclamd.ClamdNetworkSocket()
            cd.ping()
            return cd
        except pyclamd.ConnectionError:
            raise ValueError('could not connect to clamd server either by unix or network socket')


def is_s3_configured():
    s3_settings = (settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_STORAGE_BUCKET_NAME)
    are_set = (s3_setting != None and s3_setting !="" for s3_setting in s3_settings)
    return all(are_set)



def prerender_pages(sender, **kwargs):
    call_command('build')
    if is_s3_configured():
        export_directory()


def export_directory(path:str=''):
    directory_path = join(settings.BUILD_DIR, path)
    directory_contents = listdir(directory_path)
    s3_client = boto3.client(
        "s3",
        region_name = "eu-west-2",
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    )
    for f in directory_contents:
        if f != 'static':
            full_filepath = join(directory_path , f)
            local_filepath = join(path, f)
        if isfile(full_filepath):
            s3_client.upload_file(
                Filename=full_filepath,
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=local_filepath
            )
        else:
            export_directory(local_filepath)


page_published.connect(prerender_pages)
page_unpublished.connect(prerender_pages)
