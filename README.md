# Sistema Vehículos
Desarrollo de un Sistema de Vehiculos

## Instalación de Software
1. Descargar e Instalar Python en su versión 3.8.2 o superior https://www.python.org/downloads/
2. Descargar e Instalar VS Code https://code.visualstudio.com/

## Preparación del entorno Virtual
1. Ingresar a la terminal o simbolos del sistema, ingresar el siguiente código
```
pip install virtualenv
```
Esto nos descargará los paquetes para la creación del entorno virtual que utiliza el proyecto

2. Creamos una carpeta que contendra los proyectos Django, y dentro de la carpeta accedemos mediante nuestra terminal o cmd para ingresar el siguiente código.
```
C:\Directorio> virtualenv venv
```
De esta manera creamos el entorno virtual en la carpeta Directorio para poder crear nuestro proyecto.

3. Activamos el entorno virtual en el que se trabajará accediendo a nuestro directorio venv\script\activate como lo muestra el siguiente codigo
```
C:\Directorio>venv\Scritps\activate
```
Esto activa el directorio, el terminal o cmd se debe mostrar similar a esto
```
(venv) C:\Directorio>
```

4. Descargar Django en el entorno virtual para dar soporte al proyecto digitamos el siguiente código
```
(venv) C:\Directorio>pip install Django
```
Esto descargará la informacion necesaria para poder ejecutar Django en el computador. 

## Importar el proyecto desde gitHub
1. En nuestro directorio procedemos a copiar el codigo de este proyecto como se observa
```
(venv) C:\Directorio>git clone https://github.com/javtronic/sistema_vehiculos.git
```
!Importante! 
Recordar ya tener previamente instalado Git para poder realizar esta acción

## Agregar las librerias para Firebase
1. En el mismo directorio procedemos a la instalación de pyrebase que es la libreria que nos permite trabajar con Firebase en Python, ingresamos el siguiente código.
```
(venv) C:\Directorio>pip install Pyrebase
```

## Ejecutar el Proyecto
1. Accedemos al directorio que clonamos
```
(venv) C:\Directorio>cd sistema_vehiculos
```

2. Dentro del directorio ejecutamos el servidor con los siguientes comandos
```
(venv) C:\Directorio>manage.py runserver
```
Al ejecutar este comando nos mostrará la siguiente información
```
Django version 3.0.8, using settings 'sistema_vehiculos.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
Accedemos al navegador y verificamos.


