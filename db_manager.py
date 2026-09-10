"""
db_manager.py
Database manager for Student Course Registration DBMS.
Implements table operations:
- Add Course
- Withdraw Course
- Update Course
- Querying and Batch Import
"""

import sqlite3
import os
from contextlib import contextmanager
from typing import List, Dict, Any, Optional, Tuple

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "course_registration.db")


class CourseDB:
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_connection(self):
        """Yields an SQLite connection with Row factory and ensures it is closed."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        """Creates the course_registrations table if it does not exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
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
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reg_no ON course_registrations(reg_no);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_subject ON course_registrations(subject);")
            conn.commit()

    def add_course(
        self,
        reg_no: str,
        student_name: str,
        slot: str,
        subject: str,
        faculty_id: str,
        faculty_name: str
    ) -> bool:
        """
        [Add Course]
        Registers a student for a course.
        Returns True if successful, False if student is already registered for this subject.
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO course_registrations (reg_no, student_name, slot, subject, faculty_id, faculty_name)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (
                    reg_no.strip().upper(),
                    student_name.strip(),
                    slot.strip().upper(),
                    subject.strip(),
                    faculty_id.strip().upper(),
                    faculty_name.strip()
                ))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            print(f"[Error] Student '{reg_no}' is already registered for course '{subject}'.")
            return False
        except Exception as e:
            print(f"[Error] Failed to add course: {e}")
            return False

    def withdraw_course(self, reg_no: str, subject: str) -> bool:
        """
        [Withdraw Course]
        Removes a course registration for a given student registration number and subject.
        Returns True if a record was removed, False otherwise.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM course_registrations
                WHERE UPPER(reg_no) = UPPER(?) AND UPPER(subject) = UPPER(?);
            """, (reg_no.strip(), subject.strip()))
            conn.commit()
            return cursor.rowcount > 0

    def update_course(
        self,
        reg_no: str,
        subject: str,
        new_slot: Optional[str] = None,
        new_subject: Optional[str] = None,
        new_faculty_id: Optional[str] = None,
        new_faculty_name: Optional[str] = None,
        new_student_name: Optional[str] = None
    ) -> bool:
        """
        [Update]
        Updates registration details (slot, faculty ID, faculty name, etc.) for a student course.
        Returns True if record was updated, False otherwise.
        """
        updates = []
        params = []

        if new_student_name is not None:
            updates.append("student_name = ?")
            params.append(new_student_name.strip())
        if new_slot is not None:
            updates.append("slot = ?")
            params.append(new_slot.strip().upper())
        if new_subject is not None:
            updates.append("subject = ?")
            params.append(new_subject.strip())
        if new_faculty_id is not None:
            updates.append("faculty_id = ?")
            params.append(new_faculty_id.strip().upper())
        if new_faculty_name is not None:
            updates.append("faculty_name = ?")
            params.append(new_faculty_name.strip())

        if not updates:
            print("[Warning] No update fields provided.")
            return False

        query = f"""
            UPDATE course_registrations
            SET {', '.join(updates)}
            WHERE UPPER(reg_no) = UPPER(?) AND UPPER(subject) = UPPER(?);
        """
        params.extend([reg_no.strip(), subject.strip()])

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, tuple(params))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.IntegrityError as e:
            print(f"[Error] Update failed due to duplicate conflict: {e}")
            return False
        except Exception as e:
            print(f"[Error] Update failed: {e}")
            return False

    def get_courses_by_student(self, reg_no: str) -> List[Dict[str, Any]]:
        """Fetches all courses registered by a specific student."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, reg_no, student_name, slot, subject, faculty_id, faculty_name, created_at
                FROM course_registrations
                WHERE UPPER(reg_no) = UPPER(?)
                ORDER BY subject;
            """, (reg_no.strip(),))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_all_registrations(self) -> List[Dict[str, Any]]:
        """Fetches all course registrations in the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, reg_no, student_name, slot, subject, faculty_id, faculty_name, created_at
                FROM course_registrations
                ORDER BY reg_no, subject;
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_registration(self, reg_no: str, subject: str) -> Optional[Dict[str, Any]]:
        """Fetches a specific course registration."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, reg_no, student_name, slot, subject, faculty_id, faculty_name, created_at
                FROM course_registrations
                WHERE UPPER(reg_no) = UPPER(?) AND UPPER(subject) = UPPER(?);
            """, (reg_no.strip(), subject.strip()))
            row = cursor.fetchone()
            return dict(row) if row else None

    def batch_insert(self, records: List[Dict[str, str]]) -> Tuple[int, int]:
        """
        Imports a list of records.
        Each item should be a dict with keys:
        'reg_no', 'student_name', 'slot', 'subject', 'faculty_id', 'faculty_name'
        Returns: (success_count, fail_count)
        """
        success = 0
        failed = 0
        for r in records:
            res = self.add_course(
                reg_no=r.get("reg_no", ""),
                student_name=r.get("student_name", ""),
                slot=r.get("slot", ""),
                subject=r.get("subject", ""),
                faculty_id=r.get("faculty_id", ""),
                faculty_name=r.get("faculty_name", "")
            )
            if res:
                success += 1
            else:
                failed += 1
        return success, failed


# Optional MS Access Connector for environments requiring an Access .accdb database file
class MSAccessCourseDB:
    """
    Adapter for connecting to Microsoft Access (*.accdb/*.mdb) using pyodbc.
    Usage requires: pip install pyodbc and MS Access Database Engine installed on Windows.
    """
    def __init__(self, accdb_path: str):
        self.accdb_path = accdb_path
        self.conn_str = (
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
            f"DBQ={self.accdb_path};"
        )

    def get_connection(self):
        try:
            import pyodbc
            return pyodbc.connect(self.conn_str)
        except ImportError:
            raise ImportError("pyodbc is not installed. Install it via 'pip install pyodbc'")
