import os
import time
import random
import urllib.request
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from pydantic import BaseModel
from sqlalchemy.orm import Session

import config
from database import engine, Base, get_db, SessionLocal
from models import Question, ExamAttempt, CourseSectionAttempt, AttemptAnswer
from seed_questions import seed_all_questions

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
IMAGES_DIR = STATIC_DIR / "images"
TEMPLATES_DIR = BASE_DIR / "templates"

IMAGES_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

serializer = URLSafeTimedSerializer(config.SECRET_KEY)

# Simple in-memory brute-force tracker: {ip: {"fails": int, "locked_until": float}}
LOGIN_ATTEMPTS: dict[str, dict[str, float]] = {}
MAX_LOGIN_FAILS = 5
LOCKOUT_SECONDS = 180  # 3 minutes lockout after 5 wrong tries


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_all_questions(db)
    yield


app = FastAPI(title="Hillary 101 CBT Exam Portal — Powered by SAMUELL", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def ensure_utc(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def get_common_context(request: Request) -> dict:
    has_custom_logo = (IMAGES_DIR / "logo.png").exists() or (IMAGES_DIR / "logo.jpg").exists()
    logo_filename = "logo.png" if (IMAGES_DIR / "logo.png").exists() else ("logo.jpg" if (IMAGES_DIR / "logo.jpg").exists() else None)
    has_custom_bg = (IMAGES_DIR / "family-bg.jpg").exists() or (IMAGES_DIR / "family-bg.png").exists()
    bg_filename = "family-bg.jpg" if (IMAGES_DIR / "family-bg.jpg").exists() else ("family-bg.png" if (IMAGES_DIR / "family-bg.png").exists() else None)

    return {
        "request": request,
        "student_full_name": config.STUDENT_FULL_NAME,
        "student_first_name": config.STUDENT_FIRST_NAME,
        "powered_by_name": config.POWERED_BY_NAME,
        "courses_config": config.COURSES,
        "has_custom_logo": has_custom_logo,
        "logo_filename": logo_filename,
        "has_custom_bg": has_custom_bg,
        "bg_filename": bg_filename,
    }


def get_session_data(request: Request) -> Optional[dict]:
    token = request.cookies.get("cbt_session")
    if not token:
        return None
    try:
        data = serializer.loads(token, max_age=86400 * 7)
        return data
    except (BadSignature, SignatureExpired):
        return None


def set_session_cookie(response, matric_number: str, active_attempt_id: Optional[int] = None):
    payload = {
        "matric_number": matric_number,
        "active_attempt_id": active_attempt_id,
    }
    token = serializer.dumps(payload)
    response.set_cookie(
        key="cbt_session",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=86400 * 7,
    )


def create_new_exam_attempt(db: Session, matric_number: str) -> ExamAttempt:
    attempt = ExamAttempt(
        matric_number=matric_number,
        student_name=config.STUDENT_FULL_NAME,
        started_at=datetime.now(timezone.utc),
        is_completed=False,
        current_course_index=0,
        total_questions=sum(c["questions_count"] for c in config.COURSES),
    )
    db.add(attempt)
    db.flush()

    for idx, c_info in enumerate(config.COURSES):
        section = CourseSectionAttempt(
            attempt_id=attempt.id,
            course_code=c_info["code"],
            course_order=idx,
            duration_minutes=c_info["duration_minutes"],
            credit_units=c_info["credit_units"],
            total_questions=c_info["questions_count"],
            is_submitted=False,
        )
        db.add(section)
        db.flush()

        # Pick 35 random questions from the 200-question pool for this course
        pool = db.query(Question).filter(Question.course_code == c_info["code"]).all()
        sample_size = min(c_info["questions_count"], len(pool))
        chosen_questions = random.sample(pool, sample_size)

        for q_num, q_obj in enumerate(chosen_questions, start=1):
            ans = AttemptAnswer(
                section_id=section.id,
                question_id=q_obj.id,
                question_number=q_num,
                selected_option=None,
                is_flagged=False,
                is_correct=False,
            )
            db.add(ans)

    db.commit()
    db.refresh(attempt)
    return attempt


def grade_and_submit_section(db: Session, attempt: ExamAttempt, section: CourseSectionAttempt):
    if section.is_submitted:
        return

    now = datetime.now(timezone.utc)
    correct_count = 0
    for ans in section.answers:
        q = ans.question
        if ans.selected_option and q and ans.selected_option.upper() == q.correct_option.upper():
            ans.is_correct = True
            correct_count += 1
        else:
            ans.is_correct = False

    grade_info = config.score_to_nigerian_grade(correct_count, section.total_questions)
    section.score = correct_count
    section.percentage = grade_info["percentage"]
    section.grade_letter = grade_info["letter"]
    section.grade_points = grade_info["points"]
    section.is_submitted = True
    section.submitted_at = now

    # Advance attempt to the next course
    if attempt.current_course_index <= section.course_order:
        attempt.current_course_index = section.course_order + 1

    # Check if all 4 courses are now submitted
    all_sections = sorted(attempt.sections, key=lambda s: s.course_order)
    if all(s.is_submitted for s in all_sections):
        total_quality_points = sum((s.grade_points or 0) * s.credit_units for s in all_sections)
        total_units = sum(s.credit_units for s in all_sections)
        attempt.gpa = round(total_quality_points / total_units, 2) if total_units > 0 else 0.0
        attempt.total_correct = sum(s.score for s in all_sections)
        attempt.is_completed = True
        attempt.completed_at = now

    db.commit()

    # Optional phone notification via ntfy.sh when configured
    if getattr(config, "NTFY_TOPIC", ""):
        try:
            flagged_qs = [f"Q{a.question_number}" for a in section.answers if a.is_flagged]
            flag_str = f" | Flagged: {', '.join(flagged_qs)}" if flagged_qs else " | Flagged: None"
            msg = f"{attempt.student_name} ({attempt.matric_number}) submitted {section.course_code}: {section.score}/{section.total_questions} ({section.grade_letter}){flag_str}"
            if attempt.is_completed:
                msg += f"\nEXAM COMPLETED! Final CGPA: {attempt.gpa:.2f} / 5.00"
            req = urllib.request.Request(
                f"https://ntfy.sh/{config.NTFY_TOPIC}",
                data=msg.encode("utf-8"),
                headers={"Title": f"Hilary CBT Update - {section.course_code}"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=3)
        except Exception:
            pass


def compute_remaining_seconds(section: CourseSectionAttempt) -> int:
    if section.is_submitted:
        return 0
    started = ensure_utc(section.started_at)
    if not started:
        return section.duration_minutes * 60
    deadline = started + timedelta(minutes=section.duration_minutes)
    now = datetime.now(timezone.utc)
    rem = int((deadline - now).total_seconds())
    return max(0, rem)


@app.get("/", response_class=HTMLResponse)
async def welcome_page(request: Request, db: Session = Depends(get_db)):
    ctx = get_common_context(request)
    session_data = get_session_data(request)
    past_count = db.query(ExamAttempt).filter(ExamAttempt.is_completed == True).count()
    ctx["session_data"] = session_data
    ctx["past_attempts_count"] = past_count
    return templates.TemplateResponse(request=request, name="welcome.html", context=ctx)


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    ctx = get_common_context(request)
    session_data = get_session_data(request)
    ctx["session_data"] = session_data
    ctx["error"] = None
    ctx["allowed_matric_configured"] = bool(config.ALLOWED_MATRIC)
    return templates.TemplateResponse(request=request, name="login.html", context=ctx)


@app.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    matric_number: str = Form(...),
    magic_code: str = Form(...),
    db: Session = Depends(get_db),
):
    ctx = get_common_context(request)
    ctx["allowed_matric_configured"] = bool(config.ALLOWED_MATRIC)

    client_ip = request.client.host if request.client else "unknown"
    now_ts = time.time()
    record = LOGIN_ATTEMPTS.get(client_ip, {"fails": 0, "locked_until": 0.0})

    if record["locked_until"] > now_ts:
        wait_secs = int(record["locked_until"] - now_ts)
        ctx["error"] = f"Too many incorrect attempts. Please wait {wait_secs} seconds before trying again."
        return templates.TemplateResponse(request=request, name="login.html", context=ctx, status_code=429)

    clean_matric = matric_number.strip().upper()
    clean_code = magic_code.strip()

    if not clean_matric:
        ctx["error"] = "Please enter your Matric Number to continue."
        return templates.TemplateResponse(request=request, name="login.html", context=ctx, status_code=400)

    # Check if a specific Matric Number is enforced in config
    if config.ALLOWED_MATRIC and clean_matric != config.ALLOWED_MATRIC.upper():
        record["fails"] = record.get("fails", 0) + 1
        if record["fails"] >= MAX_LOGIN_FAILS:
            record["locked_until"] = now_ts + LOCKOUT_SECONDS
        LOGIN_ATTEMPTS[client_ip] = record
        ctx["error"] = "Invalid Matric Number or Magic Number. Please check and try again."
        return templates.TemplateResponse(request=request, name="login.html", context=ctx, status_code=401)

    if clean_code != config.MAGIC_CODE:
        record["fails"] = record.get("fails", 0) + 1
        remaining_tries = max(0, MAX_LOGIN_FAILS - int(record["fails"]))
        if record["fails"] >= MAX_LOGIN_FAILS:
            record["locked_until"] = now_ts + LOCKOUT_SECONDS
            LOGIN_ATTEMPTS[client_ip] = record
            ctx["error"] = "Too many wrong tries! Access is locked for 3 minutes for security."
        else:
            LOGIN_ATTEMPTS[client_ip] = record
            ctx["error"] = f"Incorrect Magic Number! Please check your access code ({remaining_tries} tries left)."
        return templates.TemplateResponse(request=request, name="login.html", context=ctx, status_code=401)

    # Reset failed login counter on success
    LOGIN_ATTEMPTS.pop(client_ip, None)

    # Check if there is an unfinished attempt for this matric number, or create a fresh one
    active_attempt = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.matric_number == clean_matric, ExamAttempt.is_completed == False)
        .order_by(ExamAttempt.id.desc())
        .first()
    )
    if not active_attempt:
        active_attempt = create_new_exam_attempt(db, clean_matric)

    response = RedirectResponse(url="/exam", status_code=303)
    set_session_cookie(response, matric_number=clean_matric, active_attempt_id=active_attempt.id)
    return response


@app.post("/start-new-attempt")
async def start_new_attempt(request: Request, db: Session = Depends(get_db)):
    session_data = get_session_data(request)
    if not session_data or not session_data.get("matric_number"):
        return RedirectResponse(url="/login", status_code=303)

    matric = session_data["matric_number"]
    new_attempt = create_new_exam_attempt(db, matric)
    response = RedirectResponse(url="/exam", status_code=303)
    set_session_cookie(response, matric_number=matric, active_attempt_id=new_attempt.id)
    return response


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("cbt_session")
    return response


@app.get("/exam", response_class=HTMLResponse)
async def exam_page(request: Request, db: Session = Depends(get_db)):
    session_data = get_session_data(request)
    if not session_data or not session_data.get("matric_number"):
        return RedirectResponse(url="/login", status_code=303)

    attempt_id = session_data.get("active_attempt_id")
    attempt = db.query(ExamAttempt).filter(ExamAttempt.id == attempt_id).first() if attempt_id else None

    if not attempt:
        attempt = (
            db.query(ExamAttempt)
            .filter(ExamAttempt.matric_number == session_data["matric_number"])
            .order_by(ExamAttempt.id.desc())
            .first()
        )
    if not attempt:
        return RedirectResponse(url="/login", status_code=303)

    if attempt.is_completed:
        return RedirectResponse(url=f"/completed/{attempt.id}", status_code=303)

    sections = sorted(attempt.sections, key=lambda s: s.course_order)

    # Check if any active section has already expired on the server clock
    while attempt.current_course_index < len(sections):
        curr_sec = sections[attempt.current_course_index]
        if curr_sec.is_submitted:
            attempt.current_course_index += 1
            db.commit()
            continue

        if curr_sec.started_at is not None and compute_remaining_seconds(curr_sec) <= 0:
            # Auto-submit expired section
            grade_and_submit_section(db, attempt, curr_sec)
            if attempt.is_completed:
                return RedirectResponse(url=f"/completed/{attempt.id}", status_code=303)
        else:
            break

    if attempt.is_completed or attempt.current_course_index >= len(sections):
        return RedirectResponse(url=f"/completed/{attempt.id}", status_code=303)

    active_section = sections[attempt.current_course_index]
    if active_section.started_at is None:
        active_section.started_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(active_section)

    remaining_seconds = compute_remaining_seconds(active_section)
    course_meta = config.COURSE_MAP.get(active_section.course_code, {})

    questions_payload = []
    for ans in sorted(active_section.answers, key=lambda a: a.question_number):
        q = ans.question
        questions_payload.append(
            {
                "answer_id": ans.id,
                "number": ans.question_number,
                "question_text": q.question_text,
                "options": {
                    "A": q.option_a,
                    "B": q.option_b,
                    "C": q.option_c,
                    "D": q.option_d,
                },
                "selected_option": ans.selected_option,
                "is_flagged": ans.is_flagged,
            }
        )

    course_steps = []
    for s in sections:
        c_info = config.COURSE_MAP.get(s.course_code, {})
        course_steps.append(
            {
                "code": s.course_code,
                "display_code": c_info.get("display_code", s.course_code),
                "title": c_info.get("title", ""),
                "duration_minutes": s.duration_minutes,
                "order": s.course_order + 1,
                "status": "completed" if s.is_submitted else ("active" if s.id == active_section.id else "upcoming"),
            }
        )

    next_course_label = None
    if attempt.current_course_index + 1 < len(sections):
        nxt_code = sections[attempt.current_course_index + 1].course_code
        nxt_meta = config.COURSE_MAP.get(nxt_code, {})
        next_course_label = f"{nxt_meta.get('display_code', nxt_code)} — {nxt_meta.get('title', '')}"

    ctx = get_common_context(request)
    ctx.update(
        {
            "attempt": attempt,
            "section": active_section,
            "course_meta": course_meta,
            "remaining_seconds": remaining_seconds,
            "questions_json": questions_payload,
            "course_steps": course_steps,
            "next_course_label": next_course_label,
        }
    )
    return templates.TemplateResponse(request=request, name="exam.html", context=ctx)


class SaveAnswerRequest(BaseModel):
    answer_id: int
    selected_option: Optional[str] = None
    is_flagged: Optional[bool] = None


@app.post("/api/save-answer")
async def api_save_answer(
    payload: SaveAnswerRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    session_data = get_session_data(request)
    if not session_data:
        raise HTTPException(status_code=401, detail="Not authenticated")

    ans = db.query(AttemptAnswer).filter(AttemptAnswer.id == payload.answer_id).first()
    if not ans:
        raise HTTPException(status_code=404, detail="Answer record not found")

    section = ans.section
    attempt = section.attempt
    if attempt.matric_number != session_data.get("matric_number"):
        raise HTTPException(status_code=403, detail="Unauthorized attempt access")

    if section.is_submitted or attempt.is_completed:
        return JSONResponse({"status": "expired", "message": "This course has already been submitted."}, status_code=400)

    # Allow 5-second grace period for in-flight requests right at timer expiry
    rem = compute_remaining_seconds(section)
    if rem <= 0:
        grade_and_submit_section(db, attempt, section)
        redirect_url = f"/completed/{attempt.id}" if attempt.is_completed else "/exam"
        return JSONResponse({"status": "time_up", "redirect_url": redirect_url})

    if payload.selected_option is not None:
        opt = payload.selected_option.strip().upper()
        ans.selected_option = opt if opt in {"A", "B", "C", "D"} else None

    if payload.is_flagged is not None:
        ans.is_flagged = bool(payload.is_flagged)

    db.commit()
    return {"status": "ok", "remaining_seconds": rem}


class SubmitSectionRequest(BaseModel):
    section_id: int


@app.post("/api/submit-section")
async def api_submit_section(
    payload: SubmitSectionRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    session_data = get_session_data(request)
    if not session_data:
        raise HTTPException(status_code=401, detail="Not authenticated")

    section = db.query(CourseSectionAttempt).filter(CourseSectionAttempt.id == payload.section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="Course section not found")

    attempt = section.attempt
    if attempt.matric_number != session_data.get("matric_number"):
        raise HTTPException(status_code=403, detail="Unauthorized attempt access")

    grade_and_submit_section(db, attempt, section)

    if attempt.is_completed:
        return {"status": "completed", "redirect_url": f"/completed/{attempt.id}"}
    else:
        return {"status": "next_course", "redirect_url": "/exam"}


@app.get("/completed/{attempt_id}", response_class=HTMLResponse)
async def exam_completed_gate(attempt_id: int, request: Request, db: Session = Depends(get_db)):
    attempt = db.query(ExamAttempt).filter(ExamAttempt.id == attempt_id).first()
    if not attempt:
        return RedirectResponse(url="/", status_code=303)
    if not attempt.is_completed:
        return RedirectResponse(url="/exam", status_code=303)

    ctx = get_common_context(request)
    ctx["attempt"] = attempt
    return templates.TemplateResponse(request=request, name="completed.html", context=ctx)


@app.get("/result/{attempt_id}", response_class=HTMLResponse)
async def result_page(attempt_id: int, request: Request, db: Session = Depends(get_db)):
    attempt = db.query(ExamAttempt).filter(ExamAttempt.id == attempt_id).first()
    if not attempt:
        return RedirectResponse(url="/", status_code=303)
    if not attempt.is_completed:
        return RedirectResponse(url="/exam", status_code=303)

    gpa_val = attempt.gpa if attempt.gpa is not None else 0.0
    classification = config.classify_gpa(gpa_val)

    sections_data = []
    for sec in sorted(attempt.sections, key=lambda s: s.course_order):
        c_meta = config.COURSE_MAP.get(sec.course_code, {})
        answers_list = []
        wrong_count = 0
        unanswered_count = 0
        flagged_count = 0

        for ans in sorted(sec.answers, key=lambda a: a.question_number):
            q = ans.question
            if not ans.selected_option:
                unanswered_count += 1
            if not ans.is_correct:
                wrong_count += 1
            if ans.is_flagged:
                flagged_count += 1

            answers_list.append(
                {
                    "number": ans.question_number,
                    "question_text": q.question_text,
                    "option_a": q.option_a,
                    "option_b": q.option_b,
                    "option_c": q.option_c,
                    "option_d": q.option_d,
                    "selected_option": ans.selected_option,
                    "correct_option": q.correct_option,
                    "is_correct": ans.is_correct,
                    "is_flagged": ans.is_flagged,
                    "explanation": q.explanation,
                }
            )

        grade_info = config.score_to_nigerian_grade(sec.score, sec.total_questions)
        sections_data.append(
            {
                "code": sec.course_code,
                "display_code": c_meta.get("display_code", sec.course_code),
                "title": c_meta.get("title", ""),
                "credit_units": sec.credit_units,
                "score": sec.score,
                "total_questions": sec.total_questions,
                "wrong_count": wrong_count,
                "unanswered_count": unanswered_count,
                "flagged_count": flagged_count,
                "percentage": sec.percentage,
                "grade_letter": sec.grade_letter or grade_info["letter"],
                "grade_points": sec.grade_points if sec.grade_points is not None else grade_info["points"],
                "quality_points": (sec.grade_points if sec.grade_points is not None else grade_info["points"]) * sec.credit_units,
                "remark": grade_info["remark"],
                "answers": answers_list,
            }
        )

    total_units = sum(s["credit_units"] for s in sections_data)
    total_quality_points = sum(s["quality_points"] for s in sections_data)
    overall_pct = round(((attempt.total_correct or 0) / attempt.total_questions) * 100, 1) if attempt.total_questions else 0.0

    # Fetch past attempts for quick progress comparison
    past_attempts = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.is_completed == True)
        .order_by(ExamAttempt.completed_at.desc())
        .limit(10)
        .all()
    )

    ctx = get_common_context(request)
    ctx.update(
        {
            "attempt": attempt,
            "gpa": f"{gpa_val:.2f}",
            "classification": classification,
            "sections_data": sections_data,
            "total_units": total_units,
            "total_quality_points": total_quality_points,
            "overall_pct": overall_pct,
            "past_attempts": past_attempts,
        }
    )
    return templates.TemplateResponse(request=request, name="result.html", context=ctx)


@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request, db: Session = Depends(get_db)):
    attempts = (
        db.query(ExamAttempt)
        .filter(ExamAttempt.is_completed == True)
        .order_by(ExamAttempt.completed_at.desc())
        .all()
    )

    history_rows = []
    for idx, att in enumerate(attempts):
        gpa_val = att.gpa if att.gpa is not None else 0.0
        cls_info = config.classify_gpa(gpa_val)
        sec_scores = {s.course_code: s for s in att.sections}
        history_rows.append(
            {
                "attempt_number": len(attempts) - idx,
                "id": att.id,
                "matric_number": att.matric_number,
                "completed_at": att.completed_at,
                "gpa": f"{gpa_val:.2f}",
                "gpa_float": gpa_val,
                "total_correct": att.total_correct or 0,
                "total_questions": att.total_questions,
                "classification": cls_info,
                "chm": sec_scores.get("CHM101"),
                "phy": sec_scores.get("PHY101"),
                "mth": sec_scores.get("MTH101"),
                "bio": sec_scores.get("BIO101"),
            }
        )

    ctx = get_common_context(request)
    ctx["history_rows"] = history_rows
    return templates.TemplateResponse(request=request, name="history.html", context=ctx)


@app.post("/history/delete/{attempt_id}")
async def delete_attempt(
    attempt_id: int,
    magic_code: str = Form(""),
    db: Session = Depends(get_db),
):
    if magic_code.strip() != config.MAGIC_CODE:
        return RedirectResponse(url="/history?error=invalid_code", status_code=303)

    attempt = db.query(ExamAttempt).filter(ExamAttempt.id == attempt_id).first()
    if attempt:
        db.delete(attempt)
        db.commit()
    return RedirectResponse(url="/history", status_code=303)
