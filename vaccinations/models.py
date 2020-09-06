from django.db import models

from drugs.models import Drug


class Vaccination(models.Model):
    rut = models.CharField(verbose_name=_("Rut"), max_length=100)
    dose = models.DecimalField(verbose_name=_("Dose"))
    date = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT)
