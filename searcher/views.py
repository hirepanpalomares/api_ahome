from searcher.models import Property, ImageProperty
from rest_framework import viewsets, permissions
from .serializers import PropertySerializer
from django.http import HttpResponse, JsonResponse
from .manage_database import search_in_database
from django.core import serializers



def load_data_base(request):
    from .manage_database.google_drive_api import read_data_base_from_sheet
    from .manage_database import property_manager

    properties_in_sheet = read_data_base_from_sheet.PropertiesInformation()
    properties_info = properties_in_sheet.get_information()

    new_properties = property_manager.check_property_db(properties_info)

    for ahome_id,params in new_properties.items():
        property_manager.create_new_Property(params, ahome_id)
    
    return JsonResponse({})

def resultsSearcher_single(request, id_):#, where, operation, propType, room, bath, price):
    resultsObject = search_in_database.Results(id_)
    matches = resultsObject.matches
    
    resp = {}
    for prop in matches:
        serializer = PropertySerializer(prop).data
        resp[prop.ahome_id] = serializer
    
    #filters = resultsObject.fancyFilters
    #img_path = resultsObject.propImagesDirectory
   
    return JsonResponse(resp)

def resultsSearcher(request, where, operationType, propertyType, check, check_bath, price):
    if where == 'any':
        where = False
    else:
        if '_' in where:
            where = where.split('_')
            where = ' '.join(where)
    if propertyType == 'any':
        propertyType = False
    if operationType == 'any':
        operationType = False
    
    parameters = {
        'where': where, 
        'operationType': operationType, 
        'propertyType': propertyType, 
        'check': check, 
        'check-bath': check_bath, 
        'price': price
    }

    resultsObject = search_in_database.Results(parameters=parameters)
    matches = resultsObject.matches
    
    resp = {}
    for prop in matches:
        serializer = PropertySerializer(prop).data
        resp[prop.ahome_id] = serializer
    
    #filters = resultsObject.fancyFilters
    #img_path = resultsObject.propImagesDirectory
   
    return JsonResponse(resp)


def imagesSearcher(request, id_ahome):
    resultsObject = search_in_database.ImageResults(id_ahome)
    return JsonResponse(resultsObject.specs)


class TopTenViewSet(viewsets.ModelViewSet):
    
    serializer_class = PropertySerializer
    def get_queryset(self):
        resultsObject = search_in_database.Results(parameters='topten', onlyCoverImage=True)
        top10 = resultsObject.matches
        return top10






    