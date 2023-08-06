"""
Querysets personalizados y comunes para usar en cualquier app.
"""

from django.utils import timezone
from django.contrib.gis.db.models import QuerySet


class SoftDeletionQuerySet(QuerySet):
    """
    QuerySet específico para el borrado `ficticio`.
    Proporciona soporte para realizar el borrado suave o ficticio y
    el borrado definitivo, así como métodos para obtener los objetos
    borrados y no borrados.
    """

    def delete(self):
        """
        Sobreescribe el método ``delete`` por defecto de un objeto actualizando
        la fecha de borrado para realizar el borrado `ficticio`.
        """
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        """
        Elimina definitivamente un objeto. Corresponde con el comportamiento
        por defecto del método ``delete``.
        """
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        """
        Helper que filtra los elementos que no están marcados como borrados.
        Posiblemente no resulte de mucha utilidad, pero se usa internamente
        por el sistema de borrado.
        """
        return self.filter(deleted_at=None)

    def dead(self):
        """
        Helper que filtra los elementos que están marcados como borrados.
        Posiblemente no resulte de mucha utilidad, pero se usa internamente
        por el sistema de borrado.
        """
        return self.exclude(deleted_at=None)
