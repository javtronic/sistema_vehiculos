"""sistema_vehiculos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vehiculo import views, v_fabricante, v_solicitud
from . import auth

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', v_fabricante.index, name="index"),
    #Vehiculo
    path('crear/', views.crear, name="crear"),
    path('post_crear/', views.post_crear, name="post_crear"),
    path('editar/', views.editar, name="editar"),
    path('detalle_vehiculo/', views.detalle_vehiculo, name="detalle_vehiculo"),
    path('lst_vehiculo/', views.lst_vehiculo, name="lst_vehiculo"),
    path('buscar_v/', views.buscar_v, name="buscar_v"),
    path('actualizar/', views.actualizar, name="actualizar"),
    path('eliminar/', views.eliminar, name="eliminar"),
    path('lst_vehiculo_by_fab/', v_fabricante.lst_vehiculo_by_fab, name="lst_vehiculo_by_fab"),
    path('buscar_v_f/', v_fabricante.buscar_v_f, name="buscar_v_f"),
    #Fabricante
    path('lst_fabricante/', v_fabricante.lst_fabricante, name="lst_fabricante"),
    path('buscar_f/', v_fabricante.buscar_f, name="buscar_f"),
    path('crear_fabricante/', v_fabricante.crear_fabricante, name="crear_fabricante"),
    path('post_crear_fabricante/', v_fabricante.post_crear_fabricante, name="post_crear_fabricante"),
    path('editar_fabricante/', v_fabricante.editar_fabricante, name="editar_fabricante"),
    path('actualizar_fabricante/', v_fabricante.actualizar_fabricante, name="actualizar_fabricante"),
    path('eliminar_fabricante/', v_fabricante.eliminar_fabricante, name="eliminar_fabricante"),
    #Pins
    path('crear_pin/', views.crear_pin, name="crear_pin"),
    path('post_crear_pin/', views.post_crear_pin, name="post_crear_pin"),
    path('eliminar_pin/', views.eliminar_pin, name="eliminar_pin"),
    path('lst_pines/', views.lst_pines, name="lst_pines"),
    #Auth
    path('sign_in/', auth.sign_in, name="sign_in"),
    path('post_sign_in/', auth.post_sign_in, name="post_sign_in"),
    path('sign_up/', auth.sign_up, name="sign_up"),
    path('post_sign_up/', auth.post_sign_up, name="post_sign_up"),
    path('logout/', auth.logout, name="logout"),
    #Solicitud
    path('crear_solicitud/', v_solicitud.crear_solicitud, name="crear_solicitud"),
    path('post_crear_solicitud/', v_solicitud.post_crear_solicitud, name="post_crear_solicitud"),
    path('lst_solicitud/', v_solicitud.lst_solicitud, name="lst_solicitud"),
    path('realizar_solicitud/', v_solicitud.realizar_solicitud, name="realizar_solicitud"),

    path('admin/', admin.site.urls),

] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
