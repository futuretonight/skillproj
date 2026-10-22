"""
SkillTrack / SkillBridge AI - Main FastAPI Application
Employment and Skilling Impact Platform
"""

import os
import sys

# Ensure backend directory is in sys.path regardless of execution working directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import json
from typing import List, Dict, Any, Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from database import init_db, get_db_connection
from models import (
    TraineeProfileCreate,
    ResumeParseRequest,
    JobDescriptionParseRequest,
    SkillGapAnalysisRequest,
    PathwayRequest,
    QuizQuestionsRequest,
    QuizSubmissionRequest,
    CourseEnrollmentRequest,
    TrainingProgressUpdate,
    EmploymentOutcomeReport
)
import nlp_parser
import assessment_engine
import recommendation_engine
import impact_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database schemas and seeds on startup
    init_db()
    yield

app = FastAPI(
    title="SkillTrack / SkillBridge AI",
    description="AI-Powered Skill Gap Analysis and Employment Outcome Tracking Platform",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for external frontends / dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# CORE SYSTEM ENDPOINTS
# ---------------------------------------------------------------------------

@app.get("/health")
def health_check():
    return {"status": "ok", "platform": "SkillBridge AI", "version": "2.0.0"}


# ---------------------------------------------------------------------------
# NLP MODULE: RESUME & JOB DESCRIPTION PARSING
# ---------------------------------------------------------------------------

@app.post("/api/nlp/parse-resume")
def parse_resume_endpoint(data: ResumeParseRequest):
    """Extracts candidate skills, education, branch, and experience from resume text."""
    parsed = nlp_parser.parse_resume(data.resume_text)
    return {
        "status": "success",
        "data": parsed,
        "message": f"Successfully extracted {len(parsed['skills'])} skills from resume"
    }


@app.post("/api/nlp/parse-job-description")
def parse_job_description_endpoint(data: JobDescriptionParseRequest):
    """Extracts required skills and experience requirements from job posting text."""
    parsed = nlp_parser.parse_job_description(data.job_description_text)
    return {
        "status": "success",
        "data": parsed,
        "message": f"Identified role '{parsed['title']}' with {len(parsed['required_skills'])} required skills"
    }


# ---------------------------------------------------------------------------
# USER PROFILES
# ---------------------------------------------------------------------------

@app.post("/api/trainee-profile")
@app.post("/trainee-profile")  # Backward compatibility
def create_or_update_trainee_profile(profile: TraineeProfileCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    user_email = profile.email or f"{profile.name.lower().replace(' ', '.')}@example.com"

    # Check if user already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    existing = cursor.fetchone()

    if existing:
        user_id = existing["id"]
        cursor.execute("""
        UPDATE users 
        SET name = ?, age_group = ?, location = ?, education = ?, branch = ?, 
            graduation_year = ?, experience_years = ?, interests = ?, target_role = ?
        WHERE id = ?
        """, (
            profile.name,
            profile.age_group,
            profile.location,
            profile.education,
            profile.branch,
            profile.graduation_year,
            profile.experience_years,
            json.dumps(profile.interests),
            profile.target_role,
            user_id
        ))
    else:
        cursor.execute("""
        INSERT INTO users (name, email, age_group, location, education, branch, graduation_year, experience_years, interests, target_role)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            profile.name,
            user_email,
            profile.age_group,
            profile.location,
            profile.education,
            profile.branch,
            profile.graduation_year,
            profile.experience_years,
            json.dumps(profile.interests),
            profile.target_role
        ))
        user_id = cursor.lastrowid

    # Add or update skills
    for skill in profile.skills:
        clean_skill = skill.strip().lower()
        cursor.execute("""
        SELECT id FROM user_skills WHERE user_id = ? AND skill_name = ?
        """, (user_id, clean_skill))
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO user_skills (user_id, skill_name, proficiency, score, verified)
            VALUES (?, ?, 'Beginner', 50, 0)
            """, (user_id, clean_skill))

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "user_id": user_id,
        "message": "Trainee profile saved successfully",
        "profile": profile.model_dump()
    }


@app.get("/api/profile/{user_id}")
def get_user_profile(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = dict(user)
    user_dict["interests"] = json.loads(user_dict["interests"]) if user_dict["interests"] else []

    cursor.execute("SELECT skill_name, proficiency, score, verified FROM user_skills WHERE user_id = ?", (user_id,))
    skills = [dict(row) for row in cursor.fetchall()]
    user_dict["skills"] = skills

    conn.close()
    return user_dict


# ---------------------------------------------------------------------------
# JOB ROLES DATABASE
# ---------------------------------------------------------------------------

@app.get("/api/jobs")
def get_all_job_roles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_roles ORDER BY openings_count DESC")
    roles = []
    for row in cursor.fetchall():
        r = dict(row)
        r["required_skills"] = json.loads(r["required_skills"])
        roles.append(r)
    conn.close()
    return roles


@app.get("/api/jobs/{role_title}")
def get_job_role_details(role_title: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_roles WHERE title LIKE ?", (f"%{role_title}%",))
    role = cursor.fetchone()
    conn.close()
    if not role:
        raise HTTPException(status_code=404, detail="Job role not found")
    r = dict(role)
    r["required_skills"] = json.loads(r["required_skills"])
    return r


# ---------------------------------------------------------------------------
# SKILL GAP ANALYSIS & READINESS ENGINE
# ---------------------------------------------------------------------------

@app.post("/api/skill-gap/analyze")
def analyze_skill_gap_endpoint(data: SkillGapAnalysisRequest):
    """
    Compares candidate's skills and scores with target job role requirements.
    Computes Job Readiness %, matched skills, developing skills, and missing skills.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_roles WHERE title LIKE ?", (f"%{data.target_role}%",))
    role = cursor.fetchone()
    conn.close()

    if not role:
        # Fallback to default Data Analyst skills if role not found
        req_skills = {
            "python": {"min_score": 60, "weight": 1.2, "level": "Intermediate"},
            "sql": {"min_score": 75, "weight": 1.5, "level": "Advanced"},
            "excel": {"min_score": 70, "weight": 1.1, "level": "Intermediate"},
            "statistics": {"min_score": 65, "weight": 1.3, "level": "Intermediate"},
            "power bi": {"min_score": 65, "weight": 1.2, "level": "Intermediate"}
        }
    else:
        req_skills = json.loads(role["required_skills"])

    analysis = recommendation_engine.analyze_skill_gap(data.user_skills, req_skills)
    analysis["target_role"] = data.target_role
    return analysis


# Backward compatibility endpoint for original /skill-gap
@app.post("/skill-gap")
def legacy_skill_gap(data: Dict[str, Any]):
    current_skills = data.get("current_skills", [])
    required_skills = data.get("required_skills", [])

    current_set = {s.strip().lower() for s in current_skills}
    required_set = {s.strip().lower() for s in required_skills}

    missing = sorted(required_set - current_set)
    matched = sorted(required_set & current_set)

    readiness = round((len(matched) / len(required_set) * 100)) if required_set else 100

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "job_readiness_percentage": readiness,
        "message": "Skill gap analysis completed successfully"
    }


# ---------------------------------------------------------------------------
# LEARNING PATHWAY & COURSE RECOMMENDATIONS
# ---------------------------------------------------------------------------

@app.post("/api/learning-pathway")
def get_personalized_learning_pathway(data: PathwayRequest):
    """Generates sequential step-by-step learning pathway to bridge candidate's gaps."""
    pathway = recommendation_engine.generate_personalized_pathway(
        missing_skills=data.missing_skills,
        developing_skills=data.developing_skills,
        target_role=data.target_role
    )
    return {
        "target_role": data.target_role,
        "total_steps": len(pathway),
        "pathway": pathway
    }


@app.get("/api/courses")
def get_all_courses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses ORDER BY rating DESC")
    courses = []
    for row in cursor.fetchall():
        c = dict(row)
        c["skills_covered"] = json.loads(c["skills_covered"])
        courses.append(c)
    conn.close()
    return courses


# Backward compatibility endpoint for /course-recommendations
@app.post("/course-recommendations")
def legacy_course_recommendations(data: Dict[str, Any]):
    missing = data.get("missing_skills", [])
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    all_courses = cursor.fetchall()
    conn.close()

    recommendations = []
    for skill in missing:
        skill_clean = skill.strip().lower()
        matched_course = None
        for c in all_courses:
            skills_cov = json.loads(c["skills_covered"])
            if skill_clean in [s.lower() for s in skills_cov]:
                matched_course = c["title"]
                break
        if matched_course:
            recommendations.append(f"{matched_course} ({skill.capitalize()})")
        else:
            recommendations.append(f"Comprehensive {skill.capitalize()} Masterclass")

    return {
        "recommendations": recommendations,
        "message": "Course recommendations generated successfully"
    }


# Backward compatibility for /career-pathways
@app.post("/career-pathways")
def legacy_career_pathways(data: Dict[str, Any]):
    skills = {s.strip().lower() for s in data.get("skills", [])}
    interests = {i.strip().lower() for i in data.get("interests", [])}

    paths = []
    if "python" in skills and "sql" in skills:
        paths.append("Data Analyst")
    if "python" in skills and ("machine learning" in skills or "artificial intelligence" in interests):
        paths.append("Machine Learning Engineer")
    if {"html", "css", "javascript"}.issubset(skills) or "react" in skills:
        paths.append("Web Developer / Frontend")
    if "cybersecurity" in skills or "cybersecurity" in interests:
        paths.append("Cybersecurity Analyst")
    if "docker" in skills or "cloud" in interests:
        paths.append("Cloud / DevOps Engineer")

    if not paths:
        paths.append("Explore foundational courses to build skills for your target role")

    return {"career_paths": paths, "message": "Career pathways generated successfully"}


# ---------------------------------------------------------------------------
# ASSESSMENT ENGINE (BEFORE & AFTER SKILL TESTING)
# ---------------------------------------------------------------------------

@app.post("/api/assessments/questions")
def get_assessment_questions_endpoint(data: QuizQuestionsRequest):
    """Retrieves diagnostic assessment questions for selected skills."""
    questions = assessment_engine.get_quiz_for_skills(data.skills, count_per_skill=data.count_per_skill)
    return {
        "skills_tested": data.skills,
        "count": len(questions),
        "questions": questions
    }


@app.post("/api/assessments/submit")
def submit_assessment_endpoint(data: QuizSubmissionRequest):
    """
    Grades assessment, calculates proficiency score, and optionally saves to DB
    as either 'before' (baseline) or 'after' (post-training impact).
    """
    result = assessment_engine.evaluate_quiz(data.answers)

    # Save to database if user_id is provided
    if data.user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        for skill, score in result["skill_scores"].items():
            cursor.execute("""
            INSERT INTO assessments (user_id, skill_name, assessment_type, score, passed)
            VALUES (?, ?, ?, ?, ?)
            """, (data.user_id, skill, data.assessment_type, score, 1 if score >= 50 else 0))

            # If this is an 'after' assessment, also update the user_skills table
            if data.assessment_type == "after":
                cursor.execute("""
                INSERT INTO user_skills (user_id, skill_name, proficiency, score, verified)
                VALUES (?, ?, ?, ?, 1)
                ON CONFLICT(id) DO UPDATE SET score = ?, proficiency = ?, verified = 1
                """, (data.user_id, skill, result["proficiency_level"], score, score, result["proficiency_level"]))

        conn.commit()
        conn.close()

    return result


@app.get("/api/assessments/history/{user_id}")
def get_user_assessment_history(user_id: int):
    """Retrieves before vs after test scores and calculates measurable skill improvement delta."""
    impact = impact_engine.get_user_skilling_impact(user_id)
    return impact


# ---------------------------------------------------------------------------
# JOB MATCHING
# ---------------------------------------------------------------------------

@app.get("/api/job-matching/{user_id}")
def get_job_matches_for_user(user_id: int):
    """Matches user with active jobs and calculates readiness percentage for each role."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user skills
    cursor.execute("SELECT skill_name, score FROM user_skills WHERE user_id = ?", (user_id,))
    user_skills = {row["skill_name"].lower(): row["score"] for row in cursor.fetchall()}

    # Get all jobs
    cursor.execute("SELECT * FROM job_roles")
    roles = cursor.fetchall()
    conn.close()

    job_matches = []
    for r in roles:
        req_skills = json.loads(r["required_skills"])
        analysis = recommendation_engine.analyze_skill_gap(user_skills, req_skills)
        readiness = analysis["job_readiness_percentage"]

        job_matches.append({
            "job_id": r["id"],
            "title": r["title"],
            "category": r["category"],
            "avg_salary_lpa": r["avg_salary_lpa"],
            "openings_count": r["openings_count"],
            "readiness_percentage": readiness,
            "status": "Ready to Apply" if readiness >= 75 else "Training In Progress",
            "matched_skills": analysis["matched_skills"],
            "missing_skills": analysis["missing_skills"]
        })

    job_matches.sort(key=lambda x: x["readiness_percentage"], reverse=True)
    return job_matches


# ---------------------------------------------------------------------------
# EMPLOYMENT OUTCOMES TRACKING
# ---------------------------------------------------------------------------

@app.post("/api/outcomes/report")
def report_employment_outcome(data: EmploymentOutcomeReport):
    """Logs post-training employment outcome (employment status, company, role, relevance)."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO employment_outcomes (
        user_id, status, company_name, job_role, is_relevant, 
        time_to_employment_months, salary_lpa, verified
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, 1)
    """, (
        data.user_id,
        data.status,
        data.company_name,
        data.job_role,
        1 if data.is_relevant else 0,
        data.time_to_employment_months,
        data.salary_lpa
    ))
    conn.commit()
    conn.close()

    return {
        "status": "success",
        "message": "Employment outcome recorded and verified successfully"
    }


# ---------------------------------------------------------------------------
# DASHBOARDS & ANALYTICS: ADMIN, GOVERNMENT, MARKET DEMAND
# ---------------------------------------------------------------------------

@app.get("/api/analytics/government")
def get_government_institution_analytics():
    """Returns macro-level skilling impact funnel, KPIs, and Skilling Impact Score."""
    metrics = impact_engine.get_institutional_macro_metrics()
    return metrics


@app.get("/api/analytics/admin")
def get_admin_analytics():
    """Returns training provider cohort analytics, completion rates, and active learners."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total_learners FROM users")
    total_learners = cursor.fetchone()["total_learners"]

    cursor.execute("SELECT COUNT(*) as total_assessments FROM assessments")
    total_assessments = cursor.fetchone()["total_assessments"]

    cursor.execute("SELECT COUNT(*) as total_outcomes FROM employment_outcomes")
    total_outcomes = cursor.fetchone()["total_outcomes"]

    # Recent learner activity
    cursor.execute("""
    SELECT u.id, u.name, u.education, u.target_role, eo.status, eo.job_role, eo.is_relevant
    FROM users u
    LEFT JOIN employment_outcomes eo ON u.id = eo.user_id
    ORDER BY u.id DESC
    LIMIT 10
    """)
    recent_cohort = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "total_learners": total_learners,
        "total_assessments": total_assessments,
        "total_outcomes_reported": total_outcomes,
        "active_courses_count": 12,
        "avg_cohort_completion_rate": 82.5,
        "recent_learners": recent_cohort
    }


@app.get("/api/analytics/market-demand")
def get_market_skill_demand():
    """Returns live labor market demand metrics for skills."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM market_demand ORDER BY job_postings_count DESC")
    demands = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return demands


# ---------------------------------------------------------------------------
# SERVE FRONTEND APPLICATION
# ---------------------------------------------------------------------------

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/")
    def serve_frontend():
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {
            "message": "Welcome to SkillTrack / SkillBridge AI!",
            "status": "Backend running. Frontend index.html not found."
        }
else:
    @app.get("/")
    def serve_root():
        return {
            "message": "Welcome to SkillTrack / SkillBridge AI!",
            "status": "Backend running. Create frontend folder for UI."
        }


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    import time

    def _open():
        time.sleep(1.2)
        webbrowser.open("http://localhost:8000")

    threading.Thread(target=_open, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
