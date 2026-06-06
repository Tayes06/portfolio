import smtplib
from email.message import EmailMessage
from app.config import settings


async def send_contact_email(name: str, email: str, subject: str | None, message: str) -> None:
    if not settings.smtp_host:
        return

    msg = EmailMessage()
    msg["Subject"] = f"[Portfolio] {subject or 'New Contact Message'}"
    msg["From"] = settings.email_from
    msg["To"] = settings.email_to
    msg.set_content(
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Subject: {subject or 'N/A'}\n"
        f"Message:\n{message}"
    )

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        smtp.starttls()
        smtp.login(settings.smtp_user, settings.smtp_password)
        smtp.send_message(msg)
