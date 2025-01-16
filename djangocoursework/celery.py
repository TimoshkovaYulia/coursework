import os
from celery import Celery

# Установите переменную окружения DJANGO_SETTINGS_MODULE.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocoursework.settings')

# Создайте экземпляр Celery.
app = Celery('djangocoursework')

# Загрузите настройки конфигурации Celery из настроек Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживать задачи в установленных приложениях Django.
app.autodiscover_tasks()

broker_connection_retry_on_startup = True
