-- Run this from pgAdmin 4 Query Tool after selecting employee_attendance_db.
-- The FastAPI backend can also create these tables automatically when it starts.
-- Date display rule used in app: DD-MM-YYYY. Time rule used in app: Indian Standard Time (IST).

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(50) DEFAULT 'employee',
    department VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_users_employee_id ON users(employee_id);
CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);

CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    attendance_date DATE NOT NULL,
    login_time TIMESTAMP,
    logout_time TIMESTAMP,
    total_hours DOUBLE PRECISION DEFAULT 0.0,
    status VARCHAR(50) DEFAULT 'Present',
    login_latitude DOUBLE PRECISION,
    login_longitude DOUBLE PRECISION,
    login_location TEXT,
    logout_latitude DOUBLE PRECISION,
    logout_longitude DOUBLE PRECISION,
    logout_location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_attendance_user_date UNIQUE(user_id, attendance_date)
);

CREATE INDEX IF NOT EXISTS ix_attendance_date ON attendance(attendance_date);
CREATE INDEX IF NOT EXISTS ix_attendance_user_date ON attendance(user_id, attendance_date);

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_password_reset_tokens_token ON password_reset_tokens(token);

-- Default admin password is Admin@123.
-- Recommended: run `python -m app.seed` instead, because it creates the bcrypt hash from Python.
