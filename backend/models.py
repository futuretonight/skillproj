"""
Pydantic Schema Models for Request and Response Payloads
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class TraineeProfileCreate(BaseModel):
    name: str
    email: Optional[str] = None
    age_group: Optional[str] = "21-25"
    location: Optional[str] = "Pune, Maharashtra"
    education: str
    branch: Optional[str] = "Computer Science"
    graduation_year: Optional[int] = 2026
    experience_years: float = 0.0
    skills: List[str] = []
    interests: List[str] = []
    target_role: Optional[str] = "Data Analyst"


class ResumeParseRequest(BaseModel):
    resume_text: str


class JobDescriptionParseRequest(BaseModel):
    job_description_text: str


class SkillGapAnalysisRequest(BaseModel):
    target_role: str
    user_skills: Dict[str, int] = Field(
        default_factory=dict,
        description="Dictionary mapping skill name to proficiency score (0-100)"
    )


class PathwayRequest(BaseModel):
    target_role: str
    missing_skills: List[str]
    developing_skills: List[Any] = []


class QuizQuestionsRequest(BaseModel):
    skills: List[str]
    count_per_skill: int = 2


class QuizSubmissionRequest(BaseModel):
    user_id: Optional[int] = None
    skill_name: Optional[str] = "Assessment"
    assessment_type: str = "before"  # 'before' or 'after'
    answers: Dict[str, str]  # question_id -> chosen option


class CourseEnrollmentRequest(BaseModel):
    user_id: int
    course_id: int


class TrainingProgressUpdate(BaseModel):
    training_id: int
    progress_percent: int
    score: Optional[int] = None


class EmploymentOutcomeReport(BaseModel):
    user_id: int
    status: str  # 'employed', 'internship', 'seeking', 'unemployed'
    company_name: Optional[str] = None
    job_role: Optional[str] = None
    is_relevant: bool = True
    time_to_employment_months: Optional[float] = 3.0
    salary_lpa: Optional[float] = 6.0
