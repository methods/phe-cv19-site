from django.contrib.staticfiles import finders
from django.conf import settings

from sass_processor.finders import CssFinder


def add_ignores(ignore_patterns):
    ignore = settings.STATICFILES_FINDERS_IGNORE

    if ignore:
        if ignore_patterns:
            ignore_patterns.extend(ignore)
        else:
            ignore_patterns = ignore

    return ignore_patterns


class FileSystemFinderIgnore(finders.FileSystemFinder):
    def list(self, ignore_patterns):
        return super().list(add_ignores(ignore_patterns))


class AppDirectoriesFinderIgnore(finders.AppDirectoriesFinder):
    def list(self, ignore_patterns):
        return super().list(add_ignores(ignore_patterns))


class DefaultStorageFinderIgnore(finders.DefaultStorageFinder):
    def list(self, ignore_patterns):
        return super().list(add_ignores(ignore_patterns))


class CssFinderIgnore(CssFinder):
    def list(self, ignore_patterns):
        return super().list(add_ignores(ignore_patterns))
