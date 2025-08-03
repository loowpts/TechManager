from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('computers/', views.computer_list, name='computer_list'),
    path('computers/<int:pk>/', views.computer_detail, name='computer_detail'),
    path('computers/add/', views.computer_create, name='computer_create'),
    path('computers/<int:pk>/edit/', views.computer_update, name='computer_edit'),
    path('computers/<int:pk>/delete/', views.computer_delete, name='computer_delete'),
    path('printers/', views.printer_list, name='printer_list'),
    path('printers/<int:pk>/', views.printer_detail, name='printer_detail'),
    path('printer/<int:printer_id>/', views.printer_detail, name='printer_detail'),
    path('cartridge/<int:printer_id>/', views.cartridge_list_view, name='cartridge_list'),
    path('cartridge/', views.cartridge_list_view, name='cartridge_list'),
    path('cartridge/add/', views.add_cartridge, name='add_cartridge'),
    path('cartridge/connect/<int:cartridge_id>/', views.connect_cartridge, name='connect_cartridge'),
    path('printers/add/', views.printer_create, name='printer_create'),
    path('printers/<int:pk>/edit/', views.printer_update, name='printer_edit'),
    path('printers/<int:pk>/delete/', views.printer_delete, name='printer_delete'),
]
