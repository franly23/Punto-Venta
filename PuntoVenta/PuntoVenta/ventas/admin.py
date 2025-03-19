from django.contrib import admin
from ventas.models import Cliente, Producto, CategoriaProd, Sucursal, PrecioUnitario
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType


# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'telefono', 'cuit_cuil', 'email', 'direccion')
    search_field = ['nombre']
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldset = ()

admin.site.register(Cliente, ClienteAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo_barras','descripcion', 'categoria', 'disponibilidad','cantidad')
    search_field = ['descripcion']
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldset = ()

admin.site.register(Producto, ProductoAdmin)

class PrecioUnitarioAdmin(admin.ModelAdmin):
    list_display = ('costo', 'gananciax1', 'gananciax10', 'gananciax25', 'gananciax50', 'gananciax100', 'gananciax1000')
    search_field = []
    readonly_fields = ('preciox1', 'preciox10', 'preciox25', 'preciox50', 'preciox100', 'preciox1000')
    filter_horizontal = ()
    list_filter = ()
    fieldset = ()

admin.site.register(PrecioUnitario, PrecioUnitarioAdmin)

class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'domicilio', 'mail', 'telefono')
    search_field = []
    readonly_fields = ('created', 'updated')
    filter_horizontal = ()
    list_filter = ()
    fieldset = ()

admin.site.register(Sucursal, SucursalAdmin)

class CategoriasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_field = ['id']
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldset = ()

admin.site.register(CategoriaProd, CategoriasAdmin)


# Crear grupo y asignar permisos 
jefe_group, created = Group.objects.get_or_create(name='Jefe')
gerente_group, created = Group.objects.get_or_create(name='Gerente')
empleado1_group, created = Group.objects.get_or_create(name='Empleado_mostrador')
empleado2_group, created = Group.objects.get_or_create(name='Empleado_envios')
# Asignar permisos a los grupos
