"""
app.py
Interactive CLI for Student Course Registration DBMS.
Implements menus for:
1. Add Course
2. Withdraw Course
3. Update Registration
4. View Courses for a Student
5. View All Course Registrations
6. Import Data from CSV
7. Exit
"""

import os
import sys
from db_manager import CourseDB


def print_table(rows):
    if not rows:
        print("\n[!] No records found.\n")
        return

    headers = ["Reg. No.", "Student Name", "Slot", "Subject", "Faculty ID", "Faculty Name"]
    col_keys = ["reg_no", "student_name", "slot", "subject", "faculty_id", "faculty_name"]

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, k in enumerate(col_keys):
            col_widths[i] = max(col_widths[i], len(str(row.get(k, ""))))

    # Separator
    sep = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
    header_row = "|" + "|".join([f" {headers[i].ljust(col_widths[i])} " for i in range(len(headers))]) + "|"

    print("\n" + sep)
    print(header_row)
    print(sep)
    for row in rows:
        line = "|" + "|".join([f" {str(row.get(col_keys[i], '')).ljust(col_widths[i])} " for i in range(len(col_keys))]) + "|"
        print(line)
    print(sep + "\n")


def main():
    db = CourseDB()
    print("=" * 60)
    print("      STUDENT COURSE REGISTRATION SYSTEM (DBMS)       ")
    print("=" * 60)

    while True:
        print("\n--- MENU ---")
        print("1. Add Course")
        print("2. Withdraw Course")
        print("3. Update Registration")
        print("4. View Courses by Student Reg. No.")
        print("5. View All Registrations")
        print("6. Bulk Import from CSV")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            print("\n[+] Add Course")
            reg_no = input("Enter Student Reg. No. : ").strip()
            student_name = input("Enter Student Name     : ").strip()
            slot = input("Enter Slot (e.g. A1)   : ").strip()
            subject = input("Enter Subject Name/Code: ").strip()
            faculty_id = input("Enter Faculty ID       : ").strip()
            faculty_name = input("Enter Faculty Name     : ").strip()

            if not all([reg_no, student_name, slot, subject, faculty_id, faculty_name]):
                print("[!] All fields are required.")
                continue

            success = db.add_course(reg_no, student_name, slot, subject, faculty_id, faculty_name)
            if success:
                print(f"[✓] Course '{subject}' successfully added for student '{reg_no}'.")
            else:
                print("[x] Failed to add course.")

        elif choice == "2":
            print("\n[-] Withdraw Course")
            reg_no = input("Enter Student Reg. No. : ").strip()
            subject = input("Enter Subject to drop  : ").strip()

            if not reg_no or not subject:
                print("[!] Reg. No. and Subject are required.")
                continue

            confirm = input(f"Are you sure you want to withdraw '{subject}' for '{reg_no}'? (y/n): ").strip().lower()
            if confirm == 'y':
                success = db.withdraw_course(reg_no, subject)
                if success:
                    print(f"[✓] Successfully withdrawn '{subject}' for student '{reg_no}'.")
                else:
                    print(f"[!] No matching registration found for '{reg_no}' and '{subject}'.")

        elif choice == "3":
            print("\n[*] Update Registration")
            reg_no = input("Enter Student Reg. No. : ").strip()
            subject = input("Enter Current Subject  : ").strip()

            existing = db.get_registration(reg_no, subject)
            if not existing:
                print(f"[!] No existing registration found for Reg. No '{reg_no}' and Subject '{subject}'.")
                continue

            print("\nCurrent Record:")
            print_table([existing])
            print("Leave blank to keep current value:")
            
            new_slot = input(f"New Slot [{existing['slot']}]: ").strip() or None
            new_subject = input(f"New Subject [{existing['subject']}]: ").strip() or None
            new_faculty_id = input(f"New Faculty ID [{existing['faculty_id']}]: ").strip() or None
            new_faculty_name = input(f"New Faculty Name [{existing['faculty_name']}]: ").strip() or None
            new_student_name = input(f"New Student Name [{existing['student_name']}]: ").strip() or None

            success = db.update_course(
                reg_no,
                subject,
                new_slot=new_slot,
                new_subject=new_subject,
                new_faculty_id=new_faculty_id,
                new_faculty_name=new_faculty_name,
                new_student_name=new_student_name
            )

            if success:
                print("[✓] Registration updated successfully.")
                updated_sub = new_subject if new_subject else subject
                updated = db.get_registration(reg_no, updated_sub)
                if updated:
                    print_table([updated])
            else:
                print("[x] Update failed.")

        elif choice == "4":
            print("\n[?] Search Courses by Student")
            reg_no = input("Enter Student Reg. No. : ").strip()
            rows = db.get_courses_by_student(reg_no)
            print_table(rows)

        elif choice == "5":
            print("\n[=] All Registered Courses")
            rows = db.get_all_registrations()
            print_table(rows)

        elif choice == "6":
            csv_path = input("Enter CSV file path: ").strip()
            if not os.path.exists(csv_path):
                print(f"[!] File not found: {csv_path}")
                continue
            
            import csv
            records = []
            try:
                with open(csv_path, mode='r', encoding='utf-8') as f:
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
                print(f"[✓] Imported {success} records successfully. ({failed} failed/duplicates)")
            except Exception as e:
                print(f"[x] Error reading CSV: {e}")

        elif choice == "7":
            print("\nExiting Student Course DBMS. Goodbye!")
            sys.exit(0)
        else:
            print("[!] Invalid option. Please choose between 1 and 7.")


if __name__ == "__main__":
    main()
