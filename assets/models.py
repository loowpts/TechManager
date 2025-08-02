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
