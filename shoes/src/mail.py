# from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
# from .config import Config
# from pathlib import Path

# Base_Dir=Path(__file__).resolve().parent

# mail_config=ConnectionConfig(
#     MAIL_USERNAME=Config.MAIL_USERNAME,
#     MAIL_PASSWORD=Config.MAIL_PASSWORD,
#     MAIL_FROM=Config.MAIL_FROM,
#     MAIL_PORT=Config.MAIL_PORT,
#     MAIL_SERVER=Config.MAIL_SERVER,
#     MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
#     MAIL_STARTTLS=True,
#     MAIL_SSL_TLS=False,
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True,
#     TEMPLATE_FOLDER=Path(Base_Dir,"templates"),
# )

# mail=FastMail(config=mail_config)

# def create_message(recipients:list[str],subject:str,body:str):
#     message=MessageSchema(
#         recipients=recipients,
#         subject=subject,
#         body=body,
#         subtype=MessageType.html,
#     )
#     return message

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from src.config import Config
from typing import List


def send_email(to_email: List[str], subject: str, html_content: str):
    try:
        message = Mail(
            from_email=(Config.MAIL_FROM, Config.MAIL_FROM_NAME),
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )

        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)

        return response.status_code

    except Exception as e:
        print("SendGrid Error:", str(e))
        raise