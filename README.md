# SkillBridge AI (SkillTrack)
### AI-Powered Skill Gap Analysis & Employment Outcome Tracking Platform

> **Smart India Hackathon (SIH) 2026 Prototype & Reference Implementation**  
> *Theme: Education and Skill Development / Employment Efficacy Tracking*

---

## 📌 Executive Summary

Traditional education and skilling programs suffer from a critical blind spot:
> *"10,000 students completed a Python training program."*  
> **...But how many actually gained employment? Did their jobs match the training? Did their skills genuinely improve, or did they only receive a paper certificate?**

**SkillBridge AI** connects the complete value chain:
```
Trainee Profile ➔ AI Skill Assessment ➔ Target Role ➔ Skill Gap Analysis ➔ Personalized Learning Pathway ➔ Hands-on Capstone ➔ Post-Training Assessment (Δ%) ➔ Job Matching ➔ Longitudinal Outcome Tracking
```

---

## 🎯 The 5-Question Problem Framework

Every decision in SkillBridge AI directly answers one of five core questions:

| # | Question | Solution Module |
|---|---|---|
| **1** | **What skills does this person currently have?** | NLP Resume Parser & Diagnostic Baseline Assessment |
| **2** | **What skills are required for their target job?** | Industry-benchmarked Job Role & Market Demand Database |
| **3** | **What skills are missing?** | AI Weighted Skill Gap Engine & Job Readiness Gauge |
| **4** | **What personalized training sequence closes the gap?** | Chronological Step-by-Step Learning Pathway & Capstone Project |
| **5** | **Did that training actually improve skills & employment?** | Post-Training Impact Validation ($\Delta\%$) & Skilling Impact Score |

---

## 🏆 One-Line Elevator Pitch for Judges

> **“Our platform analyzes a person's existing skills against the skills required for their target job, identifies skill gaps, recommends personalized training, measures skill improvement, and tracks the resulting employment outcomes.”**

---

## 📐 Transparent Skilling Impact Score Formula

Unlike arbitrary black-box metrics, SkillBridge AI employs an **audit-ready, weighted formula**:

$$\text{Skilling Impact Score} = 0.35 \times (\Delta\text{Skill Improvement \%}) + 0.25 \times (\text{Completion Rate \%}) + 0.25 \times (\text{Job Relevance Rate \%}) + 0.15 \times (\text{Employment Rate \%})$$

### Why these weights?
- **35% on Skill Improvement ($\Delta\%$):** Proves candidate actually learned rather than merely attending.
- **25% on Training Completion:** Measures retention and curriculum completion.
- **25% on Job Relevance:** Prevents artificial inflation (e.g. placing certified data analysts as generic delivery workers).
- **15% on Overall Employment:** Measures placement and economic mobility.

---

## 🏛️ The 4-Stage Government Trainee Funnel

Designed specifically for institutional and state-level policy makers to evaluate real ROI:

```
[ Stage 1: Enrolled Trainees ] ➔ 10,000 (100%)
             ↓
[ Stage 2: Completed Training ] ➔ 8,200 (82.0% Completion Rate)
             ↓
[ Stage 3: Measurable Skill Gain ] ➔ 6,000 (73.2% Post-Test Verified, +34.5 pts)
             ↓
[ Stage 4: Relevant Career Placement ] ➔ 3,500 (58.3% Relevant Employment, ₹6.8 LPA avg)
```

---

## 🛠️ System Architecture & Technology Stack

- **Backend:** Python 3.13 + FastAPI + SQLite (Lightweight, fast, production-ready)
- **NLP Engine:** Rule-based & pattern-matching skill extractor with comprehensive alias taxonomy (Python, SQL, React, Docker, Machine Learning, Power BI, etc.)
- **Assessment Engine:** Standardized multi-choice diagnostic tests with automated scoring and level classification (Beginner / Intermediate / Advanced)
- **Frontend:** Responsive Glassmorphic Single Page App (HTML5, Tailwind CSS via CDN, Chart.js, FontAwesome)
- **Dashboards:**
  - **Trainee Portal:** Profile, Resume NLP, Gap Analysis, Learning Pathway, Assessments, Job Matches.
  - **Training Provider / Admin Portal:** Cohorts, completion rates, learner status.
  - **Government / Policy Portal:** 4-Stage macro funnel, Skilling Impact Score, regional KPIs.
  - **Market Demand Portal:** Live labor market trends by job postings and salary.
  - **SIH Pitch & Flow:** Interactive presentation view for judges.

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
From the project root:
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
Or from the `backend` folder:
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

### 3. Open in Browser
Visit:
```
http://localhost:8000/
```
Interactive Swagger API documentation:
```
http://localhost:8000/docs
```

---

## 🧪 Running Automated Tests

Run the full end-to-end unit and integration test suite:
```bash
python backend/test_suite.py
```
*Tests verify NLP parsing, gap scoring, pathway sequencing, assessment grading, impact formulas, and all API endpoints.*

---

## 🌟 Demo User Story: Rahul Sharma

1. **Profile:** Rahul (B.Tech CSE) knows Python (65%), basic SQL (40%), Excel (30%).
2. **Target Role:** Data Analyst (requires SQL 75%, Python 60%, Excel 70%, Statistics 65%, Power BI 65%).
3. **AI Gap Analysis:** Readiness begins at **48%**. System identifies missing skills: *Power BI, Statistics* and developing skills: *SQL, Excel*.
4. **Personalized Pathway:** System generates 7 tailored chronological steps.
5. **Skilling Impact:** Post-training assessment scores jump: SQL (40% ➔ 78%), Excel (30% ➔ 85%), Power BI (10% ➔ 70%).
6. **Career Outcome:** Job Readiness climbs to **82%**, unlocking verified employment as *Junior Data Analyst at InfoMetrics Analytics (₹6.2 LPA)*.
