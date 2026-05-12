import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def _send_email(to_email: str, subject: str, body: str) -> bool:
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": subject,
            "html": body.replace("\n", "<br>")
        })

        print("Email sent successfully")
        return True

    except Exception as e:
        print("EMAIL ERROR:", str(e))
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
