#Librerias necesarias para crear los formularios
import re
from django import forms
from .models import Cliente, Vehiculo, Mantenimiento  #agregando los modelos para crear los formularios para cada uno
from datetime import date  

#Formulario para el inicio de sesión 
#Se agregan widgets para cada formulario para que se vea mejor en la interfaz de usuario
class LoginForm(forms.Form):
    username = forms.CharField( 
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese su usuario', 
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingrese su contraseña',
            'class': 'form-control'
        })
    )
#Formulario para el registro de un nuevo cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'dui', 'email', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder':'Ingrese el nombre completo del cliente'}),
            'dui': forms.TextInput(attrs={
            'placeholder':'Ingrese el número de DUI del cliente (Por ejemplo: 00234553-1)',
            'oninput': "this.value = this.value.replace(/[^0-9-]/g, '')"  #para que solo se ingresen numeros y guiones
            }),
            'email': forms.EmailInput(attrs={'placeholder':'Ingrese el correo electronico del cliente (Por ejemplo: nombre_cliente@gmail.com)'}),
            'telefono': forms.TextInput(attrs={'placeholder':'Ingrese el número de teléfono del cliente (Por ejemplo: 78654321)'}),
        }

        #Agregando validaciones para los campos del formulario del cliente
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not re.match(r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$", nombre): #validacion para que el nombre solo contenga letras y espacios
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return nombre
    
    #validación para el dui para que tenga formato salvadoreño 

    def clean_dui(self):
        dui=self.cleaned_data.get('dui')
        if not  re.match(r'^\d{8}-\d{1}$', dui):
            raise forms.ValidationError("El DUI debe tener el formato 12345678-9")
        return dui
    
    #validación para el telefono y que tenga formato de 8 digitos como se hace acá en el salvador

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError("El número de teléfono solo debe contener dígitos.")
        if len(telefono) != 8:
            raise forms.ValidationError("El número de teléfono debe tener exactamente 8 dígitos.")
        return telefono

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'placa', 'marca', 'modelo', 'anio', 'tipo', 'color',
                  'foto_frontal', 'foto_trasera', 'foto_costado_der',
                  'foto_costado_izq', 'foto_placa']
        widgets = {
            'placa': forms.TextInput(attrs={'placeholder':'Ingrese la placa del vehículo (Por ejemplo: P-1234)'}),
            'marca': forms.TextInput(attrs={'placeholder': 'Ingrese la marca del vehículo (Por ejemplo: Toyota, Nissan, etc)'}),
            'modelo': forms.TextInput(attrs={'placeholder': 'Ingrese el modelo del vehículo (Por ejemplo: Hilux, Sentra, Forte, etc)'}),
            'anio': forms.NumberInput(attrs={'placeholder': 'Ingrese el año del vehículo (Formato válido: 1980-2026)', 'max_length':'4', }),
            'tipo': forms.TextInput(attrs={'placeholder': 'Ingrese el tipo de vehículo (Por ejemplo: Sedan, SUV, Camioneta, etc)'}),
            'color': forms.TextInput(attrs={'placeholder': 'Ingrese el color del vehículo (Por ejemplo: Rojo, Verde, Azul, etc)'}), 


            #widgets para los campos de imagen
            'foto_frontal': forms.FileInput(),
            'foto_trasera': forms.FileInput(),
            'foto_costado_der': forms.FileInput(),
            'foto_costado_izq': forms.FileInput(),
            'foto_placa': forms.FileInput(),

               
        }
        #Se realizarán las validaciones de los campos del formulario para el vehículo
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['cliente'].empty_label = 'Seleccione un cliente registrado'

       #Se valida la placa del vehículo para que tenga el formato salvadoreño
    def clean_placa(self):
     placa = self.cleaned_data.get('placa', '').upper() #Para que se guarde en mayúsculas las placas
     if not re.match(r'^[A-Z]{1,2}\d{1,4}-[A-Z0-9]{1,4}$', placa):
        raise forms.ValidationError("La placa debe seguir el formato salvadoreño como P123-456 o P12-8F2.")
     return placa

    #Se valida el año del vehículo para que esté en un rango válido, lo pusimos de 1980-2026

    def clean_anio(self):
      anio = self.cleaned_data.get('anio')
      if not re.match(r'^\d{4}$', str(anio)):
         raise forms.ValidationError("El año debe tener exactamente 4 dígitos.")
      if int(anio) < 1980 or int(anio) > 2026:
        raise forms.ValidationError("El año del vehículo debe estar entre 1980 y 2026.")
      return anio

    #Se valida la marca del vehiculo para que solo sea letras y espacios en caso de ser necesario 
    def clean_marca(self):
        marca=self.cleaned_data.get('marca')
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', marca):
          raise forms.ValidationError('La marca solo debe contener letras y espacios.')
        return marca
    
    #Se valida el modelo del vehiculo para que sea letras numeros y espacios
    def clean_modelo(self):
        modelo=self.cleaned_data.get('modelo')
        if not re.match(r'^[A-Za-z0-9áéíóúÁÉÍÓÚñÑüÜ \-]+$', modelo):
         raise forms.ValidationError('El modelo solo debe contener letras, números, guiones y espacios.')
        return modelo 
    
     #Validación del tipo de vehiculo para que solo sea letras y espacios
    def clean_tipo(self):
        tipo=self.cleaned_data.get('tipo')
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', tipo):
            raise forms.ValidationError('El tipo de vehículo solo debe contener letras y espacios.')
        return tipo
    #Validacion del color del vehiculo para que solo sea letras y espacios
    def clean_color(self):
        color= self.cleaned_data.get('color')
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ ]+$', color):
            raise forms.ValidationError('El color del vehículo solo debe contener letras y espacios')
        return color 
    def clean(self):
        super().clean()
        required_images = [
            'foto_frontal',
            'foto_trasera',
            'foto_costado_der',
            'foto_costado_izq',
            'foto_placa'
        ]
        for img_field in required_images:
            if not self.files.get(img_field) and not self.instance.pk:
                self.add_error(img_field, 'Debe subir las fotos correspondientes al vehículo si desea registrarlo al sistema.')
    
    #Validación de las imágenes del vehículo para que sean archivos de imagen válidos

   #Formulario para el mantenimiento de vehículos 
class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = ['vehiculo', 'tipo', 'fecha', 'descripcion', 'costo', 'repuestos_utilizados', 'proximo_mantenimiento'] #Campos del formulario para el mantenimiento de vehículos

        labels={
            'vehiculo': 'Vehículos Registrados',
            'tipo': 'Seleccione el Tipo de Mantenimiento',
            'fecha': 'Fecha en que realizó el Mantenimiento',
            'descripcion': 'Descripción del Mantenimiento',
            'costo': 'Costo Total en (USD)',
            'repuestos_utilizados': 'Repuestos utilizados',
            'proximo_mantenimiento': 'Fecha del Próximo Mantenimiento',
        }
        widgets = {
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date',
                'min': '2025-01-01',  # Asegura que la fecha mínima sea el 1 de enero de 2025
                'max': '2026-12-31',  # Asegura que la fecha máxima sea el 31 de diciembre de 2026
                'placeholder': 'Seleccione la fecha actual del mantenimiento'
                }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese una descripción breve del mantenimiento realizado',
                }),
            'costo': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el costo total del mantenimiento en USD',
            }),
            'repuestos_utilizados': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los repuestos utilizados en el mantenimiento (separados por comas)',
                }),


            'proximo_mantenimiento': forms.DateInput(attrs={
                'class': 'form-control', 'type': 'date',
                'type': 'date',
                'min': '2025-01-01',  # Asegura que la fecha mínima sea el 1 de enero de 2025
                'max': '2026-12-31', # Asegura que la fecha máxima sea el 31 de diciembre de 2026
                'placeholder': 'Seleccione la fecha del próximo mantenimiento'
                }),
        }
        #Se realizarán las validaciones de los campos del formulario de mantenimiento
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehiculo'].empty_label = 'Seleccione un vehículo registrado a realizar el mantenimiento'

        #Para no cambiar el modelo, tuve que forzar a que el campo de tipo de mantenimiento sea un campo de selección
        original_choices=self.fields['tipo'].choices
        self.fields['tipo'].choices=[('', 'Seleccione el tipo de mantenimiento a realizar')]+list(original_choices)
     
     #Validación para que no se repita el mantenimiento con el mismo vehículo, tipo y fecha
    def clean(self):
     cleaned_data = super().clean()
     vehiculo = cleaned_data.get('vehiculo')
     tipo = cleaned_data.get('tipo')
     fecha = cleaned_data.get('fecha')

     if self.instance.pk is None and vehiculo and tipo and fecha:
        existe = Mantenimiento.objects.filter(
            vehiculo=vehiculo,
            tipo=tipo,
            fecha=fecha
        ).exists()
        if existe:
            raise forms.ValidationError("Ya existe un mantenimiento registrado con ese vehículo, tipo y fecha.")
     return cleaned_data

    #Validación del costo del mantenimiento para que sea un número positivo y jamas negativo
    def clean_costo(self):
       costo = self.cleaned_data.get('costo')
       if costo is not None and costo < 0:
        raise forms.ValidationError("El costo no puede ser negativo.")
       return costo
     #Validación para que desde teclado se ingrese una fecha valida para el año, debe estar entre 2025 y 2026
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if not fecha:
            raise forms.ValidationError("Debe ingresar una fecha válida.")

        if fecha.year < 2025 or fecha.year > 2026:
            raise forms.ValidationError("La fecha del mantenimiento debe estar entre los años 2025 y 2026.")

        if fecha > date.today():
            raise forms.ValidationError("La fecha del mantenimiento no puede ser futura.")
        
        return fecha
#Validación del próximo mantenimiento para que sea posterior al mantenimiento realizado y no supere el 31/12/2026
    def clean_proximo_mantenimiento(self):
     fecha_mantenimiento = self.cleaned_data.get('fecha')
     proximo_mant = self.cleaned_data.get('proximo_mantenimiento')

     if proximo_mant and fecha_mantenimiento:
        if proximo_mant.year > 2026 or proximo_mant < fecha_mantenimiento:
            raise forms.ValidationError(
                "La fecha del próximo mantenimiento debe ser posterior al mantenimiento realizado y no superar el 31/12/2026."
            )
     return proximo_mant
    
    #Validación de la descripción del mantenimiento para que tenga al menos 10 caracteres
    def clean_descripcion(self):
     descripcion = self.cleaned_data.get('descripcion', '').strip()
     if len(descripcion) < 10:
        raise forms.ValidationError("La descripción debe tener al menos 10 caracteres.")
     return descripcion
    

