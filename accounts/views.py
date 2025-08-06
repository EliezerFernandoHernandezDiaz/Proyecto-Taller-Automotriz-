from .forms import LoginForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import ClienteForm, VehiculoForm, MantenimientoForm # Importando los 3 formularios para el registro de cliente, vehiculo y mantenimiento
from .models import Cliente, Vehiculo  # Importando el modelo Cliente, para listar los clientes y  Vehiculo para listar los vehiculos
from .models import Mantenimiento  # Importando el modelo Mantenimiento para listar los mantenimientos

#Views.py prácticamente es el controlador principal de la aplicación, 
#aqui se maneja parte de la logica del negocio, validaciones, envio de información al modelo, etc.
#tambien se maneja el envio de mensajes de exito en las operaciones de crud o de error. 

#Se crea una vista para el login, que valida las credenciales de un usuario
def login_view(request):
    CREDENCIALES_VALIDAS = {
        'usuario': 'superuser@talleratm.com', #Se definen las credenciales válidas para el inicio de sesión
        'contraseña': '@super$15' #Se define la contraseña válida para el inicio de sesión, en caso de que 
        #se quiera cambiar las credenciales, se debe modificar este diccionario
    }
    
    form = LoginForm()
    # Verifica si el usuario ya está autenticado
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # Si el formulario se envía, se valida
        if form.is_valid():
            usuario = form.cleaned_data['username']
            contraseña = form.cleaned_data['password']
                    
            if usuario == CREDENCIALES_VALIDAS['usuario'] and contraseña == CREDENCIALES_VALIDAS['contraseña']:
                request.session['autenticado'] = True
                request.session['usuario'] = usuario
                messages.success(request, '¡Ha iniciado sesión exitosamente!')
                return redirect('menu_principal')  # Redirige al menú principal de gestión si las credenciales son correctas 
            else:
                messages.error(request, "Debe ingresar un usuario y contraseña válidos") # Si las credenciales no son válidas, se muestra un mensaje de error
        else:
            messages.error(request, "Por favor complete todos los campos")
    
    return render(request, 'accounts/login.html', {'form': form})  #aqui redirige al login

## Se crea una vista para el menú principal, que redirige al usuario al menú principal de la aplicación
def menu_principal(request):
    if not request.session.get('autenticado'):
        return redirect('login')
    return render(request, 'accounts/menu_principal.html')  #aqui redirige al menu principal

def cierre(request): # Vista para cerrar sesión
    request.session.flush()
    messages.info(request, 'Sesión cerrada, hasta luego.')
    return redirect('login')

#Operaciones crud para registrar clientes, vehiculos y mantenimientos
def registrar_cliente(request): # Vista para registrar un nuevo cliente
    if request.method == 'POST': 
        form = ClienteForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Cliente registrado correctamente.✅") # Mensaje de éxito al registrar un cliente
            return redirect('listar_clientes')
        else:
            messages.error(request, "❌ Error al registrar cliente. (Revisar los datos insertados).❌") # Mensaje de error al registrar un cliente
            # ⬇️ Mostrar errores en la misma pantalla de registro
            return render(request, 'accounts/registrar_cliente.html', {'form': form}) 
    else:
        form = ClienteForm()
    return render(request, 'accounts/registrar_cliente.html', {'form': form}) # #aqui redirige al formulario de registro de cliente, si se agrega correctamente el cliente

# Se crea una vista para editar un cliente, que permite modificar los datos de un cliente existente
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente) # Asegurando que se edite el cliente existente
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Cliente actualizado correctamente.✅") # Mensaje de éxito al actualizar un cliente
            return redirect('listar_clientes') # Redirige al listado de clientes después de actualizar
        else:
            messages.error(request, "❌ Error al actualizar los datos del cliente.❌") # Mensaje de error al actualizar un cliente
            return render(request,'accounts/editar_cliente.html',{'form':form,'cliente': cliente}) # Si hay un error, se muestra el formulario de edición con los errores
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'accounts/editar_cliente.html', {'form': form, 'cliente': cliente}) #aqui redirige al formulario de edicion de cliente, si se agrega correctamente el cliente


def eliminar_cliente(request, cliente_id): # Vista para eliminar un cliente
    cliente_id = get_object_or_404(Cliente, id=cliente_id)  # Obtiene el cliente por su ID
    cliente_id.delete()  # Elimina el cliente
    messages.success(request, "🗑️ Cliente eliminado correctamente.🗑️") 
    return redirect('listar_clientes')  # Redirige al listado de clientes después de eliminar


#Se programan las funciones crud para registrar, editar y listar los vehiculos
# También asegura de que se manejen los archivos para las imágenes de los vehículos
def registrar_vehiculo(request): # Vista para registrar un nuevo vehículo
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)  # Asegurando que se manejen archivos
        # request.FILES es necesario para manejar las imágenes de los vehículos
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Vehículo registrado correctamente.✅")
            return redirect('listar_vehiculos')  # Redirige a la lista de vehiculos  después de registrar el vehículo
        else:
         messages.error(request, "❌ No se pudo registrar el vehículo. (Revisar los datos insertados).❌") # Mensaje de error al registrar un vehículo
    else:
         form = VehiculoForm()
    
    return render(request, 'accounts/registrar_vehiculo.html', {'form': form})  #aqui redirige al formulario de registro de vehiculo 


def editar_vehiculo(request, vehiculo_id): # Vista para editar un vehículo existente
    vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
    if request.method == 'POST': 
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo) # Asegurando que se edite el vehículo existente y se manejen archivos
        if form.is_valid():
            form.save()
            messages.success(request, "✅ El vehículo ha sido actualizado correctamente.✅") # Mensaje de éxito al actualizar un vehículo
            return redirect('listar_vehiculos')
        else:
            messages.error(request, "❌ Error al actualizar vehículo.") # Mensaje de error al actualizar un vehículo
            return render(request, 'accounts/editar_vehiculo.html', {'form':form ,'vehiculo': vehiculo}) # Si hay un error, se muestra el formulario de edición con los errores
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'accounts/editar_vehiculo.html', {'form': form, 'vehiculo': vehiculo})  #aqui redirige al formulario de edicion de vehiculo
    
# Vista para eliminar un vehículo
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo= get_object_or_404(Vehiculo, id=vehiculo_id)  # Obtiene el vehículo por su ID
    vehiculo.delete()  # Elimina el vehículo
    messages.success(request, "🗑️ Vehículo eliminado correctamente.🗑️")
    return redirect('listar_vehiculos')  # Redirige al listado de vehículos después de eliminar



#Ahora se programan las funciones crud para mantenimiento    
    
def registrar_mantenimiento(request): # Vista para registrar un nuevo mantenimiento
    if request.method == 'POST':
        form = MantenimientoForm(request.POST) # Asegurando que se maneje el formulario de mantenimiento
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Mantenimiento registrado exitosamente.✅") # Mensaje de éxito al registrar un mantenimiento
            return redirect('ver_mantenimientos')
    else:
        form = MantenimientoForm()
    return render(request, 'accounts/registrar_mantenimiento.html', {'form': form}) #aqui redirige al formulario de registro de mantenimiento

def editar_mantenimiento(request, mantenimiento_id): # Vista para editar un mantenimiento existente
    mantenimiento = get_object_or_404(Mantenimiento, id=mantenimiento_id) # Obtiene el mantenimiento por su ID
    if request.method == 'POST':
        form = MantenimientoForm(request.POST, instance=mantenimiento) # Asegurando que se edite el mantenimiento existente
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Mantenimiento actualizado correctamente.✅') #Manejo de alerta de confirmación que se ha hecho la actualización
            return redirect('ver_mantenimientos')
        else:
            messages.error(request, '❌ Error al actualizar el mantenimiento.❌ Revise los campos.') # Mensaje de error al actualizar un mantenimiento
    else:
        form = MantenimientoForm(instance=mantenimiento)

    return render(request, 'accounts/editar_mantenimiento.html', {'form': form, 'mantenimiento': mantenimiento}) #aqui redirige al formulario de edicion de mantenimiento

     
def eliminar_mantenimiento(request, mantenimiento_id): # Vista para eliminar un mantenimiento
    mantenimiento=get_object_or_404(Mantenimiento, id=mantenimiento_id)
    mantenimiento.delete()
    messages.success(request, "🗑️ Registro de mantenimiento eliminado correctamente.🗑️") 
    return redirect('ver_mantenimientos')   # Redirige al listado de mantenimientos después de eliminar
   


#se crea una vista para listar los clientes, vehiculos, y mantenimientos

def listar_clientes(request):
    clientes = Cliente.objects.all()  #obteniendo todos los clientes
    return render(request, 'accounts/listar_clientes.html', {'clientes': clientes})  #aqui redirige al listado de clientes


def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.select_related('cliente').all() #obteniendo todos los vehiculos y sus clientes relacionados
    return render(request, 'accounts/listar_vehiculos.html', {'vehiculos': vehiculos})  #aqui redirige al listado de vehiculos

#se crea una vista para listar los mantenimientos de un vehiculo asi como se realizo con los vehiculos
def ver_mantenimientos(request):
    mantenimientos = Mantenimiento.objects.select_related('vehiculo__cliente').all()  #obteniendo todos los mantenimientos y sus vehiculos relacionados
    return render(request, 'accounts/ver_mantenimientos.html', {'mantenimientos': mantenimientos})  #aqui redirige al listado de mantenimientos
