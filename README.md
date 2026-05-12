# Employee Attendance System - PostgreSQL / pgAdmin 4

Full-stack attendance project with:

- Admin and employee login
- Separate pages for Admin Dashboard, Employees, Attendance Report
- Separate pages for User Dashboard, Profile, My Attendance
- Admin-only employee creation
- Auto-generated employee password sent by email
- Forgot password and reset password by email
- Login/logout attendance with latitude, longitude, and location
- Weekend and Indian holiday attendance blocking
- Daily/monthly filters by employee ID and name
- Excel export
- Indian date format: **DD-MM-YYYY**
- Indian time display: **IST**

## 1. Create database in pgAdmin 4

Create a database named:

```text
employee_attendance_db
```

Do not use spaces in the database name.

## 2. Backend setup

Open terminal:

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` from `.env.example`:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/employee_attendance_db
SECRET_KEY=change-this-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_ORIGIN=http://localhost:5173

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=yourgmail@gmail.com
SMTP_PASSWORD=your_gmail_app_password
FROM_EMAIL=yourgmail@gmail.com
```

Run backend:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## 3. Create default admin

In backend terminal:

```bash
python -m app.seed
```

Login:

```text
Email: admin@example.com
Password: Admin@123
```

## 4. Frontend setup

Open second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## 5. Forgot password

Forgot password sends reset link to the user's email. If SMTP is not configured, the backend terminal prints the reset link for testing.

## 6. Important pages

Admin:

```text
/admin/dashboard
/admin/employees
/admin/attendance
```

User:

```text
/user/dashboard
/user/profile
/user/attendance
```

Password:

```text
/forgot-password
/reset-password?token=TOKEN
```
