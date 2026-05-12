from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine, SessionLocal
from .models import User
from .auth import hash_password
from .routes import auth, admin, attendance, user

load_dotenv()

Base.metadata.create_all(bind=engine)

# Create default admin user if not exists
db = SessionLocal()
try:
    existing_admin = db.query(User).filter(User.email == "admin@gmail.com").first()

    if not existing_admin:
        admin_user = User(
            name="Admin",
            email="admin@gmail.com",
            password=hash_password("admin123"),
            is_admin=True,
        )
        db.add(admin_user)
        db.commit()
finally:
    db.close()

app = FastAPI(title="Employee Attendance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(attendance.router, prefix="/api")
app.include_router(user.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Employee Attendance API running"}