from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from .utils import now_ist


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(String(50), default="employee")
    department = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=now_ist)

    attendance_records = relationship("Attendance", back_populates="user")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    attendance_date = Column(Date, index=True, nullable=False)
    login_time = Column(DateTime, nullable=True)
    logout_time = Column(DateTime, nullable=True)
    total_hours = Column(Float, default=0.0)
    status = Column(String(50), default="Present")

    login_latitude = Column(Float, nullable=True)
    login_longitude = Column(Float, nullable=True)
    login_location = Column(Text, nullable=True)

    logout_latitude = Column(Float, nullable=True)
    logout_longitude = Column(Float, nullable=True)
    logout_location = Column(Text, nullable=True)

    created_at = Column(DateTime, default=now_ist)
    updated_at = Column(DateTime, default=now_ist, onupdate=now_ist)

    user = relationship("User", back_populates="attendance_records")



class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=now_ist)

    user = relationship("User")
