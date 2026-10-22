"""
Script to generate the 6-slide SIH project presentation: 'sih project.pptx'
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme Colors
    NAVY = RGBColor(15, 23, 42)       # Slate 900
    INDIGO = RGBColor(67, 56, 202)     # Indigo 700
    LIGHT_BG = RGBColor(248, 250, 252) # Slate 50
    WHITE = RGBColor(255, 255, 255)
    AMBER = RGBColor(245, 158, 11)     # Amber 500
    EMERALD = RGBColor(16, 185, 129)   # Emerald 500
    TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    CARD_BG = RGBColor(241, 245, 249)  # Slate 100

    def add_header(slide, title_text, category_text):
        # Header background banner
        banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        banner.fill.solid()
        banner.fill.fore_color.rgb = NAVY
        banner.line.color.rgb = NAVY

        # Category tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_text.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = AMBER

        # Title text
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.5), Inches(0.65))
        tf = t_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = WHITE

    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY

    # Badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(4.2), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = INDIGO
    badge.line.color.rgb = INDIGO
    b_tf = badge.text_frame
    b_p = b_tf.paragraphs[0]
    b_p.text = "SMART INDIA HACKATHON 2026"
    b_p.font.size = Pt(12)
    b_p.font.bold = True
    b_p.font.color.rgb = WHITE
    b_p.alignment = PP_ALIGN.CENTER

    # Main Title
    title_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(2.2))
    t_frame = title_box.text_frame
    t_frame.word_wrap = True
    p1 = t_frame.paragraphs[0]
    p1.text = "SkillBridge AI"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = AMBER

    p2 = t_frame.add_paragraph()
    p2.text = "AI-Powered Skill Gap Analysis & Employment Outcome Tracking Platform"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

    p3 = t_frame.add_paragraph()
    p3.text = "Bridging Education, Personalized Skilling, Measurable Capability Growth, and Verified Employment"
    p3.font.size = Pt(15)
    p3.font.color.rgb = RGBColor(203, 213, 225)

    # 4 Key Pillars in bottom cards
    pillars = [
        ("Skill Gap Diagnosis", "NLP & weighted role match vs live market expectations"),
        ("Personalized Roadmap", "Sequential chronological learning rather than generic bundles"),
        ("Pre/Post Testing", "Standardized diagnostic delta testing (+Δ% capability gain)"),
        ("Longitudinal Tracking", "Post-training job relevance, starting salary & retention")
    ]
    for i, (p_title, p_desc) in enumerate(pillars):
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0 + i * 2.9), Inches(4.5), Inches(2.7), Inches(2.0))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(30, 41, 59)
        card.line.color.rgb = RGBColor(51, 65, 85)
        c_tf = card.text_frame
        c_tf.word_wrap = True
        
        cp1 = c_tf.paragraphs[0]
        cp1.text = f"0{i+1}"
        cp1.font.size = Pt(16)
        cp1.font.bold = True
        cp1.font.color.rgb = AMBER

        cp2 = c_tf.add_paragraph()
        cp2.text = p_title
        cp2.font.size = Pt(14)
        cp2.font.bold = True
        cp2.font.color.rgb = WHITE

        cp3 = c_tf.add_paragraph()
        cp3.text = p_desc
        cp3.font.size = Pt(11)
        cp3.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: THE PROBLEM STATEMENT & 5-QUESTION FRAMEWORK
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "The Core Problem Statement & 5-Question Framework", "Problem Analysis")

    # Left Card: The Problem Breakdown
    left_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = RGBColor(226, 232, 240)
    ltf = left_card.text_frame
    ltf.word_wrap = True

    lp1 = ltf.paragraphs[0]
    lp1.text = "The Traditional Skilling Blind Spot"
    lp1.font.size = Pt(18)
    lp1.font.bold = True
    lp1.font.color.rgb = INDIGO

    lp2 = ltf.add_paragraph()
    lp2.text = "Institutions commonly state: '10,000 students completed a Python course.'\nYet they fail to answer: Did candidates get relevant jobs? Did their skills genuinely improve?"
    lp2.font.size = Pt(12)
    lp2.font.color.rgb = NAVY

    problems = [
        ("1. Unclear Role Requirements:", "Learners know they want tech careers, but don't know the exact skill combo for Data Analyst vs ML vs DevOps."),
        ("2. Generic Course Dumping:", "Students with different baselines get given the exact same 20 courses without personalization."),
        ("3. Certificate != Capability:", "Completion certificates don't prove measurable skill mastery or employability."),
        ("4. Disconnected Outcomes:", "No feedback loop tracking post-training salary, role relevance, and retention.")
    ]
    for p_title, p_desc in problems:
        pt = ltf.add_paragraph()
        pt.text = f"\n{p_title}"
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = NAVY
        pd = ltf.add_paragraph()
        pd.text = p_desc
        pd.font.size = Pt(11)
        pd.font.color.rgb = TEXT_MUTED

    # Right Card: The 5-Question Framework
    right_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = RGBColor(238, 242, 255)
    right_card.line.color.rgb = RGBColor(199, 210, 254)
    rtf = right_card.text_frame
    rtf.word_wrap = True

    rp1 = rtf.paragraphs[0]
    rp1.text = "The 5-Question Core Framework"
    rp1.font.size = Pt(18)
    rp1.font.bold = True
    rp1.font.color.rgb = INDIGO

    questions = [
        ("Q1. What skills does the candidate currently have?", "Evaluated via NLP Resume Parser & Diagnostic Baseline Tests."),
        ("Q2. What skills are required for the target job?", "Industry-benchmarked database mapped to active market demands."),
        ("Q3. What specific skills are missing or developing?", "Weighted algorithmic gap engine calculating Job Readiness %."),
        ("Q4. What personalized sequence closes the gap?", "Step-by-step chronological pathway with capstone projects."),
        ("Q5. Did the training actually improve skills & outcomes?", "Post-training standardized delta testing (+Δ%) & career tracking.")
    ]
    for q_t, q_d in questions:
        qp = rtf.add_paragraph()
        qp.text = f"\n{q_t}"
        qp.font.size = Pt(12)
        qp.font.bold = True
        qp.font.color.rgb = NAVY
        qd = rtf.add_paragraph()
        qd.text = q_d
        qd.font.size = Pt(11)
        qd.font.color.rgb = INDIGO

    # =========================================================================
    # SLIDE 3: PROPOSED SOLUTION & INNOVATION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Proposed Solution: The Complete Skilling Value Chain", "System Innovation")

    # Flow Banner
    flow_box = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.9))
    flow_box.fill.solid()
    flow_box.fill.fore_color.rgb = NAVY
    flow_box.line.color.rgb = NAVY
    f_tf = flow_box.text_frame
    f_tf.word_wrap = True
    f_p = f_tf.paragraphs[0]
    f_p.text = "Profile  ➔  NLP Extraction  ➔  Diagnostic Quiz  ➔  Skill Gap  ➔  Learning Path  ➔  Capstone  ➔  Post-Test (Δ%)  ➔  Job Placement"
    f_p.font.size = Pt(14)
    f_p.font.bold = True
    f_p.font.color.rgb = AMBER
    f_p.alignment = PP_ALIGN.CENTER

    sol_cards = [
        ("1. NLP Resume & JD Parsing", "Automatically extracts technical skills, education, experience years, and specialization from unstructured text using a comprehensive canonical taxonomy with alias matching."),
        ("2. Weighted Skill Gap Engine", "Categorizes requirements into Matched (🟢), Developing (🟡), and Missing (🔴). Calculates mathematically grounded Job Readiness % using industry skill weights."),
        ("3. Chronological Learning Pathway", "Creates a structured step-by-step roadmap: Foundation Modules -> Advanced Querying -> End-to-End Capstone Project -> Post-Training Assessment -> Interview Prep."),
        ("4. Before & After Delta Testing", "Mandatory standardized assessments before and after training to prove tangible capability growth (+Δ percentage points) rather than relying on course attendance."),
        ("5. Real-Time Job Matching", "Directly connects trainees who meet the industry readiness threshold (>=75%) to active job openings aligned with their verified skill set."),
        ("6. Longitudinal Outcome Tracking", "Captures post-training employment status, company, salary (LPA), time-to-employment, and verifies true career domain relevance.")
    ]

    for i, (sc_title, sc_desc) in enumerate(sol_cards):
        col = i % 3
        row = i // 3
        x = Inches(0.8 + col * 4.0)
        y = Inches(2.55 + row * 2.35)

        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.73), Inches(2.15))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = RGBColor(226, 232, 240)
        c_tf = card.text_frame
        c_tf.word_wrap = True

        cp1 = c_tf.paragraphs[0]
        cp1.text = sc_title
        cp1.font.size = Pt(13)
        cp1.font.bold = True
        cp1.font.color.rgb = INDIGO

        cp2 = c_tf.add_paragraph()
        cp2.text = f"\n{sc_desc}"
        cp2.font.size = Pt(10.5)
        cp2.font.color.rgb = NAVY

    # =========================================================================
    # SLIDE 4: TECHNICAL WORKFLOW & SKILLING IMPACT FORMULA
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Technical Architecture & Transparent Impact Scoring", "Methodology & Mathematics")

    # Formula Box (Top Banner)
    formula_box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(2.2))
    formula_box.fill.solid()
    formula_box.fill.fore_color.rgb = NAVY
    formula_box.line.color.rgb = NAVY
    ftf = formula_box.text_frame
    ftf.word_wrap = True

    fp1 = ftf.paragraphs[0]
    fp1.text = "THE AUDIT-READY SKILLING IMPACT SCORE FORMULA"
    fp1.font.size = Pt(12)
    fp1.font.bold = True
    fp1.font.color.rgb = AMBER

    fp2 = ftf.add_paragraph()
    fp2.text = "Impact Score = 0.35 × (ΔSkill Improvement %) + 0.25 × (Completion Rate %) + 0.25 × (Job Relevance %) + 0.15 × (Employment Rate %)"
    fp2.font.size = Pt(15)
    fp2.font.bold = True
    fp2.font.color.rgb = WHITE

    fp3 = ftf.add_paragraph()
    fp3.text = "\n• 35% Skill Improvement: Validates genuine learning gains (post-score minus pre-score) across the cohort.\n• 25% Training Completion: Evaluates course retention and instructional efficacy.\n• 25% Job Relevance: Ensures trainees are employed in jobs matching their training domain (prevents underemployment inflation).\n• 15% Overall Employment: Measures net economic placement rate."
    fp3.font.size = Pt(10.5)
    fp3.font.color.rgb = RGBColor(203, 213, 225)

    # 3 Bottom Component Cards
    arch_cards = [
        ("Readiness Scoring Formula", "Readiness % = [ Σ (weight_i * min(1.0, user_score_i / req_score_i)) / Σ weight_i ] * 100\nProvides smooth, non-linear matching accounting for skill difficulty and role priority."),
        ("Standardized Question Bank", "Curated diagnostic technical questions across Python, SQL, Excel, Statistics, Power BI, Web Dev, and ML. Automatic grading with explanations and proficiency tier assignment."),
        ("Multi-Tier Role Hierarchy", "Role database includes Data Analyst, ML Engineer, Web Developer, Backend Developer, Cybersecurity Analyst, and Cloud/DevOps with dynamic salary benchmarks.")
    ]
    for i, (ac_title, ac_desc) in enumerate(arch_cards):
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 4.0), Inches(3.8), Inches(3.73), Inches(3.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = RGBColor(226, 232, 240)
        c_tf = card.text_frame
        c_tf.word_wrap = True

        cp1 = c_tf.paragraphs[0]
        cp1.text = ac_title
        cp1.font.size = Pt(13)
        cp1.font.bold = True
        cp1.font.color.rgb = INDIGO

        cp2 = c_tf.add_paragraph()
        cp2.text = f"\n{ac_desc}"
        cp2.font.size = Pt(11)
        cp2.font.color.rgb = NAVY

    # =========================================================================
    # SLIDE 5: MULTI-TIER PLATFORM & INSTITUTIONAL FUNNEL
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Multi-Tier Impact Portals & Macro Policy Funnel", "Institutional Efficacy")

    # 4 Funnel Stages
    funnel_stages = [
        ("STAGE 1: ENROLLED", "10,000 Trainees", "Total intake registered across vocational initiatives", NAVY),
        ("STAGE 2: COMPLETED", "8,200 Trainees", "82.0% Completion Rate with finished learning pathways", INDIGO),
        ("STAGE 3: SKILL IMPROVED", "6,000 Trainees", "73.2% Post-Test Verified (+34.5 pts average delta)", RGBColor(126, 34, 206)),
        ("STAGE 4: RELEVANT JOBS", "3,500 Placed", "58.3% Relevant Placement at ₹6.8 LPA average package", EMERALD)
    ]
    for i, (st_name, st_num, st_sub, col) in enumerate(funnel_stages):
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 3.0), Inches(1.4), Inches(2.75), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = col
        card.line.color.rgb = col
        c_tf = card.text_frame
        c_tf.word_wrap = True

        p1 = c_tf.paragraphs[0]
        p1.text = st_name
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = AMBER

        p2 = c_tf.add_paragraph()
        p2.text = st_num
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = WHITE

        p3 = c_tf.add_paragraph()
        p3.text = f"\n{st_sub}"
        p3.font.size = Pt(10)
        p3.font.color.rgb = RGBColor(226, 232, 240)

    # 3 Stakeholder Portals (Bottom Row)
    portals = [
        ("1. Student / Job Seeker Portal", "• AI Resume Parsing & diagnostic skill baseline\n• Target Job Role selection & radial readiness gauge\n• Personalized chronological curriculum\n• Active career openings matched by readiness\n• Post-training before/after score delta verification"),
        ("2. Training Provider Portal", "• Cohort tracking across active curricula\n• Completion rate & assessment delta analytics\n• Course effectiveness & drop-off detection\n• Direct employer pipeline integration"),
        ("3. Government / Policy Portal", "• Macro 4-Stage Trainee Funnel monitor\n• Institutional Skilling Impact Score (82.4)\n• Employment Rate & Job Relevance benchmarking\n• Labor market skill frequency and salary trends")
    ]
    for i, (p_title, p_desc) in enumerate(portals):
        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 4.0), Inches(3.9), Inches(3.73), Inches(3.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = RGBColor(226, 232, 240)
        c_tf = card.text_frame
        c_tf.word_wrap = True

        cp1 = c_tf.paragraphs[0]
        cp1.text = p_title
        cp1.font.size = Pt(13)
        cp1.font.bold = True
        cp1.font.color.rgb = INDIGO

        cp2 = c_tf.add_paragraph()
        cp2.text = f"\n{p_desc}"
        cp2.font.size = Pt(10.5)
        cp2.font.color.rgb = NAVY

    # =========================================================================
    # SLIDE 6: CASE STUDY & TECHNICAL FEASIBILITY
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Case Study: Rahul's Journey & Technical Implementation", "Validation & Feasibility")

    # Left: Case Study Table Card
    case_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.6))
    case_card.fill.solid()
    case_card.fill.fore_color.rgb = CARD_BG
    case_card.line.color.rgb = RGBColor(226, 232, 240)
    ctf = case_card.text_frame
    ctf.word_wrap = True

    cp1 = ctf.paragraphs[0]
    cp1.text = "Prototype Case Study: Rahul Sharma (B.Tech CSE)"
    cp1.font.size = Pt(15)
    cp1.font.bold = True
    cp1.font.color.rgb = INDIGO

    cp2 = ctf.add_paragraph()
    cp2.text = "Target Role: Data Analyst (Requires Python, SQL, Excel, Stats, Power BI)\n"
    cp2.font.size = Pt(11)
    cp2.font.color.rgb = NAVY

    steps = [
        ("Initial State:", "Python 65%, SQL 40%, Excel 30%, Power BI 10% ➔ Job Readiness: 48% (Developing)"),
        ("AI Pathway:", "7 Steps: SQL Fundamentals ➔ Advanced SQL ➔ Statistics ➔ Power BI Mastery ➔ Sales Dashboard Capstone ➔ Validation ➔ Interview Prep"),
        ("Post-Training Validation:", "SQL 40% ➔ 78% (+38 pts), Excel 30% ➔ 85% (+55 pts), Power BI 10% ➔ 70% (+60 pts), Statistics 25% ➔ 72% (+47 pts)"),
        ("Resulting Impact:", "Job Readiness surged to 82% (Industry Ready)"),
        ("Verified Career Outcome:", "Employed as Junior Data Analyst at InfoMetrics Analytics (₹6.2 LPA, 2.8 months time-to-job, Relevant: YES)")
    ]
    for s_t, s_d in steps:
        p = ctf.add_paragraph()
        p.text = f"• {s_t} {s_d}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = NAVY

    # Right: Tech Stack & Feasibility
    tech_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.4), Inches(5.6), Inches(5.6))
    tech_card.fill.solid()
    tech_card.fill.fore_color.rgb = RGBColor(238, 242, 255)
    tech_card.line.color.rgb = RGBColor(199, 210, 254)
    ttf = tech_card.text_frame
    ttf.word_wrap = True

    tp1 = ttf.paragraphs[0]
    tp1.text = "Production-Ready Technology Stack"
    tp1.font.size = Pt(15)
    tp1.font.bold = True
    tp1.font.color.rgb = INDIGO

    techs = [
        ("FastAPI Backend:", "High-throughput asynchronous REST API with automatic OpenAPI documentation and CORS support."),
        ("Lightweight Database:", "SQLite / PostgreSQL schema storing relational users, assessments, courses, and verified outcomes."),
        ("NLP Skill Extraction:", "Regex & token n-gram parsing mapping unstructured resumes to canonical skill taxonomies."),
        ("Interactive Frontend:", "Responsive glassmorphism UI with Tailwind CSS and Chart.js visualizations."),
        ("One-Click Local Launcher:", "run.bat and run.py for instant localhost execution without complex configurations."),
        ("100% Automated Test Suite:", "10 comprehensive unit & integration tests validating scoring, NLP, pathways, and APIs.")
    ]
    for t_t, t_d in techs:
        p = ttf.add_paragraph()
        p.text = f"\n✔ {t_t}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY
        pd = ttf.add_paragraph()
        pd.text = t_d
        pd.font.size = Pt(10)
        pd.font.color.rgb = INDIGO

    output_path = os.path.join(os.path.dirname(__file__), "sih project.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    create_deck()
