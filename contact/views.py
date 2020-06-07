from django.shortcuts import render
from .simple_scripts import registersManager
from .models import ClientsRegistered
from django.core.mail import send_mail
from django.http import JsonResponse

# Create your views here.

def subscription_mail(request, name, phone, email, message):
    
    if registersManager.mail_does_not_exists(email):
        registersManager.create_new_entry(
            name=' '.join(name.split('_')),
            phone=' '.join(phone.split('_')),
            email=' '.join(email.split('_')),
            message=' '.join(message.split('_'))
        )
        message = registersManager.build_update_email()
        send_mail(
            "Nueva persona registrada a la red",
            message,
            'website@ahome.com.mx',
            ['hirepan.49@gmail.com'],
            fail_silently=False,
        )
        
        return JsonResponse({'Client registered succesfully, email sent': 'true'})
    else:
        return JsonResponse({'Client already registered':'false'})

def contact_message(request, name, lastname, phone, email, message):
    subject = 'Mensaje desde el sitio web'
    message_from_formulary = ' '.join(message.split('_'))
    name = ' '.join(name.split('_'))
    last_name = ' '.join(lastname.split('_'))
    email_client = ' '.join(email.split('_'))
    phone_client = ' '.join(phone.split('_'))
    email_message = "Has recibido un mensaje desde ahome.com.mx \n\nDe: %s %s\nemail: %s\n Teléfono: %s \n\nMensaje:\n%s" %(name, last_name, email_client, phone_client, message_from_formulary)

    send_mail(
        subject,
        email_message,
        'website@ahome.com.mx',
        ['hirepan.49@gmail.com'],
        fail_silently=False,
    )
    return JsonResponse({'message': 'sent'})


def home_valuation_message(request,
    name, phone, email, city, state, prop_type, baths,
    half_baths, rooms, area, comments):
    
    type_ = {"1":["Departamento"], "2":["Casa Habitación", "Residencia"], "3":["Terreno"], 
             "4":["Oficina"], "5":["Bodega"], "6":["Local Comercial"], 
             "7":["Salon de Fiestas", "Salón de Fiestas"] 
    }
    subject = 'Requisición de evaluación de patrimonio'
    
    name = ' '.join(name.split('_'))
    email_client = ' '.join(email.split('_'))
    phone_client = ' '.join(phone.split('_'))
    city = ' '.join(city.split('_'))
    state = ' '.join(state.split('_'))
    prop_type = ' '.join(prop_type.split('_'))
    bath = ' '.join(baths.split('_'))
    bath_half = ' '.join(half_baths.split('_'))
    room = ' '.join(rooms.split('_'))
    area_construction = ' '.join(area.split('_'))
    comments = ' '.join(comments.split('_'))
    email_message =  "Has recibido una requisición de evaluación de patrimonio desde ahome.com.mx \n\n"
    email_message += "Datos del cliente: ------------------------------------------------------------------ \n"
    email_message += "Nombre: %s \n" %name
    email_message += "email: %s \n" %email_client
    email_message += "Teléfono: %s \n" %phone_client
    email_message += "Ciudad: %s \n" %city
    email_message += "Estado: %s \n\n" %state 
    email_message += "Datos de la propiedad --------------------------------------------------------------- \n"
    email_message += "Tipo de propiedad: %s \n" %type_[prop_type]
    email_message += "Baños completos: %s \n" %bath
    email_message += "Medios baños: %s \n" %bath_half
    email_message += "Recámaras: %s \n" % room
    email_message += "Metros de construcción: %s \n" % area_construction
    email_message += "Comentarios adicionales: \n %s " %comments
    
    send_mail(
        subject,
        email_message,
        'website@ahome.com.mx',
        ['hirepan.49@gmail.com'],
        fail_silently=False,
    )

    return JsonResponse({'email':'sent'})

def booking_message(request,  name, lastname, email, phone, ahome_id, message):
    subject = 'Solicitud de cita'
    message_from_formulary = ' '.join(message.split('_'))
    name = ' '.join(name.split('_'))
    last_name = ' '.join(lastname.split('_'))
    email_client = ' '.join(email.split('_'))
    phone_client = ' '.join(phone.split('_'))
    ahome_id = ' '.join(ahome_id.split('_'))
    email_message = "Has recibido una solicitud de cita desde ahome.com.mx \n\n"
    email_message += "De: %s %s \n"%(name, last_name)
    email_message += "email: %s \n"%email_client
    email_message += "Teléfono: %s \n"%phone_client
    email_message += "Propiedad que le interesa: %s \n\n"%ahome_id
    email_message += "Mensaje:\n%s "%message_from_formulary
    send_mail(
        subject,
        email_message,
        'website@ahome.com.mx',
        [
            'hirepan.49@gmail.com'
        ],
        fail_silently=False,
    )
    return JsonResponse({'email':'sent'})
