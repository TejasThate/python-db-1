"""
test_db.py
Automated test suite to verify all database operations:
- Add Course
- Withdraw Course
- Update Course
- Query operations
- Duplicate constraints
"""

import os
import unittest
from db_manager import CourseDB

TEST_DB_PATH = os.path.join(os.path.dirname(__file__), "test_course_registration.db")


class TestCourseDB(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)
        self.db = CourseDB(db_path=TEST_DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_add_course(self):
        result = self.db.add_course(
            reg_no="22BCE001",
            student_name="Ananya Sen",
            slot="A1",
            subject="Operating Systems",
            faculty_id="FAC01",
            faculty_name="Dr. Gupta"
        )
        self.assertTrue(result)

        courses = self.db.get_courses_by_student("22BCE001")
        self.assertEqual(len(courses), 1)
        self.assertEqual(courses[0]["student_name"], "Ananya Sen")
        self.assertEqual(courses[0]["slot"], "A1")
        self.assertEqual(courses[0]["subject"], "Operating Systems")

    def test_duplicate_course_prevented(self):
        # Adding course first time
        self.db.add_course("22BCE001", "Ananya Sen", "A1", "Operating Systems", "FAC01", "Dr. Gupta")
        # Adding same course for same student
        dup_result = self.db.add_course("22BCE001", "Ananya Sen", "B1", "Operating Systems", "FAC02", "Dr. Rao")
        self.assertFalse(dup_result)

    def test_update_course(self):
        self.db.add_course("22BCE002", "Rahul Sharma", "C1", "Computer Networks", "FAC03", "Prof. Verma")
        
        # Update slot and faculty
        success = self.db.update_course(
            reg_no="22BCE002",
            subject="Computer Networks",
            new_slot="D1",
            new_faculty_id="FAC04",
            new_faculty_name="Dr. Nair"
        )
        self.assertTrue(success)

        rec = self.db.get_registration("22BCE002", "Computer Networks")
        self.assertIsNotNone(rec)
        self.assertEqual(rec["slot"], "D1")
        self.assertEqual(rec["faculty_id"], "FAC04")
        self.assertEqual(rec["faculty_name"], "Dr. Nair")

    def test_withdraw_course(self):
        self.db.add_course("22BCE003", "Kavya Nair", "E1", "DBMS", "FAC05", "Dr. Raman")
        
        # Withdraw existing course
        withdrawn = self.db.withdraw_course("22BCE003", "DBMS")
        self.assertTrue(withdrawn)

        # Confirm withdrawal
        courses = self.db.get_courses_by_student("22BCE003")
        self.assertEqual(len(courses), 0)

        # Withdraw non-existent course returns False
        fake_withdraw = self.db.withdraw_course("22BCE003", "DBMS")
        self.assertFalse(fake_withdraw)

    def test_batch_insert_and_get_all(self):
        records = [
            {"reg_no": "22BCE010", "student_name": "Siddharth", "slot": "A2", "subject": "DSA", "faculty_id": "F1", "faculty_name": "Dr. A"},
            {"reg_no": "22BCE010", "student_name": "Siddharth", "slot": "B2", "subject": "AI", "faculty_id": "F2", "faculty_name": "Dr. B"},
            {"reg_no": "22BCE011", "student_name": "Meera", "slot": "A2", "subject": "DSA", "faculty_id": "F1", "faculty_name": "Dr. A"},
        ]
        s_count, f_count = self.db.batch_insert(records)
        self.assertEqual(s_count, 3)
        self.assertEqual(f_count, 0)

        all_records = self.db.get_all_registrations()
        self.assertEqual(len(all_records), 3)


if __name__ == "__main__":
    unittest.main()
