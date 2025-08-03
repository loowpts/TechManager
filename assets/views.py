from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Computer, Printer, Cartridge, Stock, Movement
from .forms import ComputerForm, PrinterForm, CartridgeConnectForm, CartridgeAddForm, CartridgeManageForm, StockAddForm, MovementForm

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
            Q(location__icontains=query)
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
            messages.success(request, 'Компьютер успешно добавлен')
            return redirect('assets:computer_list')
        else:
            messages.warning(request, 'Исправьте ошибки в форме.')
    else:
        form = ComputerForm()
    return render(request, 'assets/computer_form.html', {'form': form})

@login_required
def computer_update(request, pk):
    computer = get_object_or_404(Computer, pk=pk)
    if request.method == 'POST':
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно обновлены.')
            return redirect('assets:computer_list')
        else:
            messages.warning(request, 'Исправьте ошибки в форме.')
    else:
        form = ComputerForm(instance=computer)
    return render(request, 'assets/computer_form.html', {
        'form': form,
        'title': 'Редактировать компьютер'
    })

@login_required
def computer_delete(request, pk):
    computer = get_object_or_404(Computer, pk=pk)
    if request.method == 'POST':
        computer.delete()
        messages.success(request, 'Компьютер удалён.')
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
        'query': query,
    })

@login_required
def printer_detail(request, printer_id):
    printer = get_object_or_404(Printer, id=printer_id)
    connected_cartridge = Cartridge.objects.filter(printer_model=printer, is_connected=True, is_disposed=False).first()
    available_cartridges = Cartridge.objects.filter(printer_model=printer, is_connected=False, is_disposed=False)

    if request.method == 'POST':
        form = CartridgeManageForm(request.POST, instance=connected_cartridge if connected_cartridge else None)
        if form.is_valid():
            cartridge = form.save(commit=False)
            action = request.POST.get('action')
            if action == 'return':
                cartridge.is_connected = False
                cartridge.stock_quantity += 1
                cartridge.save()
                messages.success(request, f"Картридж {cartridge.name} возвращён на склад.")
            elif action == 'dispose':
                cartridge.is_connected = False
                cartridge.is_disposed = True
                cartridge.stock_quantity = 0
                cartridge.save()
                messages.success(request, f"Картридж {cartridge.name} отправлен в утиль.")
            return redirect('assets:printer_detail', printer_id=printer.id)
    else:
        form = CartridgeManageForm(instance=connected_cartridge if connected_cartridge else None)

    return render(request, 'assets/printer_detail.html', {
        'printer': printer,
        'connected_cartridge': connected_cartridge,
        'available_cartridges': available_cartridges,
        'form': form
    })

@login_required
def printer_create(request):
    if request.method == 'POST':
        form = PrinterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Принтер успешно добавлен.')
            return redirect('assets:printer_list')
        else:
            messages.warning(request, 'Исправьте ошибки в форме.')
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
            messages.success(request, 'Данные успешно обновлены.')
            return redirect('assets:printer_list')
        else:
            messages.warning(request, 'Исправьте ошибки в форме.')
    else:
        form = PrinterForm(instance=printer)
    return render(request, 'assets/printer_form.html', {'form': form, 'title': 'Редактировать принтер'})

@login_required
def printer_delete(request, pk):
    printer = get_object_or_404(Printer, pk=pk)
    if request.method == 'POST':
        printer.delete()
        messages.success(request, 'Принтер успешно удалён.')
        return redirect('assets:printer_list')
    return render(request, 'assets/printer_confirm_delete.html', {'printer': printer})

@login_required
def cartridge_list_view(request, printer_id=None):
    if printer_id:
        printer = get_object_or_404(Printer, id=printer_id)
        cartridges = Cartridge.objects.filter(printer_model=printer)
    else:
        cartridges = Cartridge.objects.all()
    return render(request, 'assets/cartridge_list.html', {
        'cartridges': cartridges,
        'printers': Printer.objects.all(),
        'selected_printer_id': printer_id
    })

@login_required
def connect_cartridge(request, cartridge_id):
    cartridge = get_object_or_404(Cartridge, id=cartridge_id)
    if request.method == 'POST':
        form = CartridgeConnectForm(request.POST, instance=cartridge)
        if form.is_valid() and cartridge.stock_quantity > 0:
            cartridge = form.save(commit=False)
            cartridge.is_connected = True
            cartridge.stock_quantity -= 1
            cartridge.save()
            messages.success(request, f"Картридж {cartridge.name} подключён к принтеру {cartridge.printer_model.name}.")
            return redirect('assets:printer_detail', printer_id=cartridge.printer_model.id)
        else:
            messages.error(request, "Недостаточно картриджей на складе или ошибка формы.")
    else:
        form = CartridgeConnectForm(instance=cartridge)
    return render(request, 'assets/connect_cartridge.html', {'form': form, 'cartridge': cartridge})

@login_required
def add_cartridge(request):
    if request.method == 'POST':
        form = CartridgeAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Новый картридж добавлен успешно.")
            return redirect('assets:cartridge_list')
        else:
            messages.error(request, "Ошибка при добавлении картриджа. Проверьте данные.")
    else:
        form = CartridgeAddForm()
    return render(request, 'assets/add_cartridge.html', {'form': form})

@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'assets/stock_list.html', {'stocks': stocks})

@login_required
def add_stock(request):
    if request.method == 'POST':
        form = StockAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запас добавлен успешно.")
            return redirect('assets:stock_list')
        else:
            messages.error(request, "Ошибка при добавлении запаса. Проверьте данные.")
    else:
        form = StockAddForm()
    return render(request, 'assets/add_stock.html', {'form': form})

@login_required
def movement_list(request):
    movements = Movement.objects.all().order_by('-date_moved')
    return render(request, 'assets/movement_list.html', {'movements': movements})

@login_required
def add_movement(request):
    if request.method == 'POST':
        form = MovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            item = form.cleaned_data['item']
            if item:
                if isinstance(item, Computer):
                    movement.item_type = 'computer'
                elif isinstance(item, Printer):
                    movement.item_type = 'printer'
                movement.item_id = item.id
            if movement.movement_type == 'in':
                movement.save()
            elif movement.movement_type == 'out':
                if movement.item_type == 'computer':
                    Computer.objects.get(id=movement.item_id)
                elif movement.item_type == 'printer':
                    Printer.objects.get(id=movement.item_id)
                movement.is_disposed = True
                movement.save()
            elif movement.movement_type == 'transfer':
                if movement.item_type == 'computer':
                    Computer.objects.get(id=movement.item_id)
                elif movement.item_type == 'printer':
                    Printer.objects.get(id=movement.item_id)
                movement.save()
            messages.success(request, f"Перемещение {movement.movement_type} для {movement.get_item_type_display()} (ID: {movement.item_id}) выполнено.")
            return redirect('assets:movement_list')
        else:
            messages.error(request, "Ошибка при добавлении перемещения. Проверьте данные.")
    else:
        form = MovementForm()
    return render(request, 'assets/add_movement.html', {'form': form})
