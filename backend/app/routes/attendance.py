from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from ..database import get_db
from ..models import Attendance, User
from ..auth import get_current_user
from ..schemas import AttendanceLocation
from ..holidays import is_non_working_day
from ..utils import now_ist, today_ist

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/login")
def attendance_login(payload: AttendanceLocation, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = today_ist()
    blocked, reason = is_non_working_day(today)
    if blocked:
        raise HTTPException(status_code=400, detail=f"Attendance is not allowed today: {reason}")

    existing = db.query(Attendance).filter(
        Attendance.user_id == current_user.id,
        Attendance.attendance_date == today,
    ).first()

    if existing and existing.login_time:
        raise HTTPException(status_code=400, detail="Already logged in today")

    record = existing or Attendance(user_id=current_user.id, attendance_date=today)
    record.login_time = now_ist()
    record.login_latitude = payload.latitude
    record.login_longitude = payload.longitude
    record.login_location = payload.location
    record.status = "Logged In"

    db.add(record)
    db.commit()
    db.refresh(record)
    return {"message": "Login attendance recorded", "attendance": record}


@router.post("/logout")
def attendance_logout(payload: AttendanceLocation, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    today = today_ist()
    blocked, reason = is_non_working_day(today)
    if blocked:
        raise HTTPException(status_code=400, detail=f"Attendance is not allowed today: {reason}")

    record = db.query(Attendance).filter(
        Attendance.user_id == current_user.id,
        Attendance.attendance_date == today,
    ).first()

    if not record or not record.login_time:
        raise HTTPException(status_code=400, detail="Please login first")
    if record.logout_time:
        raise HTTPException(status_code=400, detail="Already logged out today")

    record.logout_time = now_ist()
    record.logout_latitude = payload.latitude
    record.logout_longitude = payload.longitude
    record.logout_location = payload.location
    seconds = (record.logout_time - record.login_time).total_seconds()
    record.total_hours = round(seconds / 3600, 2)
    record.status = "Completed"

    db.commit()
    db.refresh(record)
    return {"message": "Logout attendance recorded", "attendance": record}
