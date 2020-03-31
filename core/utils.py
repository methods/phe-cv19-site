import glob
import logging
import pyclamd

import boto3

from django.core.management import call_command
from django.conf import settings

from os.path import isfile, join, relpath, splitext

from wagtail.core.signals import page_published, page_unpublished

from errors.models import VirusException


logger = logging.getLogger(__name__)


def _log_and_print(msg: str):
    print(msg)
    logger.info(msg)


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
    return page.url


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


def is_s3_deployment_configured() -> bool:
    """
    Return True if all three settings needed to deploy site to S3 are set to something valid-seeming.
    """
    s3_settings = (
        settings.AWS_ACCESS_KEY_ID_DEPLOYMENT,
        settings.AWS_SECRET_ACCESS_KEY_DEPLOYMENT,
        settings.AWS_STORAGE_BUCKET_NAME_DEPLOYMENT,
        settings.AWS_REGION_DEPLOYMENT
    )
    are_set = (s3_setting != None and s3_setting !="" for s3_setting in s3_settings)
    return all(are_set)


def prerender_pages(sender, **kwargs):
    try:
        call_command('build')
        _log_and_print("Attempting site deployment...")
        if is_s3_deployment_configured():
            _log_and_print(f"...deploying site to s3 bucket: {settings.AWS_STORAGE_BUCKET_NAME_DEPLOYMENT}...")
            export_directory()
            _log_and_print(f"... deployment to s3 complete.")
        else:
            unset_s3_settings = [
                s3_setting["name"] for s3_setting in (
                    {
                        "name": "AWS_ACCESS_KEY_ID_DEPLOYMENT",
                        "value": settings.AWS_ACCESS_KEY_ID_DEPLOYMENT,
                    },
                    {
                        "name": "AWS_SECRET_ACCESS_KEY_DEPLOYMENT",
                        "value": settings.AWS_SECRET_ACCESS_KEY_DEPLOYMENT,
                    },
                    {
                        "name": "AWS_STORAGE_BUCKET_NAME_DEPLOYMENT",
                        "value": settings.AWS_STORAGE_BUCKET_NAME_DEPLOYMENT,
                    },
                    {
                        "name": "AWS_REGION_DEPLOYMENT",
                        "value": settings.AWS_REGION_DEPLOYMENT
                    }
                ) if s3_setting["value"] != None and s3_setting !=""
            ]
            _log_and_print(
                f"...AWS s3 access not configured - deployment skipped. Missing settings: {repr(unset_s3_settings)}"
            )
    except Exception as e:
        _log_and_print(f"Deployment to s3 failed: {repr(e)}")


def export_directory(path:str=''):
    """
    Glob directory structure found at settings.BUILD_DIR/path for html files.
    Upload html files and directory structure to AWS s3 bucket at settings.AWS_STORAGE_BUCKET_NAME_DEPLOYMENT
    (NB no empty dirs permitted in s3, so only directories with contents will be sent).
    Remove any .html files from settings.AWS_STORAGE_BUCKET_NAME_DEPLOYMENT that are NOT in settings.BUILD_DIR/path.
    """
    # get list of dicts with relative and absolute paths for each html files to upload
    directory_path = join(settings.BUILD_DIR, path)
    html_files_in_directory = glob.glob(f"{directory_path}/**/*.html", recursive=True)
    html_files_2_upload = [ {"Filename": f, "Key": relpath(f, start=directory_path)} for f in html_files_in_directory]

    # get S3 keys only as set
    s3_html_keys_2_upload = { f["Key"] for f in html_files_2_upload }

    s3_client = boto3.client(
        "s3",
        region_name = settings.AWS_REGION_DEPLOYMENT,
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID_DEPLOYMENT,
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY_DEPLOYMENT
    )

    # get complete set of bucket keys FOR HTML ONLY!
    paginator = s3_client.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket=settings.AWS_STORAGE_BUCKET_NAME_DEPLOYMENT)
    bucket_html_keys = set()
    for page in page_iterator:
        try:
            page_files = {
                s3_obj["Key"]  for s3_obj in page["Contents"]
                if splitext(s3_obj["Key"])[1] == '.html'
            }
            bucket_html_keys.update(page_files)
        except KeyError:
            continue

    # get diff of bucket keys vs uploaded s3 keys
    bucket_html_keys_2_remove = bucket_html_keys.difference(s3_html_keys_2_upload)

    # upload whats being uploaded
    for f in html_files_2_upload:
        s3_client.upload_file(
            Filename=f["Filename"],
            Bucket=settings.AWS_STORAGE_BUCKET_NAME_DEPLOYMENT,
            Key=f["Key"],
            ExtraArgs={'ContentType': 'text/html'}
        )

    # remove whats being removed
    for key in bucket_html_keys_2_remove:
        s3_client.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME_DEPLOYMENT,
            Key=key
        )

page_published.connect(prerender_pages)
page_unpublished.connect(prerender_pages)
