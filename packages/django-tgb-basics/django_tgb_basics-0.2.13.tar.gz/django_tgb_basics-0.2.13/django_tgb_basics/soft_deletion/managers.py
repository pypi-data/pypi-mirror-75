"""
Managers personalizados comunes para usar a lo largo de todas las apps.
"""

from django.contrib.gis.db import models

from .querysets import SoftDeletionQuerySet


class SoftDeletionManager(models.Manager):
    """
    Manager para gestionar el borrado `ficticio`.
    """

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        """
        Devuelve un QuerySet con solamente los objetos marcados como borrados
        o todos en función del valor del atributo ``alive_only``.
        """
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        """
        Realiza una eliminación `masiva` y definitiva (no `ficticia`) de
        los elementos del queryset.
        """
        return self.get_queryset().hard_delete()
