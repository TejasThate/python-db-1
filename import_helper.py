"""
import_helper.py
Helper script to populate the Student Course Registration database with custom data.
You can either edit the sample_data list below or call import_from_csv('your_file.csv').
"""

import os
from db_manager import CourseDB

# You can paste your dataset here:
sample_data = [
    {
        "reg_no": "21BCE1001",
        "student_name": "Aarav Sharma",
        "slot": "A1+TA1",
        "subject": "Database Management Systems",
        "faculty_id": "FAC101",
        "faculty_name": "Dr. Ramesh Kumar"
    },
    {
        "reg_no": "21BCE1001",
        "student_name": "Aarav Sharma",
        "slot": "B1+TB1",
        "subject": "Operating Systems",
        "faculty_id": "FAC105",
        "faculty_name": "Prof. Sunita Rao"
    },
    {
        "reg_no": "21BCE1042",
        "student_name": "Priya Patel",
        "slot": "C1+TC1",
        "subject": "Computer Networks",
        "faculty_id": "FAC108",
        "faculty_name": "Dr. K. Venkatesh"
    },
    {
        "reg_no": "21BCE1088",
        "student_name": "Rohan Verma",
        "slot": "A1+TA1",
        "subject": "Database Management Systems",
        "faculty_id": "FAC101",
        "faculty_name": "Dr. Ramesh Kumar"
    }
]


def load_custom_data(data_list=None):
    """Inserts a list of dictionaries into the database."""
    db = CourseDB()
    data = data_list if data_list is not None else sample_data
    print(f"Importing {len(data)} records...")
    success, failed = db.batch_insert(data)
    print(f"Import Complete: {success} succeeded, {failed} failed / duplicate.")


def import_csv(file_path: str):
    """Imports from a CSV file into the database."""
    import csv
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    db = CourseDB()
    records = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "reg_no": row.get("reg_no") or row.get("Reg. No.") or row.get("Reg No") or "",
                "student_name": row.get("student_name") or row.get("Name") or row.get("Student Name") or "",
                "slot": row.get("slot") or row.get("Slot") or "",
                "subject": row.get("subject") or row.get("Subject") or "",
                "faculty_id": row.get("faculty_id") or row.get("Faculty ID") or row.get("faculy ID") or "",
                "faculty_name": row.get("faculty_name") or row.get("Faculty Name") or row.get("Faculty") or ""
            })
    success, failed = db.batch_insert(records)
    print(f"CSV Import Complete: {success} succeeded, {failed} failed / duplicate.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
        print(f"Loading from CSV: {csv_file}")
        import_csv(csv_file)
    else:
        print("Loading sample starter data into database...")
        load_custom_data()
