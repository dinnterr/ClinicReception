import psycopg2
from django.conf import settings
from django.db import connections
from django.contrib.auth import get_user


class UserDatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Отримуємо аутентифікованого користувача
        user = get_user(request)

        '''if user.is_authenticated:'''
        # Перевіряємо, чи є дані користувача в запиті
        db_user = getattr(request, 'db_user', None)
        db_password = getattr(request, 'db_password', None)
        print(f'DB User: {db_user}, DB Password: {db_password}')
        if db_user and db_password:
            print(f"Switching database connection to user: {db_user}")  # для перевірки
            # Оновлюємо налаштування підключення до бази даних для користувача
            settings.DATABASES['default'].update({
                'USER': db_user,
                'PASSWORD': db_password
            })

            # Закриваємо існуючі з'єднання, щоб використати нові облікові дані
            connections['default'].close()

        response = self.get_response(request)
        return response
