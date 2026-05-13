import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.elasticemail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "2525"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")


def _send_email(to_email: str, subject: str, body: str) -> bool:
    print("EMAIL FUNCTION CALLED")
    print("TO:", to_email)
    print("FROM_EMAIL:", FROM_EMAIL)
    print("SMTP_HOST:", SMTP_HOST)
    print("SMTP_PORT:", SMTP_PORT)
    print("SMTP_USER EXISTS:", bool(SMTP_USER))
    print("SMTP_PASSWORD EXISTS:", bool(SMTP_PASSWORD))

    if not SMTP_USER or not SMTP_PASSWORD or not FROM_EMAIL:
        print("SMTP EMAIL NOT CONFIGURED")
        return False

    try:
        msg = EmailMessage()
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully using Elastic Email SMTP")
        return True

    except Exception as e:
        print("SMTP EMAIL EXCEPTION:", str(e))
        return False


def send_employee_credentials(
    to_email: str,
    name: str,
    employee_id: str,
    password: str,
) -> bool:
    subject = "Your Employee Attendance Portal Login Credentials"

    body = f"""
Hi {name},

Your employee attendance portal account has been created.

Employee ID: {employee_id}
Email: {to_email}
Temporary Password: {password}

Please login and start marking attendance from working days only.

Regards,
Admin Team
"""

    return _send_email(to_email, subject, body)


def send_password_reset_email(
    to_email: str,
    name: str,
    reset_link: str,
) -> bool:
    subject = "Reset Your Employee Attendance Portal Password"

    body = f"""
Hi {name},

We received a request to reset your Employee Attendance Portal password.

Click this link to set a new password:
{reset_link}

This link will expire in 30 minutes.

If you did not request this, please ignore this email.

Regards,
Admin Team
"""

    return _send_email(to_email, subject, body)