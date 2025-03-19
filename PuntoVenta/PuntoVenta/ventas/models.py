from django.db import models
from django.forms import model_to_dict #json
from django.contrib.auth.models import User



# Create your models here.

class Cliente(models.Model):
    nombre =models.CharField(max_length=200, null=True, blank=False)
    telefono =models.CharField(max_length=200, null=True, blank=False)
    cuit_cuil =models.CharField(max_length=13, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False)
    direccion = models.CharField(max_length=200, null=True, blank=False)
    created =models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name='cliente'
        verbose_name_plural='clientes'

    def __str__(self):
        return self.nombre


class CategoriaProd(models.Model):
    nombre=models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name="categoriaProd"
        verbose_name_plural="catgoriasProd"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    
    codigo_barras = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, unique=True, null=False)
    imagen = models.ImageField(upload_to="producto", default='producto/no-imagen_Dk8xCo4.jpg')
    categoria = models.ForeignKey('CategoriaProd', on_delete=models.CASCADE)
    disponibilidad = models.ForeignKey('PrecioUnitario',on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=False, blank=True)
    #precioUnit = models.PositiveIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    def calcular_precio_bulto(self):
        """Calcular precio por bulto si el tipo es Bulto."""
        if self.tipo == self.BULTO and self.cantidad_bulto:
            precio_bulto_final = self.precio_lista / self.cantidad_bulto
        return self.precio_bulto_final

    '''def calcular_precio_venta(self, cantidad):
        """Calcular precio de venta con el margen de ganancia según la cantidad seleccionada."""
        if cantidad in self.formas_venta:
            precio = self.calcular_precio_bulto() if self.tipo == self.BULTO else self.precio
            return precio + (precio * (self.ganancia / 100))
        return self.precio'''

    class Meta:
        verbose_name="Producto"
        verbose_name_plural="Productos"
        order_with_respect_to = 'descripcion'
        permissions = [
            ("can_add_product", "Can add product"),
            ("can_change_product", "Can change product"),
            ("can_delete_product", "Can delete product"),
        ]
    
    def __str__(self):
        return self.descripcion

class PrecioUnitario(models.Model):
    #producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=False) #precio del costo del producto
    preciox1 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    gananciax1 = models.PositiveIntegerField()
    preciox10 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    gananciax10 = models.PositiveIntegerField()
    preciox25 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    gananciax25 = models.PositiveIntegerField()
    preciox50 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    gananciax50 = models.PositiveIntegerField()
    preciox100 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    gananciax100 = models.PositiveIntegerField()
    preciox1000 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    gananciax1000 = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Precio unitario"
        verbose_name_plural="Precios unitarios"

    def calcular_preciox1(self):
        if self.gananciax1 > 0:
            return self.costo + (self.costo * (self.gananciax1 / 100))
        else:
            self.preciox1 = 0
    
    def calcular_preciox10(self):
        if self.gananciax10 > 0:
            return (self.costo + (self.costo * (self.gananciax10 / 100)))*10
        else:
            self.preciox10 = 0
    
    def calcular_preciox25(self):
        if self.gananciax25 > 0:
            return (self.costo + (self.costo * (self.gananciax25 / 100)))*25
        else:
            self.preciox25 = 0
    
    def calcular_preciox50(self):
        if self.gananciax50 > 0:
            return (self.costo + (self.costo * (self.gananciax50 / 100)))*50
        else:
            self.preciox50 = 0
    
    def calcular_preciox100(self):
        if self.gananciax100 > 0:
            return (self.costo + (self.costo * (self.gananciax100 / 100)))*100
        else:
            self.preciox100 = 0

    def calcular_preciox1000(self):
        if self.gananciax1000 > 0:
            return (self.costo + (self.costo * (self.gananciax1000 / 100)))*1000
        else:
            self.preciox1000 = 0

    def __str__(self):
        return f"{self.id} tiene un costo de {self.costo}"

class PrecioBulto(models.Model):
    #producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="precios_bultos")
    costo_bulto = models.DecimalField(max_digits=10, decimal_places=2)  # Costo del bulto
    cantidad_bulto = models.PositiveIntegerField()  # Número de unidades por bulto
    precio_bulto = models.DecimalField(max_digits=10, decimal_places=2)  # Precio de venta del bulto
    ganancia_bulto = models.PositiveIntegerField()  # Ganancia por bulto

    class Meta:
        verbose_name = "Precio por bulto"
        verbose_name_plural = "Precios por bulto"

    def __str__(self):
        return f"Bulto de {self.cantidad_por_bulto} unidades: {self.precio_bulto} - precio: ${self.precio_bulto}"


### Lista de precios especiales (Lista 3)
class PreciosEspeciales(models.Model):
    #producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="precios_especiales")
    cantidad_especial = models.PositiveIntegerField()  # Cantidad mínima para aplicar el precio especial
    precio_especial = models.DecimalField(max_digits=10, decimal_places=2)  # Precio especial

    class Meta:
        #unique_together = ('cantidad_especial')  # Evitar duplicados para la misma cantidad
        verbose_name_plural = "Precios especiales"

    def __str__(self):
        return f"{self.cantidad} unidades: ${self.precio_especial}"


### Ofertas
class Ofertas(models.Model):
    #producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="ofertas")
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2)  # Precio de la oferta
    fecha_inicio = models.DateField()  # Inicio de la oferta
    fecha_fin = models.DateField(null=True, blank=True)  # Fin de la oferta (opcional, puede quedar abierto)
    
    
    def is_active(self):
        """
        Método para verificar si la oferta está activa.
        """
        from datetime import date
        today = date.today()
        return (self.fecha_inicio <= today) and (self.fecha_fin is None or today <= self.fecha_fin)

    class Meta:
        verbose_name_plural = "Ofertas"

    def __str__(self):
        if self.fecha_fin:
            return f"Oferta ${self.precio_oferta} (Hasta {self.fecha_fin})"
        return f"{self.producto.descripcion} - Oferta ${self.precio_oferta} (Hasta agotar stock)"




class Egreso(models.Model):
    fecha_pedido = models.DateField(max_length=255)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL , null=True , related_name='cliente')
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ventas_realizadas')
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    comentarios = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    ticket = models.BooleanField(default=True)
    desglosar = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now_add=True , null=True)
    efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tarjeta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=100)  # O usar un campo ChoiceField


    class Meta:
        verbose_name='egreso'
        verbose_name_plural = 'egresos'
        order_with_respect_to = 'fecha_pedido'
        
    
    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre if self.cliente else 'Sin cliente'}"


class ProductosEgreso(models.Model):
    egreso = models.ForeignKey(Egreso, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2 , null=False)
    precio = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    iva = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2 , null=False , default=0)
    created = models.DateTimeField(auto_now_add=True)
    entregado = models.BooleanField(default=True)
    devolucion = models.BooleanField(default=False)

    class Meta:
        verbose_name='producto egreso'
        verbose_name_plural = 'productos egreso'
        order_with_respect_to = 'created'
    
    def __str__(self):
        return self.producto
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['created'])
        return item


class Sucursal(models.Model):
    nombre =models.CharField(max_length=200, null=True, blank=False)
    domicilio =models.CharField(max_length=200, null=True, blank=False)
    mail =models.CharField(max_length=200, null=True, blank=False)
    telefono =models.CharField(max_length=200, null=True, blank=False)
    created =models.DateTimeField(auto_now_add=True)
    updated =models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name='sucursal'
        verbose_name_plural='sucursales'

    def __str__(self):
        return self.nombre

class CierreCaja(models.Model):
    fecha = models.DateField(unique=True)
    total_ventas = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_efectivo = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_tarjeta = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_transferencia = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    comentarios = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cierre {self.fecha}"
