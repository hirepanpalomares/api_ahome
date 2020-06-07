from django.urls import path
from . import views

path_subs = '<str:name>/<str:phone>/<str:email>/<str:message>/sendSubsMessage'
path_contact = '<str:name>/<str:lastname>/<str:phone>/<str:email>/<str:message>/contactMessage'
path_home_valuation = '<str:name>/<str:phone>/<str:email>/<str:city>/<str:state>/<str:prop_type>/<str:baths>'
path_home_valuation += '/<str:half_baths>/<str:rooms>/<str:area>/<str:comments>/homeValMessage'
#path_home_valuation += '/homeValMessage'#/homeValMessage'
path_booking = '<str:name>/<str:lastname>/<str:email>/<str:phone>/<str:ahome_id>/<str:message>/bookingMessage'

urlpatterns = [
    path(path_subs, views.subscription_mail, name='subs_mail'),
    path(path_contact, views.contact_message, name='contact_mail'),
    path(path_home_valuation, views.home_valuation_message, name='homeVal_message'),
    path(path_booking, views.booking_message, name='booking_message')
]
