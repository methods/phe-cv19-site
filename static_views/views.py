import os

from bakery.views.base import BuildableMixin

from django.conf import settings
from django.shortcuts import render
from django.test.client import RequestFactory
from django.views.generic import View

from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core.models import Site


class SitemapView(View, BuildableMixin):

  @property
  def build_method(self):
    return self.build_object

  def get(self, request):
    return sitemap(request)

  def get_content(self):
    response = self.get(self.request)
    return response.render().content

  def get_build_path(self):
    return os.path.join(settings.BUILD_DIR, 'sitemap.xml')

  def get_site(self):
    return Site.objects.first()

  def build_object(self):
    site = self.get_site()
    self.request = RequestFactory(SERVER_NAME=site.hostname).get('/sitemap.xml')
    path = self.get_build_path()
    self.build_file(path, self.get_content())
