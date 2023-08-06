from rest_framework.viewsets import ViewSet


class MultiSerializerViewSet(ViewSet):
    """
    Allows using several serializers in a Django REST Framwork Viewset
    based on HTTP verb.

    You should define the attribute `serializers` as a dictionary where
    the key is the action and the value is the serializer class.
    You should define at least the `default` key.

    .. code:: python

        from django_tgb_basics.viewsets import MultiSerializerViewSet
        from .models import MyModel
        from .serializers import (
            BasicSerializer,
            AnotherSerializer
        )

        class MyModelViewSet(MultiSerializerViewSet):
            queryset = MyModel.objects.all()
            serializers = {
                'default': BasicSerializer,
                'create': BasicSerializer,
                'update': BasicSerializer,
                'partial_update': BasicSerializer,
                'retrieve': AnotherSerializer,
            }

    This is based on the following StackOverflow question
    Ref. https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset
    """

    serializers = {"default": None}

    def get_serializer_class(self):
        """
        Returns the serializer based on the HTTP verb (action).
        If no action is defined, returns the default serializer.
        """
        return self.serializers.get(self.action, self.serializers["default"])

