from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_order_confirmation_template(
        order: dict,
        email_to: EmailStr
):
    email = EmailMessage()

    email["Subject"] = "Подтверждение заказа"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1> Подтверждение заказа </h1>
            Ваш заказ на общую сумму {order["total_cost"]} рублей успешно оформлен на адрес {order["delivery_address"]}.
        """,
        subtype="html"
    )
    return email
