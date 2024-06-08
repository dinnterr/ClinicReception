import psycopg2
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class PostgresBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("Using PostgresBackend for authentication")  #для проверки
        try:
            # Підключення до бази даних PostgreSQL
            conn = psycopg2.connect(
                dbname=settings.DATABASES['default']['NAME'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                host=settings.DATABASES['default']['HOST'],
                port=settings.DATABASES['default']['PORT']
            )
            cursor = conn.cursor()

            # Перевірка користувача
            cursor.execute("""
                SELECT login, password FROM registry_users.Users WHERE login = %s AND password = crypt(%s, password)
            """, (username, password))

            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                # створити об'єкт користувача на основі знайдених даних
                user = get_user_model()(username=username, password=password)
                #user.is_authenticated = True  # встановлюємо користувача як аутентифікованого

                request.db_user = username
                request.db_password = password
                return user
            else:
                return None
        except psycopg2.Error as e:
            print(e)
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None