from django.shortcuts import render, redirect

from main.utils import reconnect_with_role


def registrator(request):
    return render(request, 'registrator/registrator_main.html')


def medcontroller(request):
    return render(request, 'cardcontroller/cardcontroller_main.html')


def admin(request):
    return render(request, 'admin/admin_main.html')


def statistic(request):
    return render(request, 'statistic/statistic_main.html')


def doctor(request):
    return render(request, 'doctor/doctor_main.html')

def head(request):
    return render(request, 'head/head_main.html')

def logout_view(request):
    role = 'registry_default'
    if request.method == 'POST':
        reconnect_with_role(role)
        # Перенаправление на главную страницу или другую страницу после успешного входа
        return redirect('home')
    return render(request, 'logout.html', {'user_role': role})

