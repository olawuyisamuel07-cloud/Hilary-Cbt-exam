import csv
import json
import sys
from pathlib import Path
from database import SessionLocal, engine, Base
from models import Question

VALID_COURSES = {"CHM101", "PHY101", "MTH101", "BIO101"}
VALID_OPTIONS = {"A", "B", "C", "D"}
LETTERS = ["A", "B", "C", "D"]


def import_file(file_path: str, replace_existing_for_course: bool = False):
    Base.metadata.create_all(bind=engine)
    path = Path(file_path)
    if not path.exists():
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    rows_to_insert = []
    courses_seen = set()

    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        for idx, item in enumerate(data, start=1):
            course = (item.get("course") or item.get("course_code") or "").strip().upper().replace(" ", "")
            if course not in VALID_COURSES:
                print(f"Skipping item {idx}: Invalid course '{course}'.")
                continue
            q_text = (item.get("question") or item.get("question_text") or "").strip()
            opts = item.get("options") or [
                item.get("option_a"),
                item.get("option_b"),
                item.get("option_c"),
                item.get("option_d"),
            ]
            if not q_text or len(opts) < 4:
                continue
            ans_idx = item.get("answer_index")
            if ans_idx is not None and 0 <= int(ans_idx) < 4:
                correct = LETTERS[int(ans_idx)]
            else:
                correct = (item.get("correct") or item.get("correct_option") or "A").strip().upper()

            explanation = (item.get("explanation") or f"The correct option is {correct} ({opts[LETTERS.index(correct)]}).").strip()
            courses_seen.add(course)
            rows_to_insert.append(
                {
                    "course_code": course,
                    "question_text": q_text,
                    "option_a": str(opts[0]).strip(),
                    "option_b": str(opts[1]).strip(),
                    "option_c": str(opts[2]).strip(),
                    "option_d": str(opts[3]).strip(),
                    "correct_option": correct,
                    "explanation": explanation,
                }
            )
    else:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=2):
                course = (row.get("course") or row.get("course_code") or "").strip().upper().replace(" ", "")
                if course not in VALID_COURSES:
                    print(f"Skipping row {idx}: Invalid course '{course}'. Must be one of {sorted(VALID_COURSES)}")
                    continue

                q_text = (row.get("question") or row.get("question_text") or "").strip()
                opt_a = (row.get("A") or row.get("option_a") or "").strip()
                opt_b = (row.get("B") or row.get("option_b") or "").strip()
                opt_c = (row.get("C") or row.get("option_c") or "").strip()
                opt_d = (row.get("D") or row.get("option_d") or "").strip()
                correct = (row.get("correct") or row.get("correct_option") or "").strip().upper()
                explanation = (row.get("explanation") or "").strip()

                if not (q_text and opt_a and opt_b and opt_c and opt_d and correct in VALID_OPTIONS):
                    print(f"Skipping row {idx}: Missing question, options A-D, or valid correct option (A/B/C/D).")
                    continue

                courses_seen.add(course)
                rows_to_insert.append(
                    {
                        "course_code": course,
                        "question_text": q_text,
                        "option_a": opt_a,
                        "option_b": opt_b,
                        "option_c": opt_c,
                        "option_d": opt_d,
                        "correct_option": correct,
                        "explanation": explanation or f"The correct option is {correct}.",
                    }
                )

    if not rows_to_insert:
        print("No valid questions found in file.")
        return

    with SessionLocal() as db:
        if replace_existing_for_course:
            for c in courses_seen:
                deleted = db.query(Question).filter(Question.course_code == c).delete()
                print(f"Cleared {deleted} existing questions for {c}.")
        db.bulk_insert_mappings(Question, rows_to_insert)
        db.commit()

    print(f"Successfully imported {len(rows_to_insert)} questions across {sorted(courses_seen)}!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_questions.py <path_to_json_or_csv> [--replace]")
        print("Example: python import_questions.py data/all_questions.json --replace")
        sys.exit(1)

    target_file = sys.argv[1]
    replace_flag = "--replace" in sys.argv
    import_file(target_file, replace_existing_for_course=replace_flag)
