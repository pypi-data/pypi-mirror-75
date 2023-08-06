"""
Define algunos permisos estándar para utilizar a lo largo de toda la
aplicación.
"""
import logging

from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()


class IsOwnerAdminOrReadOnly(BasePermission):
    """
    Permite la lectura a través del método ``GET`` para
    cualquier usuario.

    Cualquier otro tipo de operación estará limitada a que el usuario que
    realiza la petición sea usuario administrador o que coincida con el valor
    del atributo ``user`` del objeto.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        if isinstance(obj, User):
            user = obj
        elif hasattr(obj, "user"):
            user = obj.user
        else:
            return False
        return request.user.is_superuser or user == request.user


class IsOwnerOrAdmin(BasePermission):
    """
    Cualquier operación de acceso estará limitada a que el usuario que
    realiza la petición sea usuario administrador o que coincida con el valor
    del atributo ``user`` del objeto.

    Este permiso comprueba el objeto que recibe, pudiendo ser un ``User``, un
    objeto con la propiedad ``user`` o cualquiera otra cosa, en este caso
    deberíamos devolver ``False`` como tratamiento de error.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            user = obj
        elif hasattr(obj, "user"):
            user = obj.user
        else:
            return False
        return request.user.is_authenticated and (
            user == request.user or request.user.is_superuser
        )
