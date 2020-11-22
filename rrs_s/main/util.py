from datetime import datetime
from os.path import splitext


def get_timestamp_path(instance, filename):
    """Для генерации имен фото"""
    return f'{datetime.now().timestamp()}{splitext(filename)[1]}'


def is_active_post(user):
    if user.is_staff or user.is_superuser:
        return True
    else:
        return False
