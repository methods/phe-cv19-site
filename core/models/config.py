import boto3

from django.conf import settings

from wagtail.contrib.redirects.models import Redirect

from core.utils import invalidate_cache


class MethodsRedirect(Redirect):
  filename = "{0}/static_views/templates/redirects/index.html".format(settings.BASE_DIR)

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    if settings.AWS_ACCESS_KEY_ID_DEPLOYMENT:
      self.create_in_aws()

  def delete(self):
    if settings.AWS_ACCESS_KEY_ID_DEPLOYMENT:
      self.remove_from_aws()

    super().delete()

  def __str__(self):
    return "{0} -> {1}".format(self.old_path, self.link)

  @property
  def directory_key(self):
    key = self.old_path

    if key[0] =='/':
      key = key[1:]
    
    if key[-1] == '/':
      return "{0}index.html".format(key)
    return "{0}index.html".format(key + '/')

  def initialise_s3_client(self):
    return boto3.client(
      "s3",
      region_name=settings.AWS_REGION_DEPLOYMENT,
      aws_access_key_id=settings.AWS_ACCESS_KEY_ID_DEPLOYMENT,
      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_DEPLOYMENT
    )

  def create_in_aws(self):
    s3_client = self.initialise_s3_client()

    s3_client.upload_file(
      Filename=self.filename,
      Bucket=settings.AWS_STORAGE_BUCKET_NAME_DEPLOYMENT,
      Key=self.directory_key,
      ExtraArgs={'ContentType': 'text/html', 'WebsiteRedirectLocation': self.link}
    )

    invalidate_cache(settings.AWS_DISTRIBUTION_ID)

  def remove_from_aws(self):
    s3_client = self.initialise_s3_client()

    s3_client.delete_object(
      Bucket=settings.AWS_STORAGE_BUCKET_NAME_DEPLOYMENT,
      Key=self.directory_key
    )

    invalidate_cache(settings.AWS_DISTRIBUTION_ID)

  class Meta:
    verbose_name = 'Redirect'
