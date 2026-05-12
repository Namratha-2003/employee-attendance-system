from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import extract, or_
from datetime import date
from io import BytesIO
from openpyxl import Workbook
from ..database import get_db
from ..models import User, Attendance
from ..schemas import EmployeeCreate, EmployeeOut
from ..auth import require_admin, hash_password, generate_password
from ..email_utils import send_employee_credentials
from ..utils import format_date_indian, format_datetime_indian

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/employees")
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    exists = db.query(User).filter(or_(User.email == payload.email, User.employee_id == payload.employee_id)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Employee ID or email already exists")

    password = generate_password()
    user = User(
        employee_id=payload.employee_id,
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        role=payload.role,
        department=payload.department,
        password_hash=hash_password(password),
        is_admin=False,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    try:
        email_sent = send_employee_credentials(user.email, user.name, user.employee_id, password)
    except Exception as e:
        print("EMAIL ERROR:", e)
        email_sent = False

    return {"message": "Employee created", "employee": user, "email_sent": email_sent, "temporary_password_for_testing": password}


@router.get("/employees", response_model=list[EmployeeOut])
def list_employees(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(User).filter(User.is_admin == False).order_by(User.created_at.desc()).all()


def attendance_query(db: Session, employee_id: str | None, name: str | None, day: date | None, month: int | None, year: int | None):
    query = db.query(Attendance, User).join(User, Attendance.user_id == User.id)
    if employee_id:
        query = query.filter(User.employee_id.ilike(f"%{employee_id}%"))
    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    if day:
        query = query.filter(Attendance.attendance_date == day)
    if month:
        query = query.filter(extract("month", Attendance.attendance_date) == month)
    if year:
        query = query.filter(extract("year", Attendance.attendance_date) == year)
    return query.order_by(Attendance.attendance_date.desc(), User.name.asc())


@router.get("/attendance")
def get_all_attendance(
    employee_id: str | None = None,
    name: str | None = None,
    day: date | None = None,
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = None,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    rows = attendance_query(db, employee_id, name, day, month, year).all()
    result = []
    for attendance, user in rows:
        result.append({
            "id": attendance.id,
            "employee_id": user.employee_id,
            "employee_name": user.name,
            "role": user.role,
            "department": user.department,
            "attendance_date": attendance.attendance_date,
            "login_time": attendance.login_time,
            "logout_time": attendance.logout_time,
            "total_hours": attendance.total_hours,
            "status": attendance.status,
            "login_latitude": attendance.login_latitude,
            "login_longitude": attendance.login_longitude,
            "login_location": attendance.login_location,
            "logout_latitude": attendance.logout_latitude,
            "logout_longitude": attendance.logout_longitude,
            "logout_location": attendance.logout_location,
        })
    return result


@router.get("/attendance/export")
def export_attendance(
    employee_id: str | None = None,
    name: str | None = None,
    day: date | None = None,
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = None,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    rows = attendance_query(db, employee_id, name, day, month, year).all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"
    ws.append([
        "Employee ID", "Name", "Role", "Department", "Date", "Login Time", "Logout Time",
        "Total Hours", "Status", "Login Latitude", "Login Longitude", "Login Location",
        "Logout Latitude", "Logout Longitude", "Logout Location"
    ])

    for attendance, user in rows:
        ws.append([
            user.employee_id,
            user.name,
            user.role,
            user.department,
            format_date_indian(attendance.attendance_date),
            format_datetime_indian(attendance.login_time),
            format_datetime_indian(attendance.logout_time),
            attendance.total_hours,
            attendance.status,
            attendance.login_latitude,
            attendance.login_longitude,
            attendance.login_location,
            attendance.logout_latitude,
            attendance.logout_longitude,
            attendance.logout_location,
        ])

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)
    filename = "attendance_report.xlsx"
    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
    