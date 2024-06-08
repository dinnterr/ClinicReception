from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError, DatabaseError, connection
from .models import MedicalCards
from .forms import MedicalCardsForm, MedicalCardSearchForm, DeliveryForm, RemoveForm, ArchiveForm, \
    MedicalCardSearchSt, AgeAppointmentForm
import logging
from matplotlib import use as matplotlib_use

logger = logging.getLogger(__name__)

# Отключаем использование Tkinter
matplotlib_use('Agg')
def medcards_list(request):
    medcards = MedicalCards.objects.all()
    return render(request, 'medicalcards/medcards.html', {"medcards": medcards})


def medcard_create(request):
    if request.method == "POST":
        form = MedicalCardsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'medicalcards/success.html', {'message': 'Медична карта успішно створена'})
            except IntegrityError as e:
                if 'medical_cards_birth_date_check' in str(e):
                    error_message = "Помилка цілісності даних: Дата не може бути в майбутньому."
                else:
                    error_message = "Помилка цілісності даних: " + str(e)
                return render(request, 'medicalcards/medcard_form.html', {'form': form, 'error_message': error_message})
            except DatabaseError as e:
                error_message = "Помилка бази даних: " + str(e)
                return render(request, 'medicalcards/medcard_form.html', {'form': form, 'error_message': error_message})
            except Exception as e:
                # Обрабатываем любые другие исключения
                error_message = "Невідома помилка: " + str(e)
                return render(request, 'medicalcards/medcard_form.html', {'form': form, 'error_message': error_message})
    else:
        form = MedicalCardsForm(request.POST)
    return render(request, 'medicalcards/medcard_form.html', {'form': form})

def medcard_detail(request, pk):
    medcard = get_object_or_404(MedicalCards, pk=pk)
    return render(request, 'medicalcards/medcard_detail.html', {'medcard': medcard, 'show_all_fields': True})

def medcard_edit(request, pk):
    medcard = get_object_or_404(MedicalCards, pk=pk)
    if request.method == 'POST':
        form = MedicalCardsForm(request.POST, instance=medcard)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'medicalcards/medcard_detail.html',
                              {'medcard': medcard, 'message': 'Медичну карту успішно оновлено', 'show_all_fields': True})
            except IntegrityError as e:
                if 'medical_cards_birth_date_check' in str(e):
                    error_message = "Помилка цілісності даних: Дата не може бути в майбутньому."
                else:
                    error_message = "Помилка цілісності даних: " + str(e)
                return render(request, 'medicalcards/medcard_edit.html',
                              {'form': form, 'medcard': medcard, 'error_message': error_message})
            except DatabaseError as e:
                error_message = "Помилка бази даних: " + str(e)
                return render(request, 'medicalcards/medcard_edit.html',
                              {'form': form, 'medcard': medcard, 'error_message': error_message})
            except Exception as e:
                # Обрабатываем любые другие исключения
                error_message = "Невідома помилка: " + str(e)
                return render(request, 'medicalcards/medcard_edit.html',
                              {'form': form, 'medcard': medcard, 'error_message': error_message})
    else:
        # Если форма не была отправлена, создаем форму с заполненными данными из объекта талона
        form = MedicalCardsForm(instance=medcard)
        # Отображаем шаблон с формой для редактирования талона
    return render(request, 'medicalcards/medcard_edit.html', {'form': form, 'medcard': medcard})

def medcard_delete(request, pk):
    medcard = get_object_or_404(MedicalCards, pk=pk)

    if request.method == 'POST':
        try:
            medcard.delete()
            return redirect('medcards_list')  # Перенаправляем на список талонов после удаления
        except IntegrityError as e:
            if "нарушает ограничение внешнего ключа" in str(e):
                error_message = "Помилка цілісності даних: На медкарту даного пацієнта є оформлені талони. " \
                                "Спочатку видаліть талони."
            else:
                error_message = "Помилка цілісності даних: " + str(e)
            return render(request, 'medicalcards/medcard_delete.html',
                          {'medcard': medcard, 'error_message': error_message})
        except Exception as e:
            # Обрабатываем любые другие исключения
            error_message = "Невідома помилка: " + str(e)
            return render(request, 'medicalcards/medcard_delete.html',
                          {'medcard': medcard, 'error_message': error_message})

    return render(request, 'medicalcards/medcard_delete.html', {'medcard': medcard})


def search_medical_card(request):
    search_error_message = None
    if request.method == 'POST':
        form_search = MedicalCardSearchForm(request.POST)
        if form_search.is_valid():
            medcard_id = form_search.cleaned_data['medcard_id']
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM search_patient(%s)", [medcard_id])
                medcard = cursor.fetchone()
                if medcard:
                    return render(request, 'medicalcards/medcard_detail.html',
                                  {'medcard': medcard, 'message': f'Медичну карту № {medcard_id} знайдено'})
                else:
                    search_error_message = f"Медичну карту з № {medcard_id} не знайдено."
                    return render(request, 'medicalcards/search_medcard.html',
                              {'form_search': form_search, 'search_error_message': search_error_message})
    else:
        form_search = MedicalCardSearchForm()

    return render(request, 'medicalcards/search_medcard.html', {'form_search': form_search, 'search_error_message': search_error_message})


def edit_status(request):
    medcards = MedicalCards.objects.all()
    return render(request, 'medicalcards/medcard_edit_status.html', {"medcards": medcards})


def deliver_medcard(request):
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            ticket_id = form.cleaned_data['ticket_id']
            new_status = form.cleaned_data['new_status']

            with connection.cursor() as cursor:
                # Обновление статуса талона
                cursor.execute("UPDATE appointment_tickets SET card_status = %s WHERE ticket_id = %s",
                               [new_status, ticket_id])

            return render(request, 'medicalcards/success_delivery.html', {'message': 'Медична карта успішно доставлена'})  # Редирект на страницу успеха
    else:
        form = DeliveryForm()

    return render(request, 'medicalcards/deliver_medcard.html', {'form': form})


def remove_medcard(request):
    if request.method == 'POST':
        form = RemoveForm(request.POST)
        if form.is_valid():
            medcard_id = form.cleaned_data['medcard_id']
            new_status = form.cleaned_data['new_status']

            with connection.cursor() as cursor:
                # Обновление статуса талона
                cursor.execute("UPDATE medical_cards SET status = %s WHERE medcard_id = %s",
                               [new_status, medcard_id])

            return render(request, 'medicalcards/success_delivery.html',
                          {'message': 'Медична карта успішно вилучена'})  # Редирект на страницу успеха
    else:
        form = RemoveForm()

    return render(request, 'medicalcards/medcard_status_remove.html', {'form': form})

def archive_medcard(request):
    if request.method == 'POST':
        form = ArchiveForm(request.POST)
        if form.is_valid():
            medcard_id = form.cleaned_data['medcard_id']
            new_status = form.cleaned_data['new_status']

            with connection.cursor() as cursor:
                # Обновление статуса талона
                cursor.execute("UPDATE medical_cards SET status = %s WHERE medcard_id = %s",
                               [new_status, medcard_id])

            return render(request, 'medicalcards/success_delivery.html',
                          {'message': 'Медична карта успішно архівована'})  # Редирект на страницу успеха
    else:
        form = ArchiveForm()

    return render(request, 'medicalcards/medcard_status_archive.html', {'form': form})


def statistic(request):
    search_error_message = None
    medcard = None
    age_appointment_stats = None
    chart_url = None
    average_age = None

    with connection.cursor() as cursor:
        cursor.execute("SELECT calculate_average_age_of_patients()")
        average_age = cursor.fetchone()[0]

    if request.method == 'POST':
        if 'search_button' in request.POST:
            form_search = MedicalCardSearchSt(request.POST)
            form_age_appointment = AgeAppointmentForm(request.POST)
            if form_search.is_valid():
                medcard_id = form_search.cleaned_data['medcard_id']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM search_patient(%s)", [medcard_id])
                    medcard = cursor.fetchone()
                    if medcard:
                        return render(request, 'medicalcards/medcard_statistic.html',
                                      {'form_search': form_search, 'form_age_appointment': form_age_appointment, 'medcard': medcard, 'message': f'Медичну карту № {medcard_id} знайдено'})
                    else:
                        search_error_message = f"Медичну карту з № {medcard_id} не знайдено."
                        return render(request, 'medicalcards/medcard_statistic.html',
                                  {'form_search': form_search, 'form_age_appointment': form_age_appointment, 'search_error_message': search_error_message})
        elif 'age_appointment_button' in request.POST:
            form_search = MedicalCardSearchSt(request.POST)
            form_age_appointment = AgeAppointmentForm(request.POST)
            if form_age_appointment.is_valid():
                medcard_ids_str = form_age_appointment.cleaned_data['medcard_ids']
                medcard_ids = [int(id.strip()) for id in medcard_ids_str.split(',')] if medcard_ids_str else None
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM get_age_appointment_counts(%s)", [medcard_ids])
                    age_appointment_stats = cursor.fetchall()
                    if age_appointment_stats:
                        # Create a graph
                        ages = [stat[0] for stat in age_appointment_stats]
                        appointment_counts = [stat[1] for stat in age_appointment_stats]

                        plt.figure(figsize=(10, 5))
                        plt.bar(ages, appointment_counts)
                        plt.title('Кількість прийомів за віком')
                        plt.xlabel('Вік')
                        plt.ylabel('Кількість прийомів')
                        #plt.grid(True)
                        plt.grid(axis='y')
                        plt.savefig('chart.png', format='png')

                        # Save the plot to a bytes buffer
                        buf = io.BytesIO()
                        plt.savefig(buf, format='png')
                        buf.seek(0)
                        string = base64.b64encode(buf.read())
                        chart_url = 'data:image/png;base64,' + urllib.parse.quote(string)
                        plt.close()
            else:
                # Обработка ошибок валидации формы
                search_error_message = "Некоректний ввід. Перевірте правильність заповнення форми."
        elif 'patient_privileges_button' in request.POST:
            form_search = MedicalCardSearchSt(request.POST)
            form_age_appointment = AgeAppointmentForm(request.POST)
            if form_age_appointment.is_valid():
                medcard_ids_str = form_age_appointment.cleaned_data['medcard_ids']
                medcard_ids = [int(id.strip()) for id in medcard_ids_str.split(',')] if medcard_ids_str else None
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM get_patient_privileges_stats(%s)", [medcard_ids])
                    patient_privileges_stats = cursor.fetchall()
                    if patient_privileges_stats:
                        privilege_types = [stat[0] for stat in patient_privileges_stats]
                        patient_counts = [stat[1] for stat in patient_privileges_stats]

                        plt.figure(figsize=(7, 7))  # Установим равные размеры, чтобы получить круговую диаграмму
                        plt.pie(patient_counts, labels=privilege_types, autopct='%1.1f%%', startangle=140)
                        plt.title('Статистика пацієнтів за квотами')
                        plt.savefig('privileges_chart.png', format='png')

                        # Save the plot to a bytes buffer
                        buf = io.BytesIO()
                        plt.savefig(buf, format='png')
                        buf.seek(0)
                        string = base64.b64encode(buf.read())
                        chart_url_privileges = 'data:image/png;base64,' + urllib.parse.quote(string)
                        plt.close()

                        return render(request, 'medicalcards/medcard_statistic.html', {
                            "medcard": medcard, 'form_search': form_search,
                            'form_age_appointment': form_age_appointment,
                            'search_error_message': search_error_message, 'chart_url': chart_url,
                            'age_appointment_stats': age_appointment_stats,
                            'chart_url_privileges': chart_url_privileges,
                            'patient_privileges_stats': patient_privileges_stats
                        })
            else:
                search_error_message = "Некоректний ввід. Перевірте правильність заповнення форми."


    else:
        form_search = MedicalCardSearchSt()
        form_age_appointment = AgeAppointmentForm()

    return render(request, 'medicalcards/medcard_statistic.html', {"medcard": medcard, 'form_search': form_search, 'form_age_appointment': form_age_appointment,
                            'search_error_message': search_error_message, 'chart_url': chart_url, 'age_appointment_stats': age_appointment_stats, 'average_age': average_age, })


