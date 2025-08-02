from django import forms
from .models import Computer, Printer

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
