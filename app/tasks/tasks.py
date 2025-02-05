from pydantic import EmailStr

from app.tasks.celery_app import celery
from app.tasks.email_templates import create_order_confirmation_template
from app.config import settings
import smtplib


@celery.task
def send_order_confirmation_email(
        order: dict,
        email_to: EmailStr
):
    email_to_mock = settings.SMTP_USER #Тест, тк зареган на test@test отправим сами себе
    msg_contect = create_order_confirmation_template(order, email_to_mock) #Исправить на email_to

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_contect)