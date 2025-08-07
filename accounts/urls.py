from django.urls import path 

 # Importando el módulo path para definir las rutas de la aplicación
#aca se importan las funciones que se programaron en las vistas y se van a utilizar en las urls
from .views import menu_principal,login_view, cierre, registrar_cliente, editar_cliente, eliminar_cliente, registrar_vehiculo, editar_vehiculo, eliminar_vehiculo, editar_mantenimiento, eliminar_mantenimiento, registrar_mantenimiento, listar_vehiculos, ver_mantenimientos, listar_clientes

# Definición de las URLs de la aplicación accounts
# las URLs se definen utilizando el módulo path de Django, que permite asociar una URL a una vista específica
## Cada URL tiene un nombre que se puede utilizar para referenciarla en otras partes de la aplicación, como en plantillas o redirecciones

urlpatterns = [
    path('', login_view, name='login'), # Ruta para la vista de inicio de sesión
    path('menu-principal/', menu_principal, name='menu_principal'), # Ruta para el menú principal
    path('logout/', cierre, name='logout'), # Ruta para cerrar sesión
    path('registrar_cliente/', registrar_cliente, name='registrar_cliente'), # Ruta para registrar un nuevo cliente
    path('editar_cliente/<int:cliente_id>/', editar_cliente, name='editar_cliente'), # Ruta para editar un cliente existente
    path('eliminar_cliente/<int:cliente_id>/', eliminar_cliente, name='eliminar_cliente'), # Ruta para eliminar un cliente existente
    path('registar_vehiculo/', registrar_vehiculo, name='registrar_vehiculo'), # Ruta para registrar un nuevo vehículo
    path('editar_vehiculo/<int:vehiculo_id>/', editar_vehiculo, name='editar_vehiculo'), # Ruta para editar un vehículo existente
    path('eliminar_vehiculo/<int:vehiculo_id>/', eliminar_vehiculo, name='eliminar_vehiculo'), # Ruta para eliminar un vehículo existente
    path('registrar_mantenimiento/', registrar_mantenimiento, name='registrar_mantenimiento'), # Ruta para registrar un nuevo mantenimiento
    path('mantenimientos/editar/<int:mantenimiento_id>/',editar_mantenimiento, name='editar_mantenimiento'), # Ruta para editar un mantenimiento existente
    path('mantenimientos/eliminar/<int:mantenimiento_id>/',eliminar_mantenimiento, name='eliminar_mantenimiento'), # Ruta para eliminar un mantenimiento existente
    path('vehiculos/', listar_vehiculos, name='listar_vehiculos'), # Ruta para listar todos los vehículos
    path('mantenimientos/', ver_mantenimientos, name='ver_mantenimientos'), # Ruta para ver los mantenimientos de un vehículo
    path('listar_clientes/', listar_clientes, name='listar_clientes'), # Ruta para listar todos los clientes
]

