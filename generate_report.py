"""
Script to generate the MSBTE Micro-Project Report adhering strictly to:
1. Micro_ Format.pdf front matter layout.
2. Typography: Times New Roman exclusively.
   - Title / Main Headings: 16 pt, Bold.
   - Subtitles / Subheadings: 14 pt, Bold.
   - Body Text & Content: 12 pt, Regular.
   - Line spacing: 1.5.
   - Equal 1-inch margins on all sides.
   - Pure black & white, no colors/decorative themes.
3. Front matter pages (Cover, Certificate, Group Details, Weekly Progress Report, Annexure II, Index, List of Figures, List of Tables):
   NO footer.
4. Chapters Section:
   Section break restarts page numbering at 1.
   Footer:
   - Left: "Pillai HOC College of Engineering and Technology Diploma Section, Rasayani"
   - Right: Page Number
5. Complete syllabus coverage (LLOs 1.1 to 18.1), 11 embedded screenshots, tables, and calculations.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            <w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def create_formatted_report():
    doc = docx.Document()

    # Base Normal Style: Times New Roman, 12pt, 1.5 line spacing, black text
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(6)

    # Section 1: Front Matter (Pages 1-8)
    s1 = doc.sections[0]
    s1.top_margin = Inches(1.0)
    s1.bottom_margin = Inches(1.0)
    s1.left_margin = Inches(1.0)
    s1.right_margin = Inches(1.0)
    s1.header.is_linked_to_previous = False
    s1.footer.is_linked_to_previous = False

    # Helper functions
    def heading_16(text, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=6):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(16)
        r.font.color.rgb = RGBColor(0, 0, 0)
        r.bold = True
        return p

    def heading_14(text, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(0, 0, 0)
        r.bold = True
        return p

    def body_para(text, bold_prefix=None, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, italic=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(space_after)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = 'Times New Roman'
            rb.font.size = Pt(12)
            rb.font.color.rgb = RGBColor(0, 0, 0)
            rb.bold = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        r.italic = italic
        return p

    def bullet_para(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = 'Times New Roman'
            rb.font.size = Pt(12)
            rb.font.color.rgb = RGBColor(0, 0, 0)
            rb.bold = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def plain_table(table, col_widths, headers, data, header_align=WD_ALIGN_PARAGRAPH.CENTER):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table)

        # Header row
        hdr_cells = table.rows[0].cells
        for i, h in enumerate(headers):
            hdr_cells[i].text = h
            set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = header_align
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.bold = True
                r.font.name = 'Times New Roman'
                r.font.size = Pt(12)
                r.font.color.rgb = RGBColor(0, 0, 0)

        # Data rows
        for row_data in data:
            row_cells = table.add_row().cells
            for col_idx, cell_value in enumerate(row_data):
                row_cells[col_idx].text = str(cell_value)
                set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=100, right=100)
                p = row_cells[col_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(11)
                    r.font.color.rgb = RGBColor(0, 0, 0)

        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    # ════════════════════════════════════════════════════════════════════
    # PAGE 1: TITLE PAGE (Exact format from Micro_ Format.pdf)
    # ════════════════════════════════════════════════════════════════════
    p_t1 = doc.add_paragraph()
    p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t1.paragraph_format.line_spacing = 1.5
    r1 = p_t1.add_run("MAHARASHTRA STATE BOARD OF TECHNICAL EDUCATION\n")
    r1.bold = True
    r1.font.size = Pt(14)
    r2 = p_t1.add_run("PILLAI HOC POLYTECHNIC, RASAYANI (1148)\n\n")
    r2.bold = True
    r2.font.size = Pt(16)

    r3 = p_t1.add_run("MICRO PROJECT\nACADEMIC YEAR: 2026-27\n\n\n")
    r3.bold = True
    r3.font.size = Pt(14)

    r4 = p_t1.add_run("TITLE OF PROJECT\n")
    r4.bold = True
    r4.font.size = Pt(14)

    r5 = p_t1.add_run("STUDENT COMPLAINT & FEEDBACK MANAGEMENT SYSTEM\n\n\n")
    r5.bold = True
    r5.font.size = Pt(16)

    p_t2 = doc.add_paragraph()
    p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t2.paragraph_format.line_spacing = 1.5
    p_t2.add_run("Program: Diploma in Computer Engineering\t\tProgram Code: CO\n\n")
    p_t2.add_run("Course: Software Engineering\t\tCourse Code: 315323\n\n\n\n")

    p_t3 = doc.add_paragraph()
    p_t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t3.paragraph_format.line_spacing = 1.5
    p_t3.add_run("Name of the Guide: ").bold = True
    p_t3.add_run("Prof. Priyanka Kale")

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════════
    # PAGE 2: CERTIFICATE (Exact unedited template as in Micro_ Format.pdf)
    # ════════════════════════════════════════════════════════════════════
    p_c1 = doc.add_paragraph()
    p_c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c1.paragraph_format.line_spacing = 1.5
    r_c_hdr = p_c1.add_run("MAHARASHTRA STATE\nBOARD OF TECHNICAL EDUCATION\n\n")
    r_c_hdr.bold = True
    r_c_hdr.font.size = Pt(14)

    r_c_ttl = p_c1.add_run("Certificate\n\n")
    r_c_ttl.bold = True
    r_c_ttl.font.size = Pt(16)

    p_c_body = doc.add_paragraph()
    p_c_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_c_body.paragraph_format.line_spacing = 1.5
    p_c_body.add_run("This is to certify that Mr. /Ms.  _______________________________________________________\n")
    p_c_body.add_run("Roll No.  __________ of 5th Semester of Diploma in Computer Engineering\n")
    p_c_body.add_run("of Institute PILLAI HOC POLYTECHNIC (Code: 1148) has completed the Micro Project satisfactorily in Subject - Software Engineering (Course Code: 315323) for the academic year 2026-27 as prescribed in the curriculum.\n\n")

    p_c_meta = doc.add_paragraph()
    p_c_meta.paragraph_format.line_spacing = 1.5
    p_c_meta.add_run("Place: Rasayani                                      Enrollment No: __________________\n")
    p_c_meta.add_run("Date:  ______________                                Exam. Seat No: __________________\n\n\n\n\n")

    p_c_sigs = doc.add_paragraph()
    p_c_sigs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_c_sigs.paragraph_format.line_spacing = 1.3
    p_c_sigs.add_run("Subject Teacher                  Head of the Department                       Principal\n")
    p_c_sigs.add_run("(Prof. Priyanka Kale)            (Computer Engineering)                       (Pillai HOC Polytechnic)")

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════════
    # PAGE 3: GROUP DETAILS (Exact table from Micro_ Format.pdf)
    # ════════════════════════════════════════════════════════════════════
    heading_16("Group Details:\n", align=WD_ALIGN_PARAGRAPH.LEFT)

    tbl_grp = doc.add_table(rows=1, cols=5)
    headers_grp = ["Sr.\nNo.", "Names of Group Member", "Roll\nNo.", "Enrollment\nNo.", "Seat No."]
    widths_grp = [0.8, 2.5, 0.9, 1.3, 1.0]
    data_grp = [
        ["1", "Chetan Amit Sonawane", "", "25112270317", ""],
        ["2", "GAWAND SHUBHAM NARESH", "", "25112270309", ""],
        ["3", "KAVYA RAJENDRA PATIL", "", "25112270322", ""]
    ]
    plain_table(tbl_grp, widths_grp, headers_grp, data_grp)

    p_g_bot = doc.add_paragraph()
    p_g_bot.paragraph_format.space_before = Pt(40)
    p_g_bot.paragraph_format.line_spacing = 1.5
    p_g_bot.add_run("   Name of the Guide:  ").bold = True
    p_g_bot.add_run("Prof. Priyanka Kale")

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════════
    # PAGE 4: WEEKLY PROGRESS REPORT (Exact table from Micro_ Format.pdf)
    # ════════════════════════════════════════════════════════════════════
    p_wp_hdr = doc.add_paragraph()
    p_wp_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_wp_hdr.paragraph_format.line_spacing = 1.5
    r_wp1 = p_wp_hdr.add_run("WEEKLY PROGRESS  REPORT\n\nMICRO PROJECT\n")
    r_wp1.bold = True
    r_wp1.font.size = Pt(14)

    tbl_wp = doc.add_table(rows=1, cols=5)
    headers_wp = ["SR.NO.", "WEEK", "ACTIVITY", "DATE OF\nOBSERVATION", "SIGN OF THE\nGUIDE"]
    widths_wp = [0.7, 0.8, 3.1, 1.1, 0.8]
    data_wp = [
        ["1", "1st", "Discussion and finalization of Project Title; team formation and role allocation.", "Week 1", ""],
        ["2", "2nd", "Formulation of Problem Statement with bounded scope & initial feasibility study.", "Week 2", ""],
        ["3", "3rd", "Selection and justification of Process Model (Agile Scrum & Incremental approach).", "Week 3", ""],
        ["4", "4th", "Requirements gathering through student, hostel warden & faculty interviews.", "Week 4", ""],
        ["5", "5th", "Preparation of comprehensive Software Requirement Specification (SRS) document.", "Week 5", ""],
        ["6", "6th", "Design of Use Case Diagrams, Use Case Scenarios, and System Activity Diagrams.", "Week 6", ""],
        ["7", "7th", "Data modeling: DFD Level 0 (Context), DFD Level 1, and Entity-Relationship (ERD).", "Week 7", ""],
        ["8", "8th", "Detailed design: Class Diagram, Sequence Diagram, State Transition & Decision Table.", "Week 8", ""],
        ["9", "9th", "Implementation: Frontend architecture (HTML5/CSS3/Vanilla JS & Jinja2 Templates).", "Week 9", ""],
        ["10", "10th", "Implementation: Backend Flask server, SQLite relational models, authentication & sessions.", "Week 10", ""],
        ["11", "11th", "Testing: Black Box test suite preparation, execution, validation & defect logging.", "Week 11", ""],
        ["12", "12th", "Cost estimation (COCOMO, FP), PERT/CPM scheduling, SQA plan & final report compilation.", "Week 12", ""]
    ]
    plain_table(tbl_wp, widths_wp, headers_wp, data_wp)

    p_wp_bot = doc.add_paragraph()
    p_wp_bot.paragraph_format.space_before = Pt(30)
    p_wp_bot.paragraph_format.line_spacing = 1.5
    p_wp_bot.add_run("  Signature of the Guide: ____________________________________")

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════════
    # PAGE 5: ANNEXURE II EVALUATION SHEET (Exact format from Micro_ Format.pdf)
    # ════════════════════════════════════════════════════════════════════
    p_an_hdr = doc.add_paragraph()
    p_an_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_an_hdr.paragraph_format.line_spacing = 1.5
    r_an1 = p_an_hdr.add_run("ANNEXURE II\nEvaluation Sheet for the Micro Project\n")
    r_an1.bold = True
    r_an1.font.size = Pt(14)

    p_an_meta = doc.add_paragraph()
    p_an_meta.paragraph_format.line_spacing = 1.5
    p_an_meta.add_run("Academic Year: 2026-27                        Name of the Faculty: Prof. Priyanka Kale\n")
    p_an_meta.add_run("Course: Software Engineering    Course Code: 315323    Semester: 5th\n")
    p_an_meta.add_run("Title of the Project: Student Complaint & Feedback Management System\n")

    p_an_co = doc.add_paragraph()
    p_an_co.paragraph_format.line_spacing = 1.5
    p_an_co.add_run("COs addressed by Micro Project:\n").bold = True
    p_an_co.add_run("A: CO-1: Identify software development process model for given problem statement.\n")
    p_an_co.add_run("B: CO-2: Prepare SRS document for given problem statement.\n")
    p_an_co.add_run("C: CO-3: Apply software modeling and design principles for system design.\n")
    p_an_co.add_run("D: CO-4: Estimate software project cost and size.\n")
    p_an_co.add_run("E: CO-5: Prepare project schedule using project management techniques.\n")
    p_an_co.add_run("F: CO-6: Prepare SQA plan to ensure quality product and process.\n")

    p_an_out = doc.add_paragraph()
    p_an_out.paragraph_format.line_spacing = 1.5
    p_an_out.add_run("Major learning outcomes achieved by students by doing the project:\n").bold = True
    p_an_out.add_run("Practical Outcome: Design and development of a full-stack web application following software engineering lifecycle phases.\n")
    p_an_out.add_run("Unit outcomes in Cognitive domain: Formulating SRS, UML models, Black Box test suites, Function Points and COCOMO calculations.\n")
    p_an_out.add_run("Outcomes in Affective domain: Professional teamwork, peer code reviews, documentation integrity, and adherence to ethics.\n")

    p_an_com = doc.add_paragraph()
    p_an_com.paragraph_format.line_spacing = 1.5
    p_an_com.add_run("Comments/suggestions about team work /leadership/inter-personal communication (if any):\n").bold = True
    p_an_com.add_run("...........................................................................................................................................................\n")
    p_an_com.add_run("...........................................................................................................................................................\n")

    tbl_an = doc.add_table(rows=1, cols=5)
    headers_an = [
        "Roll No.",
        "Student Name",
        "Marks out of 6\nfor performance\nin group activity\n(D5 Col.8)",
        "Marks out of 4\nfor\nperformance\nin oral/\npresentation\n(D5 Col.9)",
        "Total out\nof 10"
    ]
    widths_an = [0.9, 2.3, 1.3, 1.2, 0.8]
    data_an = [
        ["", "Chetan Amit Sonawane", "", "", ""],
        ["", "GAWAND SHUBHAM NARESH", "", "", ""],
        ["", "KAVYA RAJENDRA PATIL", "", "", ""]
    ]
    plain_table(tbl_an, widths_an, headers_an, data_an)

    p_an_sig = doc.add_paragraph()
    p_an_sig.paragraph_format.space_before = Pt(30)
    p_an_sig.paragraph_format.line_spacing = 1.5
    p_an_sig.add_run("(Signature of Faculty)\nProf. Priyanka Kale")

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════════
    # PAGE 6: INDEX / TABLE OF CONTENTS
    # ════════════════════════════════════════════════════════════════════
    heading_16("INDEX / TABLE OF CONTENTS\n", align=WD_ALIGN_PARAGRAPH.CENTER)

    tbl_idx = doc.add_table(rows=1, cols=3)
    headers_idx = ["Sr. No.", "Topic / Chapter Name", "Page No."]
    widths_idx = [0.8, 4.7, 1.0]
    data_idx = [
        ["--", "PART A: MICRO-PROJECT PROPOSAL", "1"],
        ["", "1.0 Aims / Benefits of the Micro-Project", "1"],
        ["", "2.0 Proposed Methodology", "1"],
        ["", "3.0 Action Plan (12-Week Execution Schedule)", "2"],
        ["", "4.0 Resources Required", "2"],
        ["--", "PART B: TECHNICAL PROJECT REPORT", "3"],
        ["1", "CHAPTER 1: INTRODUCTION & PROBLEM STATEMENT", "3"],
        ["", "1.1 Background & Problem Statement", "3"],
        ["", "1.2 Problem Title with Bounded Scope", "4"],
        ["2", "CHAPTER 2: SOFTWARE PROCESS MODEL SELECTION", "4"],
        ["", "2.1 Process Model Selection: Agile Scrum & Incremental Approach", "4"],
        ["", "2.2 Technical Justification for Agile Methodology", "5"],
        ["3", "CHAPTER 3: SOFTWARE REQUIREMENT ENGINEERING", "5"],
        ["", "3.1 Requirement Elicitation & Gathering Techniques", "5"],
        ["", "3.2 Software Requirement Specification (SRS) - Functional Requirements", "6"],
        ["", "3.3 Non-Functional Requirements (NFR)", "6"],
        ["4", "CHAPTER 4: SOFTWARE MODELING & SYSTEM DESIGN", "7"],
        ["", "4.1 Use Case Modeling & Construct Use Cases", "7"],
        ["", "4.2 Activity Diagram", "8"],
        ["", "4.3 Data Flow Diagrams (DFD Level 0 & Level 1)", "8"],
        ["", "4.4 Entity-Relationship (ER) Diagram & Relational Schema", "9"],
        ["", "4.5 UML Class Diagram & State Transition Diagram", "10"],
        ["", "4.6 Grievance Routing Decision Table", "11"],
        ["5", "CHAPTER 5: SOFTWARE TESTING & QUALITY ASSURANCE", "12"],
        ["", "5.1 Black Box Testing Strategy", "12"],
        ["", "5.2 Black Box Test Cases Matrix (TC-01 to TC-10)", "12"],
        ["", "5.3 Software Quality Assurance (SQA) Plan", "14"],
        ["6", "CHAPTER 6: PROJECT MANAGEMENT & COST ESTIMATION", "15"],
        ["", "6.1 Risk Management (RMMM Plan)", "15"],
        ["", "6.2 Function Point (FP) Sizing Metric", "16"],
        ["", "6.3 COCOMO Cost & Effort Estimation (Organic Mode)", "17"],
        ["", "6.4 Project Scheduling: CPM / PERT & Critical Path", "18"],
        ["7", "CHAPTER 7: RESULTS & USER INTERFACE SCREENSHOTS", "19"],
        ["8", "CHAPTER 8: REAL-LIFE GRIEVANCE SYSTEMS BENCHMARKING", "25"],
        ["9", "CHAPTER 9: DISCUSSION, CONCLUSION & FUTURE SCOPE", "26"],
        ["10", "10.0 REFERENCES", "27"]
    ]
    plain_table(tbl_idx, widths_idx, headers_idx, data_idx)

    doc.add_page_break()

    # ════════════════════════════════════════════════════════════════════
    # PAGE 7: LIST OF FIGURES & LIST OF TABLES
    # ════════════════════════════════════════════════════════════════════
    heading_16("LIST OF FIGURES\n", align=WD_ALIGN_PARAGRAPH.CENTER)

    tbl_lof = doc.add_table(rows=1, cols=3)
    headers_lof = ["Figure No.", "Figure Caption / Description", "Page No."]
    widths_lof = [1.2, 4.3, 1.0]
    data_lof = [
        ["Figure 7.1", "Role-Based Login Screen (Student, Staff, Admin)", "19"],
        ["Figure 7.2", "Student Self-Registration Screen", "20"],
        ["Figure 7.3", "Student Dashboard Overview & Escalation Matrix", "20"],
        ["Figure 7.4", "Grievance Submission Form Interface", "21"],
        ["Figure 7.5", "Complaint Lifecycle Tracking & Audit Timeline", "21"],
        ["Figure 7.6", "Post-Resolution Student Rating & Feedback Submission", "22"],
        ["Figure 7.7", "Staff / HOD Dashboard Screen", "22"],
        ["Figure 7.8", "Staff Complaint Management & Action Remark Submission", "23"],
        ["Figure 7.9", "Administrative Control Center & SLA Policies", "23"],
        ["Figure 7.10", "Administrator User Management Directory", "24"],
        ["Figure 7.11", "Institutional Grievance Analytics & Performance Reports", "24"]
    ]
    plain_table(tbl_lof, widths_lof, headers_lof, data_lof)

    doc.add_paragraph().paragraph_format.space_before = Pt(14)
    heading_16("LIST OF TABLES\n", align=WD_ALIGN_PARAGRAPH.CENTER)

    tbl_lot = doc.add_table(rows=1, cols=3)
    headers_lot = ["Table No.", "Table Title", "Page No."]
    widths_lot = [1.2, 4.3, 1.0]
    data_lot = [
        ["Table 1", "Action Plan (12-Week Execution Schedule)", "2"],
        ["Table 2", "Resources Required (Hardware & Software)", "2"],
        ["Table 3", "Grievance Routing Decision Table", "11"],
        ["Table 4", "Black Box Test Cases Matrix (TC-01 to TC-10)", "13"],
        ["Table 5", "RMMM Risk Management Plan Matrix", "15"],
        ["Table 6", "Function Point Sizing Components Table", "16"],
        ["Table 7", "COCOMO Sizing & Mathematical Calculation Summary", "17"]
    ]
    plain_table(tbl_lot, widths_lot, headers_lot, data_lot)

    # ════════════════════════════════════════════════════════════════════
    # SECTION 2: CHAPTERS START HERE!
    # (Footer enabled: "Pillai HOC College of Engineering and Technology Diploma Section, Rasayani" on left, Page number on right starting at 1)
    # ════════════════════════════════════════════════════════════════════
    s2 = doc.add_section()
    s2.top_margin = Inches(1.0)
    s2.bottom_margin = Inches(1.0)
    s2.left_margin = Inches(1.0)
    s2.right_margin = Inches(1.0)
    s2.header.is_linked_to_previous = False
    s2.footer.is_linked_to_previous = False

    # Restart page number at 1 in Section 2
    sectPr2 = s2._sectPr
    pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")} w:start="1"/>')
    sectPr2.append(pgNumType)

    # Setup Footer with exact text and page number
    footer = s2.footer
    p_ftr = footer.paragraphs[0]
    p_ftr.text = "Pillai HOC College of Engineering and Technology Diploma Section, Rasayani\t"
    p_ftr.paragraph_format.line_spacing = 1.0
    p_ftr.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT)
    p_ftr.runs[0].font.name = "Times New Roman"
    p_ftr.runs[0].font.size = Pt(10)
    p_ftr.runs[0].font.color.rgb = RGBColor(0, 0, 0)

    # Add Page Number field to right of tab
    r_pg = p_ftr.add_run()
    r_pg.font.name = "Times New Roman"
    r_pg.font.size = Pt(10)
    r_pg.font.color.rgb = RGBColor(0, 0, 0)

    fld1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    fld_txt = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fld2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fld3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    r_pg._r.append(fld1)
    r_pg._r.append(fld_txt)
    r_pg._r.append(fld2)
    r_pg._r.append(fld3)

    # ─── PART A: MICRO-PROJECT PROPOSAL ─────────────────────────────────
    heading_16("PART A: MICRO-PROJECT PROPOSAL\n", align=WD_ALIGN_PARAGRAPH.CENTER)

    heading_14("1.0 Aims / Benefits of the Micro-Project")
    body_para("The primary aim of this micro-project is to systematically apply the fundamental principles, design patterns, testing strategies, and project management methodologies of Software Engineering (Course Code: 315323) to solve an actual, real-world campus problem: managing and resolving student complaints and feedback efficiently.")
    body_para("Key Institutional Benefits:")
    bullet_para("Elimination of paper-based logbook failures through persistent database tracking.")
    bullet_para("Clear accountability through role-based privileges for Students, Staff/HODs, and System Administrators.")
    bullet_para("Real-time lifecycle visibility (Submitted -> Assigned -> In Progress -> Resolved -> Closed).")
    bullet_para("Continuous institutional improvement through post-resolution student rating and feedback collection.")

    heading_14("2.0 Proposed Methodology")
    body_para("The project adopts an Agile Scrum & Incremental development lifecycle consisting of three 2-week iterations:")
    bullet_para("Sprint 1 (Inception & Requirements): Stakeholder interviews, SRS specification, Use Case and Activity modeling.")
    bullet_para("Sprint 2 (Design & Core Development): Relational database modeling (DFD & ERD), Flask server routing, and Student portal UI.")
    bullet_para("Sprint 3 (Resolution Workflow, Testing & SQA): Staff assignment engine, status transitions, Black Box test execution, COCOMO sizing, and report generation.")

    heading_14("3.0 Action Plan (12-Week Execution Schedule)")
    body_para("Table 1 summarizes the milestone timeline and work allocation among group members:")

    tbl_ap = doc.add_table(rows=1, cols=5)
    headers_ap = ["Sr.", "Milestone / Detail of Activity", "Planned Start", "Planned Finish", "Responsible Member"]
    widths_ap = [0.5, 3.1, 1.0, 1.0, 1.4]
    data_ap = [
        ["1", "Problem Identification & Scope Bounding", "Week 1", "Week 2", "All Members"],
        ["2", "Process Model Selection & Agile Sprint Planning", "Week 3", "Week 3", "Chetan Sonawane"],
        ["3", "Requirements Elicitation & Broad SRS Document", "Week 4", "Week 5", "Kavya Patil"],
        ["4", "UML Design: Use Case, Activity & Sequence Models", "Week 6", "Week 6", "Chetan Sonawane"],
        ["5", "Data Flow (DFD 0/1) & Entity-Relationship Modeling", "Week 7", "Week 7", "Gawand Shubham"],
        ["6", "Detailed Design: Class Diagram & Decision Table", "Week 8", "Week 8", "Gawand Shubham"],
        ["7", "Frontend Implementation (Responsive UI/UX)", "Week 9", "Week 9", "Chetan Sonawane"],
        ["8", "Backend Server & Relational Database Coding", "Week 10", "Week 10", "Gawand Shubham"],
        ["9", "Black Box Software Test Execution & Validation", "Week 11", "Week 11", "Kavya Patil"],
        ["10", "COCOMO Sizing, FP Matrix, CPM/PERT & SQA Plan", "Week 12", "Week 12", "Kavya Patil"],
        ["11", "Final Micro-Project Report Compilation & Review", "Week 12", "Week 12", "All Members"]
    ]
    plain_table(tbl_ap, widths_ap, headers_ap, data_ap)

    heading_14("4.0 Resources Required")
    body_para("Table 2 lists the hardware and software tools utilized during project execution:")

    tbl_res = doc.add_table(rows=1, cols=4)
    headers_res = ["Sr. No.", "Resource / Tool Name", "Specifications / Version", "Purpose"]
    widths_res = [0.6, 2.0, 2.3, 2.1]
    data_res = [
        ["1", "Hardware (PC / Laptop)", "Intel Core i3/i5, 8GB RAM, 256GB SSD", "Development, Modeling & Testing"],
        ["2", "Operating System", "Windows 10 / 11 (64-bit)", "Platform environment"],
        ["3", "Development Stack", "Python 3.11, Flask 3.1, SQLite, HTML5, CSS3", "Full-Stack Web App Execution"],
        ["4", "UML & Modeling Tools", "Draw.io, PlantUML, VS Code", "DFD, ER, Class & Sequence Diagrams"],
        ["5", "Documentation Tools", "Microsoft Word, python-docx, Git", "Report preparation & Version Control"]
    ]
    plain_table(tbl_res, widths_res, headers_res, data_res)

    doc.add_page_break()

    # ─── PART B: CHAPTER 1 ──────────────────────────────────────────────
    heading_16("PART B: TECHNICAL PROJECT REPORT\n", align=WD_ALIGN_PARAGRAPH.CENTER)

    heading_16("CHAPTER 1: INTRODUCTION & PROBLEM STATEMENT\n", align=WD_ALIGN_PARAGRAPH.LEFT)

    heading_14("1.1 Background & Problem Statement (LLO 1.1)")
    body_para("In polytechnic institutes, colleges, and university campuses, hundreds of students encounter daily grievances concerning hostel facilities (e.g., plumbing, electrical fixtures), mess food hygiene and quality, computer and electronics laboratory equipment breakdowns, faculty syllabus completion pacing, and library resource availability. Historically, these complaints were lodged via paper-based complaint registers kept at department desks or warden offices.")
    body_para("Severe Bottlenecks in the Conventional Paper System:")
    bullet_para("Complaint Loss & Oversight: Paper registers frequently suffer from damaged pages, illegible handwriting, or complete misplacement.")
    bullet_para("Zero Status Visibility: Students have no mechanism to track whether an issue has been reviewed, dispatched to a technician, or resolved.")
    bullet_para("Lack of Accountability: Campus authorities cannot verify how long tickets remain open or which staff member was assigned to resolve them.")
    bullet_para("No Audit Trail or Feedback: Once verbal resolution is claimed, there is no system to record student satisfaction or calculate institutional performance metrics.")

    heading_14("1.2 Problem Title with Bounded Scope")
    body_para("Project Title: Student Complaint & Feedback Management System (SCFMS)", bold_prefix=None, italic=True)
    body_para("Bounded Scope: The system is designed specifically as an intranet and web portal for Pillai HOC Polytechnic, Rasayani. It covers five primary campus grievance categories (Hostel, Mess, Laboratories, Faculty/Academics, Library) plus General Campus amenities. It implements role-based interfaces for Students, Staff/HODs, and System Administrators with automated audit logging and post-resolution student rating.")

    doc.add_page_break()

    # ─── CHAPTER 2 ──────────────────────────────────────────────────────
    heading_16("CHAPTER 2: SOFTWARE PROCESS MODEL SELECTION (LLO 2.1)\n", align=WD_ALIGN_PARAGRAPH.LEFT)

    heading_14("2.1 Process Model Selection: Agile Scrum & Incremental Approach")
    body_para("For the development of this micro-project, the Agile Scrum Methodology combined with an Incremental Process Model was selected over the traditional Linear Sequential (Waterfall) Model.")

    heading_14("2.2 Technical Justification for Agile Methodology")
    bullet_para("Shorter Development Cycles: Micro-projects operate within a strict 12-week semester timeframe. Agile allows breaking development into three manageable 2-week sprints.")
    bullet_para("Continuous Verification & Early Prototypes: In Sprint 1, the student portal and complaint logging mechanism were functional, enabling immediate feedback from teachers and peers.")
    bullet_para("Evolving Requirements: Additional attributes like urgency-based decision tables and multi-role audit timelines were incorporated iteratively without destabilizing prior modules.")
    bullet_para("Direct Mapping to Software Engineering Practicals: Agile allows documentation (SRS, DFD, ERD, Test cases) to evolve synchronously alongside code development.")

    doc.add_page_break()

    # ─── CHAPTER 3 ──────────────────────────────────────────────────────
    heading_16("CHAPTER 3: SOFTWARE REQUIREMENT ENGINEERING (LLOs 3.1 & 4.1)\n", align=WD_ALIGN_PARAGRAPH.LEFT)

    heading_14("3.1 Requirement Elicitation & Gathering Techniques (LLO 3.1)")
    body_para("Requirements were gathered through structured interviews with 10 students across Computer, Mechanical, and Civil branches, 2 hostel wardens, and 2 department HODs at Pillai HOC Polytechnic. The survey revealed that 90% of students demanded digital ticket tracking, while wardens requested an urgent priority flag for sanitary and electrical safety issues.")

    heading_14("3.2 Software Requirement Specification (SRS) - Functional Requirements (LLO 4.1)")
    bullet_para("FR-1 (User Authentication): Secure role-based login and registration for Students, Faculty/Staff, and System Administrators using PBKDF2/SHA-256 password hashing.")
    bullet_para("FR-2 (Complaint Logging): Students can lodge complaints specifying Category (Hostel, Mess, Lab, Faculty, Library, Other), Priority (High, Medium, Low), Title, and detailed Description.")
    bullet_para("FR-3 (Ticket Allocation & Dispatch): Administrators can review incoming unassigned complaints and allocate them to the appropriate HOD, Warden, or Technician.")
    bullet_para("FR-4 (Progress Lifecycle Tracking): The ticket transitions strictly through state milestones: SUBMITTED -> ASSIGNED -> IN PROGRESS -> RESOLVED -> CLOSED.")
    bullet_para("FR-5 (Action Remarks & Audit Trail): Assigned staff can record resolution notes, technician actions, and change status to In Progress or Resolved.")
    bullet_para("FR-6 (Student Feedback Rating): Upon issue resolution, students can submit a 1 to 5-star rating with qualitative feedback comments.")
    bullet_para("FR-7 (Notification Alerts): Automated real-time alerts notify students upon ticket assignment and status transitions.")
    bullet_para("FR-8 (Institutional Reporting): Administrative analytics on category distribution, urgency ratios, and SLA resolution turnaround.")

    heading_14("3.3 Non-Functional Requirements (NFR)")
    bullet_para("Performance: System responds to queries and form submissions within 1.0 second on local campus network.")
    bullet_para("Security: Protection against SQL injection using SQLAlchemy ORM parameterized queries; session isolation preventing unauthorized cross-role data tampering.")
    bullet_para("Usability: Intuitive responsive interface complying with accessibility standards; mobile and desktop viewport adaptability.")
    bullet_para("Reliability: Persistent ACID-compliant SQLite relational database with cascading foreign keys to prevent orphan records.")

    doc.add_page_break()

    # ─── CHAPTER 4 ──────────────────────────────────────────────────────
    heading_16("CHAPTER 4: SOFTWARE MODELING & SYSTEM DESIGN (LLOs 5.1 to 9.1)\n", align=WD_ALIGN_PARAGRAPH.LEFT)

    heading_14("4.1 Use Case Modeling & Construct Use Cases (LLO 5.1)")
    body_para("The system defines three primary actors with distinct operational boundaries:")
    bullet_para("Student Actor: Register Account, Authenticate/Login, Submit Complaint, View Complaint Status, Read Notifications, Submit Feedback Rating.")
    bullet_para("Staff/HOD Actor: Authenticate/Login, View Assigned Complaints, Inspect Ticket Details, Update Status to In Progress/Resolved, Enter Action Notes.")
    bullet_para("Admin Actor: Authenticate/Login, Manage User Accounts, Assign Unassigned Complaints to Staff, Override Ticket Status, Delete Inappropriate Tickets, View Institutional Analytics.")

    heading_14("4.2 Activity Diagram (LLO 6.1)")
    body_para("The activity flow represents the end-to-end operational pipeline:")
    body_para("Student Logs In -> Fills Complaint Form -> Validation Check [Valid: Create Ticket Record in DB; Invalid: Display Form Error] -> Notify Admin -> Admin Reviews Ticket -> Admin Dispatches Ticket to Staff -> Staff Inspects Issue -> Staff Updates Status to 'In Progress' with Action Note -> Repair/Action Taken -> Staff Marks 'Resolved' -> Notify Student -> Student Tests Resolution -> Student Submits 1-5 Star Feedback -> Ticket Automatically Closed.")

    heading_14("4.3 Data Flow Diagrams (DFD Level 0 & Level 1) (LLO 7.1)")
    body_para("Level 0 (Context Diagram):", italic=True)
    body_para("External Entities: [Student], [Staff/HOD], [Administrator]. Central Process: (0.0 Student Complaint & Feedback Management System). Data Flows: Student sends [Registration Data, Complaint Details, Star Rating]; System returns [Status Updates, Ticket ID]. Staff sends [Resolution Notes, Status Updates]; System returns [Assigned Complaint Records]. Admin sends [User Management Commands, Staff Assignment]; System returns [Institutional Reports, Unassigned Alerts].")
    body_para("Level 1 DFD Decomposition:", italic=True)
    bullet_para("Process 1.0 (Authentication & Session): Interacts with Data Store D1 [Users Database].")
    bullet_para("Process 2.0 (Complaint Registration & Validation): Interacts with Data Store D2 [Complaints Database].")
    bullet_para("Process 3.0 (Dispatch & Ticket Allocation Engine): Interacts with D1 [Users] and D2 [Complaints].")
    bullet_para("Process 4.0 (Resolution Audit & Timeline Tracking): Interacts with Data Store D3 [Timeline Events].")
    bullet_para("Process 5.0 (Feedback Collection & Analytics): Interacts with Data Store D4 [Feedbacks] and D5 [Notifications].")

    heading_14("4.4 Entity-Relationship (ER) Diagram & Relational Schema (LLO 7.2)")
    body_para("Relational Entities & Multiplicity:")
    bullet_para("User Entity (PK: id, name, email, password_hash, role, roll_no, branch, semester, department, designation). One User (Student) submits Many Complaints (1:N). One User (Staff) is assigned Many Complaints (1:N).")
    bullet_para("Complaint Entity (PK: id, FK: student_id, FK: assigned_to, title, description, category, priority, status, created_at, updated_at). One Complaint has Many TimelineEvents (1:N). One Complaint has One Feedback (1:1).")
    bullet_para("TimelineEvent Entity (PK: id, FK: complaint_id, status, note, created_at).")
    bullet_para("Feedback Entity (PK: id, FK: complaint_id, FK: student_id, rating, comment, created_at).")
    bullet_para("Notification Entity (PK: id, FK: user_id, title, message, is_read, created_at).")

    heading_14("4.5 UML Class Diagram & State Transition Diagram (LLO 8.1)")
    body_para("Class Structure:")
    bullet_para("User Class: Attributes: id: int, name: str, email: str, role: str. Methods: set_password(), check_password(), get_assigned_tasks().")
    bullet_para("Complaint Class: Attributes: id: int, title: str, category: str, priority: str, status: str. Methods: create(), assign_to(staff_id), update_status(new_status), get_timeline().")
    bullet_para("Feedback Class: Attributes: id: int, rating: int, comment: str. Methods: submit_rating(), get_score().")
    bullet_para("NotificationService Class: Methods: dispatch_alert(user_id, title, msg), mark_read().")
    body_para("State Transition Diagram Lifecycle:", italic=True)
    body_para("[State: SUBMITTED] --(Admin assigns staff)--> [State: ASSIGNED] --(Staff begins inspection)--> [State: IN PROGRESS] --(Staff completes repair)--> [State: RESOLVED] --(Student rates feedback)--> [State: CLOSED].")

    heading_14("4.6 Grievance Routing Decision Table (LLO 9.1)")
    body_para("Table 3 outlines the formal decision rules governing institutional complaint triage:")

    tbl_dt = doc.add_table(rows=1, cols=6)
    headers_dt = ["Rule No.", "Grievance Category", "Urgency / Priority", "Assigned Authority", "SLA Target", "Escalation Action"]
    widths_dt = [0.6, 1.4, 1.2, 1.4, 1.0, 1.4]
    data_dt = [
        ["R1", "Hostel / Mess", "High (Health/Safety)", "Hostel Warden", "24 Hours", "Immediate phone alert & inspection"],
        ["R2", "Hostel / Mess", "Medium (Maintenance)", "Hostel Warden", "3 Days", "Standard maintenance queue"],
        ["R3", "Laboratory", "High (PC/Machine down)", "Department HOD", "24 Hours", "Lab assistant dispatch"],
        ["R4", "Laboratory", "Medium (Projector/Fan)", "Lab In-Charge", "48 Hours", "Routine service request"],
        ["R5", "Faculty / Academics", "High (Misconduct)", "Principal / HOD", "24 Hours", "Confidential counseling inquiry"],
        ["R6", "Faculty / Academics", "Medium (Syllabus delay)", "Department HOD", "3 Days", "Extra lecture schedule planned"],
        ["R7", "Library / Other", "Low (Minor suggestions)", "Admin / Librarian", "7 Days", "Periodic committee review"]
    ]
    plain_table(tbl_dt, widths_dt, headers_dt, data_dt)

    doc.add_page_break()

    # ─── CHAPTER 5 ──────────────────────────────────────────────────────
    heading_16("CHAPTER 5: SOFTWARE TESTING & QUALITY ASSURANCE (LLOs 10.1, 11.1, 17.1, 18.1)\n", align=WD_ALIGN_PARAGRAPH.LEFT)

    heading_14("5.1 Black Box Testing Strategy (LLO 10.1)")
    body_para("Black Box testing was conducted to validate functional requirements against system specifications without inspecting internal code logic. Techniques utilized include Equivalence Partitioning (EP) and Boundary Value Analysis (BVA).")

    heading_14("5.2 Black Box Test Cases Matrix (LLO 11.1)")
    body_para("Table 4 outlines the verification test cases executed on the system:")

    tbl_tc = doc.add_table(rows=1, cols=6)
    headers_tc = ["Test ID", "Test Scenario", "Test Input Data", "Expected Output", "Actual Result", "Status"]
    widths_tc = [0.6, 1.6, 1.5, 1.5, 1.2, 0.6]
    data_tc = [
        ["TC-01", "Student Login with valid credentials", "student@pillai.edu, student123, role=student", "Authentication succeeds, redirect to student dashboard", "Redirected to dashboard", "PASS"],
        ["TC-02", "Login with invalid password", "student@pillai.edu, wrongpass, role=student", "Display error alert 'Invalid email, password or role'", "Error alert displayed", "PASS"],
        ["TC-03", "Student Registration with mismatched passwords", "pass='student123', confirm='abc123'", "Registration fails, alert 'Passwords do not match!'", "Alert displayed", "PASS"],
        ["TC-04", "Submit Complaint with blank title", "title='', category='hostel', priority='high'", "HTML5 form validation blocks submission", "Form prompt shown", "PASS"],
        ["TC-05", "Submit valid complaint", "title='Water leakage', category='hostel', priority='high'", "Record saved in DB, ticket ID generated, status='submitted'", "Ticket created (#13)", "PASS"],
        ["TC-06", "Admin assigns complaint to staff", "complaint_id=4, staff_id=2 (Warden)", "Complaint status updated to 'assigned', notification sent", "Assigned to Warden", "PASS"],
        ["TC-07", "Staff updates status to In Progress", "status='inprogress', note='Inspection started'", "Timeline event added, student notified", "Status updated", "PASS"],
        ["TC-08", "Staff marks complaint Resolved", "status='resolved', note='Pipe repaired'", "Ticket marked resolved, feedback enabled for student", "Resolved state verified", "PASS"],
        ["TC-09", "Student submits 5-star rating", "rating=5, comment='Fixed quickly!'", "Feedback record inserted, stars displayed on ticket", "Feedback stored", "PASS"],
        ["TC-10", "Role authorization check", "Student visits /admin/dashboard directly", "Access denied, redirect to login page", "Redirected to login", "PASS"]
    ]
    plain_table(tbl_tc, widths_tc, headers_tc, data_tc)

    heading_14("5.3 Software Quality Assurance (SQA) Plan (LLOs 17.1 & 18.1)")
    body_para("The SQA Plan ensures both process quality and product quality based on ISO/IEC 25010 standards:")
    bullet_para("Process Quality: Code formatting according to PEP 8 standards, weekly peer code walkthroughs, version control commit history, and traceability from SRS to test cases.")
    bullet_para("Product Quality Attributes:")
    bullet_para("Functional Suitability: 100% of functional requirements (FR-1 to FR-8) implemented and tested.")
    bullet_para("Reliability: Graceful exception handling for invalid inputs; foreign key constraints prevent database inconsistencies.")
    bullet_para("Usability: Responsive modern web interface, clean role-based dashboards, and intuitive visual cues.")
    bullet_para("Security: PBKDF2 hashing of passwords, Flask session cryptographic signing, and role verification decorators.")
    bullet_para("Maintainability: Modular blueprint architecture separating auth, student, staff, and admin routes.")

    doc.add_page_break()

    # ─── CHAPTER 6 ──────────────────────────────────────────────────────
    heading_16("CHAPTER 6: PROJECT MANAGEMENT, SIZING & COST ESTIMATION (LLOs 12.1 to 16.1)\n", align=WD_ALIGN_PARAGRAPH.LEFT)

    heading_14("6.1 Risk Management (RMMM Plan - LLO 12.1 & 12.2)")
    body_para("Table 5 presents the Risk Mitigation, Monitoring, and Management plan:")

    tbl_rm = doc.add_table(rows=1, cols=5)
    headers_rm = ["Risk ID", "Risk Description", "Category", "Mitigation Strategy", "Monitoring & Management"]
    widths_rm = [0.6, 2.0, 1.2, 2.0, 1.2]
    data_rm = [
        ["R-01", "Team member illness or unavailability", "People", "Cross-training on frontend & backend; modular architecture.", "Weekly progress review."],
        ["R-02", "Data loss or database file corruption", "Technical", "Automated SQLite file backups; Git repository versioning.", "Daily git push."],
        ["R-03", "Scope creep / Uncontrolled feature additions", "Project", "Strictly bounded scope defined in SRS; teacher review.", "Sprint backlog freeze."],
        ["R-04", "Testing schedule slippage near deadline", "Schedule", "Test-driven verification concurrently with coding.", "Milestone tracking."]
    ]
    plain_table(tbl_rm, widths_rm, headers_rm, data_rm)

    heading_14("6.2 Function Point (FP) Sizing Metric (LLO 13.1)")
    body_para("Function Point analysis measures software size based on functionality delivered to users:")

    tbl_fp = doc.add_table(rows=1, cols=5)
    headers_fp = ["Function Component", "Description in SCFMS", "Count", "Complexity Weight", "Unadjusted FP (UFP)"]
    widths_fp = [1.5, 2.7, 0.7, 1.1, 1.0]
    data_fp = [
        ["External Inputs (EI)", "Login, Register, Add Complaint, Assign, Update Status, Submit Feedback", "6", "4 (Average)", "24"],
        ["External Outputs (EO)", "Dashboard Statistics, Alerts, Redressal Audit Report", "3", "5 (Average)", "15"],
        ["External Inquiries (EQ)", "Complaint Search, Category Filter, Audit Timeline Query", "3", "4 (Average)", "12"],
        ["Internal Logical Files (ILF)", "Users DB, Complaints DB, Timelines DB, Feedback DB, Notifications DB", "5", "10 (Average)", "50"],
        ["External Interface Files (EIF)", "SQLite engine, Browser Local Storage interface", "2", "7 (Average)", "14"],
        ["Total Unadjusted FP", "Sum of all functional components", "--", "--", "115 UFP"]
    ]
    plain_table(tbl_fp, widths_fp, headers_fp, data_fp)

    body_para("Calculation of Adjusted Function Points:")
    body_para("Formula: FP = UFP * [0.65 + 0.01 * sum(Fi)], where sum(Fi) is the Total Degree of Influence (TDI) across 14 General System Characteristics (GSCs). For SCFMS, TDI = 32 (moderate complexity).")
    body_para("Value Adjustment Factor (VAF) = 0.65 + (0.01 * 32) = 0.97")
    body_para("Adjusted Function Points (FP) = 115 * 0.97 ≈ 111.55 ≈ 112 Function Points", italic=True)

    heading_14("6.3 COCOMO Cost & Effort Estimation (Organic Mode - LLO 14.1)")
    body_para("Basic COCOMO (Constructive Cost Model) was applied using the Organic Mode, which represents small, experienced teams working in familiar application domains.")
    bullet_para("Project Size: Estimated Code Size = 3,000 Lines of Code (3.0 KLOC).")
    bullet_para("Effort Equation (Organic Mode): Effort = a * (KLOC)^b [where a = 2.4, b = 1.05]")
    body_para("Effort Calculation: Effort = 2.4 * (3.0)^1.05 = 2.4 * 3.169 ≈ 7.606 ≈ 7.6 Person-Months (PM).")
    bullet_para("Development Time Equation (Organic Mode): Time = c * (Effort)^d [where c = 2.5, d = 0.38]")
    body_para("Schedule Calculation: Time = 2.5 * (7.6)^0.38 = 2.5 * 2.158 ≈ 5.395 ≈ 5.4 Months.")
    bullet_para("Average Staff Size: Staff = Effort / Time = 7.6 / 5.4 ≈ 1.4 Developers.")
    body_para("Staffing Analysis: Since student micro-projects are part-time diploma academic activities (approx 15-20 hours/week per student), our team of 3 members matches the exact staffing requirement for semester execution.")

    heading_14("6.4 Project Scheduling: CPM / PERT & Critical Path (LLO 15.1 & 16.1)")
    body_para("Task Network and Critical Path Analysis:")
    bullet_para("Task A: Problem Formulation & Scope (Duration: 2 weeks) -> Predecessor: None")
    bullet_para("Task B: Agile Process Model Setup (Duration: 1 week) -> Predecessor: Task A")
    bullet_para("Task C: Requirements Gathering & SRS (Duration: 2 weeks) -> Predecessor: Task B")
    bullet_para("Task D: UML System Design (DFD, ER, Class) (Duration: 2 weeks) -> Predecessor: Task C [CRITICAL PATH]")
    bullet_para("Task E: Frontend & Backend Coding (Duration: 3 weeks) -> Predecessor: Task D [CRITICAL PATH]")
    bullet_para("Task F: Black Box Testing & Verification (Duration: 1 week) -> Predecessor: Task E [CRITICAL PATH]")
    bullet_para("Task G: Project Report Compilation & Documentation (Duration: 1 week) -> Predecessor: Task F [CRITICAL PATH]")
    body_para("Critical Path: A -> B -> C -> D -> E -> F -> G = Total 12 Weeks (Zero slack on critical activities).", bold_prefix="Critical Path: ", italic=True)

    doc.add_page_break()

    # ─── CHAPTER 7 ──────────────────────────────────────────────────────
    heading_16("CHAPTER 7: RESULTS & USER INTERFACE SCREENSHOTS\n", align=WD_ALIGN_PARAGRAPH.LEFT)
    body_para("The working full-stack web application was executed and captured across all major workflows. The screenshots below demonstrate the implementation of all functional requirements:")

    screenshot_dir = r"D:\Student Complaint & Feedback Management System\screenshort"
    screenshots_data = [
        ("login_page.png", "Figure 7.1: Role-Based Login Screen (Student, Staff, Admin tabs with hidden passwords)"),
        ("registerpage.png", "Figure 7.2: Student Self-Registration Screen (Branch, Semester, Enrollment No.)"),
        ("Student Dashboard.png", "Figure 7.3: Student Dashboard Overview (Status metrics, recent tickets & escalation matrix)"),
        ("Complaint Submission Form.png", "Figure 7.4: Grievance Submission Form (Category, Urgency Priority, Detailed Description)"),
        ("Complaint Detail & Audit Timeline.png", "Figure 7.5: Ticket Lifecycle Tracking & Audit Timeline Screen"),
        ("Student Rating & Feedback.png", "Figure 7.6: Post-Resolution Student Rating & Feedback Submission Interface"),
        ("staffdashboard.png", "Figure 7.7: Staff / HOD Dashboard Screen (Assigned ticket queue & pending actions)"),
        ("staff complaint page.png", "Figure 7.8: Staff Complaint Management & Action Remark Submission Screen"),
        ("Admin Dashboard & Management.png", "Figure 7.9: Administrative Control Center (Unassigned tickets & SLA guidelines)"),
        ("Admin   User Management.png", "Figure 7.10: Administrator User Management Directory"),
        ("Admin Software Engineering Analytics.png", "Figure 7.11: Institutional Grievance Analytics & Performance Reports")
    ]

    for fname, caption in screenshots_data:
        fpath = os.path.join(screenshot_dir, fname)
        if os.path.exists(fpath):
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.line_spacing = 1.5
            p_cap.paragraph_format.space_before = Pt(8)
            p_cap.paragraph_format.space_after = Pt(4)
            r_c = p_cap.add_run(caption)
            r_c.font.name = "Times New Roman"
            r_c.font.size = Pt(12)
            r_c.bold = True
            try:
                doc.add_picture(fpath, width=Inches(5.8))
                p_sp = doc.add_paragraph()
                p_sp.paragraph_format.space_after = Pt(12)
            except Exception as e:
                body_para(f"[Image: {fname} could not be embedded: {e}]", italic=True)
        else:
            body_para(f"[{caption} - Image file not found: {fname}]", italic=True)

    doc.add_page_break()

    # ─── CHAPTER 8 ──────────────────────────────────────────────────────
    heading_16("CHAPTER 8: REAL-LIFE GRIEVANCE SYSTEMS BENCHMARKING\n", align=WD_ALIGN_PARAGRAPH.LEFT)
    body_para("To validate our application design against industry standards, three real-world systems were studied:")
    bullet_para("CPGRAMS (Centralized Public Grievance Redress and Monitoring System - Govt of India): Provides centralized citizen grievance tracking across ministries with 30-day resolution targets. Our SCFMS replicates its hierarchical role delegation and escalation rules.")
    bullet_para("AICTE / UGC National Student Grievance Portal: Mandates online grievance handling for engineering institutions in India. SCFMS adopts its categorization (Hostel, Academics, Canteen, Harassment).")
    bullet_para("MoHUA Swachhata Complaint App: Citizen cleanliness reporting with photo evidence and geotracking. SCFMS adopts its 24-hour urgency SLA for sanitation and water supply issues.")

    # ─── CHAPTER 9 ──────────────────────────────────────────────────────
    heading_16("CHAPTER 9: DISCUSSION, CONCLUSION & FUTURE SCOPE\n", align=WD_ALIGN_PARAGRAPH.LEFT)

    heading_14("9.1 Outcomes Achieved")
    bullet_para("Successfully developed a fully operational, responsive web application for Student Complaint & Feedback Management.")
    bullet_para("Executed all 18 Laboratory Learning Outcomes (LLOs) prescribed by the MSBTE Software Engineering curriculum.")
    bullet_para("Validated system functionality through 10 comprehensive Black Box test cases with 100% pass rate.")
    bullet_para("Calculated accurate software sizing metrics using Function Points (112 FP) and basic COCOMO (7.6 Person-Months).")

    heading_14("9.2 Challenges Encountered & Problem Solving")
    bullet_para("Challenge 1: Handling simultaneous multi-role authorization. Solved using Flask-Login user loaders and route protection decorators.")
    bullet_para("Challenge 2: Maintaining tamper-proof timeline event tracking. Solved by implementing an append-only relational audit table.")

    heading_14("9.3 Conclusion")
    body_para("The Student Complaint & Feedback Management System provides an effective, transparent, and scalable digital solution to replace outdated paper-based complaint registers. By adhering rigorously to Software Engineering methodologies—from requirements engineering and UML modeling to black box testing and quality assurance—the project demonstrates how engineering rigor transforms an unstructured problem into an enterprise-ready software product.")

    heading_14("10.0 References")
    bullet_para("Pressman, Roger S. & Bruce R. Maxim, 'Software Engineering: A Practitioner's Approach', McGraw-Hill Higher Education, 9th Edition.")
    bullet_para("Desikan, Srinivasan & Gopalaswamy Ramesh, 'Software Testing: Principles and Practices', Pearson Education, 2007.")
    bullet_para("MSBTE Curriculum Document - Course Code 315323: Software Engineering (Semester 5, K-Scheme), Maharashtra State Board of Technical Education, Mumbai.")
    bullet_para("Centralized Public Grievance Redress and Monitoring System (CPGRAMS), Ministry of Personnel, Public Grievances and Pensions, Govt of India.")

    # Save to Word Document
    out_file = r"D:\Student Complaint & Feedback Management System\Student_Complaint_Feedback_Management_System_Micro_Project_Report.docx"
    doc.save(out_file)
    print(f"Formatted report successfully created at: {out_file}")

if __name__ == '__main__':
    create_formatted_report()
