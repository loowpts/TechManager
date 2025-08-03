from django.contrib import admin
from .models import Computer, Printer, Cartridge, Stock, Movement

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


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'location', 'last_updated']
    list_filter = ['location']
    search_fields = ['item__name', 'location']


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ['get_item_type_display', 'item_id', 'quantity', 'movement_type', 'from_location', 'to_location', 'date_moved', 'moved_by']
    list_filter = ['movement_type', 'date_moved']
    search_fields = ['item_id', 'from_location', 'to_location']

    def get_item_type_display(self, obj):
        return obj.get_item_type_display()
    get_item_type_display.short_description = 'Тип техники'
