from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date


class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str = "employee"
    department: Optional[str] = None


class EmployeeOut(BaseModel):
    id: int
    employee_id: str
    name: str
    email: EmailStr
    phone: Optional[str]
    role: str
    department: Optional[str]
    is_admin: bool
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AttendanceLocation(BaseModel):
    latitude: float
    longitude: float
    location: Optional[str] = None


class AttendanceOut(BaseModel):
    id: int
    attendance_date: date
    login_time: Optional[datetime]
    logout_time: Optional[datetime]
    total_hours: float
    status: str
    login_latitude: Optional[float]
    login_longitude: Optional[float]
    login_location: Optional[str]
    logout_latitude: Optional[float]
    logout_longitude: Optional[float]
    logout_location: Optional[str]
    employee_id: Optional[str] = None
    employee_name: Optional[str] = None
    role: Optional[str] = None

    model_config = {"from_attributes": True}



class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
