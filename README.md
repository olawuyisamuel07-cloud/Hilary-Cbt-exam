# Hillary 101 CBT Examination Portal — BY SAMUELL

A custom University First Semester 100-Level Computer-Based Test (CBT) web application built with **FastAPI**, **SQLAlchemy (SQLite / PostgreSQL)**, **Jinja2**, and **Tailwind CSS** for **Olawuyi Eniola Hillary**.

---

## ✨ Key Features Built

1. **Calm & Inspiring Welcome Page (`/`)**
   - Personalized greeting for **Olawuyi Eniola Hillary** ("Welcome, Hillary!").
   - Fashionable **"BY SAMUELL"** branding + candidate spotlight frame.
   - Automatic support for a custom family photo (`static/images/family-bg.jpg` or `.png`) and custom logo (`static/images/logo.png` or `.jpg`).
2. **Secure Candidate Verification (`/login`)**
   - **Magic Number (Access Code)**: Set to **`1120`** on the server (`config.py`).
   - **Matric Number**: Currently accepts any Matric Number she enters and records it on her attempt. Once you get her official Matric Number, set `ALLOWED_MATRIC` in `config.py` (or `.env`) to lock it exclusively to that Matric Number.
   - Includes brute-force lockout protection (locks for 3 minutes after 5 wrong tries).
3. **Distraction-Free Exam Engine (`/exam`)**
   - **Pure white background and crisp black text** for a genuine university CBT exam feel.
   - **4 Sequential Courses (140 Questions Total • 85 Minutes)**:
     1. **CHM 101 (General Chemistry I)** — 35 Questions — **20 Minutes** — 2 Units
     2. **PHY 101 (General Physics I)** — 35 Questions — **20 Minutes** — 2 Units
     3. **MTH 101 (Elementary Mathematics I)** — 35 Questions — **25 Minutes** — 2 Units
     4. **BIO 101 (General Biology I)** — 35 Questions — **20 Minutes** — 2 Units
   - **Server-Authoritative Timer**: Refreshing the browser does not reset the timer. Auto-submits the active course when its timer reaches `00:00`.
   - **Full Intra-Course Navigation**: Skip questions, flag questions for review, jump to any question `1–35`, and change options (`A–D`) freely before submitting a course. Once a course is submitted, she cannot return to it.
4. **800-Question Preloaded University Pool + CSV Importer**
   - Pre-seeded with **200 questions per course (800 total questions)** with step-by-step explanations (`seed_questions.py`).
   - Each attempt randomly draws 35 questions per course.
   - Easily add or replace questions from Excel/CSV using `import_questions.py`.
5. **Dynamic 5.0 CGPA Result & Explanations (`/result/{attempt_id}`)**
   - Preceded by the **"Click to See Your Result"** screen (`/completed/{attempt_id}`).
   - Displays **"Olawuyi Eniola Hillary, this is your result"** with a **giant GPA score** inside a light ticket card over a full-bleed color background:
     - **First Class (`4.50 – 5.00`)**: **GREEN** background
     - **Second Class Upper / 2:1 (`3.50 – 4.49`)**: **YELLOW** background
     - **Second Class Lower / 2:2 (`2.40 – 3.49`), Third Class (`1.50 – 2.39`), or Fail (`< 1.50`)**: **RED** background
   - Full question-by-question review showing every missed question, her selected option vs. the correct option, and the **explanation**.
   - **Saved Attempts History (`/history`)** to track her progress over time.

---

## 🚀 Running Locally

```powershell
cd C:\Users\Ayokunle\.gemini\antigravity\scratch\hillary-cbt-exam
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

Then open **http://127.0.0.1:8000** in your browser.

---

## 🖼️ Adding Hillary's Family Photo, Logo, or Matric Number

- **Family Photo on Welcome Page**: Drop an image named `family-bg.jpg` (or `family-bg.png`) into `static/images/`. It will automatically appear on the Welcome page!
- **"BY SAMUELL" Logo**: Drop an image named `logo.png` (or `logo.jpg`) into `static/images/`.
- **Exact Matric Number**: When you have her Matric Number, open `config.py` and update:
  ```python
  ALLOWED_MATRIC = os.getenv("ALLOWED_MATRIC", "HER_MATRIC_NUMBER_HERE").strip()
  ```

---

## 📊 Importing Your Own Questions from Excel / CSV

Open `questions_template.csv` in Excel, add your questions with columns `course,question,A,B,C,D,correct,explanation`, and run:

```powershell
# Append questions to the existing pool:
.\.venv\Scripts\python.exe import_questions.py questions_template.csv

# Or replace existing questions for those courses:
.\.venv\Scripts\python.exe import_questions.py questions_template.csv --replace
```

---

## 🌐 Free Online Hosting (Render + Neon PostgreSQL)

1. **Create a Free Neon Postgres Database**:
   - Go to [neon.tech](https://neon.tech), create a free project, and copy your `postgresql://...` connection string.
2. **Push this folder to a GitHub repository**.
3. **Deploy on Render**:
   - Go to [render.com](https://render.com) -> **New +** -> **Web Service** -> connect your GitHub repo.
   - Render will automatically detect `render.yaml` (or use Build Command `pip install -r requirements.txt` and Start Command `uvicorn main:app --host 0.0.0.0 --port $PORT`).
   - Add Environment Variable `DATABASE_URL` = your Neon PostgreSQL URL.
   - Add Environment Variable `MAGIC_CODE` = `1120`.
