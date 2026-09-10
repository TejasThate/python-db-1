# System Architecture & Workflow Diagrams

This document details the complete end-to-end architecture and operational flow of the **Student Course Registration DBMS** (based on the FFCS model).

---

## 1. Visual Workflow Architecture

![Student Course Registration Workflow](workflow_diagram.png)

---

## 2. User & Administrative Workflow (Whiteboard Flow)

The system reflects the 3 core actors and approval flow:
- **User / Student**: Selects courses, requests additions, updates, and withdrawals.
- **FFCS Coordinator**: Verifies slot clash free allocation (e.g. A1, B1), credit limits, and faculty workloads.
- **Account Section**: Validates fee status, authorizes credit registration, and commits enrollment.

```mermaid
sequenceDiagram
    autonumber
    actor Student as User / Student
    actor FFCS as FFCS Coordinator
    actor Accounts as Account Section
    participant App as Application (app.py)
    participant DB as DBMS (db_manager.py)

    Note over Student, Accounts: Course Registration Phase
    Student->>FFCS: Submits Course & Slot Preferences
    FFCS->>FFCS: Validates Timetable & Slot Clash
    FFCS->>Accounts: Forwards Approved Selection
    Accounts->>Accounts: Verifies Tuition / Credit Clearance
    Accounts->>App: Authorizes Enrollment Entry
    App->>DB: add_course(reg_no, name, slot, subject, faculty_id, faculty_name)
    DB-->>App: Confirms Unique Record Inserted
    App-->>Student: Registration Successful (Timetable Updated)

    Note over Student, Accounts: Course Withdrawal / Update Phase
    Student->>App: Requests Drop / Slot Change
    App->>DB: withdraw_course() / update_course()
    DB-->>App: Record Updated / Dropped
    App-->>Student: Updated Registration Status Displayed
```

---

## 3. Application Component Architecture

```mermaid
graph TD
    subgraph UI_Layer["User Interaction Layer"]
        CLI["app.py<br/>(Interactive CLI Menu)"]
        Importer["import_helper.py<br/>(CSV / List Importer)"]
    end

    subgraph Logic_Layer["Business Logic & Data Access Layer"]
        Manager["db_manager.py<br/>(CourseDB Class)"]
        F1["add_course()"]
        F2["withdraw_course()"]
        F3["update_course()"]
        F4["get_courses_by_student()"]
        F5["get_all_registrations()"]
        F6["batch_insert()"]
    end

    subgraph Storage_Layer["Database Storage Layer"]
        SQLite[("course_registration.db<br/>(SQLite3 Engine)")]
        MSAccess[("MS Access DB (*.accdb)<br/>(Optional via pyodbc)")]
        Table["Table: course_registrations<br/>• reg_no (TEXT)<br/>• student_name (TEXT)<br/>• slot (TEXT)<br/>• subject (TEXT)<br/>• faculty_id (TEXT)<br/>• faculty_name (TEXT)<br/>• UNIQUE(reg_no, subject)"]
    end

    CLI -->|Calls CRUD| Manager
    Importer -->|Calls batch_insert| Manager

    Manager --> F1
    Manager --> F2
    Manager --> F3
    Manager --> F4
    Manager --> F5
    Manager --> F6

    F1 & F2 & F3 & F4 & F5 & F6 --> SQLite
    F1 & F2 & F3 & F4 & F5 & F6 -.-> MSAccess
    SQLite --- Table
```

---

## 4. Operation Flowcharts

### A. Add Course Flow
```mermaid
flowchart TD
    Start([User Inputs Course Details]) --> InputCheck{Are all 6 fields<br/>provided?}
    InputCheck -- No --> ErrorFields[Show validation error] --> End([Return])
    InputCheck -- Yes --> CheckDup{Does (reg_no, subject)<br/>already exist?}
    CheckDup -- Yes --> ErrorDup[Raise Unique Constraint Error:<br/>Student already enrolled in this course] --> End
    CheckDup -- No --> InsertSQL[Execute INSERT INTO course_registrations]
    InsertSQL --> Commit[Commit Transaction]
    Commit --> Success[Display Success & Updated Table] --> End
```

### B. Withdraw Course Flow
```mermaid
flowchart TD
    StartW([User requests Course Withdrawal]) --> QueryRec{Record exists for<br/>reg_no & subject?}
    QueryRec -- No --> NotFound[Display: No matching registration found] --> EndW([Return])
    QueryRec -- Yes --> ConfirmPrompt{Confirm withdrawal?}
    ConfirmPrompt -- No --> Cancelled[Operation Cancelled] --> EndW
    ConfirmPrompt -- Yes --> DeleteSQL[Execute DELETE FROM course_registrations]
    DeleteSQL --> CommitW[Commit Transaction]
    CommitW --> SuccessW[Display: Course successfully withdrawn] --> EndW
```

### C. Update Course Flow
```mermaid
flowchart TD
    StartU([User requests Course Update]) --> FetchCurrent[Fetch existing record by reg_no & subject]
    FetchCurrent --> FoundRec{Record found?}
    FoundRec -- No --> ErrorNotFound[Display: Record not found] --> EndU([Return])
    FoundRec -- Yes --> PromptFields[Prompt new Slot, Subject, Faculty ID, or Faculty Name]
    PromptFields --> AnyChanges{Any field modified?}
    AnyChanges -- No --> NoOp[Keep current values] --> EndU
    AnyChanges -- Yes --> ExecUpdate[Execute dynamic UPDATE with sanitized parameters]
    ExecUpdate --> CommitU[Commit Transaction & Fetch updated row]
    CommitU --> DisplayTable[Display Updated Table] --> EndU
```
