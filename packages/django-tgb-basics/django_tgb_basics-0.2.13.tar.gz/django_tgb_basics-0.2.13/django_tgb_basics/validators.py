"""
Validadores generales.

Por el momento incluye validadores a nivel de imágenes y archivos.
Ver más info en:

https://docs.djangoproject.com/en/2.0/ref/validators/

List of MIME types: https://www.sitepoint.com/mime-types-complete-list/

Cómo usarlo:

Se recomienda insertar las restricciones en el archivo ``settings.py``:

    # Para los validadores de fichero
    MAX_UPLOAD_SIZE = 1048576   # 1Mb
    ALLOWED_IMAGE_MIME_TYPES = ['image/jpeg', 'image/png', 'image/gif']
    ALLOWED_VIDEO_MIME_TYPES = ['video/mpeg', 'video/quicktime', 'video/mp4']

Supongamos que tenemos un modelo de elemento que contiene un atributo ``media``
que puede contener un vídeo o una imagen. Lo definimos entonces como de tipo
``FileField``:

.. code-block:: python

    class Element(models.Model):

        def get_upload_path(instance, filename):
            ...

        ...
        media = models.FileField(
            upload_to=get_upload_path, null=True, blank=True,
            validators=[ContentTypeValidator(
                accepted_types=settings.ELEMENTS_SETTINGS['ALLOWED_IMAGE_MIME_TYPES'] +
                               settings.ALLOWED_VIDEO_MIME_TYPES),
                MaxFileSizeValidator(max_size=settings.ELEMENTS_SETTINGS['MAX_UPLOAD_SIZE'])])
        ...

En el ejemplo solamente se aceptarían archivos de tipos MIME contenidos en
``ALLOWED_IMAGE_MIME_TYPES`` y ``ALLOWED_VIDEO_MIME_TYPES``.

Así mismo, solamente se aceptan imágenes de máximo 1Mb de tamaño. Date cuenta
que el tamaño está especificado en bytes: 1024 x 1024 = 1048576.
"""

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.deconstruct import deconstructible


@deconstructible
class ContentTypeValidator:

    """
    Valida que el `content_type` de un archivo esté contenido en la lista
    `accepted_types`.
    Debe ser serializable para que funcione con las migraciones:
    https://docs.djangoproject.com/en/2.0/ref/validators/
    """

    message = 'Content type not accepted'
    code = 'content_type'

    def __init__(self, accepted_types):
        self.accepted_types = accepted_types

    def __call__(self, file):
        # Solamente validamos si el archivo es nuevo
        # y no si el archivo ya estaba en el campo
        # de una operación anterior, en cuyo caso
        # ya estaría validado
        if type(file.file) == InMemoryUploadedFile:
            content_type = file.file.content_type
            if content_type not in self.accepted_types:
                raise ValidationError(message=self.message, code=self.code)


@deconstructible
class MaxFileSizeValidator:

    """
    Valida que un archivo sea menor que el tamaño máximo permitido.
    El tamaño se especifica en bytes.
    Debe ser serializable para que funcione con las migraciones:
    https://docs.djangoproject.com/en/2.0/ref/validators/
    """

    message = 'File is too large'
    code = 'max_file_size'

    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, file):
        if self.max_size < file.size:
            raise ValidationError(message=self.message, code=self.code)
