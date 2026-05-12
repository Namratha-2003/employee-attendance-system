from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import extract
from ..database import get_db
from ..models import User, Attendance
from ..auth import get_current_user
from ..schemas import EmployeeOut
from ..utils import today_ist

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/profile", response_model=EmployeeOut)
def profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/dashboard")
def dashboard(month: int | None = None, year: int | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = today_ist()
    month = month or today.month
    year = year or today.year

    today_attendance = db.query(Attendance).filter(
        Attendance.user_id == current_user.id,
        Attendance.attendance_date == today
    ).first()

    monthly_records = db.query(Attendance).filter(
        Attendance.user_id == current_user.id,
        extract("month", Attendance.attendance_date) == month,
        extract("year", Attendance.attendance_date) == year,
    ).order_by(Attendance.attendance_date.desc()).all()

    total_month_hours = round(sum(r.total_hours or 0 for r in monthly_records), 2)

    return {
        "profile": {
            "id": current_user.id,
            "employee_id": current_user.employee_id,
            "name": current_user.name,
            "email": current_user.email,
            "phone": current_user.phone,
            "role": current_user.role,
            "department": current_user.department,
            "created_at": current_user.created_at,
        },
        "today": today_attendance,
        "monthly_records": monthly_records,
        "total_month_hours": total_month_hours,
    }
