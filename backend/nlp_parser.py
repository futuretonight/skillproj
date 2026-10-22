"""
NLP Skill Extraction & Document Parsing Module
Extracts technical skills, qualifications, and experience from resumes and job descriptions.
"""

import re
from typing import Dict, List, Any, Set

# Standardized Skill Taxonomy with aliases
SKILL_TAXONOMY: Dict[str, List[str]] = {
    # Data & Analytics
    "python": ["python", "py", "python3", "python 3"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite", "tsql", "plsql", "pl/sql"],
    "excel": ["excel", "ms excel", "microsoft excel", "spreadsheets", "advanced excel", "vlookup"],
    "statistics": ["statistics", "statistical analysis", "probability", "inferential statistics", "hypothesis testing"],
    "power bi": ["power bi", "powerbi", "pbi", "dax"],
    "tableau": ["tableau", "tableau desktop"],
    "data visualization": ["data visualization", "data viz", "dataviz", "matplotlib", "seaborn", "plotly"],
    "pandas": ["pandas", "dataframe"],
    "numpy": ["numpy"],

    # AI & Machine Learning
    "machine learning": ["machine learning", "ml", "scikit-learn", "sklearn", "supervised learning", "unsupervised learning"],
    "deep learning": ["deep learning", "neural networks", "pytorch", "torch", "tensorflow", "keras"],
    "natural language processing": ["natural language processing", "nlp", "transformers", "spacy", "nltk", "bert", "llm", "large language models"],
    "computer vision": ["computer vision", "opencv", "cnn", "image processing"],

    # Web & Software Development
    "html": ["html", "html5"],
    "css": ["css", "css3", "sass", "tailwind", "bootstrap"],
    "javascript": ["javascript", "js", "es6", "vanilla js"],
    "typescript": ["typescript", "ts"],
    "react": ["react", "react.js", "reactjs", "next.js", "nextjs"],
    "node.js": ["node.js", "nodejs", "node", "express", "expressjs"],
    "rest apis": ["rest apis", "rest api", "restful api", "rest", "api design", "fastapi", "flask"],
    "java": ["java", "core java", "spring", "spring boot", "springboot"],
    "c++": ["c++", "cpp"],
    "c": ["c language", "ansi c"],
    "system design": ["system design", "microservices", "distributed systems", "software architecture"],

    # DevOps & Cloud
    "docker": ["docker", "containers", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "git": ["git", "github", "gitlab", "version control"],
    "cloud computing": ["cloud computing", "aws", "azure", "gcp", "google cloud platform", "amazon web services"],
    "linux": ["linux", "bash", "shell scripting", "ubuntu"],

    # Security & Infrastructure
    "cybersecurity": ["cybersecurity", "information security", "infosec", "network security"],
    "ethical hacking": ["ethical hacking", "penetration testing", "pen testing", "kali linux", "wireshark"],
    "networking": ["networking", "tcp/ip", "dns", "subnets", "firewalls"],

    # Soft Skills & Management
    "communication": ["communication", "presentation skills", "written communication", "verbal communication"],
    "problem solving": ["problem solving", "analytical thinking", "critical thinking"],
    "teamwork": ["teamwork", "collaboration", "cross-functional"]
}

EDUCATION_PATTERNS = [
    r"\b(b\.?tech|bachelor of technology|b\.?e\.?|bachelor of engineering)\b",
    r"\b(m\.?tech|master of technology|m\.?e\.?|master of engineering)\b",
    r"\b(bca|bachelor of computer applications)\b",
    r"\b(mca|master of computer applications)\b",
    r"\b(b\.?sc|bachelor of science)\b",
    r"\b(m\.?sc|master of science)\b",
    r"\b(b\.?com|bachelor of commerce)\b",
    r"\b(mba|master of business administration)\b",
    r"\b(diploma|high school|higher secondary)\b"
]

BRANCH_PATTERNS = [
    (r"\b(computer science|cse|comp\s*sci)\b", "Computer Science"),
    (r"\b(information technology|it)\b", "Information Technology"),
    (r"\b(electronics and communication|ece|electronics)\b", "Electronics & Communication"),
    (r"\b(data science|ai|artificial intelligence)\b", "Data Science & AI"),
    (r"\b(electrical|eee)\b", "Electrical Engineering"),
    (r"\b(mechanical|mech)\b", "Mechanical Engineering"),
    (r"\b(civil)\b", "Civil Engineering")
]


def extract_skills_from_text(text: str) -> List[str]:
    """Scans free-form text and identifies technical & professional skills."""
    if not text:
        return []

    clean_text = " " + text.lower() + " "
    # Replace common punctuation with spaces except those in skills like c++
    clean_text = re.sub(r"[,/|;()\[\]{}:]", " ", clean_text)

    found_skills: Set[str] = set()

    for canonical_name, aliases in SKILL_TAXONOMY.items():
        for alias in aliases:
            # Word-boundary check or exact phrase check
            pattern = r"(?:^|\s|\W)" + re.escape(alias) + r"(?:$|\s|\W)"
            if re.search(pattern, clean_text):
                found_skills.add(canonical_name)
                break

    return sorted(list(found_skills))


def parse_resume(resume_text: str) -> Dict[str, Any]:
    """
    Extracts structured candidate profile data from raw resume text:
    - Skills identified
    - Education / Degree
    - Branch / Specialization
    - Experience Years (estimated)
    - Contact Info (email, phone)
    """
    if not resume_text:
        return {
            "skills": [],
            "education": "Not specified",
            "branch": "General",
            "experience_years": 0.0,
            "email": "",
            "phone": ""
        }

    # Extract Skills
    skills = extract_skills_from_text(resume_text)

    # Extract Education
    education = "Undergraduate"
    for pat in EDUCATION_PATTERNS:
        match = re.search(pat, resume_text, re.IGNORECASE)
        if match:
            education = match.group(0).upper().replace(".", "")
            break

    # Extract Branch
    branch = "Computer Science"
    for pat, canonical_branch in BRANCH_PATTERNS:
        if re.search(pat, resume_text, re.IGNORECASE):
            branch = canonical_branch
            break

    # Extract Experience Years (e.g., "3 years of experience", "2+ yrs")
    experience_years = 0.0
    exp_matches = re.findall(r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|yrs?)(?:\s+of)?\s+experience", resume_text, re.IGNORECASE)
    if exp_matches:
        try:
            experience_years = float(exp_matches[0])
        except ValueError:
            experience_years = 0.0
    elif "fresher" in resume_text.lower() or "student" in resume_text.lower():
        experience_years = 0.0

    # Extract Email
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", resume_text)
    email = email_match.group(0) if email_match else ""

    # Extract Phone
    phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", resume_text)
    phone = phone_match.group(0) if phone_match else ""

    return {
        "skills": skills,
        "education": education,
        "branch": branch,
        "experience_years": experience_years,
        "email": email,
        "phone": phone
    }


def parse_job_description(jd_text: str) -> Dict[str, Any]:
    """
    Extracts required skills, experience level, and role title from raw job postings.
    """
    if not jd_text:
        return {"skills": [], "title": "Custom Role", "min_experience_years": 0}

    skills = extract_skills_from_text(jd_text)

    # Detect Role Title
    titles = [
        "Data Analyst", "Machine Learning Engineer", "Frontend Developer",
        "Backend Developer", "Full Stack Developer", "Cybersecurity Analyst",
        "DevOps Engineer", "Cloud Engineer", "UI/UX Designer", "Software Engineer"
    ]
    detected_title = "Technical Role"
    for title in titles:
        if re.search(r"\b" + re.escape(title) + r"\b", jd_text, re.IGNORECASE):
            detected_title = title
            break

    # Detect Experience requirement
    min_exp = 0.0
    exp_matches = re.findall(r"(\d+(?:\.\d+)?)\s*(?:to\s*\d+)?\s*(?:\+)?\s*(?:years?|yrs?)", jd_text, re.IGNORECASE)
    if exp_matches:
        try:
            min_exp = float(exp_matches[0])
        except ValueError:
            min_exp = 0.0

    return {
        "title": detected_title,
        "required_skills": skills,
        "min_experience_years": min_exp
    }
