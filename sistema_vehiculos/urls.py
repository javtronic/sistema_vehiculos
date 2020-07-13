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
from vehiculo import views

urlpatterns = [
    path('', views.index, name="index"),
    #Vehiculo
    path('crear/', views.crear, name="crear"),
    path('post_crear/', views.post_crear, name="post_crear"),
    path('editar/', views.editar, name="editar"),
    path('detalle_vehiculo/', views.detalle_vehiculo, name="detalle_vehiculo"),
    path('lst_vehiculo/', views.lst_vehiculo, name="lst_vehiculo"),
    path('actualizar/', views.actualizar, name="actualizar"),
    path('eliminar/', views.eliminar, name="eliminar"),
    #Fabricante
    path('lst_fabricante/', views.lst_fabricante, name="lst_fabricante"),
    path('crear_fabricante/', views.crear_fabricante, name="crear_fabricante"),
    path('post_crear_fabricante/', views.post_crear_fabricante, name="post_crear_fabricante"),
    path('editar_fabricante/', views.editar_fabricante, name="editar_fabricante"),
    path('actualizar_fabricante/', views.actualizar_fabricante, name="actualizar_fabricante"),
    path('eliminar_fabricante/', views.eliminar_fabricante, name="eliminar_fabricante"),
    path('admin/', admin.site.urls),
]
