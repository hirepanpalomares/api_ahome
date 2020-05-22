from searcher.models import Property, ImageProperty
from rest_framework import viewsets, permissions
from .serializers import SearcherSerializer

# Searcher Viewset

class SearcherViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SearcherSerializer