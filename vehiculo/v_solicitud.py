from django.shortcuts import render, redirect
from django.contrib import messages

import pyrebase

from vehiculo import views

config = {
    'apiKey': "AIzaSyA9FRv5pqrjqufN9SIE6tRzG6JRU-dr_QI",
    'authDomain': "vehiculos-6f105.firebaseapp.com",
    'databaseURL': "https://vehiculos-6f105.firebaseio.com",
    'projectId': "vehiculos-6f105",
    'storageBucket': "vehiculos-6f105.appspot.com",
    'messagingSenderId': "536521949602",
    'appId': "1:536521949602:web:0e91684ecc9ec97613f2fb",
    'measurementId': "G-Z4DYJM14XJ",
    'serviceAccount': "vehiculos-6f105-firebase-adminsdk-6ak95-9f6f55eaa2.json"
}

#Initialize Firebase
firebase = pyrebase.initialize_app(config)

database = firebase.database()

def crear_solicitud(request):
    return render(request,'crear_solicitud.html')

def post_crear_solicitud(request):
    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('America/Guayaquil')
    time_now = datetime.now(timezone.utc).astimezone(tz)

    id_solicitud = int(time.mktime(time_now.timetuple()))
    tipo = request.POST.get('tipo')
    descripcion = request.POST.get('descripcion') 
    realizado = 'no'

    data = {
        'tipo': tipo,
        'descripcion': descripcion,
        'realizado': realizado
    }

    database.child('solicitud').child(id_solicitud).set(data)
    messages.success(request, '¡Su Solicitud ha sido enviada!')
    return views.index(request)

def lst_solicitud(request):
    lst_solicitud = database.child('solicitud').shallow().get().val()
    solicitud = []

    if lst_solicitud != None:
        for i in lst_solicitud:
            solicitud.append(i)

    solicitud.sort(reverse=True)

    tipo = []
    descripcion = []
    realizado = []

    for i in solicitud:
        t = database.child('solicitud').child(i).child('tipo').get().val()
        d = database.child('solicitud').child(i).child('descripcion').get().val()
        r = database.child('solicitud').child(i).child('realizado').get().val()
        tipo.append(t)
        descripcion.append(d)
        realizado.append(r)
    
    comb_list = zip(solicitud,tipo,descripcion,realizado)
    return render(request,'lst_solicitud.html',{
            'comb_list': comb_list,
        })


def realizar_solicitud(request):
    id_solicitud = request.GET.get('k')
    tipo = database.child('solicitud').child(id_solicitud).child('tipo').get().val()
    descripcion = database.child('solicitud').child(id_solicitud).child('descripcion').get().val()
    realizado = 'si'

    database.child('solicitud').child(id_solicitud).update({
        'tipo': tipo,
        'descripcion': descripcion,
        'realizado': realizado
    })

    messages.success(request, 'Ha marcado como Realizada la Solictud ' + descripcion)
    return lst_solicitud(request)
