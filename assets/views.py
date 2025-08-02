from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Computer, Printer
from .forms import ComputerForm, PrinterForm
from django.utils import timezone


@login_required
def index_view(request):
    return render(request, 'assets/index.html', {
        'current_datetime': timezone.now().strftime('%d %B %Y, %H:%M %Z')
    })


@login_required
def computer_list(request):
    query = request.GET.get('q', '')
    computers = Computer.objects.all()
    if query:
        computers = computers.filter(
            Q(name__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(location_icontains=query)
        )
    return render(request, 'assets/computer_list.html', {
        'computers': computers,
        'query': query
    })


@login_required
def computer_detail(request, pk):
    computer = get_object_or_404(Computer, pk=pk)
    return render(request, 'assets/computer_detail.html', {'computer': computer})


@login_required
def computer_create(request):
    if request.method == 'POST':
        form = ComputerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Комьютер успешно добавлен')
            return redirect('assets:computer_list')
        else:
            messages.warning(request, 'Исправьте ошибки в форме!')
    else:
        form = ComputerForm()
    return render(request, 'assets/computer_form.html', {'form': form})


@login_required
def computer_update(request, pk):
    computer = get_object_or_404(Computer, pk=pk)
    if request.method == 'POST':
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            form.save
            messages.success(request, 'Данные успешно обновлены!')
            return redirect('assets:computer_list')
        else:
            messages.warning(request, 'Исправьте ошибки в форме!')
    else:
        form = ComputerForm(instance=computer)
    return redirect(request, 'users/computer_form.html', {
        'form': form,
        'title': 'Редактировать компьютер'
    })


@login_required
def computer_delete(request, pk):
    computer = get_object_or_404(Computer, pk=pk)
    if request.method == 'POST':
        computer.delete()
        messages.success(request, 'Компьютер удален!')
        return redirect('assets:computer_list')
    return render(request, 'assets/computer_confirm_delete.html', {'computer': computer})


@login_required
def printer_list(request):
    query = request.GET.get('q', '')
    printers = Printer.objects.all()
    if query:
        printers = printers.filter(
        Q(name__icontains=query) |
        Q(model__icontains=query) |
        Q(location__icontains=query)
        )
    return render(request, 'assets/printer_list.html', {
        'printers': printers,
        'query':  query,
    })


@login_required
def printer_detail(request, pk):
    printer = get_object_or_404(Printer, pk=pk)
    return render(request, 'assets/printer_detail.html', {'printer': printer})


@login_required
def printer_create(request):
    if request.method == 'POST':
        form = PrinterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Принтер успешно добавлен')
            return redirect('assets:printer_list')
        else:
            messages.warning(request, 'Исправьте ошибки в форме!')
    else:
        form = PrinterForm()
    return render(request, 'assets/printer_form.html', {'form': form, 'title': 'Добавить принтер'})


@login_required
def printer_update(request, pk):
    printer = get_object_or_404(Printer, pk=pk)
    if request.method == 'POST':
        form = PrinterForm(request.POST, instance=printer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно обновлены')
            return redirect('assets:printer_list')
        else:
            messages.warning(request, 'Исправьте ошибки в форме!')
    else:
        form = PrinterForm(instance=printer)
    return render(request, 'assets/printer_form.html', {'form': form, 'title': 'Редактировать принтер'})


@login_required
def printer_delete(request, pk):
    printer = get_object_or_404(Printer, pk=pk)
    if request.method == 'POST':
        printer.delete()
        messages.success(request, 'Принтер успешно удален!')
    return render(request, 'assets/printer_confirm_delete.html', {'printer': printer})
