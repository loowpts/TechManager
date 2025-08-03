from django.db import models
from django.contrib.auth.models import User


class Computer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    serial_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        verbose_name='Серийный номер'
        )
    location = models.CharField(max_length=50, verbose_name='Кабинет')
    technician = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Ответственный'
        )
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Активен'), ('inactive', 'Неактивен')],
        default='active',
        verbose_name="Статус"
        )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self) -> str:
        return f'{self.name} - ({self.serial_number})'
    
    class Meta:
        verbose_name = 'Компьютер'
        verbose_name_plural = 'Компьютеры'


class Printer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    model = models.CharField(max_length=100, verbose_name="Модель")
    location = models.CharField(max_length=50, verbose_name="Кабинет")
    status = models.CharField(
        max_length=20,
        choices=[('active', 'Активен'), ('inactive', 'Неактивен')],
        default='active',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
        )

    def __str__(self):
        return f"{self.name} ({self.model})"

    class Meta:
        verbose_name = "Принтер"
        verbose_name_plural = "Принтеры"


class Cartridge(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название картриджа')
    printer_model = models.ForeignKey(Printer, on_delete=models.CASCADE, verbose_name='Модель принтера')
    compatible_cartridge = models.CharField(max_length=100, verbose_name='Совместимый картридж')
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    is_connected = models.BooleanField(default=False, verbose_name='Подключен к принтеру')
    is_disposed = models.BooleanField(default=False, verbose_name='Отправлен в утиль')

    def __str__(self):
        return f"{self.name} для {self.printer_model}"

    class Meta:
        verbose_name = 'Картридж'
        verbose_name_plural = 'Картриджи'


from django.db import models
from django.contrib.auth.models import User
from .models import Printer, Cartridge, Computer

class Stock(models.Model):
    item = models.ForeignKey(Cartridge, on_delete=models.CASCADE, verbose_name='Элемент')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    location = models.CharField(max_length=100, verbose_name='Местоположение')
    last_updated = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')

    def __str__(self):
        return f"{self.item.name} - {self.quantity} шт. в {self.location}"

    class Meta:
        verbose_name = 'Запас'
        verbose_name_plural = 'Запасы'

class Movement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'Поступление'),
        ('out', 'Выбытие'),
        ('transfer', 'Перемещение'),
    ]
    item_type = models.CharField(max_length=20, choices=[('computer', 'Компьютер'), ('printer', 'Принтер')], verbose_name='Тип техники')
    item_id = models.PositiveIntegerField(verbose_name='ID техники')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES, verbose_name='Тип перемещения')
    from_location = models.CharField(max_length=100, verbose_name='Откуда', blank=True, null=True)
    to_location = models.CharField(max_length=100, verbose_name='Куда', blank=True, null=True)
    date_moved = models.DateTimeField(auto_now_add=True, verbose_name='Дата перемещения')
    moved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Кем перемещено')
    is_disposed = models.BooleanField(default=False, verbose_name='Отправлено в утиль')

    def __str__(self):
        return f"{self.get_item_type_display()} (ID: {self.item_id}) - {self.movement_type}"

    class Meta:
        verbose_name = 'Перемещение'
        verbose_name_plural = 'Перемещения'

    def get_item(self):
        if self.item_type == 'computer':
            return Computer.objects.get(id=self.item_id)
        elif self.item_type == 'printer':
            return Printer.objects.get(id=self.item_id)
        return None
