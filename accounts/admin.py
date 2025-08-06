#Confiuguración del panel de administración para las aplicaciones de cuentas
from django.contrib import admin
from .models import Cliente, Vehiculo, Mantenimiento

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dui', 'telefono', 'email')

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'marca', 'modelo', 'anio', 'cliente')

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'fecha', 'tipo', 'costo')
