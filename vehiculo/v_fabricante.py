from django.shortcuts import render, redirect
from django.contrib import messages

import pyrebase

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

'''
    Datos Fabricante
'''
def index(request):
    timestamps = database.child('fabricante').shallow().get().val()
    list_time=[]
    if timestamps != None:
        for i in timestamps:
            list_time.append(i)

    list_time.sort(reverse=True)

    nombre = []
    imagen = []
        
    for i in list_time:
        image = database.child('fabricante').child(i).child('imagen').get().val()
        name = database.child('fabricante').child(i).child('nombre').get().val()

        nombre.append(name)
        imagen.append(image)
        
    comb_lst = zip(list_time,nombre,imagen)
        
    return render(request,'index.html',{
        'comb_lst': comb_lst,
    })

def lst_fabricante(request):
    timestamps = database.child('fabricante').shallow().get().val()
    list_time=[]
    if timestamps != None:
        for i in timestamps:
            list_time.append(i)

    list_time.sort(reverse=True)

    nombre = []
    imagen = []
        
    for i in list_time:
        image = database.child('fabricante').child(i).child('imagen').get().val()
        name = database.child('fabricante').child(i).child('nombre').get().val()

        nombre.append(name)
        imagen.append(image)
        
    comb_lst = zip(list_time,nombre,imagen)
        
    return render(request,'lst_fabricante.html',{
        'comb_lst': comb_lst,
    })

def buscar_f(request):
    if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
        search = request.GET.get('search')
        index = request.GET.get('ind')
        search = search.lower()

        timestamps = database.child('fabricante').shallow().get().val()
        fabricante_id = []

        for i in timestamps:
            f = database.child('fabricante').child(i).child('nombre').get().val()
            f = str(f)+"$"+str(i)
            fabricante_id.append(f)
        
        matching = [str(string) for string in fabricante_id if search in string.lower()]

        s_nombre=[]
        s_imagen=[]
        s_id=[]

        for i in matching:
            name,id = i.split("$")
            s_nombre.append(name)
            s_id.append(id)

        for i in s_id:
            img = database.child('fabricante').child(i).child('imagen').get().val()
            s_imagen.append(img)

        comb_lst = zip(s_id,s_nombre,s_imagen)

        if index == 'ind':   
            return render(request,'index.html',{
                'comb_lst': comb_lst,
            })
        else: 
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
    id_fabricante = int(time.mktime(time_now.timetuple()))

    nombre = request.POST.get('nombre') 
    imagen = request.POST.get('imagen')

    data = {
        'nombre': nombre,
        'imagen': imagen
    }

    database.child('fabricante').child(id_fabricante).set(data)
    messages.success(request, 'Fabricante Ingresado')
    return lst_fabricante(request)

def editar_fabricante(request):
    i = request.GET.get('z')
    nombre = database.child('fabricante').child(i).child('nombre').get().val()
    imagen = database.child('fabricante').child(i).child('imagen').get().val()

    return render(request,'editar_fabricante.html',{'nombre':nombre, 'imagen':imagen, 'i':i})

def actualizar_fabricante(request):
    id_fabricante =  request.GET.get('i')
    nombre = request.GET.get('nombre')
    imagen = request.GET.get('imagen')

    database.child('fabricante').child(id_fabricante).update({
        "nombre": nombre,
        "imagen": imagen
    })
    messages.success(request, 'se ha Actualizado el Fabricante ' + nombre)

    return lst_fabricante(request)

def eliminar_fabricante(request):
    id_fabricante = request.GET.get('z')
    nombref = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
    lst_fabricantes = database.child('fabricante').child(id_fabricante).child('vehiculos').shallow().get().val()
    if lst_fabricantes != None:
        messages.error(request, 'No se ha podido eliminar el Fabricante '+ nombref + ' contiene Vehículos Registrados')
        return lst_fabricante(request)
    else:
        messages.error(request, 'Se ha eliminado el Fabricante '+ nombref)
        database.child('fabricante').child(id_fabricante).remove()
        return lst_fabricante(request)

def lst_vehiculo_by_fab(request):
    id_fabricante = request.GET.get('z')
    nombre_fabricante = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
    autos = database.child('fabricante').child(id_fabricante).child('vehiculos').shallow().get().val()
    list_v = []
    modelo_vehiculo = []
    img_vehiculo = []
    socket_a = []
    socket_b = []
    descripcion = []
    if autos != None:    
        for i in autos:
            list_v.append(i)

        for i in list_v:
            model = database.child('fabricante').child(id_fabricante).child('vehiculos').child(i).child('modelo').get().val()
            imgs = database.child('fabricante').child(id_fabricante).child('vehiculos').child(i).child('imagen').get().val()
            s_a = database.child('fabricante').child(id_fabricante).child('vehiculos').child(i).child('socket_a').get().val()
            s_b = database.child('fabricante').child(id_fabricante).child('vehiculos').child(i).child('socket_b').get().val()
            descr = database.child('fabricante').child(id_fabricante).child('vehiculos').child(i).child('descripcion').get().val()
            if model != None:    
                modelo_vehiculo.append(model)
                img_vehiculo.append(imgs)
                socket_a.append(s_a)
                socket_b.append(s_b)
                descripcion.append(descr)
    
    comb_list = zip(list_v,modelo_vehiculo,img_vehiculo,socket_a,socket_b,descripcion)

    return render(request,'lst_vehiculo_by_fab.html',{ 'nombre_fabricante':nombre_fabricante,
        'id_fabricante':id_fabricante, 'comb_list': comb_list,
    })