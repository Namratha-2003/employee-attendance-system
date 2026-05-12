import os
import secrets
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, PasswordResetToken
from ..schemas import LoginRequest, Token, ForgotPasswordRequest, ResetPasswordRequest
from ..auth import verify_password, create_access_token, hash_password
from ..email_utils import send_password_reset_email
from ..utils import now_ist

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is inactive")

    token = create_access_token({"sub": str(user.id), "is_admin": user.is_admin})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "employee_id": user.employee_id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "department": user.department,
            "is_admin": user.is_admin,
        },
    }


@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    # Do not expose whether the email exists.
    if not user:
        return {"message": "If this email exists, a reset link has been sent."}

    token = secrets.token_urlsafe(32)
    reset = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=now_ist() + timedelta(minutes=30),
        used=False,
    )
    db.add(reset)
    db.commit()

    frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    reset_link = f"{frontend_origin}/reset-password?token={token}"
    email_sent = send_password_reset_email(user.email, user.name, reset_link)
    return {
        "message": "If this email exists, a reset link has been sent.",
        "email_sent": email_sent,
        "reset_link_for_testing": reset_link if not email_sent else None,
    }


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    if len(payload.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    reset = db.query(PasswordResetToken).filter(PasswordResetToken.token == payload.token).first()
    if not reset or reset.used or reset.expires_at < now_ist():
        raise HTTPException(status_code=400, detail="Invalid or expired reset link")

    user = db.query(User).filter(User.id == reset.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(payload.new_password)
    reset.used = True
    db.commit()
    return {"message": "Password reset successfully. Please login with your new password."}
