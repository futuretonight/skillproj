# SkillBridge AI (SkillTrack)
### AI-Powered Skill Gap Analysis & Employment Outcome Tracking Platform

> **Comprehensive Employment & Skilling Impact Intelligence Platform**  
> *Connecting Education, Capability Development, and Verified Industry Outcomes*

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

## 💡 Core Platform Vision

> **“Our platform analyzes a person's existing skills against the skills required for their target job, identifies skill gaps, recommends personalized training, measures skill improvement, and tracks the resulting employment outcomes.”**

---

## 📊 Presentation Deck

A complete 6-slide widescreen presentation deck is available directly in the repository:
* **File:** [`sih project.pptx`](file:///C:/Users/yajath%20krushna/Documents/vscode%20projects/skillproj/sih%20project.pptx)
* **Slides Overview:**
  1. Title & Executive Summary
  2. The Problem Statement & The 5-Question Framework
  3. Proposed Solution & The Complete Skilling Value Chain
  4. Technical Architecture & Transparent Impact Scoring Formula
  5. Multi-Tier Impact Portals & Macro Policy Funnel
  6. Case Study ("Rahul's Journey") & Technical Feasibility

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

## 🚀 Super Simple Localhost Run (One-Click)

You don't need complicated commands to run this locally! Choose any of these 3 easy methods:

### Method 1: Just Double-Click (Easiest for Windows)
Double-click the **`run.bat`** file in the project folder.
It will automatically start the server and open your browser!

### Method 2: Single Python Command
Open your terminal in this folder and run:
```bash
python run.py
```
*(This starts the backend and automatically opens `http://localhost:8000` in your default browser).*

### Method 3: Direct Script
```bash
python backend/main.py
```

---

### 🌐 Access URLs
* **Web Application UI:** [http://localhost:8000](http://localhost:8000)
* **Interactive API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Running Automated Tests
To run the full test suite verifying all 10 modules:
```bash
python backend/test_suite.py
```

---

## 🌟 Demo User Story: Rahul Sharma

1. **Profile:** Rahul (B.Tech CSE) knows Python (65%), basic SQL (40%), Excel (30%).
2. **Target Role:** Data Analyst (requires SQL 75%, Python 60%, Excel 70%, Statistics 65%, Power BI 65%).
3. **AI Gap Analysis:** Readiness begins at **48%**. System identifies missing skills: *Power BI, Statistics* and developing skills: *SQL, Excel*.
4. **Personalized Pathway:** System generates 7 tailored chronological steps.
5. **Skilling Impact:** Post-training assessment scores jump: SQL (40% ➔ 78%), Excel (30% ➔ 85%), Power BI (10% ➔ 70%).
6. **Career Outcome:** Job Readiness climbs to **82%**, unlocking verified employment as *Junior Data Analyst at InfoMetrics Analytics (₹6.2 LPA)*.
