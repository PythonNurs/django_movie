from django_movie.celery import app
from django.core.mail import send_mail


@app.task
def send_info_email(user_email):
    send_mail(
        'Hello',
        'Hello from django-movie',
        'nursultankaragulov0220@gmail.com',
        [user_email],
        fail_silently=False,
    )
