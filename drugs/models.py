from django.db import models

from django.utils.translation import ugettext_lazy as _


class Drug(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    code = models.CharField(verbose_name=_("Code"), max_length=10, unique=True)
    description = models.CharField(verbose_name=_("Description"), max_length=255)
