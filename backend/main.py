from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="SkillTrack",
    description="Employment and Skilling Impact Platform",
    version="1.0.0"
)


class TraineeProfile(BaseModel):
    name: str
    education: str
    skills: List[str]
    interests: List[str]
    experience_years: int = 0


class TraineeProfileResponse(BaseModel):
    message: str
    profile: TraineeProfile


@app.get("/")
def home():
    return {
        "message": "Welcome to SkillTrack!",
        "project": "Employment and Skilling Impact",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/trainee-profile", response_model=TraineeProfileResponse)
def create_trainee_profile(profile: TraineeProfile):
    return {
        "message": "Trainee profile received successfully",
        "profile": profile.model_dump()
    }


class SkillGapRequest(BaseModel):
    current_skills: List[str]
    required_skills: List[str]
class SkillGapResponse(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    message: str

@app.post("/skill-gap", response_model=SkillGapResponse)
def analyze_skill_gap(data: SkillGapRequest):
    current = {skill.strip().lower() for skill in data.current_skills}
    required = {skill.strip().lower() for skill in data.required_skills}

    missing = sorted(required - current)
    matched = sorted(required & current)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "message": "Skill gap analysis completed successfully"
    }


class CourseRecommendationRequest(BaseModel):
    missing_skills: List[str]


class CourseRecommendationResponse(BaseModel):
    recommendations: List[str]
    message: str


@app.post("/course-recommendations", response_model=CourseRecommendationResponse)
def recommend_courses(data: CourseRecommendationRequest):
    course_catalog = {
        "python": "Python for Beginners",
        "sql": "SQL and Database Fundamentals",
        "communication": "Communication Skills",
        "machine learning": "Introduction to Machine Learning",
        "excel": "Excel for Data Analysis",
        "web development": "Web Development Fundamentals"
    }

    recommendations = []

    for skill in data.missing_skills:
        normalized_skill = skill.strip().lower()

        if normalized_skill in course_catalog:
            recommendations.append(course_catalog[normalized_skill])
        else:
            recommendations.append(
                f"Find a beginner course for {skill.strip()}"
            )

    return {
        "recommendations": recommendations,
        "message": "Course recommendations generated successfully"
    }
class CareerPathwayRequest(BaseModel):
    skills: List[str]
    interests: List[str]


class CareerPathwayResponse(BaseModel):
    career_paths: List[str]
    message: str


@app.post("/career-pathways", response_model=CareerPathwayResponse)
def recommend_career_paths(data: CareerPathwayRequest):
    skills = {skill.strip().lower() for skill in data.skills}
    interests = {interest.strip().lower() for interest in data.interests}

    career_paths = []

    if "python" in skills and "sql" in skills:
        career_paths.append("Data Analyst")

    if "python" in skills and (
        "machine learning" in skills or "artificial intelligence" in interests
    ):
        career_paths.append("Machine Learning Engineer")

    if {"html", "css", "javascript"}.issubset(skills):
        career_paths.append("Web Developer")

    if "cybersecurity" in skills or "cybersecurity" in interests:
        career_paths.append("Cybersecurity Analyst")

    if "design" in interests or "ui/ux" in interests:
        career_paths.append("UI/UX Designer")

    if not career_paths:
        career_paths.append(
            "Explore beginner courses to build skills for your interests"
        )

    return {
        "career_paths": career_paths,
        "message": "Career pathway recommendations generated successfully"
    }
