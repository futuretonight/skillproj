"""
Database layer for SkillTrack / SkillBridge AI
Handles SQLite persistence, schema creation, and realistic data seeding.
"""

import sqlite3
import json
import os
from typing import Dict, List, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "skilltrack.db")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age_group TEXT,
        location TEXT,
        education TEXT,
        branch TEXT,
        graduation_year INTEGER,
        experience_years REAL DEFAULT 0,
        interests TEXT, -- JSON array of strings
        target_role TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # User Skills
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        skill_name TEXT NOT NULL,
        proficiency TEXT, -- Beginner, Intermediate, Advanced
        score INTEGER DEFAULT 50, -- 0-100
        verified BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # Job Roles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        category TEXT,
        description TEXT,
        required_skills TEXT, -- JSON object: {"skill_name": {"min_score": 70, "weight": 1.2}}
        avg_salary_lpa REAL,
        openings_count INTEGER DEFAULT 0
    )
    """)

    # Courses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        provider TEXT,
        level TEXT, -- Beginner, Intermediate, Advanced
        duration_weeks INTEGER,
        skills_covered TEXT, -- JSON array
        rating REAL DEFAULT 4.5,
        url TEXT
    )
    """)

    # User Trainings / Course Enrollments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trainings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        course_id INTEGER,
        status TEXT DEFAULT 'enrolled', -- enrolled, in_progress, completed
        progress_percent INTEGER DEFAULT 0,
        score INTEGER DEFAULT 0,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
    """)

    # Skill Assessments (Before & After)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        skill_name TEXT NOT NULL,
        assessment_type TEXT NOT NULL, -- 'before' or 'after'
        score INTEGER NOT NULL, -- 0-100
        passed BOOLEAN DEFAULT 1,
        taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Employment Outcomes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employment_outcomes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        status TEXT NOT NULL, -- 'employed', 'internship', 'seeking', 'unemployed'
        company_name TEXT,
        job_role TEXT,
        is_relevant BOOLEAN DEFAULT 0,
        time_to_employment_months REAL,
        salary_lpa REAL,
        verified BOOLEAN DEFAULT 1,
        reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Market Skill Demand Trends
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_demand (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT UNIQUE NOT NULL,
        category TEXT,
        demand_level TEXT, -- High, Medium, Emerging
        job_postings_count INTEGER,
        growth_rate_percent REAL,
        avg_salary_lpa REAL
    )
    """)

    conn.commit()
    conn.close()
    seed_database_if_empty()


def seed_database_if_empty():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if job roles exist
    cursor.execute("SELECT COUNT(*) as cnt FROM job_roles")
    if cursor.fetchone()["cnt"] == 0:
        seed_job_roles(cursor)
        seed_courses(cursor)
        seed_market_demand(cursor)
        seed_cohort_data(cursor)
        conn.commit()

    conn.close()


def seed_job_roles(cursor):
    roles = [
        (
            "Data Analyst",
            "Data & Analytics",
            "Extracts, inspects, cleans, and models data to uncover actionable business insights and support data-driven decision making.",
            json.dumps({
                "python": {"min_score": 60, "weight": 1.2, "level": "Intermediate"},
                "sql": {"min_score": 75, "weight": 1.5, "level": "Advanced"},
                "excel": {"min_score": 70, "weight": 1.1, "level": "Intermediate"},
                "statistics": {"min_score": 65, "weight": 1.3, "level": "Intermediate"},
                "power bi": {"min_score": 65, "weight": 1.2, "level": "Intermediate"},
                "data visualization": {"min_score": 65, "weight": 1.0, "level": "Intermediate"},
                "communication": {"min_score": 60, "weight": 0.8, "level": "Intermediate"}
            }),
            6.5,
            3400
        ),
        (
            "Machine Learning Engineer",
            "AI & Data Science",
            "Designs, develops, and deploys predictive machine learning models and end-to-end data pipelines.",
            json.dumps({
                "python": {"min_score": 85, "weight": 1.5, "level": "Advanced"},
                "machine learning": {"min_score": 80, "weight": 1.5, "level": "Advanced"},
                "sql": {"min_score": 65, "weight": 1.0, "level": "Intermediate"},
                "statistics": {"min_score": 75, "weight": 1.3, "level": "Advanced"},
                "deep learning": {"min_score": 70, "weight": 1.2, "level": "Intermediate"},
                "docker": {"min_score": 60, "weight": 0.9, "level": "Intermediate"},
                "git": {"min_score": 65, "weight": 0.8, "level": "Intermediate"}
            }),
            11.5,
            1850
        ),
        (
            "Web Developer / Frontend",
            "Software Engineering",
            "Builds responsive, intuitive, and performant web interfaces using modern frameworks and web standards.",
            json.dumps({
                "html": {"min_score": 80, "weight": 1.0, "level": "Advanced"},
                "css": {"min_score": 80, "weight": 1.0, "level": "Advanced"},
                "javascript": {"min_score": 85, "weight": 1.5, "level": "Advanced"},
                "react": {"min_score": 75, "weight": 1.4, "level": "Advanced"},
                "git": {"min_score": 65, "weight": 0.8, "level": "Intermediate"},
                "rest apis": {"min_score": 65, "weight": 0.9, "level": "Intermediate"}
            }),
            7.0,
            4200
        ),
        (
            "Backend Developer",
            "Software Engineering",
            "Architects scalable server-side systems, RESTful APIs, microservices, and database schemas.",
            json.dumps({
                "python": {"min_score": 80, "weight": 1.4, "level": "Advanced"},
                "sql": {"min_score": 75, "weight": 1.3, "level": "Advanced"},
                "rest apis": {"min_score": 80, "weight": 1.4, "level": "Advanced"},
                "docker": {"min_score": 65, "weight": 1.0, "level": "Intermediate"},
                "git": {"min_score": 70, "weight": 0.8, "level": "Intermediate"},
                "system design": {"min_score": 65, "weight": 1.1, "level": "Intermediate"}
            }),
            8.5,
            3800
        ),
        (
            "Cybersecurity Analyst",
            "Security & Infrastructure",
            "Monitors networks for security breaches, investigates incidents, and implements defensive security measures.",
            json.dumps({
                "cybersecurity": {"min_score": 80, "weight": 1.5, "level": "Advanced"},
                "networking": {"min_score": 75, "weight": 1.4, "level": "Advanced"},
                "linux": {"min_score": 70, "weight": 1.2, "level": "Intermediate"},
                "python": {"min_score": 60, "weight": 0.9, "level": "Intermediate"},
                "ethical hacking": {"min_score": 70, "weight": 1.3, "level": "Intermediate"}
            }),
            8.0,
            1600
        ),
        (
            "Cloud / DevOps Engineer",
            "Cloud & DevOps",
            "Automates deployment pipelines, manages cloud infrastructure, and ensures system reliability and scalability.",
            json.dumps({
                "cloud computing": {"min_score": 75, "weight": 1.4, "level": "Advanced"},
                "docker": {"min_score": 80, "weight": 1.4, "level": "Advanced"},
                "linux": {"min_score": 75, "weight": 1.2, "level": "Intermediate"},
                "git": {"min_score": 75, "weight": 0.9, "level": "Intermediate"},
                "python": {"min_score": 65, "weight": 1.0, "level": "Intermediate"},
                "kubernetes": {"min_score": 65, "weight": 1.2, "level": "Intermediate"}
            }),
            9.5,
            2400
        )
    ]

    cursor.executemany("""
    INSERT INTO job_roles (title, category, description, required_skills, avg_salary_lpa, openings_count)
    VALUES (?, ?, ?, ?, ?, ?)
    """, roles)


def seed_courses(cursor):
    courses = [
        ("SQL and Relational Database Fundamentals", "SkillBridge Academy", "Beginner", 4, json.dumps(["sql", "databases"]), 4.7, "https://skillbridge.edu/courses/sql-basics"),
        ("Advanced SQL for Analytics & Data Warehousing", "National Tech Institute", "Advanced", 6, json.dumps(["sql", "data warehousing", "performance tuning"]), 4.8, "https://skillbridge.edu/courses/adv-sql"),
        ("Python for Beginners & Data Structures", "OpenSkill", "Beginner", 5, json.dumps(["python", "programming basics"]), 4.6, "https://skillbridge.edu/courses/python-101"),
        ("Business Statistics & Exploratory Data Analysis", "Analytics Lab", "Intermediate", 4, json.dumps(["statistics", "data analysis", "python"]), 4.7, "https://skillbridge.edu/courses/stats"),
        ("Power BI & Interactive Dashboard Mastery", "DataCraft", "Intermediate", 4, json.dumps(["power bi", "data visualization", "business intelligence"]), 4.9, "https://skillbridge.edu/courses/powerbi"),
        ("Excel for Data Analytics & Financial Modeling", "ExcelPro Academy", "Intermediate", 3, json.dumps(["excel", "spreadsheets", "data visualization"]), 4.5, "https://skillbridge.edu/courses/excel"),
        ("Hands-on Machine Learning with Scikit-Learn", "AI Builders", "Intermediate", 8, json.dumps(["machine learning", "python", "statistics"]), 4.8, "https://skillbridge.edu/courses/ml-intro"),
        ("Modern Web Development with React & Tailwind", "Frontend Guild", "Intermediate", 6, json.dumps(["javascript", "react", "html", "css"]), 4.8, "https://skillbridge.edu/courses/react"),
        ("Building RESTful APIs with FastAPI & Python", "Backend Forge", "Intermediate", 4, json.dumps(["python", "rest apis", "databases"]), 4.9, "https://skillbridge.edu/courses/fastapi"),
        ("Cybersecurity Fundamentals & Network Defense", "CyberShield Institute", "Beginner", 6, json.dumps(["cybersecurity", "networking", "linux"]), 4.7, "https://skillbridge.edu/courses/cyber-sec"),
        ("Docker & Containerization for Developers", "DevOps Essentials", "Beginner", 3, json.dumps(["docker", "devops", "linux"]), 4.6, "https://skillbridge.edu/courses/docker"),
        ("Data Visualization Principles & Storytelling", "Design & Data", "Beginner", 3, json.dumps(["data visualization", "communication"]), 4.6, "https://skillbridge.edu/courses/data-viz")
    ]

    cursor.executemany("""
    INSERT INTO courses (title, provider, level, duration_weeks, skills_covered, rating, url)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, courses)


def seed_market_demand(cursor):
    demands = [
        ("python", "Programming", "High", 12500, 24.5, 8.5),
        ("sql", "Databases", "High", 11200, 18.2, 7.5),
        ("machine learning", "AI & Data Science", "High", 7600, 32.0, 12.0),
        ("power bi", "Business Intelligence", "High", 6800, 28.4, 6.8),
        ("statistics", "Data & Math", "Medium", 5200, 14.1, 7.0),
        ("excel", "Productivity", "High", 9400, 8.5, 5.5),
        ("react", "Web Development", "High", 8900, 21.0, 8.0),
        ("docker", "DevOps", "High", 6400, 29.5, 9.8),
        ("cybersecurity", "Security", "High", 5800, 31.2, 9.0),
        ("rest apis", "Software Engineering", "High", 7100, 19.0, 8.2),
        ("javascript", "Programming", "High", 10800, 15.6, 7.8),
        ("data visualization", "Data & Analytics", "Medium", 4900, 17.3, 6.5)
    ]

    cursor.executemany("""
    INSERT INTO market_demand (skill_name, category, demand_level, job_postings_count, growth_rate_percent, avg_salary_lpa)
    VALUES (?, ?, ?, ?, ?, ?)
    """, demands)


def seed_cohort_data(cursor):
    """Seed benchmark cohorts to demonstrate Government and Admin dashboards."""
    # Seed sample user: Rahul Sharma (from user story)
    cursor.execute("""
    INSERT INTO users (name, email, age_group, location, education, branch, graduation_year, experience_years, interests, target_role)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "Rahul Sharma",
        "rahul.sharma@example.edu",
        "21-25",
        "Pune, Maharashtra",
        "B.Tech",
        "Computer Science",
        2026,
        0.5,
        json.dumps(["Data Analytics", "Artificial Intelligence", "Cloud Computing"]),
        "Data Analyst"
    ))
    rahul_id = cursor.lastrowid

    # Rahul's initial skills (Before training)
    initial_skills = [
        (rahul_id, "python", "Intermediate", 65, 1),
        (rahul_id, "sql", "Beginner", 40, 1),
        (rahul_id, "excel", "Beginner", 30, 1),
        (rahul_id, "statistics", "Beginner", 25, 1),
        (rahul_id, "power bi", "Beginner", 10, 0)
    ]
    cursor.executemany("""
    INSERT INTO user_skills (user_id, skill_name, proficiency, score, verified)
    VALUES (?, ?, ?, ?, ?)
    """, initial_skills)

    # Rahul's Before Assessments
    before_assessments = [
        (rahul_id, "python", "before", 65, 1),
        (rahul_id, "sql", "before", 40, 0),
        (rahul_id, "excel", "before", 30, 0),
        (rahul_id, "statistics", "before", 25, 0),
        (rahul_id, "power bi", "before", 10, 0)
    ]
    cursor.executemany("""
    INSERT INTO assessments (user_id, skill_name, assessment_type, score, passed)
    VALUES (?, ?, ?, ?, ?)
    """, before_assessments)

    # Rahul's After Assessments (Post training)
    after_assessments = [
        (rahul_id, "python", "after", 82, 1),
        (rahul_id, "sql", "after", 78, 1),
        (rahul_id, "excel", "after", 85, 1),
        (rahul_id, "statistics", "after", 72, 1),
        (rahul_id, "power bi", "after", 70, 1)
    ]
    cursor.executemany("""
    INSERT INTO assessments (user_id, skill_name, assessment_type, score, passed)
    VALUES (?, ?, ?, ?, ?)
    """, after_assessments)

    # Rahul's outcome
    cursor.execute("""
    INSERT INTO employment_outcomes (user_id, status, company_name, job_role, is_relevant, time_to_employment_months, salary_lpa, verified)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        rahul_id,
        "employed",
        "InfoMetrics Analytics",
        "Junior Data Analyst",
        1,
        2.8,
        6.2,
        1
    ))

    # Seed 25 additional cohort records for aggregate analytics
    cohort_profiles = [
        ("Priya Patil", "priya.p@test.com", "21-25", "Mumbai", "B.Sc Statistics", "Data Analyst", 45, 82, "employed", "Data Analyst", 1, 3.1, 6.0),
        ("Amit Verma", "amit.v@test.com", "21-25", "Nagpur", "B.Tech IT", "Web Developer / Frontend", 50, 88, "employed", "Frontend Developer", 1, 2.5, 7.2),
        ("Sneha Joshi", "sneha.j@test.com", "21-25", "Pune", "BCA", "Data Analyst", 38, 75, "employed", "Business Analyst", 1, 3.5, 5.8),
        ("Rohan Kulkarni", "rohan.k@test.com", "21-25", "Nashik", "B.E Electronics", "Backend Developer", 42, 80, "employed", "Backend Engineer", 1, 4.0, 7.5),
        ("Ananya Das", "ananya.d@test.com", "21-25", "Bangalore", "B.Tech CSE", "Machine Learning Engineer", 55, 89, "employed", "Associate ML Engineer", 1, 2.0, 10.5),
        ("Kavita Rao", "kavita.r@test.com", "21-25", "Hyderabad", "B.Tech ECE", "Data Analyst", 35, 74, "internship", "Data Analytics Intern", 1, 1.8, 4.2),
        ("Vikas Nair", "vikas.n@test.com", "26-30", "Pune", "MCA", "Cloud / DevOps Engineer", 48, 84, "employed", "DevOps Engineer", 1, 3.2, 9.0),
        ("Pooja Shinde", "pooja.s@test.com", "21-25", "Aurangabad", "B.Sc Computer Science", "Web Developer / Frontend", 40, 78, "employed", "Web Designer", 0, 5.0, 4.0),
        ("Karan Malhotra", "karan.m@test.com", "21-25", "Delhi", "B.Tech CSE", "Cybersecurity Analyst", 52, 85, "employed", "Security Analyst", 1, 3.0, 8.2),
        ("Neha Gupta", "neha.g@test.com", "21-25", "Thane", "B.Com + Comp", "Data Analyst", 30, 71, "seeking", None, 0, None, None),
        ("Siddharth Roy", "sid.r@test.com", "21-25", "Kolkata", "B.Tech IT", "Machine Learning Engineer", 60, 91, "employed", "AI Specialist", 1, 2.2, 11.0),
        ("Divya Menon", "divya.m@test.com", "21-25", "Chennai", "B.Tech CSE", "Backend Developer", 45, 83, "employed", "API Developer", 1, 3.4, 7.8),
        ("Manish Tiwari", "manish.t@test.com", "26-30", "Indore", "BCA", "Data Analyst", 35, 69, "employed", "Operations Analyst", 0, 4.5, 4.8),
        ("Tanvi Deshmukh", "tanvi.d@test.com", "21-25", "Solapur", "B.E Comp", "Data Analyst", 40, 79, "employed", "BI Developer", 1, 3.0, 6.5),
        ("Aditya Chopra", "aditya.c@test.com", "21-25", "Pune", "B.Tech CSE", "Cloud / DevOps Engineer", 50, 86, "employed", "Cloud Engineer", 1, 2.7, 9.5),
        ("Shweta More", "shweta.m@test.com", "21-25", "Kolhapur", "B.Sc IT", "Web Developer / Frontend", 36, 73, "employed", "UI Developer", 1, 3.8, 5.5),
        ("Gaurav K", "gaurav.k@test.com", "21-25", "Pune", "B.Tech Mechanical", "Data Analyst", 25, 70, "internship", "Analytics Intern", 1, 2.0, 3.6),
        ("Ritika Sen", "ritika.s@test.com", "21-25", "Mumbai", "BCA", "Cybersecurity Analyst", 44, 80, "employed", "SOC Analyst", 1, 3.3, 7.5),
        ("Deepak S", "deepak.s@test.com", "21-25", "Nagpur", "B.E Comp", "Backend Developer", 48, 81, "seeking", None, 0, None, None),
        ("Sanjana Hegde", "sanjana.h@test.com", "21-25", "Bangalore", "B.Tech CSE", "Machine Learning Engineer", 58, 92, "employed", "Data Scientist", 1, 1.9, 12.0)
    ]

    for p in cohort_profiles:
        cursor.execute("""
        INSERT INTO users (name, email, age_group, location, education, target_role)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (p[0], p[1], p[2], p[3], p[4], p[5]))
        uid = cursor.lastrowid

        # Insert Before & After Assessments
        cursor.execute("INSERT INTO assessments (user_id, skill_name, assessment_type, score) VALUES (?, ?, 'before', ?)",
                       (uid, "Core Skill", p[6]))
        cursor.execute("INSERT INTO assessments (user_id, skill_name, assessment_type, score) VALUES (?, ?, 'after', ?)",
                       (uid, "Core Skill", p[7]))

        # Insert Outcome
        if p[8] == "seeking":
            cursor.execute("""
            INSERT INTO employment_outcomes (user_id, status, is_relevant, verified)
            VALUES (?, 'seeking', 0, 1)
            """, (uid,))
        else:
            cursor.execute("""
            INSERT INTO employment_outcomes (user_id, status, company_name, job_role, is_relevant, time_to_employment_months, salary_lpa, verified)
            VALUES (?, ?, 'Partner Company', ?, ?, ?, ?, 1)
            """, (uid, p[8], p[9], p[10], p[11], p[12]))
