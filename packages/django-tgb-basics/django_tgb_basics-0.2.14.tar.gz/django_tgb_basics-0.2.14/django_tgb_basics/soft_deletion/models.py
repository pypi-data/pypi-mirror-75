class SoftDeletionModel(models.Model):
    """
    Modelo abstracto para la gestión de la eliminación
    *ficticia* de entidades.

    Cualquier clase que herede de ``SoftDeletionModel`` permite realizar un
    borrado `virtual`, es decir, los objetos no se eliminan de la base de datos
    sino que se marcan como eliminados en una operación estándar de borrado.

    Por defecto, cualquier consulta realizada sobre la colección ``objects``
    devolverá solamente aquellos objetos que no están marcados como eliminados.

    Para permitir el acceso a lo elementos marcados como eliminados,
    proporciona la colección ``all_objects`` que accede a **TODOS** los
    elementos. En realidad, no es más que un alias de la colección ``objects``
    original.

    Asimismo, proporciona el método ``hard_delete`` para la eliminación
    real (a nivel de base de datos) del objeto.

    Por ejemplo, supongamos que tenemos definido el model ``MyModel``, definido
    como cualquier otro modelo de Django, pero que hereda de
    ``SoftDeletionModel``:

    .. code-block::python

        from common.models import SoftDeletionModel


        class MyModel(SoftDeletionModel):
            ...


    - ``MyModel.objects.get(pk=123).delete()`` no eliminará el objeto de la
      base de datos, sino que actualizará el atributo ``deleted_at`` con la
      fecha y hora actual. Esto lo marca como eliminado.

    - ``MyModel.objects.all()`` devolverá todos los objetos que no tengan valor
      en el atributo ``deleted_at``, es decir, todos los que no están marcados
      como eliminados.

    - Si llamamos a ``MyModel.objects.get(pk=123)`` después de la llamada a
      ``delete`` obtendremos una excepción ``ObjectDoesNotExist``. En cambio,
      si llamamos a ``MyModel.all_objects.get(pk=123)`` sí que obtendremos
      el objeto marcado como eliminado. Evidentemente esto nos permite hacer un
      *restaurar* o *undelete* simplemente eliminando el valor del atributo
      ``deleted_at``, es decir, estableciendo su valor a ``None``.
    """

    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        Marca un objeto como eliminado, es decir, realiza la operación de
        borrado `ficticio`.
        """
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        """
        Realiza la operación de borrado definitivo (no `ficticio`).
        """
        super(SoftDeletionModel, self).delete(using=using, keep_parents=keep_parents)

