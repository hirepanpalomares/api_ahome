from django.db import models

# Create your models here.

class PropertyManager(models.Manager):
    def create_property (self, ahome_id, property_type, action, status, city, state, 
    zone, hood, addres, price, total_area, construction_area, rooms, baths, half_baths,
    parking, description):
        property_ = self.create(
            ahome_id=ahome_id,
            property_type=property_type,
            action=action,
            status=status,
            city=city,
            state=state,
            zone=zone,
            hood=hood,
            addres=addres,
            #transaction_type=transaction_type,
            price=price,
            #scout=scout,
            #comission=comission,
            total_area=total_area,
            construction_area=construction_area,
            rooms=rooms,
            half_baths=half_baths,
            baths=baths,
            parking=parking,
            description=description
        )
        # do something with the property
        return property_


class Property(models.Model):
    ahome_id = models.CharField(max_length=10, default='')
    property_type = models.CharField(max_length=50, default='')
    action = models.CharField(max_length=50, default='')
    status = models.BooleanField(default=True)
    city= models.CharField(max_length=50, default='')
    state= models.CharField(max_length=50, default='')
    zone = models.CharField(max_length=100, default='')
    hood = models.CharField(max_length=100, default='')
    addres = models.CharField(max_length=100, default='')
    price = models.IntegerField(default=0)
    total_area = models.FloatField(default=0.0)
    construction_area = models.FloatField(default=0.0)
    rooms = models.CharField(max_length=20, default='')
    half_baths = models.IntegerField(default=0)
    baths = models.IntegerField(default=0)
    parking = models.IntegerField(default=0)
    description = models.CharField(max_length=1000, default='')

    objects = PropertyManager()


class ImageProperty(models.Model):
    ahome_id = models.CharField(max_length=10, default='')
    image_url = models.CharField(max_length=500, default='')