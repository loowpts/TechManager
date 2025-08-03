from django import forms
from .models import Computer, Printer, Cartridge, Stock, Movement

class ComputerForm(forms.ModelForm):
    class Meta:
        model = Computer
        fields = ['name', 'serial_number', 'location', 'technician', 'status']
        labels = {
            'name': 'Название',
            'serial_number': 'Серийный номер',
            'location': 'Кабинет',
            'technician': 'Ответственный',
            'status': 'Статус',
        }
        widgets = {
            'status': forms.Select(),
        }

class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ['name', 'model', 'location', 'status']
        labels = {
            'name': 'Название',
            'model': 'Модель',
            'location': 'Кабинет',
            'status': 'Статус',
        }
        widgets = {
            'status': forms.Select(),
        }


class CartridgeConnectForm(forms.ModelForm):
    class Meta:
        model = Cartridge
        fields = ['is_connected']
        labels = {
            'is_connected': 'Подключить картридж',
        }


class CartridgeAddForm(forms.ModelForm):
    class Meta:
        model = Cartridge
        fields = ['name', 'printer_model', 'compatible_cartridge', 'stock_quantity']
        labels = {
            'name': 'Название картриджа',
            'printer_model': 'Модель принтера',
            'compatible_cartridge': 'Совместимый картридж',
            'stock_quantity': 'Количество на складе',
        }


class CartridgeManageForm(forms.ModelForm):
    action = forms.ChoiceField(choices=[('return', 'Вернуть на склад'), ('dispose', 'Просрочено')], required=False, widget=forms.RadioSelect)

    class Meta:
        model = Cartridge
        fields = ['is_connected', 'is_disposed']
        labels = {
            'is_connected': 'Подключён',
            'is_disposed': 'Отправлен в утиль',
        }


from django import forms
from .models import Stock, Movement, Computer, Printer

class StockAddForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item', 'quantity', 'location']
        labels = {
            'item': 'Элемент',
            'quantity': 'Количество',
            'location': 'Местоположение',
        }

class MovementForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=Computer.objects.all(), label='Техника', required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'item_type' in self.data:
            item_type = self.data.get('item_type')
            if item_type == 'computer':
                self.fields['item'].queryset = Computer.objects.all()
            elif item_type == 'printer':
                self.fields['item'].queryset = Printer.objects.all()
        elif self.instance.pk and self.instance.item_type:
            if self.instance.item_type == 'computer':
                self.fields['item'].queryset = Computer.objects.all()
            elif self.instance.item_type == 'printer':
                self.fields['item'].queryset = Printer.objects.all()
        self.fields['quantity'].widget = forms.HiddenInput()
        if 'item' in self.data:
            item_id = self.data.get('item')
            if item_id:
                try:
                    item = Computer.objects.get(id=item_id)
                    self.initial['from_location'] = item.location
                except (Computer.DoesNotExist, ValueError):
                    pass

    class Meta:
        model = Movement
        fields = ['item_type', 'item', 'quantity', 'movement_type', 'from_location', 'to_location']
        labels = {
            'item_type': 'Тип техники',
            'item': 'Техника',
            'quantity': 'Количество',
            'movement_type': 'Тип перемещения',
            'from_location': 'Откуда',
            'to_location': 'Куда',
        }
