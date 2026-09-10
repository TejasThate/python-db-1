"""
generate_diagram.py
Generates a high-resolution, modern workflow diagram image (workflow_diagram.png)
representing the Student Course Registration System (FFCS / DBMS).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_workflow_diagram():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    fig.patch.set_facecolor('#0f172a') # Dark slate modern background
    ax.set_facecolor('#0f172a')

    # Title & Subtitle
    plt.text(8, 10.3, "STUDENT COURSE REGISTRATION SYSTEM (FFCS / DBMS)", 
             fontsize=18, fontweight='bold', color='#38bdf8', ha='center')
    plt.text(8, 9.9, "End-to-End Workflow: Roles, Application Logic, Operations & Database Architecture", 
             fontsize=11, color='#94a3b8', ha='center')

    # Box styling helper
    def draw_card(x, y, w, h, title, items, header_bg='#1e293b', border_col='#38bdf8', title_col='#f8fafc'):
        # Card body
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.15",
                                      facecolor='#1e293b', edgecolor=border_col, linewidth=2)
        ax.add_patch(rect)
        # Header banner
        header = patches.FancyBboxPatch((x, y + h - 0.65), w, 0.65, boxstyle="round,pad=0.1,rounding_size=0.15",
                                        facecolor=header_bg, edgecolor='none')
        ax.add_patch(header)
        # Title text
        ax.text(x + w / 2, y + h - 0.35, title, fontsize=11, fontweight='bold', color=title_col, ha='center', va='center')
        # Body items
        curr_y = y + h - 0.95
        for item in items:
            ax.text(x + 0.25, curr_y, item, fontsize=9.5, color='#cbd5e1', va='center')
            curr_y -= 0.4

    # Arrow helper
    def draw_arrow(x1, y1, x2, y2, label="", col='#38bdf8'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(facecolor=col, edgecolor=col, width=2, headwidth=8, headlength=8, shrink=0.08))
        if label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(mid_x, mid_y + 0.15, label, fontsize=8.5, fontweight='bold', color='#e2e8f0', ha='center',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#0f172a', edgecolor=col, alpha=0.9))

    # --- ROW 1: USER ROLES (From Whiteboard) ---
    draw_card(0.8, 6.8, 4.2, 2.4, "1. USER / STUDENT", [
        "• Selects desired Course & Slot",
        "• Initiates Add Course Request",
        "• Requests Course Withdrawal",
        "• Requests Slot/Faculty Update"
    ], header_bg='#0369a1', border_col='#38bdf8')

    draw_card(5.9, 6.8, 4.2, 2.4, "2. FFCS COORDINATOR", [
        "• Validates Slot Conflicts (A1, B1...)",
        "• Verifies Faculty Allocation",
        "• Monitors Seat Limits & Credits",
        "• Approves Registration Changes"
    ], header_bg='#047857', border_col='#34d399')

    draw_card(11.0, 6.8, 4.2, 2.4, "3. ACCOUNT SECTION", [
        "• Verifies Tuition Fee Clearance",
        "• Validates Student Credit Limit",
        "• Authorizes Course Enrollment",
        "• Finalizes Registration Clearance"
    ], header_bg='#b45309', border_col='#fbbf24')

    # Connecting arrows between roles
    draw_arrow(5.0, 8.0, 5.9, 8.0, "Course Choice")
    draw_arrow(10.1, 8.0, 11.0, 8.0, "Credit Approval")

    # Arrow from roles to application
    draw_arrow(13.1, 6.8, 13.1, 5.7, "Final Authorization")

    # --- ROW 2: APPLICATION & INTERFACE LAYER ---
    draw_card(0.8, 3.7, 4.2, 2.2, "INTERACTIVE CLIENT (app.py)", [
        "• Menu 1: Add Course",
        "• Menu 2: Withdraw Course",
        "• Menu 3: Update Registration",
        "• Menu 4/5: Query & View",
        "• Menu 6: Bulk CSV Import"
    ], header_bg='#4338ca', border_col='#818cf8')

    draw_card(5.9, 3.7, 4.2, 2.2, "DATA IMPORTER (import_helper.py)", [
        "• Loads Raw Python Data / Lists",
        "• Parses External CSV Files",
        "• Validates Column Headers",
        "• Executes batch_insert(...)"
    ], header_bg='#6d28d9', border_col='#c084fc')

    draw_card(11.0, 3.7, 4.2, 2.2, "BUSINESS LOGIC (db_manager.py)", [
        "• add_course(reg_no, name, slot...)",
        "• withdraw_course(reg_no, subject)",
        "• update_course(reg_no, subject...)",
        "• Duplicate Check (UNIQUE constraint)"
    ], header_bg='#be185d', border_col='#f472b6')

    # Connections in application layer
    draw_arrow(5.0, 4.8, 5.9, 4.8, "CLI Action")
    draw_arrow(10.1, 4.8, 11.0, 4.8, "Invoke Function")
    draw_arrow(2.9, 6.8, 2.9, 5.9, "Student Actions")

    # --- ROW 3: STORAGE & DATABASE LAYER ---
    draw_card(2.5, 0.4, 11.0, 2.6, "DATABASE ENGINE (SQLite / MS Access Connectivity)", [
        "Table: course_registrations",
        "Columns: [reg_no] | [student_name] | [slot] | [subject] | [faculty_id] | [faculty_name] | [created_at]",
        "Constraints: PRIMARY KEY (id), UNIQUE(reg_no, subject)",
        "Indices: idx_reg_no, idx_subject for high-speed queries",
        "Target DBMS: SQLite (course_registration.db) & Optional MS Access (*.accdb via pyodbc)"
    ], header_bg='#0f766e', border_col='#2dd4bf')

    # Connections to DB layer (spaced out to avoid text collision)
    draw_arrow(13.2, 3.7, 11.5, 3.0, "SQL Execute", col='#2dd4bf')
    draw_arrow(5.5, 3.0, 7.5, 3.7, "Data Import", col='#c084fc')
    draw_arrow(8.5, 3.0, 9.5, 3.7, "Query Results", col='#fbbf24')

    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')

    plt.tight_layout()
    output_path = "workflow_diagram.png"
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"[OK] Workflow diagram generated: {output_path}")

if __name__ == "__main__":
    create_workflow_diagram()
