from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError, DatabaseError, connection

from django.shortcuts import render
from .models import Doctors
from .forms import DoctorForm, DoctorFilterForm, DismissDoctorForm, SelectDoctorForm, EditDoctorForm, PatientVisitsForm



def get_doctors_by_status(working):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM doctors_list(%s);", [working])
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return results


def doctors_list(request):
    doctors_id = Doctors.objects.all()
    #return render(request, 'doctors/doctors.html', {"doctors": doctors})
    doctors = []
    if request.method == 'GET':
        form = DoctorFilterForm(request.GET)
        if form.is_valid():
            status = form.cleaned_data['status'] == 'True'
            doctors = get_doctors_by_status(status)
    else:
        form = DoctorFilterForm()

    return render(request, 'doctors/doctors.html', {'form': form, 'doctors': doctors, 'doctors_id': doctors_id})


def doctor_create(request):
    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            try:
                full_name = form.cleaned_data['full_name']
                job_title = form.cleaned_data['job_title']
                specialization = form.cleaned_data['specialization'].specialization_id
                birth_date = form.cleaned_data['birth_date']
                status = form.cleaned_data['status']
                doctor_login = form.cleaned_data['doctor_login']
                doctor_password = form.cleaned_data['doctor_password']

                with connection.cursor() as cursor:
                    cursor.execute("CALL register_doctor(%s, %s, %s, %s, %s, %s, %s);",
                                   [full_name, job_title, specialization, birth_date, status, doctor_login,
                                    doctor_password])

                return render(request, 'doctors/success.html', {'message': 'Лікаря успішно створено'})
            except IntegrityError as e:
                if 'doctors_birth_date_check' in str(e):
                    error_message = "Помилка цілісності даних: Лікар не може бути молодше 25 років."
                else:
                    error_message = "Помилка цілісності даних: " + str(e)
                return render(request, 'doctors/doctor_form.html', {'form': form, 'error_message': error_message})
            except DatabaseError as e:
                if 'check_doctor_age()' in str(e):
                    error_message = "Лікар не може бути молодше 25 років."
                else:
                    error_message = "Помилка бази даних: " + str(e)
                return render(request, 'doctors/doctor_form.html', {'form': form, 'error_message': error_message})
            except Exception as e:
                # Обрабатываем любые другие исключения
                error_message = "Невідома помилка: " + str(e)
                return render(request, 'doctors/doctor_form.html', {'form': form, 'error_message': error_message})
    else:
        form = DoctorForm(request.POST)
    return render(request, 'doctors/doctor_form.html', {'form': form})


def doctor_delete(request):
    if request.method == 'POST':
        form = DismissDoctorForm(request.POST)
        if form.is_valid():
            doctor_id = form.cleaned_data['doctor'].doctor_id

            with connection.cursor() as cursor:
                try:
                    cursor.execute("CALL dismiss_doctor(%s);", [doctor_id])
                    return redirect('doctor_list')
                except IntegrityError as e:
                    if "нарушает ограничение внешнего ключа" in str(e):
                        error_message = "Помилка цілісності даних: У лікаря назначені прийоми."
                    else:
                        error_message = "Помилка цілісності даних: " + str(e)
                    return render(request, 'doctors/doctor_delete.html',
                                  {'form': form, 'error_message': error_message})
                except DatabaseError as e:
                    if 'check_pending_appointments' in str(e):
                        error_message = "Помилка бази даних: Лікар має незавершені прийоми і не може бути звільнений."
                    else:
                        error_message = "Помилка бази даних: " + str(e)
                    return render(request, 'doctors/doctor_delete.html',
                                  {'form': form, 'error_message': error_message})
                except Exception as e:
                    # Обрабатываем любые другие исключения
                    error_message = "Невідома помилка: " + str(e)
                    return render(request, 'doctors/doctor_delete.html',
                                  {'form': form, 'error_message': error_message})
    else:
        form = DismissDoctorForm()

    return render(request, 'doctors/doctor_delete.html', {'form': form})


def select_doctor_view(request):
    if request.method == 'POST':
        form = SelectDoctorForm(request.POST)
        if form.is_valid():
            doctor_id = form.cleaned_data['doctor'].doctor_id
            return redirect('doctor_edit', doctor_id=doctor_id)
    else:
        form = SelectDoctorForm()

    return render(request, 'doctors/select_doctor.html', {'form': form})


def edit_doctor_view(request, doctor_id):
    doctor = get_object_or_404(Doctors, doctor_id=doctor_id)
    if request.method == 'POST':
        form = EditDoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'doctors/success.html', {'message': 'Лікаря успішно оновлено'})
            except IntegrityError as e:
                if 'doctors_birth_date_check' in str(e):
                    error_message = "Помилка цілісності даних: Лікар не може бути молодше 25 років."
                else:
                    error_message = "Помилка цілісності даних: " + str(e)
                return render(request, 'doctors/edit_doctor.html', {'form': form, 'error_message': error_message})
            except DatabaseError as e:
                error_message = "Помилка бази даних: " + str(e)
                return render(request, 'doctors/edit_doctor.html', {'form': form, 'error_message': error_message})
            except Exception as e:
                # Обрабатываем любые другие исключения
                error_message = "Невідома помилка: " + str(e)
                return render(request, 'doctors/edit_doctor.html', {'form': form, 'error_message': error_message})
    else:
        form = EditDoctorForm(instance=doctor)

    return render(request, 'doctors/edit_doctor.html', {'form': form})


def doctor_statistic(request):
    search_error_message = None
    form_patient_visits = PatientVisitsForm()
    patient_visits_stats = None
    count_visits_stats = None

    if request.method == 'POST':
        form_patient_visits = PatientVisitsForm(request.POST)
        if form_patient_visits.is_valid():
            start_date = form_patient_visits.cleaned_data['start_date']
            end_date = form_patient_visits.cleaned_data['end_date']
            doctor_id = form_patient_visits.cleaned_data['doctor_id']

            if 'patient_visits_button' in request.POST:  # Обработчик для получения статистики посещений
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM get_patient_visits(%s, %s, %s)", [start_date, end_date, doctor_id])
                    patient_visits_stats = cursor.fetchall()

            elif 'count_visits_button' in request.POST:  # Обработчик для получения количества посещений
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM get_count_visits(%s, %s, %s)", [start_date, end_date, doctor_id])
                    count_visits_stats = cursor.fetchall()

            if not patient_visits_stats and not count_visits_stats:
                search_error_message = "Помилка"

            return render(request, 'doctors/doctor_statistic.html', {
                'form_patient_visits': form_patient_visits,
                'patient_visits_stats': patient_visits_stats,
                'count_visits_stats': count_visits_stats,
                'search_error_message': search_error_message
            })

    return render(request, 'doctors/doctor_statistic.html', {
        'form_patient_visits': form_patient_visits,
        'search_error_message': search_error_message,
        'patient_visits_stats': patient_visits_stats,
        'count_visits_stats': count_visits_stats
    })
