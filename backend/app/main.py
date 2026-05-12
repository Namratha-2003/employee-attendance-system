import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import auth, admin, attendance, user

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Attendance API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://courageous-chebakia-4cfc48.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(set(origins)),
    allow_credentials=True,
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