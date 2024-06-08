# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, IntegrityError, DatabaseError
from .forms import ReceptionistForm, ReceptionistFilterForm, DismissReceptionistForm
from .models import Receptionists

def get_receptionists_by_status(working):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_receptionists_by_status(%s);", [working])
        columns = [col[0] for col in cursor.description]
        results = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    return results

def receptionists_list(request):
    receptionists_id = Receptionists.objects.all()
    receptionists = []
    if request.method == 'GET':
        form = ReceptionistFilterForm(request.GET)
        if form.is_valid():
            status = form.cleaned_data['status'] == 'True'
            receptionists = get_receptionists_by_status(status)
    else:
        form = ReceptionistFilterForm()

    return render(request, 'receptionists/receptionists_list.html', {'form': form, 'receptionists': receptionists, 'receptionists_id': receptionists_id})

def receptionist_create(request):
    if request.method == "POST":
        form = ReceptionistForm(request.POST)
        if form.is_valid():
            try:
                full_name = form.cleaned_data['full_name']
                job_title = form.cleaned_data['job_title']
                birth_date = form.cleaned_data['birth_date']
                status = form.cleaned_data['status']
                receptionist_login = form.cleaned_data['receptionist_login']
                receptionist_password = form.cleaned_data['receptionist_password']

                with connection.cursor() as cursor:
                    cursor.execute("CALL register_worker(%s, %s, %s, %s, %s, %s);",
                                   [full_name, job_title, birth_date, status, receptionist_login,
                                    receptionist_password])

                return render(request, 'receptionists/success.html', {'message': 'Працівника успішно створено'})
            except IntegrityError as e:
                if 'receptionists_birth_date_check' in str(e):
                    error_message = "Помилка цілісності даних: Працівник не може бути молодше 21 року."
                else:
                    error_message = "Помилка цілісності даних: " + str(e)
                return render(request, 'receptionists/receptionist_form.html', {'form': form, 'error_message': error_message})
            except DatabaseError as e:
                if 'check_receptionist_age()' in str(e):
                    error_message = "Працівник не може бути молодше 21 року."
                else:
                    error_message = "Помилка бази даних: " + str(e)
                return render(request, 'receptionists/receptionist_form.html', {'form': form, 'error_message': error_message})
            except Exception as e:
                error_message = "Невідома помилка: " + str(e)
                return render(request, 'receptionists/receptionist_form.html', {'form': form, 'error_message': error_message})
    else:
        form = ReceptionistForm()
    return render(request, 'receptionists/receptionist_form.html', {'form': form})

def receptionist_delete(request):
    if request.method == 'POST':
        form = DismissReceptionistForm(request.POST)
        if form.is_valid():
            receptionist_id = form.cleaned_data['receptionist'].receptionist_id

            with connection.cursor() as cursor:
                try:
                    cursor.execute("CALL dismiss_receptionist(%s);", [receptionist_id])
                    return redirect('receptionists_list')
                except IntegrityError as e:
                    error_message = "Помилка цілісності даних: " + str(e)
                    return render(request, 'receptionists/receptionist_delete.html',
                                  {'form': form, 'error_message': error_message})
                except DatabaseError as e:
                    error_message = "Помилка бази даних: " + str(e)
                    return render(request, 'receptionists/receptionist_delete.html',
                                  {'form': form, 'error_message': error_message})
                except Exception as e:
                    error_message = "Невідома помилка: " + str(e)
                    return render(request, 'receptionists/receptionist_delete.html',
                                  {'form': form, 'error_message': error_message})
    else:
        form = DismissReceptionistForm()

    return render(request, 'receptionists/receptionist_delete.html', {'form': form})

