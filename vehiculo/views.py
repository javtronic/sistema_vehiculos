from django.shortcuts import render, redirect
from django.contrib import messages, auth

import pyrebase

config = {
    'apiKey': "AIzaSyA9FRv5pqrjqufN9SIE6tRzG6JRU-dr_QI",
    'authDomain': "vehiculos-6f105.firebaseapp.com",
    'databaseURL': "https://vehiculos-6f105.firebaseio.com",
    'projectId': "vehiculos-6f105",
    'storageBucket': "vehiculos-6f105.appspot.com",
    'messagingSenderId': "536521949602",
    'appId': "1:536521949602:web:0e91684ecc9ec97613f2fb",
    'measurementId': "G-Z4DYJM14XJ"
}

#Initialize Firebase
firebase = pyrebase.initialize_app(config)

# authentication = firebase.auth()
database = firebase.database()

# Create your views here.
def index(request):
    import datetime
    timestamps = database.child('fabricante').shallow().get().val()
    list_time=[]

    for i in timestamps:
        list_time.append(i)

    list_time.sort(reverse=True)

    #condicion par aver si tiene o no vehiculos el fabricante
    for i in list_time:
        a = database.child('fabricante').child(i).child('vehiculos').shallow().get().val()
        if a == None:
            list_time.remove(i)

    nombre_fabricante = []
    modelo_vehiculo = []
    img_vehiculo = []
    socket_a = []
    socket_b = []
    list_v = []

    if timestamps != None:
        for i in list_time:
            name_factory = database.child('fabricante').child(i).child('nombre').get().val() 
            
            autos = database.child('fabricante').child(i).child('vehiculos').shallow().get().val()
            if autos != None:    
                for j in autos:
                    list_v.append(j)

                for j in list_v:
                    model = database.child('fabricante').child(i).child('vehiculos').child(j).child('modelo').get().val()
                    imgs = database.child('fabricante').child(i).child('vehiculos').child(j).child('imagen').get().val()
                    s_a = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_a').get().val()
                    s_b = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_b').get().val()

                nombre_fabricante.append(name_factory)
                modelo_vehiculo.append(model)
                img_vehiculo.append(imgs)
                socket_a.append(s_a)
                socket_b.append(s_b)

        print(list_time)
    
    comb_list = zip(list_time,list_v,nombre_fabricante,modelo_vehiculo,img_vehiculo,socket_a,socket_b)

    return render(request,'index.html',{
        'comb_list': comb_list,
    })

def crear(request):
    import datetime
    timestamps = database.child('fabricante').shallow().get().val()
    list_time=[]
    for i in timestamps:
        list_time.append(i)
    list_time.sort(reverse=True)

    nombre = []
    for i in list_time:
        name = database.child('fabricante').child(i).child('nombre').get().val()
        nombre.append(name)
    
    comb_lst = zip(list_time,nombre)


    return render(request,'crear.html',{
        'comb_lst': comb_lst,
    })

def post_crear(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('America/Guayaquil')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    id_vehiculo = int(time.mktime(time_now.timetuple())) #antes millis
    #print("mills" + str(millis))
    #Request Fabricante
    id_fabricante = request.POST.get('fabricante')
    #Request Datos
    modelo = request.POST.get('modelo')
    descripcion = request.POST.get('descripcion')
    socket_a = request.POST.get('socket_a')
    socket_b = request.POST.get('socket_b')
    imagen = request.POST.get('imagen')

    data = {
        'modelo': modelo,
        'descripcion' : descripcion,
        'socket_a': socket_a,
        'socket_b': socket_b,
        'imagen': imagen
    }
    database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).set(data)

    messages.success(request, 'Vehiculo Ingresado')

    return lst_vehiculo(request)

def editar(request):
    parameter = request.GET.get('k')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]

    nombre_fabricante = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
    modelo = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('modelo').get().val()
    descripcion = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('descripcion').get().val()
    imagen = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('imagen').get().val()
    socket_a = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('socket_a').get().val()
    socket_b = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('socket_b').get().val()

    timestamps = database.child('fabricante').shallow().get().val()
    list_time=[]
    for i in timestamps:
        list_time.append(i)
    list_time.sort(reverse=True)

    nombre = []
    for i in list_time:
        name = database.child('fabricante').child(i).child('nombre').get().val()
        nombre.append(name)
    
    comb_lst = zip(list_time,nombre)

    return render(request,'editar.html',{'nombre_fabricante':nombre_fabricante, 'socket_b':socket_b, 'socket_a':socket_a, 
    'modelo':modelo, 'descripcion':descripcion, 'imagen':imagen, 'comb_lst': comb_lst, 'id_fabricante':id_fabricante, 'id_vehiculo':id_vehiculo})

def actualizar(request):
    id_fabricante = request.GET.get('id_fabricante')
    id_vehiculo =  request.GET.get('id_vehiculo')
    modelo = request.GET.get('modelo')
    descripcion = request.GET.get('descripcion')
    socket_a = request.GET.get('socket_a')
    socket_b = request.GET.get('socket_b')
    imagen = request.GET.get('imagen')

    print(id_fabricante, id_vehiculo, modelo)
    database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).update({
        'modelo': modelo,
        'descripcion' : descripcion,
        'socket_a': socket_a,
        'socket_b': socket_b,
        'imagen': imagen
    })
    messages.success(request, 'Se ha Actualizado el Vehículo')

    return lst_vehiculo(request)

def eliminar(request):
    parameter = request.GET.get('k')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]
    database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).remove()

    return lst_vehiculo(request)

def detalle_vehiculo(request):

    parameter = request.GET.get('k')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]

    nombre_fabricante = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
    modelo = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('modelo').get().val()
    descripcion = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('descripcion').get().val()
    imagen = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('imagen').get().val()
    socket_a = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('socket_a').get().val()
    socket_b = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('socket_b').get().val()

  
    print(id_fabricante, nombre_fabricante, modelo)
    return render(request,'detalle_vehiculo.html',{'nombre_fabricante':nombre_fabricante, 'socket_b':socket_b, 'socket_a':socket_a, 
    'modelo':modelo, 'descripcion':descripcion, 'imagen':imagen})

def lst_vehiculo(request):
    import datetime
    timestamps = database.child('fabricante').shallow().get().val()
    list_time=[]

    for i in timestamps:
        list_time.append(i)

    list_time.sort(reverse=True)

    #condicion par aver si tiene o no vehiculos el fabricante
    for i in list_time:
        a = database.child('fabricante').child(i).child('vehiculos').shallow().get().val()
        if a == None:
            list_time.remove(i)

    nombre_fabricante = []
    modelo_vehiculo = []
    img_vehiculo = []
    socket_a = []
    socket_b = []
    descripcion = []
    list_v = []

    if timestamps != None:
        for i in list_time:
            name_factory = database.child('fabricante').child(i).child('nombre').get().val() 
            
            autos = database.child('fabricante').child(i).child('vehiculos').shallow().get().val()
            if autos != None:    
                for j in autos:
                    list_v.append(j)

                for j in list_v:
                    model = database.child('fabricante').child(i).child('vehiculos').child(j).child('modelo').get().val()
                    imgs = database.child('fabricante').child(i).child('vehiculos').child(j).child('imagen').get().val()
                    s_a = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_a').get().val()
                    s_b = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_b').get().val()
                    descr = database.child('fabricante').child(i).child('vehiculos').child(j).child('descripcion').get().val()

                nombre_fabricante.append(name_factory)
                modelo_vehiculo.append(model)
                img_vehiculo.append(imgs)
                socket_a.append(s_a)
                socket_b.append(s_b)
                descripcion.append(descr)

        print(list_time)
    
    comb_list = zip(list_time,list_v,nombre_fabricante,modelo_vehiculo,img_vehiculo,socket_a,socket_b,descripcion)

    return render(request,'lst_vehiculo.html',{
        'comb_list': comb_list,
    })

'''
   Datos Fabricante
'''
def lst_fabricante(request):
    import datetime
    timestamps = database.child('fabricante').shallow().get().val()
    list_time=[]
    for i in timestamps:
        list_time.append(i)
    list_time.sort(reverse=True)

    nombre = []
    imagen = []

    date = []
    for i in list_time:
        image = database.child('fabricante').child(i).child('imagen').get().val()
        name = database.child('fabricante').child(i).child('nombre').get().val()

        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)
        nombre.append(name)
        imagen.append(image)

    
    comb_lst = zip(list_time,date,nombre,imagen)
    
    return render(request,'lst_fabricante.html',{
        'comb_lst': comb_lst,
    })

def crear_fabricante(request):
    return render(request,'crear_fabricante.html')

def post_crear_fabricante(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('America/Guayaquil')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    #print("mills" + str(millis))
    nombre = request.POST.get('nombre') 
    imagen = request.POST.get('imagen') #antes url

    data = {
        'nombre': nombre,
        'imagen': imagen
    }
    database.child('fabricante').child(millis).set(data)
    messages.success(request, 'Fabricante Ingresado')

    return lst_fabricante(request)

def editar_fabricante(request):
    import datetime
    time = request.GET.get('z')
    nombre = database.child('fabricante').child(time).child('nombre').get().val()
    imagen = database.child('fabricante').child(time).child('imagen').get().val()
    i = int(time)
    print(i)
    dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')

    return render(request,'editar_fabricante.html',{'nombre':nombre, 'imagen':imagen, 'i':i})

def actualizar_fabricante(request):
    time =  request.GET.get('i')
    nombre = request.GET.get('nombre')
    imagen = request.GET.get('imagen')
    i = str(time)
    print(i)
    database.child('fabricante').child(i).update({
        "nombre": nombre,
        "imagen": imagen
    })
    messages.success(request, 'se ha Actualizado el Fabricante ' + nombre)

    return lst_fabricante(request)

def eliminar_fabricante(request):
    time = request.GET.get('z')
    database.child('fabricante').child(time).remove()

    return lst_fabricante(request)