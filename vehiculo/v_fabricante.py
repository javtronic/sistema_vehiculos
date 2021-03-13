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
    nombre = []
    imagen = []
    list_time=[]
    fabricantes = database.child('fabricante').shallow().get().val()
    if fabricantes != None:
        for i in fabricantes:
            lst_fabricantes = database.child('fabricante').child(i).get().val()
            imagen.append(lst_fabricantes['imagen'])
            nombre.append(lst_fabricantes['nombre'])
            list_time.append(i)
        
    comb_lst = zip(list_time,nombre,imagen)
        
    return render(request,'index.html',{
        'comb_lst': comb_lst,
    })

def lst_fabricante(request):
    nombre = []
    imagen = []
    list_time=[]
    fabricantes = database.child('fabricante').shallow().get().val()
    if fabricantes != None:
        for i in fabricantes:
            lst_fabricantes = database.child('fabricante').child(i).get().val()
            imagen.append(lst_fabricantes['imagen'])
            nombre.append(lst_fabricantes['nombre'])
            list_time.append(i)
        
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
    messages.success(request, 'Fabricante '+ nombre +' Ingresado')
    return redirect('/lst_fabricante/')

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
    return redirect('/lst_fabricante/')

def eliminar_fabricante(request):
    id_fabricante = request.GET.get('z')
    nombref = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
    lst_fabricantes = database.child('fabricante').child(id_fabricante).child('vehiculos').shallow().get().val()
    if lst_fabricantes != None:
        messages.error(request, 'No se ha podido eliminar el Fabricante '+ nombref + ' contiene Vehículos Registrados')
        return redirect('/lst_fabricante/')
    else:
        messages.error(request, 'Se ha eliminado el Fabricante '+ nombref)
        database.child('fabricante').child(id_fabricante).remove()
        return redirect('/lst_fabricante/')

def lst_vehiculo_by_fab(request):
    id_fabricante = request.GET.get('z')
    nombre_fabricante = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
    autos = database.child('fabricante').child(id_fabricante).child('vehiculos').shallow().get().val()
    list_v = []
    modelo_vehiculo = []
    img_vehiculo = []
    nsockets = []
    descripcion = []
    if autos != None:   
        for i in autos:
            lst_auto = database.child('fabricante').child(id_fabricante).child('vehiculos').child(i).get().val()
            modelo_vehiculo.append(lst_auto['modelo'])
            img_vehiculo.append(lst_auto['imagen'])
            nsockets.append(lst_auto['nsockets'])
            descripcion.append(lst_auto['descripcion'])
            list_v.append(i)
    
    comb_list = zip(list_v,modelo_vehiculo,img_vehiculo,nsockets,descripcion)

    return render(request,'lst_vehiculo_by_fab.html',{ 'nombre_fabricante':nombre_fabricante,
        'id_fabricante':id_fabricante, 'comb_list': comb_list,
    })

def buscar_v_f(request):
    if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
        search = request.GET.get('search')
        fabricante = request.GET.get('fabricante')
        search = search.lower()

        list_vehiculos=[]
        name_factory = database.child('fabricante').child(fabricante).child('nombre').get().val()            
        autos = database.child('fabricante').child(fabricante).child('vehiculos').shallow().get().val()
        if autos != None:    
            for j in autos:
                lst_auto = database.child('fabricante').child(fabricante).child('vehiculos').child(j).get().val()
                lst = str(fabricante)+"$"+str(name_factory)+"$"+str(j)+"$"+str(lst_auto['modelo'])+"$"+str(lst_auto['descripcion'])
                list_vehiculos.append(lst)                       
        
        matching = [str(string) for string in list_vehiculos if search in string.lower()]

        nombre_fabricante = []
        modelo_vehiculo = []
        descripcion = []
        img_vehiculo = []
        socket = []
        list_v = []
        list_f = []

        for i in matching:
            lst_f,n_fabricante,lst_v,m_vehiculo,desc = i.split("$")
            list_f.append(lst_f)
            nombre_fabricante.append(n_fabricante)
            list_v.append(lst_v)
            modelo_vehiculo.append(m_vehiculo)
            descripcion.append(desc)

        for i in range(len(list_f)):
            imgs = database.child('fabricante').child(list_f[i]).child('vehiculos').child(list_v[i]).child('imagen').get().val()
            nsocket = database.child('fabricante').child(list_f[i]).child('vehiculos').child(list_v[i]).child('nsocket').get().val()
            img_vehiculo.append(imgs)
            socket.append(nsocket)

        comb_list = zip(list_f,list_v,nombre_fabricante,modelo_vehiculo,img_vehiculo,socket,descripcion)
        return render(request,'lst_vehiculo.html',{
            'comb_list': comb_list,
        })