from django.urls import path
from. import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.ventas_view, name='Ventas'),
    path('clientes/', views.clientes_view, name='Clientes'),
    path('add_cliente/', views.add_cliente_view, name='AddCliente'),
    path('edit_cliente/', views.edit_cliente_view, name='EditCliente'),
    path('delete_cliente/', views.delete_cliente_view, name='DeleteCliente'),
    path('productos/', views.productos_view, name='Productos'),
    path('add_producto/', views.add_producto_view, name='AddProducto'),
    path('edit_producto/', views.edit_producto_view, name='EditProduct'),
    path('delete_producto/', views.delete_producto_view, name='DeleteProducto'),
    path('add_venta/',views.add_ventas.as_view(), name='AddVenta'),
    path('export/', views.export_pdf_view, name="ExportPDF" ),
    path('export/<id>/<iva>', views.export_pdf_view, name="ExportPDF" ),
    path('delete_venta/', views.delete_venta_view.as_view(), name='DeleteVenta'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('cierre/',views.cierre_view.as_view(), name='Cierre'),
    path('guardar_cierre/', views.GuardarCierreView.as_view(), name='guardar_cierre'),
]
