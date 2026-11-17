import os

# Core Student & Access Settings
MAGIC_CODE = os.getenv("MAGIC_CODE", "1120").strip()
# Hilary's official required Matric Number: BU26MED1035
ALLOWED_MATRIC = os.getenv("ALLOWED_MATRIC", "BU26MED1035").strip()

# Free phone push notification topic via https://ntfy.sh
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "samuell-hilary-cbt-1120").strip()

STUDENT_FULL_NAME = os.getenv("STUDENT_FULL_NAME", "Olawuyi Eniola Hilary").strip()
STUDENT_FIRST_NAME = os.getenv("STUDENT_FIRST_NAME", "Hilary").strip()
POWERED_BY_NAME = os.getenv("POWERED_BY_NAME", "SAMUEL").strip()

SECRET_KEY = os.getenv("SECRET_KEY", "hillary-cbt-secret-key-1120-samuell")

# Course Configuration (Fixed sequential order, individual timers, 2 credit units each)
COURSES = [
    {
        "code": "CHM101",
        "display_code": "CHM 101",
        "title": "General Chemistry I",
        "questions_count": 35,
        "duration_minutes": 20,
        "credit_units": 2,
        "order": 1,
    },
    {
        "code": "PHY101",
        "display_code": "PHY 101",
        "title": "General Physics I",
        "questions_count": 35,
        "duration_minutes": 20,
        "credit_units": 2,
        "order": 2,
    },
    {
        "code": "MTH101",
        "display_code": "MTH 101",
        "title": "Elementary Mathematics I",
        "questions_count": 35,
        "duration_minutes": 25,
        "credit_units": 2,
        "order": 3,
    },
    {
        "code": "BIO101",
        "display_code": "BIO 101",
        "title": "General Biology I",
        "questions_count": 35,
        "duration_minutes": 20,
        "credit_units": 2,
        "order": 4,
    },
]

COURSE_MAP = {c["code"]: c for c in COURSES}
COURSE_ORDER = [c["code"] for c in COURSES]


def score_to_nigerian_grade(correct_count: int, total_questions: int = 35) -> dict:
    """
    Standard Nigerian 5.0 Grading Scale:
    70 - 100% -> A (5 points)
    60 - 69%  -> B (4 points)
    50 - 59%  -> C (3 points)
    45 - 49%  -> D (2 points)
    40 - 44%  -> E (1 point)
    0  - 39%  -> F (0 points)
    """
    if total_questions <= 0:
        pct = 0.0
    else:
        pct = round((correct_count / total_questions) * 100, 1)

    # Use integer/rounded percentage check for standard cutoffs
    pct_check = round(pct)
    if pct_check >= 70:
        return {"letter": "A", "points": 5, "percentage": pct, "remark": "Excellent"}
    elif pct_check >= 60:
        return {"letter": "B", "points": 4, "percentage": pct, "remark": "Very Good"}
    elif pct_check >= 50:
        return {"letter": "C", "points": 3, "percentage": pct, "remark": "Good"}
    elif pct_check >= 45:
        return {"letter": "D", "points": 2, "percentage": pct, "remark": "Fair"}
    elif pct_check >= 40:
        return {"letter": "E", "points": 1, "percentage": pct, "remark": "Pass"}
    else:
        return {"letter": "F", "points": 0, "percentage": pct, "remark": "Fail"}


def classify_gpa(gpa: float) -> dict:
    """
    Standard Nigerian University Class of Degree Cutoffs on 5.00 scale:
    - First Class: 4.50 - 5.00 -> GREEN background
    - Second Class Upper (2:1): 3.50 - 4.49 -> YELLOW background
    - Second Class Lower (2:2): 2.40 - 3.49 -> RED background
    - Third Class: 1.50 - 2.39 -> RED background
    - Fail / Pass below Third Class: < 1.50 -> RED background
    """
    gpa_rounded = round(gpa, 2)
    if gpa_rounded >= 4.50:
        return {
            "class_name": "First Class Honours",
            "theme": "green",
            "bg_class": "bg-emerald-600",
            "text_class": "text-white",
            "ticket_bg": "bg-white text-emerald-800 border-emerald-200",
            "badge_bg": "bg-emerald-800/80 text-emerald-100",
            "headline": "This is really great — keep it up!",
            "caption": "You did great, Hilary! Outstanding First Class performance across your 101 courses. Keep this momentum going into your main university exams!",
        }
    elif gpa_rounded >= 3.50:
        return {
            "class_name": "Second Class Honours (Upper Division — 2:1)",
            "theme": "yellow",
            "bg_class": "bg-amber-400",
            "text_class": "text-slate-950",
            "ticket_bg": "bg-white text-amber-900 border-amber-300",
            "badge_bg": "bg-slate-900 text-amber-300",
            "headline": "You can do better!",
            "caption": "Solid effort, Hilary, but you need to read more and focus more to push into First Class territory. Review the questions you missed below!",
        }
    elif gpa_rounded >= 2.40:
        return {
            "class_name": "Second Class Honours (Lower Division — 2:2)",
            "theme": "red",
            "bg_class": "bg-red-600",
            "text_class": "text-white",
            "ticket_bg": "bg-red-50 text-red-700 border-red-200",
            "badge_bg": "bg-red-900/90 text-red-100",
            "headline": "This is not good enough — you need to improve!",
            "caption": "You are capable of much more than this, Hilary. You need to read more, focus harder, and carefully study the explanations below before retaking the exam.",
        }
    elif gpa_rounded >= 1.50:
        return {
            "class_name": "Third Class Honours",
            "theme": "red",
            "bg_class": "bg-red-700",
            "text_class": "text-white",
            "ticket_bg": "bg-red-50 text-red-800 border-red-200",
            "badge_bg": "bg-red-950 text-red-100",
            "headline": "This is a poor performance — you need to improve!",
            "caption": "This score is far below your potential. Please study your 101 course materials thoroughly, go through every explanation below, and practice again.",
        }
    else:
        return {
            "class_name": "Below Honours (Needs Urgent Improvement)",
            "theme": "red",
            "bg_class": "bg-red-800",
            "text_class": "text-white",
            "ticket_bg": "bg-red-50 text-red-900 border-red-300",
            "badge_bg": "bg-black/60 text-red-100",
            "headline": "This is a poor performance — you need to improve!",
            "caption": "Don't be discouraged, but you must buckle down and revise seriously. Read every single explanation below and keep practicing until your concepts are solid.",
        }
