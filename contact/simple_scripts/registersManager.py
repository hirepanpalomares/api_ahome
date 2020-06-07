from django.db import models
from contact.models import ClientsRegistered
from django.core.exceptions import ObjectDoesNotExist


import os

def mail_does_not_exists(email):
    try:
        ClientsRegistered.objects.get(email=email)
        return False
    except ObjectDoesNotExist:
        return True


def create_new_entry(name, phone, email, message):
    newRegister = ClientsRegistered(
        name=name,
        phone=phone,
        email=email,
        message=message
    )
    newRegister.save()

def build_update_email():
    people = ClientsRegistered.objects.all()
    message = "Una nueva persona se ha registrado en nuestra red para publicidad\n\n\n"
    message += "Lista actualizada: \n\n"
    
    for person in people:
        email = person.email
        name = person.name
        phone = person.phone

        message += "%s   %s   %s\n"%(email,name,phone)
    return message
