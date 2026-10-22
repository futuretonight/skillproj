"""
Comprehensive Test Suite for SkillTrack / SkillBridge AI
Tests NLP, Database, Assessments, Recommendations, Impact Metrics, and API Endpoints.
"""

import unittest
import json
import os
import sys

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(__file__))

from database import init_db, get_db_connection
import nlp_parser
import assessment_engine
import recommendation_engine
import impact_engine
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestSkillBridgeAI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def test_01_nlp_resume_parsing(self):
        sample_resume = """
        Rahul Sharma
        B.Tech in Computer Science and Engineering
        Skills: Python, SQL, Excel, Pandas, React, Docker.
        Experience: 2 years of experience as a Junior Data Analyst.
        Contact: rahul@example.com
        """
        parsed = nlp_parser.parse_resume(sample_resume)
        self.assertIn("python", parsed["skills"])
        self.assertIn("sql", parsed["skills"])
        self.assertIn("excel", parsed["skills"])
        self.assertEqual(parsed["education"], "BTECH")
        self.assertEqual(parsed["branch"], "Computer Science")
        self.assertEqual(parsed["experience_years"], 2.0)
        self.assertEqual(parsed["email"], "rahul@example.com")

    def test_02_nlp_job_description_parsing(self):
        jd = "Looking for a Data Analyst with experience in SQL, Python, Excel, Power BI and Statistics."
        parsed = nlp_parser.parse_job_description(jd)
        self.assertEqual(parsed["title"], "Data Analyst")
        self.assertIn("sql", parsed["required_skills"])
        self.assertIn("python", parsed["required_skills"])
        self.assertIn("power bi", parsed["required_skills"])

    def test_03_skill_gap_analysis(self):
        user_skills = {"python": 65, "sql": 40, "excel": 30}
        required_skills = {
            "python": {"min_score": 60, "weight": 1.2, "level": "Intermediate"},
            "sql": {"min_score": 75, "weight": 1.5, "level": "Advanced"},
            "excel": {"min_score": 70, "weight": 1.1, "level": "Intermediate"},
            "power bi": {"min_score": 65, "weight": 1.2, "level": "Intermediate"}
        }

        analysis = recommendation_engine.analyze_skill_gap(user_skills, required_skills)
        self.assertIn("python", analysis["matched_skills"])
        self.assertIn("power bi", analysis["missing_skills"])
        # Developing skills: SQL and Excel
        dev_skills = [d["skill"] for d in analysis["developing_skills"]]
        self.assertIn("sql", dev_skills)
        self.assertIn("excel", dev_skills)
        self.assertGreaterEqual(analysis["job_readiness_percentage"], 20)
        self.assertLessEqual(analysis["job_readiness_percentage"], 65)

    def test_04_personalized_learning_pathway(self):
        missing = ["power bi", "statistics"]
        developing = [{"skill": "sql", "gap": 35}]
        pathway = recommendation_engine.generate_personalized_pathway(missing, developing, "Data Analyst")
        self.assertGreater(len(pathway), 3)
        # Check that capstone project and validation steps exist
        types = [step["type"] for step in pathway]
        self.assertIn("Real-World Project", types)
        self.assertIn("Skill Validation", types)

    def test_05_assessment_engine(self):
        # Test quiz questions generation
        questions = assessment_engine.get_quiz_for_skills(["python", "sql"], count_per_skill=2)
        self.assertGreaterEqual(len(questions), 2)
        # Verify correct answer is NOT leaked in quiz questions
        for q in questions:
            self.assertNotIn("correct_answer", q)

        # Test evaluation with known question
        answers = {"py_1": "True", "sql_1": "HAVING"}
        evaluation = assessment_engine.evaluate_quiz(answers)
        self.assertEqual(evaluation["score_percentage"], 100)
        self.assertEqual(evaluation["correct_count"], 2)
        self.assertEqual(evaluation["proficiency_level"], "Advanced")

    def test_06_skilling_impact_score(self):
        impact = impact_engine.calculate_skilling_impact_score(
            avg_skill_improvement=36.0,
            completion_rate=82.0,
            job_relevance_rate=78.0,
            employment_rate=68.0
        )
        # Formula: 0.35*36 + 0.25*82 + 0.25*78 + 0.15*68 = 12.6 + 20.5 + 19.5 + 10.2 = 62.8
        self.assertAlmostEqual(impact["skilling_impact_score"], 62.8, delta=0.5)

    def test_07_api_health_and_profile(self):
        resp = client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["status"], "ok")

        # Test profile creation endpoint
        payload = {
            "name": "Test Candidate",
            "education": "B.Tech",
            "branch": "IT",
            "skills": ["python", "sql"],
            "interests": ["Data Analytics"],
            "target_role": "Data Analyst"
        }
        res = client.post("/api/trainee-profile", json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertIn("user_id", res.json())

    def test_08_api_skill_gap_endpoint(self):
        payload = {
            "target_role": "Data Analyst",
            "user_skills": {"python": 65, "sql": 40}
        }
        res = client.post("/api/skill-gap/analyze", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("job_readiness_percentage", data)
        self.assertIn("skill_breakdown", data)

    def test_09_api_government_analytics(self):
        res = client.get("/api/analytics/government")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("macro_funnel", data)
        self.assertIn("kpis", data)
        self.assertIn("impact_score_details", data)
        self.assertGreaterEqual(data["macro_funnel"]["enrolled"], 10000)

    def test_10_api_market_demand(self):
        res = client.get("/api/analytics/market-demand")
        self.assertEqual(res.status_code, 200)
        demands = res.json()
        self.assertGreater(len(demands), 5)


if __name__ == "__main__":
    unittest.main()
