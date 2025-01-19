from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_every_minute():
    '''функция отправки письма каждую минуту '''
    send_mail(
        "Письмо раз в минуту",
        "Привет, получатель!",
        "timoshkova@coursework.com",
        ["recipient@example.com"],
        fail_silently=False,
    )


@shared_task
def send_email_new_year():
    '''функция отправки письма на новый год '''
    send_mail(
        "Новогодняя рассылка",
        f"С новым годом, с новым счастьем!",
        "timoshkova@coursework.com",
        ["recipient@example.com"],
        fail_silently=False,
    )
