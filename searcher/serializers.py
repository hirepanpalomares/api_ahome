"""
    This file (serializers) is to convert the Query Sets to a JSON file
    or other Python datatypes that can be easilly rendered, so here is
    where the consults to the data base will be requested

"""

from rest_framework import serializers
from searcher.models import ImageProperty, Property


#searcher serializer

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'