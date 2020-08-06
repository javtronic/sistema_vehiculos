from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.sessions.backends.base import SessionBase
import pyrebase

from vehiculo import v_fabricante

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

authentication = firebase.auth()
database = firebase.database()

#method Log    

def sign_in(request):
    return render(request,"sign_in.html")

def post_sign_in(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authentication.sign_in_with_email_and_password(email, password)
    except:
        messages.error(request, 'Credenciales Invalidas')
        return render(request, "sign_in.html")
    
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return v_fabricante.index(request)

def sign_up(request):
    return render(request,"sign_up.html")

def post_sign_up(request):
    nombre = request.POST.get('name')
    email = request.POST.get('email')
    password_1 = request.POST.get('password_1')
    password_2 = request.POST.get('password_2')
    try:       
        if password_1 != password_2:
            messages.error(request, 'La contraseña no coincide')
            return render(request,'sign_up.html')
        else:
            user = authentication.create_user_with_email_and_password(email,password_1)
    except:
        messages.error(request, 'No se puede crear la cuenta intente de nuevo')
        return render(request,'sign_up.html')
    
    uid = user['localId']
    data={
        "nombre":nombre,
        "status":"1"
    }

    database.child("usuarios").child(uid).child("detalles").set(data)
    return render(request,'sign_in.html')

def logout(request):
    if "uid" in request.session:        
        del request.session['uid']
        return v_fabricante.index(request)

    

