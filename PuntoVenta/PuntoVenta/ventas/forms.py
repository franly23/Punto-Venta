from django import forms
from ventas.models import Cliente, Producto, PrecioUnitario, PrecioBulto, PreciosEspeciales, Ofertas


class AddClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre', 'telefono', 'cuit_cuil', 'email', 'direccion')
        labels = {
            'nombre': 'Nómbre cliente: ',
            'telefono': 'Teléfono (contacto): ',
            'cuit_cuil': 'cuit/cuil: ',
            'email': 'email (contacto): ',
            'direccion': 'Dirección: ',
        }

class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre', 'telefono',  'cuit_cuil', 'email', 'direccion')
        labels = {
            'nombre': 'Nómbre cliente: ',
            'telefono': 'Teléfono (contacto): ',
            'cuit_cuil': 'cuit/cuil: ',
            'email': 'email (contacto): ',
            'direccion': 'Dirección: ',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'id': 'text', 'id':'nombre_editar'}),
            'telefono': forms.TextInput(attrs={'id': 'text', 'id':'telefono_editar'}),
            'cuit_cuil': forms.TextInput(attrs={'id': 'text', 'id':'cuit-cuil_editar'}),
            'email': forms.TextInput(attrs={'id': 'text', 'id':'email_editar'}),
            'direccion': forms.TextInput(attrs={'id': 'text', 'id':'direccion_editar'}),
        }

class AddProductoForm(forms.ModelForm):
    tipo_producto = forms.ChoiceField(
        choices=[('unidad', 'Por unidad'), ('bulto', 'Por bulto')],
        widget=forms.RadioSelect,
        label="Tipo de producto",
    )
    precio_bulto = forms.DecimalField(
        required=False,
        label="Precio del bulto",
        widget=forms.NumberInput(attrs={"placeholder": "Ingrese el precio del bulto"}),
    )
    precio_unitario = forms.DecimalField(
        required=False,
        label="Precio unitario",
        widget=forms.NumberInput(attrs={"placeholder": "Ingrese el precio unitario"}),
    )
    class Meta:
        model = Producto
        fields = ['codigo_barras', 'descripcion', 'imagen', 'categoria', 'disponibilidad','cantidad']
        labels = {
            'codigo_barras': 'Cód. Barras: ',
            'descripcion': 'Descripcion del producto: ',
            'imagen': 'Imagen: ',
            'categoria': 'Categoria a la que pertenece: ',
            'disponibilidad': '¿El producto esta disponible?: ',
            'cantidad': 'Cantidad: ',
        }
        
        widgets = {
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
        }

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo_barras'].widget.attrs['placeholder'] = 'xxxxxxxx'
        self.fields['descripcion'].widget.attrs['placeholder'] = 'bandejas'
        self.fields['cantidad'].widget.attrs['placeholder'] = '12345'

    def clean(self):
        cleaned_data = super().clean()
        tipo_producto = cleaned_data.get("tipo")
        cantidad_bulto = cleaned_data.get("cantidad_bulto")
        precio_unitario = cleaned_data.get("precio_lista")

        if tipo_producto == Producto.BULTO and not cantidad_bulto:
            raise forms.ValidationError("Debe especificar la cantidad por bulto si el tipo es 'Bulto'.")
        if tipo_producto == Producto.BULTO and not precio_unitario:
            raise forms.ValidationError("Debe especificar el precio de lista si el tipo es 'Bulto'.")
        return cleaned_data

class AddPreciosUnitariosForm(forms.ModelForm):
    
    class Meta:
        model = PrecioUnitario
        fields = [ 'costo', 'preciox1', 'gananciax1', 'preciox10', 'gananciax10', 'preciox25', 'gananciax25', 'preciox50', 'gananciax50', 'preciox100', 'gananciax100', 'preciox1000','gananciax1000']
        labels = {
            'costo': 'Costo: ',
            'preciox1': 'Por Unidad: ',
            'gananciax1': 'Por Unidad: ',
            'preciox10': 'Por 10: ',
            'gananciax10': 'Por 10: ',
            'preciox25': 'Por 25: ',
            'gananciax25': 'Por 25: ',
            'preciox50': 'Por 50: ',
            'gananciax50': 'Por 50: ',
            'preciox100': 'Por 100: ',
            'gananciax100': 'Por 100: ',
            'preciox1000': 'Por 1000: ',
            'gananciax1000': 'Por 1000: ',
        }
        widgets = {
            #'producto': forms.Select(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox1': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox10': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax10': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox25': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax25': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox50': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax50': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox100': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax100': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox1000': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax1000': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    '''def calcular_precios(self, costo):
        preciox1 = costo * (1 + (self.cleaned_data[gananciax1] / 100))
        preciox10 = (costo * (1 + (self.cleaned_data[gananciax10] / 100))) * 10
        preciox25 = (costo * (1 + (self.cleaned_data[gananciax25] / 100))) * 25
        preciox50 = (costo * (1 + (self.cleaned_data[gananciax50] / 100))) * 50
        preciox100 = (costo * (1 + (self.cleaned_data[gananciax100] / 100))) * 100
        preciox1000 = (costo * (1 + (self.cleaned_data[gananciax100] / 100))) * 1000
        return preciox1, preciox10, preciox25, preciox50, preciox100, preciox1000'''

class AddPreciosBultosForm(forms.ModelForm):
    class Meta:
        model = PrecioBulto
        fields = [ 'costo_bulto', 'cantidad_bulto', 'precio_bulto', 'ganancia_bulto']

        widgets = {
            #'producto': forms.Select(attrs={'class': 'form-control'}),
            'costo_bulto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cantidad_bulto': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_bulto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ganancia_bulto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class EditarProductoForm(forms.ModelForm):
    tipo_producto = forms.ChoiceField(
        choices=[('unidad', 'Por unidad'), ('bulto', 'Por bulto')],
        widget=forms.RadioSelect,
        label="Tipo de producto",
    )
    precio_bulto = forms.DecimalField(
        required=False,
        label="Precio del bulto",
        widget=forms.NumberInput(attrs={"placeholder": "Ingrese el precio del bulto"}),
    )
    precio_unitario = forms.DecimalField(
        required=False,
        label="Precio unitario",
        widget=forms.NumberInput(attrs={"placeholder": "Ingrese el precio unitario"}),
    )
    class Meta:
        model = Producto
        fields = ['codigo_barras', 'descripcion', 'imagen', 'categoria', 'disponibilidad','cantidad']
        labels = {
            'codigo_barras': 'Cód. Barras: ',
            'descripcion': 'Descripcion del producto: ',
            'imagen': 'Imagen: ',
            'categoria': 'Categoria a la que pertenece: ',
            'disponibilidad': '¿El producto esta disponible?: ',
            'cantidad': 'Cantidad: ',
        }
        
        widgets = {
            'codigo_barras': forms.TextInput(attrs={'id': 'text', 'id':'codigo_barras_editar'}),
            'descripcion': forms.TextInput(attrs={'id': 'text', 'id':'nombre_editar'}),
            'imagen': forms.ClearableFileInput(attrs={'id': 'text', 'id':'nombre_editar'}),
            'categoria': forms.Select(attrs={'id': 'text', 'id':'nombre_editar'}),
            'cantidad': forms.TextInput(attrs={'id': 'text', 'id':'nombre_editar'}),
        }

        
    

    def clean(self):
        cleaned_data = super().clean()
        tipo_producto = cleaned_data.get("tipo")
        cantidad_bulto = cleaned_data.get("cantidad_bulto")
        precio_unitario = cleaned_data.get("precio_lista")

        if tipo_producto == Producto.BULTO and not cantidad_bulto:
            raise forms.ValidationError("Debe especificar la cantidad por bulto si el tipo es 'Bulto'.")
        if tipo_producto == Producto.BULTO and not precio_unitario:
            raise forms.ValidationError("Debe especificar el precio de lista si el tipo es 'Bulto'.")
        return cleaned_data


class EditarPreciosUnitariosForm(forms.ModelForm):
    
    class Meta:
        model = PrecioUnitario
        fields = ['costo', 'preciox1', 'gananciax1', 'preciox10', 'gananciax10', 'preciox25', 'gananciax25', 'preciox50', 'gananciax50', 'preciox100', 'gananciax100', 'preciox1000','gananciax1000']
        labels = {
            'costo': 'Costo: ',
            'preciox1': 'Por Unidad: ',
            'gananciax1': 'Por Unidad: ',
            'preciox10': 'Por 10: ',
            'gananciax10': 'Por 10: ',
            'preciox25': 'Por 25: ',
            'gananciax25': 'Por 25: ',
            'preciox50': 'Por 50: ',
            'gananciax50': 'Por 50: ',
            'preciox100': 'Por 100: ',
            'gananciax100': 'Por 100: ',
            'preciox1000': 'Por 1000: ',
            'gananciax1000': 'Por 1000: ',
        }
        widgets = {
            #'producto': forms.Select(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox1': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox10': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax10': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox25': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax25': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox50': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax50': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox100': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax100': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preciox1000': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'gananciax1000': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

    '''def calcular_precios(self, costo):
        preciox1 = costo * (1 + (self.cleaned_data[gananciax1] / 100))
        preciox10 = (costo * (1 + (self.cleaned_data[gananciax10] / 100))) * 10
        preciox25 = (costo * (1 + (self.cleaned_data[gananciax25] / 100))) * 25
        preciox50 = (costo * (1 + (self.cleaned_data[gananciax50] / 100))) * 50
        preciox100 = (costo * (1 + (self.cleaned_data[gananciax100] / 100))) * 100
        preciox1000 = (costo * (1 + (self.cleaned_data[gananciax100] / 100))) * 1000
        return preciox1, preciox10, preciox25, preciox50, preciox100, preciox1000'''

class EditarPreciosBultosForm(forms.ModelForm):
    class Meta:
        model = PrecioBulto
        fields = ['costo_bulto', 'cantidad_bulto', 'precio_bulto', 'ganancia_bulto']

        widgets = {
            #'producto': forms.Select(attrs={'class': 'form-control'}),
            'costo_bulto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cantidad_bulto': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_bulto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ganancia_bulto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }