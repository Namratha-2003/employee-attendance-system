from .database import Base, engine, SessionLocal
from .models import User
from .auth import hash_password

Base.metadata.create_all(bind=engine)

def seed_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(
                employee_id="ADMIN001",
                name="Admin User",
                email="admin@example.com",
                phone="9999999999",
                role="Admin",
                department="Management",
                password_hash=hash_password("Admin@123"),
                is_admin=True,
                is_active=True,
            )
            db.add(admin)
            db.commit()
            print("Admin created: admin@example.com / Admin@123")
        else:
            print("Admin already exists: admin@example.com / Admin@123")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
