from django.db import models
from searcher.models import Property, ImageProperty
from . import formData


class Results(object):

    fields = [
        'where', 
        'operationType', 
        'propertyType', 
        'check', 
        'check-bath', 
        'price'
    ]
    cities = {
        'MORELIA':[
            'TRES MARIAS', 
            'LAS AMERICAS', 
            'ALTOZANO', 
            'SALIDA SALAMANCA', 
            'MADERO', 
            'CAMELINAS', 
            'CIUDAD INDUSTRIAL',
            'LA HUERTA', 
            'NICOLAITAS ILUSTRES'
        ],
        'URUAPAN':[
            'URUAPAN'
        ],
        'PATZCUARO':[
            'PATZCUARO'
        ],
        'IXTAPA':[
            'IXTAPA'
        ],
        'QUERETARO':[
            'QUERETARO'
        ],
        'CIUDAD DE MEXICO':[
            'POLANCO'
        ]
    }

    def __init__(self, parameters, onlyCoverImage=False, specific_id=False):
        self.filters = parameters
        self.only_cover_image = onlyCoverImage
        self.specific_id = specific_id
        self.formularyData = {}
        self.matches = {}
        self.fancyFilters = {}
        self.propImagesDirectory = {}
        self.cleanData = {}
        if self.specific_id:
            pass
        else:
            if self.filters == 'topten':
                self.__findTopten()
                
            else:
                self.__many_fields()
                self.cleanData = formData.process(self.formularyData)
                self.__findExactMatch()
        self.__findPropertyImages()
        #self.__processOut()
    
    def __only_one_field(self):
        type_ = ["1", "2", "3", "4", "5", "6", "7"]
        if self.only_one_field == 'ventas':
            self.formularyData = {'operationType':'1'}
        elif self.only_one_field == 'rentas':
            self.formularyData = {'operationType':'2'}
        elif self.only_one_field in type_:
            self.formularyData = {'propertyType': self.only_one_field}
        else:
            if '_' in self.only_one_field:
                self.only_one_field = ' '.join(self.only_one_field.split('_'))
            self.formularyData = {'where':self.only_one_field}
        for f in self.fields:
            if f not in self.formularyData:
                    self.formularyData[f] = False

    def __many_fields(self):
        self.formularyData = {f:self.filters[f] for f in self.fields if f in self.filters}
        for f in self.fields:
            if f not in self.formularyData:
                self.formularyData[f] = False
    
    def __findTopten(self):
        query_set = Property.objects.order_by('price')[::-1][:10]
        for prop in query_set:
            img = ImageProperty.objects.filter(ahome_id=prop.ahome_id)
            format_ = ''
            try:
                assert(len(img) >= 1)
                format_ = img[0].format_image
            except AssertionError:
                # no hay imagenes
                pass
            prop.img_format = format_
            
        self.matches = query_set

    def __findSpecificProperty(self):
        results = Property.objects.all()
        results = results.filter(ahome_id=self.specific_id)
        self.matches = results

    def __findExactMatch(self):
        """
            Antes de empezar a llamar a este metodo dprecar a self.cities
        """
        place_filter = self.cleanData['where']
        operation_filter = self.cleanData['operationType']
        type_filter = self.cleanData['propertyType']
        room_filter = self.cleanData['rooms']
        bath_filter = self.cleanData['baths']
        price_filter = self.cleanData['price']
        results = Property.objects.all()
        # Filtering by place .......
        if place_filter: #assuring is not false
            if place_filter in self.cities:
                results = results.filter(zone__in=self.cities[place_filter])
            else:
                results = results.filter(zone=place_filter)
        # Filtering by operation (renta, compra, etc)
        if operation_filter:
            results = results.filter(action=operation_filter)
        # Filtering by property type 
        if type_filter:
            results = results.filter(property_type__in=type_filter)
        # Filtering by rooms 
        if room_filter:
            results = results.filter(rooms__gt=room_filter)
        # Filtering by baths 
        if bath_filter:
            results = results.filter(baths__gt=bath_filter)
        # Filtering by price
        if price_filter:
            if price_filter != 1E+06 and price_filter != 1E+03:
                results = results.filter(price__lt=price_filter*1.25)
        # Filtering by status
        for prop in results:
            img = ImageProperty.objects.filter(ahome_id=prop.ahome_id)
            format_ = ''
            try:
                assert(len(img) >= 1)
                format_ = img[0].format_image
            except AssertionError:
                # no hay imagenes
                pass
            prop.img_format = format_
        self.matches = results
    
    def __findPropertyImages(self):
        dictionary = {}
        imgs = ImageProperty.objects.all()
        for prop in self.matches:
            prop_imgs = imgs.filter(ahome_id=prop.ahome_id)
            
            try:
                assert(len(prop_imgs) != 0)
                if self.only_cover_image:
                    dictionary[prop.ahome_id] = prop_imgs[:1]
                else:
                    dictionary[prop.ahome_id] = prop_imgs
            except AssertionError:
                pass
        self.propImagesDirectory = dictionary
            
    def __processOut(self):
        for prop in self.matches:
            print(prop.price)
            prop.price = "{:,}".format(prop.price)
            print(prop.price)
        
        applied_filters = {filter_:self.cleanData[filter_] for filter_ in self.cleanData if self.cleanData[filter_] != False}
        if 'propertyType' in applied_filters:
            applied_filters['propertyType'] = applied_filters['propertyType'][0]
        
        if 'price' in applied_filters:
            applied_filters['price'] = "$ " + "{:,}".format(applied_filters['price'])
        
        filters = [applied_filters[filt] for filt in applied_filters]
        self.fancyFilters = filters

    @staticmethod
    def getSpecificProperty(id):
        return Property.objects.filter(ahome_id=id)[0]
    
    @staticmethod
    def getImagesFromSpecificProperty(id):
        imgs = ImageProperty.objects.filter(ahome_id=id)
        return imgs



class ImageResults(object):


    def __init__(self, id_ahome):
        self.id = id_ahome
        self.specs = {}
        self.main()
    
    def main(self):
        info = ImageProperty.objects.all()
        info = info.filter(ahome_id=self.id)[0]
        self.specs = {
            'number': info.number_of_images,
            'format': info.format_image
        }
        


