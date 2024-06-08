from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError, DatabaseError
from .models import AppointmentTickets
from .forms import AppointmentTicketsForm, EditAppointmentTicketsForm, AppointmentTicketStatusForm


def tickets_list(request):
    tickets = AppointmentTickets.objects.all()
    return render(request, 'tickets/tickets.html', {"tickets": tickets})

def ticket_create(request):
    if request.method == "POST":
        form = AppointmentTicketsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'tickets/success.html', {'message': 'Талон успішно створений'})
            except IntegrityError as e:
                if 'нарушает ограничение-проверку \"appointment_tickets_ticket_date_check\"' in str(e):
                    error_message = "Помилка цілісності даних: порушує обмеження-перевірку \"Дата талону\""
                elif 'нарушает ограничение-проверку \"appointment_tickets_ticket_time_check\"' in str(e):
                    error_message = "Помилка цілісності даних: порушує обмеження-перевірку \"Час талону\""
                return render(request, 'tickets/ticket_form.html', {'form': form, 'error_message': error_message})
            except DatabaseError as e:
                # Обробляємо виняток користувача з тригера
                if 'Лікар не може проводити цю процедуру.' in str(e):
                    error_message = "Лікар не може проводити цю процедуру."
                elif 'В обраний день у лікаря вихідний.' in str(e):
                    error_message = "В обраний день у лікаря вихідний."
                elif 'Час запису вже зайнятий. Оберіть інший час.' in str(e):
                    error_message = "Час запису вже зайнятий. Оберіть інший час."
                elif 'Зазначений час не може бути кінцем робочого дня/після кінця робочого дня. Оберіть інший час.' in str(e):
                    error_message = "Зазначений час не може бути кінцем робочого дня/після кінця робочого дня. Оберіть інший час."
                else:
                    error_message = "Помилка бази даних: " + str(e)
                return render(request, 'tickets/ticket_form.html', {'form': form, 'error_message': error_message})
            except Exception as e:
                # Обробляємо будь-які інші винятки
                error_message = "Невідома помилка: " + str(e)
                return render(request, 'tickets/ticket_form.html', {'form': form, 'error_message': error_message})
    else:
        form = AppointmentTicketsForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})

def ticket_detail(request, pk):
    ticket = get_object_or_404(AppointmentTickets, pk=pk)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

def ticket_edit(request, pk):
    ticket = get_object_or_404(AppointmentTickets, pk=pk)

    # Проверяем, была ли отправлена форма для сохранения изменений
    if request.method == 'POST':
        form = EditAppointmentTicketsForm(request.POST, instance=ticket)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'message': 'Талон успішно оновлений'})
            except IntegrityError as e:
                if 'нарушает ограничение-проверку \"appointment_tickets_ticket_date_check\"' in str(e):
                    error_message = "Помилка цілісності даних: порушує обмеження-перевірку \"Дата талону\""
                elif 'нарушает ограничение-проверку \"appointment_tickets_ticket_time_check\"' in str(e):
                    error_message = "Помилка цілісності даних: порушує обмеження-перевірку \"Час талону\""
                return render(request, 'tickets/ticket_edit.html', {'form': form, 'ticket': ticket, 'error_message': error_message})
            except DatabaseError as e:
                # Обрабатываем пользовательское исключение из триггера
                if 'Лікар не може проводити цю процедуру.' in str(e):
                    error_message = "Лікар не може проводити цю процедуру."
                elif 'В обраний день у лікаря вихідний.' in str(e):
                    error_message = "В обраний день у лікаря вихідний."
                elif 'Час запису вже зайнятий. Оберіть інший час.' in str(e):
                    error_message = "Час запису вже зайнятий. Оберіть інший час."
                elif 'Зазначений час не може бути кінцем робочого дня/після кінця робочого дня. Оберіть інший час.' in str(
                        e):
                    error_message = "Зазначений час не може бути кінцем робочого дня/після кінця робочого дня. Оберіть інший час."
                else:
                    error_message = "Помилка бази даних: " + str(e)
                return render(request, 'tickets/ticket_edit.html', {'form': form, 'ticket': ticket, 'error_message': error_message})
            except Exception as e:
                # Обрабатываем любые другие исключения
                error_message = "Невідома помилка: " + str(e)
                return render(request, 'tickets/ticket_edit.html', {'form': form, 'ticket': ticket, 'error_message': error_message})
    else:
        # Если форма не была отправлена, создаем форму с заполненными данными из объекта талона
        form = EditAppointmentTicketsForm(instance=ticket)

    # Отображаем шаблон с формой для редактирования талона
    return render(request, 'tickets/ticket_edit.html', {'form': form, 'ticket': ticket})

def ticket_delete(request, pk):
    ticket = get_object_or_404(AppointmentTickets, pk=pk)

    if request.method == 'POST':
        ticket.delete()
        return redirect('ticket_list')  # Перенаправляем на список талонов после удаления

    return render(request, 'tickets/ticket_delete.html', {'ticket': ticket})

def edit_ticket_status(request, ticket_id):
    ticket = get_object_or_404(AppointmentTickets, pk=ticket_id)
    error_message = None

    if request.method == 'POST':
        form = AppointmentTicketStatusForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
        else:
            error_message = "Помилка збереження статусу талону. Перевірте введені дані."
    else:
        form = AppointmentTicketStatusForm(instance=ticket)

    return render(request, 'registrator/edit_ticket_status.html', {
        'form': form,
        'ticket': ticket,
        'error_message': error_message,
    })


def appointment_ticket_list(request):
    tickets = AppointmentTickets.objects.all()

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        ticket = get_object_or_404(AppointmentTickets, pk=ticket_id)
        form = AppointmentTicketStatusForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('appointment_ticket_list')
    else:
        ticket_forms = [(ticket, AppointmentTicketStatusForm(instance=ticket)) for ticket in tickets]

    return render(request, 'tickets/appointment_ticket_list.html', {
        'ticket_forms': ticket_forms
    })