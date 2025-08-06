from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

# se crean los modelos que sirven como entidades para la base de datos

#se creo un modelo para los clientes
# este modelo tiene los campos que se necesitan para almacenar la informacion de los clientes

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    dui = models.CharField(max_length=10, unique=True, validators=[
        RegexValidator(r'^\d{8}-\d{1}$', 
        message="El DUI debe tener el formato 12345678-9 (con guión)" ,) # 8 dígitos y un guión seguido de un dígito
    ])
    email = models.EmailField()
    telefono = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(r'^\d{8}$', 
            message="El número de teléfono debe tener exactamente 8 dígitos.")
        ])

    def __str__(self):
        return self.nombre
    
#ahora se crea un modelo para los vehiculos
# este modelo tiene los campos que se necesitan para almacenar la informacion de los vehiculos
#para el año del vehiculo se agregan validaciones para que el año sea ente 1980 y 2026

class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    placa = models.CharField(
        max_length=10, 
        unique=True,
        validators=[
           RegexValidator(
            regex=r'^[A-Z]{1,2}\d{1,4}-[A-Z0-9]{1,4}$',
            message="La placa debe tener un formato válido como P123-456 o P12-8F2."
        )
        ]
    )
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio= models.PositiveIntegerField(
        validators=[
            MinValueValidator(1980), 
            MaxValueValidator(2026), 
            RegexValidator(r'^\d{4}$', message="El año debe ser de exactamente 4 dígitos. Debe estar entre 1980 y 2026.")] , 
            verbose_name= "Año del vehiculo"
        
    )
    tipo = models.CharField(max_length=30) 
    color = models.CharField(max_length=30)

    #Para las fotos de los vehiculos, se crea un campo de imagen
    foto_frontal = models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    foto_trasera= models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    foto_costado_der = models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    foto_costado_izq = models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    foto_placa = models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"


    #se crea un modelo para representar los mantenimientos
    # este modelo tiene los campos que se necesitan para almacenar la informacion de los mantenimientos

class Mantenimiento(models.Model):
    TIPO_CHOICES = [
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
        ('cambio de aceite', 'Cambio de aceite'),
        ('revision general', 'Revisión general'),
        ('reparacion', 'Reparación'),
        ('alineado y balanceo', 'Alineado y balanceo'),
        ('otro', 'Otro'),
    ]
 
    #se crea un campo para el vehiculo relacionado con el mantenimiento
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='mantenimientos') # Relación con el modelo Vehiculo
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES) 
    fecha = models.DateField()
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    repuestos_utilizados = models.TextField(blank=True, null=True)
    proximo_mantenimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.vehiculo.placa} - {self.fecha.strftime('%Y-%m-%d')}" # Formato de fecha para mejor legibilidad
    