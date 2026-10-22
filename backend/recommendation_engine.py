"""
Recommendation & Skill Gap Engine
Analyzes skill gaps against target job roles, computes Job Readiness %,
and generates sequential learning pathways and course recommendations.
"""

from typing import Dict, List, Any, Optional
import json


def analyze_skill_gap(user_skills: Dict[str, int], required_skills: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compares user's current skill profile against target job role requirements.

    user_skills: {"python": 65, "sql": 40, "excel": 30, ...}
    required_skills: {
        "python": {"min_score": 60, "weight": 1.2, "level": "Intermediate"},
        "sql": {"min_score": 75, "weight": 1.5, "level": "Advanced"}, ...
    }
    """
    matched_skills = []
    developing_skills = []
    missing_skills = []

    total_weighted_score = 0.0
    max_possible_weight = 0.0

    skill_breakdown = []

    for skill_name, req in required_skills.items():
        canonical_skill = skill_name.strip().lower()
        min_score = req.get("min_score", 60)
        weight = req.get("weight", 1.0)
        req_level = req.get("level", "Intermediate")

        user_score = user_skills.get(canonical_skill, 0)
        max_possible_weight += weight * 100.0

        # Calculate weighted contribution
        effective_score = min(user_score, 100)
        total_weighted_score += weight * min(effective_score, 100)

        # Categorize
        if user_score >= min_score:
            status = "sufficient"
            matched_skills.append(canonical_skill)
        elif user_score > 0:
            status = "developing"
            gap_points = min_score - user_score
            developing_skills.append({
                "skill": canonical_skill,
                "current_score": user_score,
                "target_score": min_score,
                "gap": gap_points
            })
        else:
            status = "missing"
            missing_skills.append(canonical_skill)

        skill_breakdown.append({
            "skill": canonical_skill,
            "status": status,
            "user_score": user_score,
            "required_score": min_score,
            "required_level": req_level,
            "weight": weight
        })

    # Calculate overall Job Readiness Percentage
    readiness_percentage = round((total_weighted_score / max_possible_weight) * 100) if max_possible_weight > 0 else 0
    readiness_percentage = min(100, max(0, readiness_percentage))

    return {
        "job_readiness_percentage": readiness_percentage,
        "matched_skills": matched_skills,
        "developing_skills": developing_skills,
        "missing_skills": missing_skills,
        "skill_breakdown": skill_breakdown,
        "total_required": len(required_skills),
        "sufficient_count": len(matched_skills)
    }


def generate_personalized_pathway(missing_skills: List[str], developing_skills: List[Any], target_role: str) -> List[Dict[str, Any]]:
    """
    Generates a structured, chronological step-by-step learning pathway
    specifically tailored to bridge the identified gaps.
    """
    pathway = []
    step_num = 1

    # Extract skill names from developing list
    dev_skill_names = [d["skill"] if isinstance(d, dict) else d for d in developing_skills]
    priority_skills = missing_skills + dev_skill_names

    # Curated hands-on modules & projects
    PROJECT_TEMPLATES = {
        "data analyst": "End-to-End Sales & Customer Retention Dashboard with SQL & Power BI",
        "machine learning engineer": "Predictive Churn Model Pipeline with FastAPI & Scikit-Learn",
        "web developer / frontend": "Full-Featured SaaS Analytics Dashboard using React & Tailwind",
        "backend developer": "High-Throughput Microservice with FastAPI, PostgreSQL & Docker",
        "cybersecurity analyst": "Automated Vulnerability Scanner & Incident Response Playbook",
        "cloud / devops engineer": "CI/CD Pipeline with Docker & Cloud Deployment Infrastructure"
    }

    # Step 1-N: Target missing and developing skills in order of foundational priority
    for skill in priority_skills:
        skill_clean = skill.strip().lower()
        pathway.append({
            "step": step_num,
            "title": f"Master Core {skill.capitalize()}",
            "type": "Course & Practice",
            "duration": "2-3 weeks",
            "description": f"Targeted deep-dive into {skill.capitalize()} focusing on core concepts, syntax, and applied exercises.",
            "status": "pending",
            "skill": skill_clean
        })
        step_num += 1

    # Step: Capstone Project
    capstone_title = PROJECT_TEMPLATES.get(target_role.lower(), f"Industry-Standard {target_role} Capstone Project")
    pathway.append({
        "step": step_num,
        "title": "Hands-on Capstone Project",
        "type": "Real-World Project",
        "duration": "2 weeks",
        "description": f"Build '{capstone_title}' integrating your learned skills to showcase to recruiters.",
        "status": "pending",
        "skill": "practical implementation"
    })
    step_num += 1

    # Step: Post-Training Assessment
    pathway.append({
        "step": step_num,
        "title": "Post-Training Impact Assessment",
        "type": "Skill Validation",
        "duration": "1 week",
        "description": "Retake standardized assessments to measure your skill score improvements and verify credentials.",
        "status": "pending",
        "skill": "validation"
    })
    step_num += 1

    # Step: Career Placement & Interview Readiness
    pathway.append({
        "step": step_num,
        "title": "Resume Polish & Mock Technical Interviews",
        "type": "Employment Prep",
        "duration": "1 week",
        "description": f"Align resume highlights with {target_role} keywords, rehearse technical questions, and activate job matching.",
        "status": "pending",
        "skill": "placement readiness"
    })

    return pathway
