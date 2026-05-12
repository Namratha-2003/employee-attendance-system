import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def _send_email(to_email: str, subject: str, body: str) -> bool:
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    from_email = os.getenv("FROM_EMAIL", smtp_user)

    if not smtp_host or not smtp_user or not smtp_password or not from_email:
        print("\nEMAIL NOT CONFIGURED")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(body)
        print()
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print("Email sent successfully")
        return True
    except Exception as e:
        print("EMAIL ERROR:", e)
        return False


def send_employee_credentials(to_email: str, name: str, employee_id: str, password: str) -> bool:
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


def send_password_reset_email(to_email: str, name: str, reset_link: str) -> bool:
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
