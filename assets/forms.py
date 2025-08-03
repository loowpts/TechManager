from django import forms
from .models import Computer, Printer, Cartridge

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
