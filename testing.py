import streamlit as st
import requests
import os
import sqlite3
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="NSUK AI Essay Marking System",
    page_icon="📝",
    layout="wide"
)

st.title("📝 NSUK AI Essay Marking System")
st.markdown("**Nasarawa State University Keffi | Intelligent Assessment Platform v4.0**")
st.divider()

# =========================
# CONFIG / SECURITY
# =========================
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

if not OPENROUTER_KEY:
    st.error("Missing OPENROUTER_KEY in environment variables")
    st.stop()

LECTURER_PASSWORD = os.getenv("LECTURER_PASSWORD", "admin123")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# =========================
# DATABASE
# =========================
def get_conn():
    return sqlite3.connect("nsuk_exams.db", check_same_thread=False)

def init_database():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT,
        course_title TEXT,
        lecturer_name TEXT,
        question TEXT,
        marking_guide TEXT,
        max_score INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_active INTEGER DEFAULT 1
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exam_id INTEGER,
        student_id TEXT,
        student_name TEXT,
        essay TEXT,
        score TEXT,
        grade TEXT,
        percentage TEXT,
        feedback TEXT,
        submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        approved INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_database()

# =========================
# AI MARKING ENGINE (JSON ONLY)
# =========================
def mark_essay(question, guide, max_score, essay, student_id):

    prompt = f"""
You are a strict university examiner.

Return ONLY valid JSON (no markdown, no text).

Question: {question}
Marking Guide: {guide}
Max Score: {max_score}
Student ID: {student_id}

Essay:
{essay}

JSON FORMAT:
{{
  "score": "number/{max_score}",
  "grade": "A|B|C|D|F",
  "percentage": "number%",
  "points_covered": [],
  "points_missed": [],
  "feedback": "short constructive feedback"
}}
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
            json={
                "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            },
            timeout=120
        )

        data = response.json()

        if "error" in data:
            return None, data["error"]["message"]

        content = data["choices"][0]["message"]["content"]

        return json.loads(content), None

    except json.JSONDecodeError:
        return None, "AI returned invalid JSON format"
    except Exception as e:
        return None, str(e)

# =========================
# DB HELPERS
# =========================
def save_result(exam_id, sid, name, essay, result):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO results (
        exam_id, student_id, student_name, essay,
        score, grade, percentage, feedback
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        exam_id,
        sid,
        name,
        essay,
        result["score"],
        result["grade"],
        result["percentage"],
        result["feedback"]
    ))

    conn.commit()
    conn.close()

def get_active_exam():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM exams WHERE is_active=1 ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()

    conn.close()
    return row

def student_exists(exam_id, sid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM results WHERE exam_id=? AND student_id=?", (exam_id, sid))
    exists = cur.fetchone() is not None

    conn.close()
    return exists

# =========================
# ROLE SELECTION
# =========================
role = st.sidebar.selectbox(
    "Select Role",
    ["🎓 Student", "👨‍🏫 Lecturer", "📊 Admin"]
)

# =========================
# STUDENT PANEL
# =========================
if role == "🎓 Student":

    exam = get_active_exam()

    if not exam:
        st.warning("No active exam available")
        st.stop()

    exam_id, code, title, lecturer, question, guide, max_score, *_ = exam

    st.info(f"{code} - {title}")

    if "verified" not in st.session_state:
        st.session_state.verified = False

    if not st.session_state.verified:

        sid = st.text_input("Matric Number")
        name = st.text_input("Full Name")

        if st.button("Start Exam"):
            if sid and name:
                if student_exists(exam_id, sid):
                    st.error("Already submitted")
                else:
                    st.session_state.verified = True
                    st.session_state.sid = sid
                    st.session_state.name = name
                    st.rerun()
            else:
                st.error("Fill all fields")

    else:
        st.success(f"Welcome {st.session_state.name}")

        st.markdown("### Question")
        st.info(question)

        essay = st.text_area("Your Answer", height=300)

        if st.button("Submit"):

            if len(essay.split()) < 10:
                st.error("Minimum 10 words required")
                st.stop()

            with st.spinner("Marking..."):
                result, error = mark_essay(
                    question, guide, max_score,
                    essay, st.session_state.sid
                )

            if error:
                st.error(error)
                st.stop()

            save_result(exam_id, st.session_state.sid, st.session_state.name, essay, result)

            st.success("Submitted successfully")

            st.json(result)

            st.session_state.verified = False

# =========================
# LECTURER PANEL
# =========================
elif role == "👨‍🏫 Lecturer":

    password = st.text_input("Password", type="password")

    if password != LECTURER_PASSWORD:
        st.warning("Enter lecturer password")
        st.stop()

    st.subheader("Create Exam")

    code = st.text_input("Course Code")
    title = st.text_input("Course Title")
    name = st.text_input("Lecturer Name")
    max_score = st.number_input("Max Score", 1, 100, 20)
    question = st.text_area("Question")
    guide = st.text_area("Marking Guide")

    if st.button("Save Exam"):

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO exams (course_code, course_title, lecturer_name, question, marking_guide, max_score)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (code, title, name, question, guide, max_score))

        conn.commit()
        conn.close()

        st.success("Exam created")

# =========================
# ADMIN PANEL
# =========================
elif role == "📊 Admin":

    password = st.text_input("Admin Password", type="password")

    if password != ADMIN_PASSWORD:
        st.stop()

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM exams")
    exams = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM results")
    results = cur.fetchone()[0]

    st.metric("Total Exams", exams)
    st.metric("Total Submissions", results)

    conn.close()