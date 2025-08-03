from django.contrib import admin
from .models import Computer, Printer,Cartridge

@admin.register(Computer)
class ComputerAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'location', 'technician', 'status', 'created_at']
    list_filter = ['status', 'location', 'technician']
    search_fields = ['name', 'serial_number', 'location']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    ordering = ['name']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(
                name__icontains=search_term
            ) | self.model.objects.filter(
                serial_number__icontains=search_term
            ) | self.model.objects.filter(
                location__icontains=search_term
            )
        return queryset, use_distinct

@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'location', 'status', 'created_at']
    list_filter = ['status', 'location']
    search_fields = ['name', 'model', 'location']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    ordering = ['name']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            queryset |= self.model.objects.filter(
                name__icontains=search_term
            ) | self.model.objects.filter(
                model__icontains=search_term
            ) | self.model.objects.filter(
                location__icontains=search_term
            )
        return queryset, use_distinct


@admin.register(Cartridge)
class CartridgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'printer_model', 'compatible_cartridge', 'stock_quantity', 'is_connected', 'is_disposed']
    list_filter = ['printer_model', 'is_connected', 'is_disposed']
    search_fields = ['name', 'printer_model__name', 'compatible_cartridge']
