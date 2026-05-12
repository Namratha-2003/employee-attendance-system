import os
import requests
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")


def _send_email(to_email: str, subject: str, body: str) -> bool:

    if not RESEND_API_KEY or not FROM_EMAIL:
        print("\nEMAIL NOT CONFIGURED")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(body)
        print()
        return False

    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "from": FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "text": body
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )

        if response.status_code in [200, 201]:
            print("Email sent successfully")
            return True
        else:
            print("EMAIL ERROR:", response.text)
            return False

    except Exception as e:
        print("EMAIL ERROR:", e)
        return False


def send_employee_credentials(
    to_email: str,
    name: str,
    employee_id: str,
    password: str
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
    reset_link: str
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
