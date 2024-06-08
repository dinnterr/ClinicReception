from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, IntegrityError, DatabaseError

from .forms import DoctorSelectForm, ScheduleCreateForm, ScheduleUpdateForm
from .models import Schedules


def schedules_list(request):
    schedule_id = Schedules.objects.all()
    return render(request, 'schedules/schedules_list.html', {"schedules": schedule_id})


def select_doctor_view(request):
    if request.method == 'POST':
        form = DoctorSelectForm(request.POST)
        if form.is_valid():
            doctor_id = form.cleaned_data['doctor'].doctor_id
            doctor_name = form.cleaned_data['doctor'].full_name
            return redirect('doctor_schedule', doctor_id=doctor_id, doctor_name=doctor_name)
    else:
        form = DoctorSelectForm()

    return render(request, 'schedules/select_doctor.html', {'form': form})

def get_doctor_schedule_view(request, doctor_id, doctor_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_doctor_schedule(%s)", [doctor_id])
        schedule = cursor.fetchall()

    # Преобразование данных для удобства отображения в шаблоне
    schedule_list = []
    for row in schedule:
        schedule_list.append({
            'day_for_visits': row[0],
            'start_time': row[1],
            'end_time': row[2],
            'cabinet': row[3],
        })

    return render(request, 'schedules/doctor_schedule.html', {'schedule': schedule_list, 'doctor_id': doctor_id,
                                                              'doctor_name': doctor_name})


def schedules_management(request):
    select_form = DoctorSelectForm()
    create_form = ScheduleCreateForm()
    doctor_schedule = None
    doctor_name = None
    error_message = None

    if request.method == 'POST':
        if 'view_schedule_button' in request.POST:
            select_form = DoctorSelectForm(request.POST)
            if select_form.is_valid():
                doctor_id = select_form.cleaned_data['doctor'].doctor_id
                doctor_name = select_form.cleaned_data['doctor'].full_name
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM get_doctor_schedule(%s)", [doctor_id])
                    doctor_schedule = cursor.fetchall()
                    doctor_schedule = [
                        {'schedule_id': row[0], 'day_for_visits': row[1], 'start_time': row[2],
                         'end_time': row[3], 'cabinet': row[4]}
                        for row in doctor_schedule
                    ]

        elif 'create_schedule_button' in request.POST:
            create_form = ScheduleCreateForm(request.POST)
            if create_form.is_valid():
                try:
                    create_form.save()
                    return redirect('schedules_management')
                except IntegrityError as e:
                    if 'schedules_start_time_check' in str(e):
                        error_message = "Помилка цілісності даних: Час початку повинен бути між 08:00 та 13:00."
                    elif 'schedules_end_time_check' in str(e):
                        error_message = "Помилка цілісності даних: Час закінчення повинен бути між 13:00 та 18:00."
                    elif 'schedules_cabinet_check' in str(e):
                        error_message = "Помилка цілісності даних: Номер кабінету повинен бути невід'ємним."
                    else:
                        error_message = "Помилка цілісності даних: " + str(e)
                    return render(request, 'schedules/schedules_management.html', {
                        'select_form': select_form,
                        'create_form': create_form,
                        'doctor_schedule': doctor_schedule,
                        'doctor_name': doctor_name,
                        'error_message': error_message
                    })
                except DatabaseError as e:
                    error_message = "Помилка бази даних: " + str(e)
                    return render(request, 'schedules/schedules_management.html', {
                        'select_form': select_form,
                        'create_form': create_form,
                        'doctor_schedule': doctor_schedule,
                        'doctor_name': doctor_name,
                        'error_message': error_message
                    })
                except Exception as e:
                    # Обрабатываем любые другие исключения
                    error_message = "Невідома помилка: " + str(e)
                    return render(request, 'schedules/schedules_management.html', {
                        'select_form': select_form,
                        'create_form': create_form,
                        'doctor_schedule': doctor_schedule,
                        'doctor_name': doctor_name,
                        'error_message': error_message
                    })

        elif 'edit_schedule_button' in request.POST:
            schedule_id = request.POST.get('schedule_id')
            schedule = get_object_or_404(Schedules, pk=schedule_id)
            update_form = ScheduleUpdateForm(instance=schedule)
            return render(request, 'schedules/schedules_management.html', {
                'select_form': select_form,
                'create_form': create_form,
                'doctor_schedule': doctor_schedule,
                'doctor_name': doctor_name,
                'update_form': update_form
            })

        elif 'update_schedule_button' in request.POST:
            schedule_id = request.POST.get('schedule_id')
            schedule = get_object_or_404(Schedules, pk=schedule_id)
            update_form = ScheduleUpdateForm(request.POST, instance=schedule)
            if update_form.is_valid():
                update_form.save()
                return redirect('schedules_management')

        elif 'delete_schedule_button' in request.POST:
            schedule_id = request.POST.get('schedule_id')
            schedule = get_object_or_404(Schedules, pk=schedule_id)
            schedule.delete()
            return redirect('schedules_management')

    return render(request, 'schedules/schedules_management.html', {
        'select_form': select_form,
        'create_form': create_form,
        'doctor_schedule': doctor_schedule,
        'doctor_name': doctor_name
    })