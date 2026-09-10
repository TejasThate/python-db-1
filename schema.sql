-- Schema for Student Course Registration DBMS
CREATE TABLE IF NOT EXISTS course_registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reg_no TEXT NOT NULL,
    student_name TEXT NOT NULL,
    slot TEXT NOT NULL,
    subject TEXT NOT NULL,
    faculty_id TEXT NOT NULL,
    faculty_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(reg_no, subject)
);

CREATE INDEX IF NOT EXISTS idx_reg_no ON course_registrations(reg_no);
CREATE INDEX IF NOT EXISTS idx_subject ON course_registrations(subject);
