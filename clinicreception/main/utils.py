from django.conf import settings
from django.db import connection, connections


ROLE_PASSWORDS = {
    'registry_default': '0000',
    'registry_medregistrator': 'registrator',
    'registry_medcontroller': 'controller',
    'registry_admin': 'admin',
    'registry_analyst': 'analyst',
    'registry_manager': 'manager',
    'registry_doctor': 'doctor',
}


def check_user(username, password):
    cursor = connection.cursor()

    # Перевірка користувача
    cursor.execute("""
                    SELECT login, password FROM registry_users.Users WHERE login = %s AND password = crypt(%s, password)
                """, (username, password))

    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        return username
    else:
        return None


def authenticate_user(username, password):
    checked = check_user(username, password)

    with connection.cursor() as cursor:
        cursor.execute("SELECT role FROM registry_users.users WHERE login = %s;", [checked])
        user_role = cursor.fetchone()
        if user_role:
            return user_role[0]
        else:
            return None

def reconnect_with_role(role):
    # Получаем пароль для роли
    role_password = ROLE_PASSWORDS.get(role)
    if role_password:
        # Обновляем настройки подключения к базе данных
        settings.DATABASES['default'].update({
            'USER': role,
            'PASSWORD': role_password
        })
        # Закрываем текущее соединение, чтобы использовать новые учетные данные
        connections['default'].close()
        # Проверяем текущего пользователя
        with connection.cursor() as cursor:
            cursor.execute(f"SET ROLE {role};")
            cursor.execute("SELECT current_user;")
            current_user = cursor.fetchone()[0]
            print(f"Successfully switched to user: {current_user}")
    else:
        print(f"Password for role {role} not found.")

