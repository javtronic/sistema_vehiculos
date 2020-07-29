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

# View Index
def index(request):
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
                    id_f = database.child('fabricante').child(i).get().key()
                    model = database.child('fabricante').child(i).child('vehiculos').child(j).child('modelo').get().val()
                    imgs = database.child('fabricante').child(i).child('vehiculos').child(j).child('imagen').get().val()
                    s_a = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_a').get().val()
                    s_b = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_b').get().val()

                    if model != None:    
                        lst = str(id_f)+"$"+str(name_factory)+"$"+str(j)+"$"+str(model)+"$"+str(imgs)+"$"+str(s_a)+"$"+str(s_b)
                        list_vehiculos.append(lst)
        
        matching = [str(string) for string in list_vehiculos if search in string.lower()]

        nombre_fabricante = []
        modelo_vehiculo = []
        img_vehiculo = []
        socket_a = []
        socket_b = []
        list_v = []
        list_f = []

        for i in matching:
            lst_f,n_fabricante,lst_v,m_vehiculo,i_vehiculo,soc_a,soc_b = i.split("$")
            list_f.append(lst_f)
            nombre_fabricante.append(n_fabricante)
            list_v.append(lst_v)
            modelo_vehiculo.append(m_vehiculo)
            img_vehiculo.append(i_vehiculo)
            socket_a.append(soc_a)
            socket_b.append(soc_b)

        comb_list = zip(list_f,list_v,nombre_fabricante,modelo_vehiculo,img_vehiculo,socket_a,socket_b)
        
        return render(request,'index.html',{
            'comb_list': comb_list,
        })

    else:
        db_fabricantes = database.child('fabricante').shallow().get().val()
        list_fabricantes=[]

        for i in db_fabricantes:
            list_fabricantes.append(i)
        list_fabricantes.sort(reverse=True)

        nombre_fabricante = []
        modelo_vehiculo = []
        img_vehiculo = []
        socket_a = []
        socket_b = []
        list_v = []
        list_f = []

        for i in list_fabricantes:
            name_factory = database.child('fabricante').child(i).child('nombre').get().val() 
                
            autos = database.child('fabricante').child(i).child('vehiculos').shallow().get().val()
            if autos != None:    
                for j in autos:
                    list_v.append(j)

                for j in list_v:
                    id_f = database.child('fabricante').child(i).get().key()
                    model = database.child('fabricante').child(i).child('vehiculos').child(j).child('modelo').get().val()
                    imgs = database.child('fabricante').child(i).child('vehiculos').child(j).child('imagen').get().val()
                    s_a = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_a').get().val()
                    s_b = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_b').get().val()

                    if model != None:    
                        nombre_fabricante.append(name_factory)
                        modelo_vehiculo.append(model)
                        img_vehiculo.append(imgs)
                        socket_a.append(s_a)
                        socket_b.append(s_b)
                        list_f.append(id_f)
        
        comb_list = zip(list_f,list_v,nombre_fabricante,modelo_vehiculo,img_vehiculo,socket_a,socket_b)
        
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

    nombre_fabricante = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
    modelo = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('modelo').get().val()
    descripcion = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('descripcion').get().val()
    imagen = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('imagen').get().val()
    socket_a = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('socket_a').get().val()
    socket_b = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('socket_b').get().val()

    lst_pines = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').shallow().get().val()
    pines=[]
    if lst_pines != None:
        for i in lst_pines:
            pines.append(i)
    
    socket = []
    id_pin_a = []
    id_pin_b = []
    pin_a = []
    pin_b = []
    imagen_pin_a = []
    imagen_pin_b = []

    if lst_pines != None:
        for i in pines:
            id_p = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(i).get().key()
            sock = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(i).child('socket').get().val()
            p = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(i).child('pin').get().val()
            imag_pin = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(i).child('imagen').get().val()

            if sock == 'A':
                id_pin_a.append(id_p)
                pin_a.append(p)
                imagen_pin_a.append(imag_pin)
            elif sock == 'B':
                id_pin_b.append(id_p)
                pin_b.append(p)
                imagen_pin_b.append(imag_pin)

    comb_lst_a = zip(id_pin_a,pin_a,imagen_pin_a)
    comb_lst_b = zip(id_pin_b,pin_b,imagen_pin_b)
  
    return render(request,'detalle_vehiculo.html',{'parameter':parameter, 'nombre_fabricante':nombre_fabricante, 'socket_b':socket_b, 'socket_a':socket_a, 
    'modelo':modelo, 'descripcion':descripcion, 'imagen':imagen, 'comb_lst_a':comb_lst_a, 'comb_lst_b':comb_lst_b})

def lst_vehiculo(request):
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
                    id_f = database.child('fabricante').child(i).get().key()
                    model = database.child('fabricante').child(i).child('vehiculos').child(j).child('modelo').get().val()
                    imgs = database.child('fabricante').child(i).child('vehiculos').child(j).child('imagen').get().val()
                    s_a = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_a').get().val()
                    s_b = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_b').get().val()
                    descr = database.child('fabricante').child(i).child('vehiculos').child(j).child('descripcion').get().val()

                    if model != None:    
                        lst = str(id_f)+"$"+str(name_factory)+"$"+str(j)+"$"+str(model)+"$"+str(imgs)+"$"+str(s_a)+"$"+str(s_b)+"$"+str(descr)
                        list_vehiculos.append(lst)
        
        matching = [str(string) for string in list_vehiculos if search in string.lower()]

        nombre_fabricante = []
        modelo_vehiculo = []
        img_vehiculo = []
        socket_a = []
        socket_b = []
        descripcion = []
        list_v = []
        list_f = []

        for i in matching:
            lst_f,n_fabricante,lst_v,m_vehiculo,i_vehiculo,soc_a,soc_b,desc = i.split("$")
            list_f.append(lst_f)
            nombre_fabricante.append(n_fabricante)
            list_v.append(lst_v)
            modelo_vehiculo.append(m_vehiculo)
            img_vehiculo.append(i_vehiculo)
            socket_a.append(soc_a)
            socket_b.append(soc_b)
            descripcion.append(desc)

        comb_list = zip(list_f,list_v,nombre_fabricante,modelo_vehiculo,img_vehiculo,socket_a,socket_b,descripcion)

        return render(request,'lst_vehiculo.html',{
            'comb_list': comb_list,
        })

    else:
        db_fabricantes = database.child('fabricante').shallow().get().val()
        list_fabricantes=[]

        for i in db_fabricantes:
            list_fabricantes.append(i)
        list_fabricantes.sort(reverse=True)

        nombre_fabricante = []
        modelo_vehiculo = []
        img_vehiculo = []
        socket_a = []
        socket_b = []
        descripcion = []
        list_v = []
        list_f = []

        for i in list_fabricantes:
            name_factory = database.child('fabricante').child(i).child('nombre').get().val() 
                
            autos = database.child('fabricante').child(i).child('vehiculos').shallow().get().val()
            if autos != None:    
                for j in autos:
                    list_v.append(j)

                for j in list_v:
                    id_f = database.child('fabricante').child(i).get().key()
                    model = database.child('fabricante').child(i).child('vehiculos').child(j).child('modelo').get().val()
                    imgs = database.child('fabricante').child(i).child('vehiculos').child(j).child('imagen').get().val()
                    s_a = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_a').get().val()
                    s_b = database.child('fabricante').child(i).child('vehiculos').child(j).child('socket_b').get().val()
                    descr = database.child('fabricante').child(i).child('vehiculos').child(j).child('descripcion').get().val()

                    if model != None:    
                        nombre_fabricante.append(name_factory)
                        modelo_vehiculo.append(model)
                        img_vehiculo.append(imgs)
                        socket_a.append(s_a)
                        socket_b.append(s_b)
                        descripcion.append(descr)
                        list_f.append(id_f)
        
        comb_list = zip(list_f,list_v,nombre_fabricante,modelo_vehiculo,img_vehiculo,socket_a,socket_b,descripcion)

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
    nombre_fabricante = database.child('fabricante').child(id_fabricante).child('nombre').get().val()
    modelo = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('modelo').get().val()
    return render(request,'crear_pin.html',{'parameter':parameter, 'nombre_fabricante':nombre_fabricante, 'modelo':modelo})

def post_crear_pin(request):
    import time
    from datetime import datetime, timezone
    import pytz

    tz = pytz.timezone('America/Guayaquil')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    id_pin = int(time.mktime(time_now.timetuple()))

    #obtiene parametros para saber donde insertar
    parameter = request.POST.get('parameter')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]

    a = int(database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('socket_a').get().val())
    b = int(database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('socket_b').get().val())

    socket = request.POST.get('socket')
    pin = request.POST.get('pin')
    imagen = request.POST.get('imagen')

    p = int(pin)
    #Verificacion de pin existente
    lst_pines = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').shallow().get().val()
    pines=[]
    if lst_pines != None:
        for i in lst_pines:
            pines.append(i)

    if lst_pines != None:
        for i in pines:
            sock = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(i).child('socket').get().val()
            pi = int(database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(i).child('pin').get().val())
            if sock == socket and pi == p:
                messages.error(request, 'El Pin a registrar ya existe = '+pin)
                return redirect('/crear_pin/?k='+parameter)
    
    if socket == "A":
        if p <= a:
            data = {
                'socket': socket,
                'pin':pin,
                'imagen': imagen
            }
            database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(id_pin).set(data)
            messages.success(request, 'Pin del Socket A Ingresado')
            return redirect('/detalle_vehiculo/?k='+parameter)
        else:
            messages.error(request, 'El vehiculo no cuenta con ese número de socket '+pin)
            return redirect('/crear_pin/?k='+parameter)

    elif socket == "B":
        if p <= b:
            data = {
                'socket': socket,
                'pin':pin,
                'imagen': imagen
            }
            database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(id_pin).set(data)
            messages.success(request, 'Pin del Socket B Ingresado')
            return redirect('/detalle_vehiculo/?k='+parameter)
        else:
            messages.error(request, 'El vehiculo no cuenta con ese número de socket '+pin)
            return redirect('/crear_pin/?k='+parameter)

def eliminar_pin(request):
    parameter = request.GET.get('k')
    x = parameter.split(',')
    id_fabricante = x[0]
    id_vehiculo = x[1]
    id_pin = x[2]
    p = database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(id_pin).child('pin').get().val()
    database.child('fabricante').child(id_fabricante).child('vehiculos').child(id_vehiculo).child('pines').child(id_pin).remove()
    messages.error(request, 'Se ha eliminado el Pin '+ p)
    return redirect('/detalle_vehiculo/?k='+id_fabricante+','+id_vehiculo)


