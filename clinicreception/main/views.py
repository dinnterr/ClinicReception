
from django.contrib.auth.models import User
from django.db import connections, connection
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import LoginForm
from .utils import authenticate_user, reconnect_with_role

# Словарь для маршрутов в зависимости от роли
ROLE_REDIRECTS = {
    'registry_medregistrator': 'registrator_main',
    'registry_medcontroller': 'medcontroller_main',
    'registry_admin': 'admin_main',
    'registry_analyst': 'statistic_main',
    'registry_manager': 'head_main',
    'registry_doctor': 'doctor_main',
}

# Словарь для хранения паролей для каждой роли
ROLE_PASSWORDS = {
    'registry_default': '0000'
}

def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def contacts(request):
    return render(request, 'main/contacts.html')


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Аутентификация пользователя
            user = authenticate_user(username, password)
            # Проверяем, существует ли пользователь с таким именем

            if user:
                # Переподключение с ролью пользователя
                reconnect_with_role(user)

                # Перенаправление на страницу в зависимости от роли
                redirect_url = ROLE_REDIRECTS.get(user, 'home')
                # Перенаправление на главную страницу или другую страницу после успешного входа
                return redirect(redirect_url)
            else:
                error = 'Неправильний логін або пароль'
                return render(request, 'main/login.html', {'form': form, 'error': error})

    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        reconnect_with_role('registry_default')

        # Перенаправление на главную страницу или другую страницу после успешного входа
        return redirect('home')
    return render(request, 'main/logout.html')

