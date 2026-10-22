"""
Skill Assessment Engine
Interactive diagnostic tests for technical skills with scoring and evaluation.
"""

from typing import Dict, List, Any, Optional

# Comprehensive Question Bank
QUESTION_BANK = [
    # --- PYTHON ---
    {
        "id": "py_1",
        "skill": "python",
        "question": "What is the output of `type([]) is list` in Python?",
        "options": ["True", "False", "TypeError", "None"],
        "correct_answer": "True",
        "explanation": "`[]` creates an empty list instance, which is of type `list`."
    },
    {
        "id": "py_2",
        "skill": "python",
        "question": "Which Python built-in function returns an iterator of tuples containing index and value?",
        "options": ["enumerate()", "zip()", "range()", "map()"],
        "correct_answer": "enumerate()",
        "explanation": "`enumerate(iterable)` yields pairs of `(index, item)`."
    },
    {
        "id": "py_3",
        "skill": "python",
        "question": "In Python, which data structure provides O(1) average time complexity for lookups and insertions?",
        "options": ["Dictionary (dict)", "List", "Tuple", "Linked List"],
        "correct_answer": "Dictionary (dict)",
        "explanation": "Python dictionaries are hash tables providing average O(1) key lookups."
    },

    # --- SQL ---
    {
        "id": "sql_1",
        "skill": "sql",
        "question": "Which SQL clause filters records after an aggregate function (e.g., SUM or COUNT) is computed?",
        "options": ["HAVING", "WHERE", "ORDER BY", "GROUP BY"],
        "correct_answer": "HAVING",
        "explanation": "`HAVING` filters aggregated groups; `WHERE` filters individual rows prior to grouping."
    },
    {
        "id": "sql_2",
        "skill": "sql",
        "question": "Which JOIN returns all rows from both tables, matching rows where possible and filling NULLs otherwise?",
        "options": ["FULL OUTER JOIN", "INNER JOIN", "LEFT JOIN", "CROSS JOIN"],
        "correct_answer": "FULL OUTER JOIN",
        "explanation": "FULL OUTER JOIN combines the results of both LEFT and RIGHT outer joins."
    },
    {
        "id": "sql_3",
        "skill": "sql",
        "question": "What is the primary purpose of an index on a database table?",
        "options": ["Speed up data retrieval queries", "Enforce encryption", "Store backup copies", "Reduce table storage space"],
        "correct_answer": "Speed up data retrieval queries",
        "explanation": "Indexes create B-Tree or Hash search structures to accelerate SELECT query performance."
    },

    # --- EXCEL ---
    {
        "id": "excel_1",
        "skill": "excel",
        "question": "Which modern Excel formula is designed to look up values in any column and replace VLOOKUP/INDEX+MATCH?",
        "options": ["XLOOKUP", "HLOOKUP", "SEARCHLOOKUP", "DYNAMICLOOKUP"],
        "correct_answer": "XLOOKUP",
        "explanation": "XLOOKUP works in any direction, searches left/right, and handles exact match by default."
    },
    {
        "id": "excel_2",
        "skill": "excel",
        "question": "What Excel feature allows you to summarize, group, count, and analyze large datasets without complex formulas?",
        "options": ["Pivot Table", "Format Painter", "Data Validation", "Goal Seek"],
        "correct_answer": "Pivot Table",
        "explanation": "Pivot Tables allow interactive dynamic aggregation and cross-tabulation."
    },

    # --- STATISTICS ---
    {
        "id": "stat_1",
        "skill": "statistics",
        "question": "What statistical measure represents the value that divides the upper half from the lower half of a dataset?",
        "options": ["Median", "Mean", "Mode", "Standard Deviation"],
        "correct_answer": "Median",
        "explanation": "The median is the 50th percentile, robust against extreme outliers."
    },
    {
        "id": "stat_2",
        "skill": "statistics",
        "question": "What does a p-value of less than 0.05 typically indicate in hypothesis testing?",
        "options": [
            "Statistically significant evidence to reject the null hypothesis",
            "The null hypothesis is proven true",
            "The experiment is flawed",
            "Standard deviation is zero"
        ],
        "correct_answer": "Statistically significant evidence to reject the null hypothesis",
        "explanation": "p < 0.05 indicates low probability that the observed result occurred by random chance under H0."
    },

    # --- POWER BI ---
    {
        "id": "pbi_1",
        "skill": "power bi",
        "question": "What is the formula language used in Power BI for custom calculations and measures?",
        "options": ["DAX (Data Analysis Expressions)", "PowerScript", "M-Code", "SQL-BI"],
        "correct_answer": "DAX (Data Analysis Expressions)",
        "explanation": "DAX is the formula and query language utilized across Power BI, Analysis Services, and Power Pivot."
    },
    {
        "id": "pbi_2",
        "skill": "power bi",
        "question": "Which tool inside Power BI Desktop is used for data extraction, transformation, and cleaning (ETL)?",
        "options": ["Power Query Editor", "Report View", "Model View", "DAX Studio"],
        "correct_answer": "Power Query Editor",
        "explanation": "Power Query provides graphical ETL capabilities driven by the M language."
    },

    # --- MACHINE LEARNING ---
    {
        "id": "ml_1",
        "skill": "machine learning",
        "question": "What technique is commonly used to prevent overfitting in decision trees and neural networks?",
        "options": ["Regularization & Pruning", "Increasing model parameters", "Removing test data", "Zero epochs"],
        "correct_answer": "Regularization & Pruning",
        "explanation": "Regularization (L1/L2, dropout) penalizes model complexity to enhance generalization."
    },
    {
        "id": "ml_2",
        "skill": "machine learning",
        "question": "Which metric is most appropriate for evaluating a binary classification model on an imbalanced dataset?",
        "options": ["F1-Score / PR-AUC", "Accuracy", "Mean Squared Error", "R-squared"],
        "correct_answer": "F1-Score / PR-AUC",
        "explanation": "Standard accuracy is misleading on skewed class distributions; F1 balances precision and recall."
    },

    # --- WEB DEVELOPMENT ---
    {
        "id": "web_1",
        "skill": "react",
        "question": "In React, which hook is used to handle side-effects like data fetching and subscriptions?",
        "options": ["useEffect", "useState", "useMemo", "useContext"],
        "correct_answer": "useEffect",
        "explanation": "`useEffect` lets developers synchronize components with external systems."
    },
    {
        "id": "web_2",
        "skill": "javascript",
        "question": "What is the result of `['10', '10', '10'].map(parseInt)` in standard JavaScript?",
        "options": ["[10, NaN, 2]", "[10, 10, 10]", "[NaN, NaN, NaN]", "TypeError"],
        "correct_answer": "[10, NaN, 2]",
        "explanation": "`map` passes item, index, array; `parseInt` treats the index as radix (radix 0: decimal, radix 1: invalid -> NaN, radix 2: binary -> 2)."
    },

    # --- CYBERSECURITY ---
    {
        "id": "sec_1",
        "skill": "cybersecurity",
        "question": "What type of attack involves tricking users into revealing sensitive credentials via spoofed communications?",
        "options": ["Phishing", "SQL Injection", "DDoS", "Cross-Site Scripting (XSS)"],
        "correct_answer": "Phishing",
        "explanation": "Phishing is social engineering targeting individuals through deceptive messages."
    }
]


def get_quiz_for_skills(skills: List[str], count_per_skill: int = 2) -> List[Dict[str, Any]]:
    """Returns questions for selected skills without answers for client-side testing."""
    target_skills = {s.strip().lower() for s in skills}
    selected_questions = []

    for q in QUESTION_BANK:
        if q["skill"].lower() in target_skills or any(s in q["skill"].lower() for s in target_skills):
            # Omit correct_answer and explanation for the quiz presentation
            selected_questions.append({
                "id": q["id"],
                "skill": q["skill"],
                "question": q["question"],
                "options": q["options"]
            })

    # If no specific skill matched or too few, supply foundational questions
    if len(selected_questions) < 3:
        for q in QUESTION_BANK[:5]:
            if q["id"] not in [x["id"] for x in selected_questions]:
                selected_questions.append({
                    "id": q["id"],
                    "skill": q["skill"],
                    "question": q["question"],
                    "options": q["options"]
                })

    return selected_questions


def evaluate_quiz(answers: Dict[str, str]) -> Dict[str, Any]:
    """
    Grades user answers against the question bank.
    `answers` is a dict of question_id -> user_choice
    """
    q_map = {q["id"]: q for q in QUESTION_BANK}

    total_questions = len(answers)
    if total_questions == 0:
        return {
            "score_percentage": 0,
            "correct_count": 0,
            "total_questions": 0,
            "skill_scores": {},
            "proficiency_level": "Beginner",
            "feedback": []
        }

    correct_count = 0
    skill_totals: Dict[str, int] = {}
    skill_correct: Dict[str, int] = {}
    feedback: List[Dict[str, Any]] = []

    for q_id, user_choice in answers.items():
        if q_id in q_map:
            q_info = q_map[q_id]
            skill = q_info["skill"]
            skill_totals[skill] = skill_totals.get(skill, 0) + 1

            is_correct = (user_choice.strip() == q_info["correct_answer"].strip())
            if is_correct:
                correct_count += 1
                skill_correct[skill] = skill_correct.get(skill, 0) + 1

            feedback.append({
                "question_id": q_id,
                "skill": skill,
                "question": q_info["question"],
                "your_answer": user_choice,
                "correct_answer": q_info["correct_answer"],
                "is_correct": is_correct,
                "explanation": q_info["explanation"]
            })

    score_percentage = round((correct_count / total_questions) * 100)

    # Per-skill scores
    skill_scores = {}
    for skill, total in skill_totals.items():
        correct = skill_correct.get(skill, 0)
        skill_scores[skill] = round((correct / total) * 100)

    # Proficiency determination
    if score_percentage >= 80:
        proficiency = "Advanced"
    elif score_percentage >= 50:
        proficiency = "Intermediate"
    else:
        proficiency = "Beginner"

    return {
        "score_percentage": score_percentage,
        "correct_count": correct_count,
        "total_questions": total_questions,
        "skill_scores": skill_scores,
        "proficiency_level": proficiency,
        "feedback": feedback
    }
