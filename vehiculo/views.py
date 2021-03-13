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

def crear(request):
    parameter = request.GET.get('k')
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
    print(parameter)
    return render(request,'crear.html',{ 'parameter':parameter,
        'comb_lst': comb_lst,
    })

def post_crear(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('America/Guayaquil')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    id_vehiculo = int(time.mktime(time_now.timetuple()))
    #Request Fabricante
    id_fabricante = request.POST.get('fabricante')
    #Request Datos
    modelo = request.POST.get('modelo')
    descripcion = request.POST.get('descripcion')
    nsockets = request.POST.get('nsockets')
    imagen = request.POST.get('imagen')
    imagen_sec = request.POST.get('imagen_sec')

    data = {
        'modelo': modelo,
        'descripcion' : descripcion,
        'nsockets': int(nsockets),
        'imagen': imagen,
        'imagen_sec':imagen_sec
    }
    database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).set(data)
    messages.success(request, 'Vehiculo Ingresado')

    return lst_vehiculo(request)

def editar(request):
    parameter = request.GET.get('k')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]
    f = x[2]
    nombre_fabricante = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
    modelo = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('modelo').get().val()
    descripcion = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('descripcion').get().val()
    imagen = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('imagen').get().val()
    imagen_sec = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('imagen_sec').get().val()
    nsockets = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('nsockets').get().val()

    if f == 'f':
        return render(request,'editar.html',{'nombre_fabricante':nombre_fabricante, 'nsockets':nsockets, 'f':id_fabricante,
        'modelo':modelo, 'descripcion':descripcion, 'imagen':imagen, 'imagen_sec':imagen_sec, 'id_fabricante':id_fabricante, 'id_vehiculo':id_vehiculo})
    else:
        return render(request,'editar.html',{'nombre_fabricante':nombre_fabricante, 'nsockets':nsockets, 'f':'v',
        'modelo':modelo, 'descripcion':descripcion, 'imagen':imagen, 'imagen_sec':imagen_sec, 'id_fabricante':id_fabricante, 'id_vehiculo':id_vehiculo})

def actualizar(request):
    id_fabricante = request.GET.get('id_fabricante')
    id_vehiculo =  request.GET.get('id_vehiculo')
    modelo = request.GET.get('modelo')
    descripcion = request.GET.get('descripcion')
    nsockets = request.GET.get('nsockets')
    imagen = request.GET.get('imagen')
    imagen_sec = request.GET.get('imagen_sec')
    nav = request.GET.get('nav')
    ant_nsocket = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('nsockets').get().val()
    if int(nsockets) < int(ant_nsocket):
        nombre_fabricante = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
        messages.error(request, 'No se ha Actualizado el Vehículo '+ modelo+ ' el Nro de Sockets es inferior al existente')
        return render(request,'editar.html',{'nombre_fabricante':nombre_fabricante,'nsockets':nsockets,
    'modelo':modelo, 'descripcion':descripcion, 'imagen':imagen, 'imagen_sec':imagen_sec, 'id_fabricante':id_fabricante, 'id_vehiculo':id_vehiculo})
    else:
        database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).update({
        'modelo': modelo,
        'descripcion' : descripcion,
        'nsockets': int(nsockets),
        'imagen': imagen,
        'imagen_sec':imagen_sec
        })
        messages.success(request, 'Se ha Actualizado el Vehículo '+ modelo)
    if nav == 'v':
        return redirect('/lst_vehiculo/')
    else:  
        return redirect('/lst_vehiculo_by_fab/?z='+nav)

def eliminar(request):
    parameter = request.GET.get('k')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]
    modelo = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('modelo').get().val()
    
    lst_pines = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').shallow().get().val()
    if lst_pines != None:
        messages.error(request, 'No se ha podido eliminar el Vehículo '+ modelo + ' contiene Pines Registrados')
        return lst_vehiculo(request)
    else:
        messages.error(request, 'Se ha eliminado el Vehículo '+ modelo)
        database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).remove()
        return lst_vehiculo(request)

def detalle_vehiculo(request):
    parameter = request.GET.get('k')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]
    f = x[2]
    nombre_fabricante = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
    modelo = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('modelo').get().val()
    descripcion = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('descripcion').get().val()
    imagen = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('imagen').get().val()
    imagen_sec = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('imagen_sec').get().val()
    nsockets = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('nsockets').get().val()
    lst_sockets = sockets_definition(nsockets)

    if f == 'f':
        return render(request,'detalle_vehiculo.html',{'parameter':parameter, 'nombre_fabricante':nombre_fabricante, 'id_fabricante': id_fabricante, 'id_vehiculo':id_vehiculo,
    'nsockets':nsockets, 'lst_sockets':lst_sockets, 'modelo':modelo, 'descripcion':descripcion, 'imagen':imagen, 'imagen_sec':imagen_sec, 'f':id_fabricante})
    else:
        return render(request,'detalle_vehiculo.html',{'parameter':parameter, 'nombre_fabricante':nombre_fabricante, 'id_fabricante': id_fabricante, 'id_vehiculo':id_vehiculo,
    'nsockets':nsockets, 'lst_sockets':lst_sockets, 'modelo':modelo, 'descripcion':descripcion, 'imagen':imagen, 'imagen_sec':imagen_sec})

def lst_vehiculo(request):
    db_fabricantes = database.child('fabricante').shallow().get().val()
    list_fabricantes=[]
    for i in db_fabricantes:
        list_fabricantes.append(i)
    list_fabricantes.sort(reverse=True)

    nombre_fabricante = []
    modelo_vehiculo = []
    img_vehiculo = []
    nsockets = []
    descripcion = []
    list_f = []
    list_v = []

    for i in list_fabricantes:
        name_factory = database.child('fabricante').child(i).child('nombre').get().val() 
        autos = database.child('fabricante').child(i).child('vehiculos').shallow().get().val()
        if autos != None:    
            for j in autos:
                lst_auto = database.child('fabricante').child(i).child('vehiculos').child(j).get().val()
                nombre_fabricante.append(name_factory)
                modelo_vehiculo.append(lst_auto['modelo'])
                img_vehiculo.append(lst_auto['imagen'])
                nsockets.append(lst_auto['nsockets'])
                descripcion.append(lst_auto['descripcion'])
                list_f.append(i)
                list_v.append(j)
        
    comb_list = zip(list_f,list_v,nombre_fabricante,modelo_vehiculo,img_vehiculo,nsockets,descripcion)

    return render(request,'lst_vehiculo.html',{
        'comb_list': comb_list,
    })

def buscar_v(request):
    if request.method == 'GET' and 'csrfmiddlewaretoken' in request.GET:
        search = request.GET.get('search')
        search = search.lower()

        db_fabricantes = database.child('fabricante').shallow().get().val()
        list_vehiculos=[]

        for i in db_fabricantes:
            name_factory = database.child('fabricante').child(i).child('nombre').get().val() 
            autos = database.child('fabricante').child(i).child('vehiculos').shallow().get().val()
            if autos != None:    
                for j in autos:
                    lst_auto = database.child('fabricante').child(i).child('vehiculos').child(j).get().val()
                    lst = str(i)+"$"+str(name_factory)+"$"+str(j)+"$"+str(lst_auto['modelo'])+"$"+str(lst_auto['descripcion'])
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

'''
    Datos de Pin
'''
def crear_pin(request):
    parameter = request.GET.get('k')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]
    actual_sock = x[2]
    nombre_fabricante = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
    modelo = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('modelo').get().val()
    nro = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('nsockets').get().val()
    lst_sockets = sockets_definition(nro)
    for i in lst_sockets:
        if i == actual_sock:
            lst_sockets.remove(i)
    return render(request,'crear_pin.html',{'parameter':parameter, 'nombre_fabricante':nombre_fabricante, 
    'modelo':modelo, 'lst_sockets':lst_sockets, 'actual_sock':actual_sock})

def post_crear_pin(request):
    #obtiene parametros para saber donde insertar
    parameter = request.POST.get('parameter')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]

    socket = request.POST.get('socket')
    pin = request.POST.get('pin')
    imagen = request.POST.get('imagen')
    data = {
        'pin':int(pin),
        'imagen': imagen
    }

    lst_sockets = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').shallow().get().val()
    #Validacion de Pin por Socket
    if lst_sockets != None:
        for i in lst_sockets:
            if i == socket:
                lst_pins = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(i).shallow().get().val()
                for j in lst_pins:
                    if int(j) == int(pin):
                        messages.error(request, 'En el '+ socket +' ya se ha registrado el Pin '+pin)
                        return redirect('/crear_pin/?k='+parameter)

    database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(socket).child(pin).set(data)
    messages.success(request, 'Pin del '+ socket +' Ingresado')
    return redirect('/lst_pines/?k='+parameter)

def eliminar_pin(request):
    parameter = request.GET.get('k')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]
    nsocket = x[2]
    id_pin = x[3]
    database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(nsocket).child(id_pin).remove()
    messages.error(request, 'Se ha eliminado el Pin ' + str(id_pin))
    return redirect('/lst_pines/?k='+id_fabricante+','+id_vehiculo+','+nsocket)

def lst_pines(request):
    parameter = request.GET.get('k')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]
    nsocket = x[2]
    nombre_vehiculo = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('modelo').get().val()
    lst_pines = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(nsocket).shallow().get().val()

    id_pin = []
    pin = []
    imagen_pin = []
    values = []
    comb_lst = zip()
    if lst_pines != None:
        for i in lst_pines:
            value_pin = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(nsocket).child(i).get().val()
            values.append(list(value_pin.items()))

        values.sort(key=lambda x: x[1]) #sort por pin   
        # print(values) 
        for i in values:
            id_pin.append(i[1][1])
            pin.append(i[1][1])
            imagen_pin.append(i[0][1])  

        comb_lst = zip(id_pin,pin,imagen_pin)
        mensaje = ""
    else:
        mensaje = "No se han registrado Pines"

    return render(request,'lst_pines.html', {'parameter':parameter, 'mensaje': mensaje, 'nombre_vehiculo':nombre_vehiculo,
    'comb_lst':comb_lst})

'''
    Definicion utilitarios
'''
def sockets_definition(nsockets):
    socket = "Socket "
    lst_sockets = []
    if nsockets != None:
        for i in range(nsockets):
            val = chr(ord('@')+(i+1))
            lst_sockets.append(f'{socket}{val}')
    return lst_sockets
