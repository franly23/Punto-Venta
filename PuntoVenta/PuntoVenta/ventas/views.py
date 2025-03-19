import os
import json
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Producto, Egreso, ProductosEgreso, CategoriaProd, CierreCaja, PrecioUnitario, PrecioBulto, PreciosEspeciales, Ofertas
from django.core.paginator import Paginator
from .forms import AddClienteForm, EditarClienteForm, AddProductoForm, EditarProductoForm, AddPreciosUnitariosForm, AddPreciosBultosForm
from django.contrib import messages
from django.views.generic import ListView, View, TemplateView
from django.http import JsonResponse, HttpResponse
from weasyprint.text.fonts import FontConfiguration
from django.template.loader import get_template
from weasyprint import HTML, CSS
from django.conf import settings
from django.templatetags.static import static
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.db.models import Sum
from datetime import date
from django.contrib.auth.models import Permission

# Create your views here.

def ventas_view(request):

    is_jefe = request.user.groups.filter(name="Jefe").exists()

    # Obtener la fecha actual
    hoy = timezone.now().date()
    mes_actual = hoy.month
    anio_actual = hoy.year

    # Determinar el filtro
    filtro = request.GET.get('filtro', 'hoy')  # Por defecto mostramos ventas de hoy

    if filtro == 'hoy':
        ventas = Egreso.objects.filter(fecha_pedido=hoy)
    elif filtro == 'mes':
        ventas = Egreso.objects.filter(fecha_pedido__year=anio_actual, fecha_pedido__month=mes_actual)
    elif filtro == 'anio':
        ventas = Egreso.objects.filter(fecha_pedido__year=anio_actual)
    else:
        ventas = Egreso.objects.all()

    num_ventas = ventas.count()  # Contar el número de ventas

    context = {
        'ventas': ventas,
        'num_ventas': num_ventas,
        'filtro': filtro,
        'is_jefe': is_jefe,
    }

    return render(request, 'ventas.html', context)


def clientes_view(request):
    clientes = Cliente.objects.all()
    form_personal = AddClienteForm()
    form_editar = EditarClienteForm()

    context = {
        'clientes': clientes,
        'form_personal': form_personal,
        'form_editar': form_editar
    }
    return render(request, 'clientes.html', context)


def add_cliente_view(request):
    if request.POST:
        form = AddClienteForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                form.save()
            except:
                messages(request, "Error al guardar el cliente")
                return redirect('Clientes')
    return redirect('Clientes')


def edit_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_editar'))
        form = EditarClienteForm(
            request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
    return redirect('Clientes')


def delete_cliente_view(request):
    if request.POST:
        cliente = Cliente.objects.get(pk=request.POST.get('id_personal_eliminar'))
        cliente.delete()

    return redirect('Clientes')


def productos_view(request):
    
    is_jefe = request.user.groups.filter(name="Jefe").exists()
    can_add_product = request.user.has_perm('ventas.can_add_product')
    can_edit_product = request.user.has_perm('ventas.can_edit_product')
    can_delete_product = request.user.has_perm('ventas.can_delete_product')

    filtro = request.GET.get('filtro')
    if filtro:
        productos = Producto.objects.filter(categoria_id=filtro)
    else:
        productos = Producto.objects.select_related('precioU').all()

    


    paginator = Paginator(productos, 20)  # Número de productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    form_add = AddProductoForm()
    form_preciosU = AddPreciosUnitariosForm()
    form_preciosB = AddPreciosBultosForm()
    form_editar = EditarProductoForm()
    categoria = CategoriaProd.objects.all()
    precioU = PrecioUnitario.objects.all()

    '''productos_info = []
    for producto in productos:
        precios = {}
        for cantidad in producto.formas_venta.all():
            precios[cantidad.cantidad] = producto.calcular_precio_venta(cantidad)
        productos_info.append({'producto': producto, 'precios': precios})'''
    

    context = {
        'productos': productos,
        'form_add': form_add,
        'form_editar': form_editar,
        'categoria': categoria,
        'is_jefe': is_jefe,
        'can_add_product': can_add_product,
        'can_edit_product': can_edit_product,
        'can_delete_product': can_delete_product,
        #'productos_info': productos_info,
        'form_preciosU': form_preciosU,
        'form_preciosB': form_preciosB,
        'precioU': precioU,

    }
    return render(request, 'productos.html', context)
    


def add_producto_view(request):
    
    if request.POST:

        form = AddProductoForm(request.POST, request.FILES)
        unidades = AddPreciosUnitariosForm(request.POST)
        bultos = AddPreciosBultosForm(request.POST)

        if form.is_valid():
            producto = form.save(commit=False)
            try:
                producto.save()
                if unidades.is_valid():
                    unidades = unidades.save(commit=False)
                    unidades.producto = producto
                    unidades.save()

                if bultos.is_valid():
                    bultos = bultos.save(commit=False)
                    bultos.producto = producto
                    bultos.save()

                messages.success(request, "Producto y precios guardados exitosamente.")
                return redirect('Productos')
            except:
                messages.error(request, "Hubo un error al guardar el producto o los precios.")
                return redirect('Productos')
        else:
            messages.error(request, "Error al guardar el producto")
            return redirect('Productos')
    else:
        form = AddProductoForm()
        unidades = AddPreciosUnitariosForm()   
        bultos = AddPreciosBultosForm()     
        
    return render(request, 'productos.html', {'form': form, 'unidades': unidades, 'bultos': bultos})



def edit_producto_view(request):
    if request.method == "POST":
        producto = get_object_or_404(Producto, pk=request.POST.get('id_producto_editar'))
        form = EditarProductoForm(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            form.save()
            return redirect('Productos')
    return redirect('Productos')


def delete_producto_view(request):
    if request.POST:
        producto = Producto.objects.get(pk=request.POST.get('id_producto_eliminar'))
        producto.delete()

    return redirect('Productos')


class add_ventas(ListView):
    template_name = 'add_ventas.html'
    model = Egreso

    def dispatch(self, request,*args,**kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request,*ars, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'autocomplete':
                data = []
                for i in Producto.objects.filter(descripcion__icontains=request.POST["term"])[0:10]:
                    item = i.toJSON()
                    item['value'] = i.descripcion
                    data.append(item)
            elif action == 'save':
                efectivo = float(request.POST.get("efectivo", 0))
                tarjeta = float(request.POST.get("tarjeta", 0))
                transferencia = float(request.POST.get("transferencia", 0))
                if efectivo <= 0 and tarjeta <= 0 and transferencia <= 0:
                    raise Exception("Debe ingresar al menos un método de pago válido.")
                
                metodos_pago = []
                if efectivo > 0:
                    metodos_pago.append("Efectivo")
                if tarjeta > 0:
                    metodos_pago.append("Tarjeta")
                if transferencia > 0:
                    metodos_pago.append("Transferencia")
                metodo_pago = ", ".join(metodos_pago)  # Ejemplo: "Efectivo, Tarjeta"



                
                total_pagado = efectivo + tarjeta + transferencia
                fecha = request.POST["fecha"]
                id_cliente = int(request.POST["id_cliente"])
                cliente_obj = Cliente.objects.get(pk=id_cliente)
                datos = json.loads(request.POST["verts"])
                total_venta = float(datos["total"])
                comentarios = request.POST["comentarios"]
                ticket_num = int(request.POST["ticket"])
                if ticket_num == 1:
                    ticket = True
                else:
                    ticket = False
                desglosar_iva_num = int(request.POST["desglosar"])
                if desglosar_iva_num == 0:
                    desglosar_iva = False
                elif desglosar_iva_num == 1:
                    desglosar_iva = True
                
                vendedor_id = request.POST.get("vendedor", None)
                if vendedor_id:
                    vendedor = User.objects.get(pk=int(vendedor_id))
                else:
                    vendedor = request.user

                
                nueva_venta = Egreso(fecha_pedido = fecha, cliente = cliente_obj, total = total_venta, comentarios = comentarios, ticket = ticket, desglosar = desglosar_iva, vendedor=vendedor, efectivo = efectivo, transferencia = transferencia, tarjeta = tarjeta, metodo_pago = metodo_pago)
                nueva_venta.save()

                for producto in datos["items"]:
                    producto_obj = Producto.objects.get(pk=producto["id"])
                    cantidad = float(producto["cantidad"])
                    precio = float(producto["precio"])
                    subtotal = cantidad * precio
                    iva = subtotal * 0.21
                    total_producto = subtotal + iva

                    ProductosEgreso.objects.create(
                        egreso=nueva_venta,
                        producto=producto_obj,
                        cantidad=cantidad,
                        precio=precio,
                        subtotal=subtotal,
                        iva=iva,
                        total=total_producto
                    )

                    # Actualizar el stock
                    producto_obj.cantidad -= cantidad
                    producto_obj.save()
                
                # Crear registros de pago
                if efectivo > 0:
                    Pago.objects.create(venta=nueva_venta, metodo="Efectivo", monto=efectivo)
                if tarjeta > 0:
                    Pago.objects.create(venta=nueva_venta, metodo="Tarjeta", monto=tarjeta)
                if transferencia > 0:
                    Pago.objects.create(venta=nueva_venta, metodo="Transferencia", monto=transferencia)

                data = {"success": True, "message": "Venta registrada correctamente."}


            else:
                data['error'] = "Ha ocurrido un error"
        except Exception as e:
            data['error'] = str(e)
            print(e)

        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productos_lista"] = Producto.objects.all()
        context["clientes_lista"] = Cliente.objects.all()
        return context


class delete_venta_view(View):
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            if not request.user.groups.filter(name='jefe').exists():
                data['error'] = "No tienes permisos para eliminar ventas"
                return JsonResponse(data)
                
            body = json.loads(request.body)
            venta_id = body.get("id")
            venta = get_object_or_404(Egreso, id=venta_id)
            venta.delete()
            data['message'] = "Venta eliminada correctamente"
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


def export_pdf_view(request, id, iva):
    from django.http import Http404
    try:
        venta = Egreso.objects.get(pk=float(id))
    except Egreso.DoesNotExist:
        raise Http404("Venta no encontrada")

    #print(id)
    template = get_template("ticket.html")
    #print(id)
    subtotal = 0 
    iva_suma = 0 

    datos = ProductosEgreso.objects.filter(egreso=venta)
    for i in datos:
        subtotal += float(i.subtotal)
        iva_suma += float(i.iva)

    '''venta = Egreso.objects.get(pk=float(id))
    datos = ProductosEgreso.objects.filter(egreso=venta)
    for i in datos:
        subtotal = subtotal + float(i.subtotal)
        iva_suma = iva_suma + float(i.iva)'''

    empresa = "Mi empresa S.A. De C.V"
    context ={
        'num_ticket': id,
        'iva': iva,
        'fecha': venta.fecha_pedido,
        'cliente': venta.cliente.nombre,
        'items': datos, 
        'total': venta.total, 
        'empresa': empresa,
        'comentarios': venta.comentarios,
        'subtotal': subtotal,
        'iva_suma': iva_suma,
    }
    html_template = template.render(context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename=ticket.pdf"
    #HTML(string=html_template).write_pdf(target="ticket.pdf", stylesheets=[CSS(css_url)])
    css_url = static('index/css/bootstrap.min.css')

    font_config = FontConfiguration()
    HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(target=response, font_config=font_config,stylesheets=[CSS(css_url)])

    return response


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('Ventas')


class CustomLogoutView(LogoutView):
    
    next_page = reverse_lazy('login')


class cierre_view(TemplateView):
    template_name = "cierre.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = date.today()

        # Filtrar ventas por método de pago
        ventas_efectivo = Egreso.objects.filter(fecha_pedido=hoy, metodo_pago='EF').aggregate(total=Sum('total'))['total'] or 0
        ventas_transferencia = Egreso.objects.filter(fecha_pedido=hoy, metodo_pago='TR').aggregate(total=Sum('total'))['total'] or 0
        ventas_tarjeta = Egreso.objects.filter(fecha_pedido=hoy, metodo_pago='TJ').aggregate(total=Sum('total'))['total'] or 0

        # Total del día
        total_dia = ventas_efectivo + ventas_transferencia + ventas_tarjeta

        # Agregar al contexto
        context['ventas_efectivo'] = ventas_efectivo
        context['ventas_transferencia'] = ventas_transferencia
        context['ventas_tarjeta'] = ventas_tarjeta
        context['total_dia'] = total_dia

        return context


def historial_cierres_view(request):
    cierres = CierreCaja.objects.all().order_by('-fecha')
    context = {'cierres': cierres}
    return render(request, 'cierre.html', context)


class GuardarCierreView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        cierre = CierreCaja.objects.create(
            fecha=date.today(),
            total_efectivo=data['ventasEfectivo'],
            total_transferencia=data['ventasTransferencia'],
            total_tarjeta=data['ventasTarjeta'],
            efectivo_caja=data['efectivoCaja'],
            nota=data['nota'],
            total_dia=data['total']
        )
        return JsonResponse({'message': 'Cierre guardado exitosamente!'})







def edit_producto_view(request):
    if request.method == "POST":
        producto = get_object_or_404(Producto, pk=request.POST.get('id_producto_editar'))
        form = EditarProductoForm(request.POST, request.FILES, instance=producto)

        if form.is_valid():
            try:
                producto = form.save()

                # Actualizar precios unitarios si el tipo es unidad
                if producto.tipo == 'unidad':
                    precios_unitarios = PreciosUnitarios.objects.filter(producto=producto).first()
                    if precios_unitarios:
                        precios_unitarios.costo = request.POST.get('costo_unidad', 0)
                        precios_unitarios.descuento = request.POST.get('descuento_unidad', 0)
                        precios_unitarios.cantidad = request.POST.get('cantidad_unidad', 1)
                        precios_unitarios.save()

                # Actualizar precios por bulto si el tipo es bulto
                elif producto.tipo == 'bulto':
                    precios_bulto = PreciosBultos.objects.filter(producto=producto).first()
                    if precios_bulto:
                        precios_bulto.costo_bulto = request.POST.get('costo_bulto', 0)
                        precios_bulto.cantidad_por_bulto = request.POST.get('cantidad_bulto', 0)
                        precios_bulto.precio_final = request.POST.get('precio_bulto', 0)
                        precios_bulto.save()

                messages.success(request, "Producto editado correctamente.")
                return redirect('Productos')
            except Exception as e:
                messages.error(request, f"Error al editar el producto: {e}")
                return redirect('Productos')

    return redirect('Productos')