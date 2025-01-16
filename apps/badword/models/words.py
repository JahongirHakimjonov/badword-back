from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.shared.models import AbstractBaseModel


class Word(AbstractBaseModel):
    word = models.CharField(max_length=255, unique=True, verbose_name=_("Word"))
    is_active = models.BooleanField(default=False, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Word")
        verbose_name_plural = _("Words")
        ordering = ["word"]
        db_table = "bad_word"

    def __str__(self):
        return str(self.word)
