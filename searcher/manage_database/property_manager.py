from django.db import models
from searcher.models import Property, ImageProperty
from django.core.exceptions import ObjectDoesNotExist
#from . import formData

def check_property_db(info):
    new = {}
    for ahome_identifier in info:
        try:
            Property.objects.get(ahome_id=ahome_identifier)
        except ObjectDoesNotExist:
            new[ahome_identifier] = info[ahome_identifier]
    return new

def check_image_url_db(info):
    new = {}
    for ahome_identifier in info:
        try:
            ImageProperty.objects.get(ahome_id=ahome_identifier)
        except ObjectDoesNotExist:
            new[ahome_identifier] = info[ahome_identifier]
    return new

def create_new_Property(obj, a_id):
    type_ = obj['TYPE']
    act = obj['ACTION']
    city = obj['CITY']
    state = obj['STATE']
    zone = obj['ZONE']
    hood = obj['HOOD']
    addr = obj['ADDRES']
    price = obj['PRICE']
    tot_a = obj['TOTAL AREA']
    const_a = obj['CONSTRUCTION AREA']
    room = obj['ROOMS']
    half_baths = obj['HALF BATHS']
    bath = obj['BATHS']
    park = obj['PARKING']
    des = obj['DESCRIPTION']
    prop = Property.objects.create_property(
        a_id, type_, act, city, state, zone, hood, addr, price, tot_a, const_a, 
        room, bath, half_baths, park, des
    )
    prop.save()

def create_new_ImageProperty(a_id):
    static_path = 'searcher/static/searcher/img/'
    path_template = "/static/searcher/img/"
    #path_template = "{% static 'searcher/img/"
    img_dirs = os.listdir(static_path)
    try:
        folder_img = [direc for direc in img_dirs if a_id in direc][0]
    except IndexError:
        # No hay imagenes para ese ahome id
        return 0
    propImages = [
        path_template + folder_img + '/' + f  for f in os.listdir(static_path + folder_img)
    ]
    for path in propImages:
        img_prop = ImageProperty(ahome_id=a_id, image_url=path)
        img_prop.save()