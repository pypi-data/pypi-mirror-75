from django.db import models

from django.utils.translation import ugettext as _


class TimeStampedModel(models.Model):
    """
    Clase abstracta que proporciona campos de fecha de cración y modificación
    autogestionadas.
    """

    #: Date and time of creation
    created = models.DateTimeField(_("created"), auto_now_add=True, db_index=True)
    #: Date and time of the last update
    modified = models.DateTimeField(_("modified"), auto_now=True, db_index=True)

    class Meta:
        get_latest_by = "modified"
        ordering = ("-modified", "-created")
        abstract = True
