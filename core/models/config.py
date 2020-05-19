from wagtail.contrib.redirects.models import Redirect


class MethodsRedirect(Redirect):
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

  def __str__(self):
    return "{0} -> {1}".format(self.old_path, self.link)

  class Meta:
    verbose_name = 'Redirect'
