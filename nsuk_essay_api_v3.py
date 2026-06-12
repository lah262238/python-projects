import streamlit as st
import requests
import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="NSUK AI Essay Marking System",
    page_icon="📝",
    layout="wide"
)

st.title("📝 NSUK AI Essay Marking System")
st.markdown("**Nasarawa State University Keffi | Intelligent Assessment Platform v3.0**")
st.divider()

# ============================================================
# DATABASE SETUP
# ============================================================
def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect("nsuk_exams.db", check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT NOT NULL,
            course_title TEXT,
            lecturer_name TEXT,
            question TEXT NOT NULL,
            marking_guide TEXT NOT NULL,
            max_score INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER,
            student_id TEXT NOT NULL,
            student_name TEXT,
            essay TEXT NOT NULL,
            score TEXT,
            grade TEXT,
            percentage TEXT,
            points_covered TEXT,
            points_missed TEXT,
            feedback TEXT,
            submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            approved INTEGER DEFAULT 0
        )
    """)
    
    conn.commit()
    return conn

conn = init_database()

# ============================================================
# AI MARKING ENGINE
# ============================================================
def mark_essay_with_guide(question, marking_guide, max_score, student_essay, student_id):
    """Mark essay strictly using lecturer marking guide with proper error handling"""
    try:
        # Safety checks for empty inputs
        if not question or question.strip() == "":
            return None, "Question is empty"
        if not marking_guide or marking_guide.strip() == "":
            return None, "Marking guide is empty"
        if not student_essay or student_essay.strip() == "":
            return None, "Student essay is empty"
        
        prompt = f"""
You are an official examiner at Nasarawa State University Keffi, Nigeria.

Mark this student essay STRICTLY based on the lecturer's marking guide.

STUDENT ID: {student_id}
EXAM QUESTION: {question}
MAXIMUM SCORE: {max_score} marks

LECTURER'S MARKING GUIDE:
{marking_guide}

STUDENT ESSAY:
{student_essay}

STRICT INSTRUCTIONS:
- Award marks ONLY for points in the marking guide
- Each point in the guide has allocated marks
- Be consistent and fair
- Do not award marks for irrelevant content
- Nigerian English is acceptable

Format EXACTLY as:
SCORE: [number]/{max_score}
GRADE: [A/B/C/D/F]
PERCENTAGE: [number]%
POINTS COVERED:
- [marking guide point addressed by student]
POINTS MISSED:
- [marking guide point missed by student]
FEEDBACK: [2 constructive sentences]
"""
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": "Bearer " + os.getenv("OPENROUTER_KEY")},
            json={
                "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            },
            timeout=120,
            verify=False
        )
        
        data = response.json()
        
        # Check for API errors
        if "error" in data:
            return None, f"API Error: {data['error']['message']}"
        
        # Check if response has choices
        if "choices" not in data or len(data["choices"]) == 0:
            return None, "No response from AI"
        
        # Extract result safely
        result = data["choices"][0]["message"]["content"]
        
        # Verify result is not empty
        if result is None or result.strip() == "":
            return None, "AI returned empty response"
        
        return result, None
    
    except requests.exceptions.Timeout:
        return None, "Request timeout - AI service is slow. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Connection error - Check your internet connection."
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

# ============================================================
# RESULT PARSING
# ============================================================
def parse_result(result_text, max_score):
    """Parse AI marking result safely"""
    parsed = {
        "score": "N/A",
        "grade": "N/A",
        "percentage": "N/A",
        "points_covered": [],
        "points_missed": [],
        "feedback": "N/A"
    }
    
    # Handle None or empty results
    if result_text is None or not isinstance(result_text, str):
        return parsed
    
    if result_text.strip() == "":
        return parsed
    
    current_section = None
    
    for line in result_text.replace("None", "").strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # Parse score
        if line.startswith("SCORE:"):
            parsed["score"] = line.replace("SCORE:", "").strip()
        
        # Parse grade
        elif line.startswith("GRADE:"):
            parsed["grade"] = line.replace("GRADE:", "").strip()
        
        # Parse percentage
        elif line.startswith("PERCENTAGE:"):
            parsed["percentage"] = line.replace("PERCENTAGE:", "").strip()
        
        # Section markers
        elif "POINTS COVERED" in line.upper():
            current_section = "covered"
        elif "POINTS MISSED" in line.upper():
            current_section = "missed"
        elif line.startswith("FEEDBACK:") or line.startswith("Feedback:"):
            feedback_text = line.replace("FEEDBACK:", "").replace("Feedback:", "").strip()
            if feedback_text:
                parsed["feedback"] = feedback_text
            current_section = "feedback"
        
        # Parse points
        elif line.startswith("- "):
            point_text = line[2:]
            if current_section == "covered":
                parsed["points_covered"].append(point_text)
            elif current_section == "missed":
                parsed["points_missed"].append(point_text)
        
        # Continue feedback multi-line
        elif current_section == "feedback" and line:
            
            if parsed["feedback"] == "N/A":
                parsed["feedback"] = line
            else:
                parsed["feedback"] = parsed["feedback"] + " " + line
        else:
                parsed["feedback"] = line
    
    return parsed

# ============================================================
# DATABASE OPERATIONS
# ============================================================
def save_result(exam_id, student_id, student_name, essay, parsed):
    """Save marking result to database"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO results (
                exam_id, student_id, student_name, essay,
                score, grade, percentage,
                points_covered, points_missed, feedback
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            exam_id, student_id, student_name, essay,
            parsed["score"], parsed["grade"], parsed["percentage"],
            ", ".join(parsed["points_covered"]),
            ", ".join(parsed["points_missed"]),
            parsed["feedback"]
        ))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return False

def get_active_exam():
    """Get the currently active exam"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM exams WHERE is_active = 1 
        ORDER BY created_at DESC LIMIT 1
    """)
    return cursor.fetchone()

def get_all_results(exam_id):
    """Get all results for an exam"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM results WHERE exam_id = ?
        ORDER BY submitted_at DESC
    """, (exam_id,))
    return cursor.fetchall()

def student_already_submitted(exam_id, student_id):
    """Check if student already submitted"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM results 
        WHERE exam_id = ? AND student_id = ?
    """, (exam_id, student_id))
    return cursor.fetchone() is not None

# ============================================================
# STREAMLIT UI
# ============================================================

# Role Selection
role = st.sidebar.selectbox(
    "Select Your Role",
    ["🎓 Student Panel", "👨‍🏫 Lecturer Panel", "📊 Admin Panel"]
)

# ============================================================
# STUDENT PANEL
# ============================================================
if role == "🎓 Student Panel":
    st.subheader("🎓 Student Examination Portal")
    
    active_exam = get_active_exam()
    
    if not active_exam:
        st.warning("⚠️ No active exam at the moment. Please check with your lecturer.")
    
    else:
        exam_id = active_exam[0]
        course_code = active_exam[1]
        course_title = active_exam[2]
        question = active_exam[4]
        marking_guide = active_exam[5]
        max_score = active_exam[6]
        
        st.info(f"**Active Exam:** {course_code} - {course_title}")
        
        if "student_verified" not in st.session_state:
            st.session_state.student_verified = False
        
        if not st.session_state.student_verified:
            st.markdown("### Enter Your Details to Begin")
            col1, col2 = st.columns(2)
            with col1:
                matric = st.text_input(
                    "Matriculation Number",
                    placeholder="e.g. NSU/2021/001",
                    key="student_matric_input"
                )
            with col2:
                name = st.text_input(
                    "Full Name",
                    placeholder="e.g. Abdulkadir Hassan",
                    key="student_name_input"
                )
            
        if st.button("Start Exam", type="primary"):
            if matric and name:
                    if student_already_submitted(exam_id, matric):
                        st.error("You have already submitted this exam.")
                    else:
                        st.session_state.student_verified = True
                        st.session_state.matric = matric
                        st.session_state.student_name = name
                        st.session_state.exam_id = exam_id
                        st.rerun()
            else:
                    st.error("Please enter your matriculation number and name.")
        
        else:
            st.success(f"Welcome {st.session_state.student_name} | {st.session_state.matric}")
            st.warning("⏱️ Read the question carefully before answering.")
            st.divider()
            
            st.markdown("### Exam Question")
            st.info(question)
            
            st.markdown(f"**Maximum Score:** {max_score} marks")
            st.divider()
            
            st.markdown("### Your Answer")
            
            input_method = st.radio(
                "How do you want to submit?",
                ["Type Answer", "Upload from File (.txt)"],
                horizontal=True,
                key="student_input_method"
            )
            
            student_essay = ""
            
            if input_method == "Type Answer":
                student_essay = st.text_area(
                    "Write your essay answer here",
                    placeholder="Type your answer here...",
                    height=300,
                    key="student_essay_text"
                )
            else:
                uploaded = st.file_uploader(
                    "Upload your answer (.txt file)",
                    type=["txt"],
                    key="student_essay_file"
                )
                if uploaded:
                    student_essay = uploaded.read().decode("utf-8", errors="ignore")
                    st.success(f"File loaded: {uploaded.name}")
                    st.text_area("Preview", student_essay, height=200, disabled=True)
            
            st.divider()
            
            if st.button("📤 Submit Essay", type="primary", use_container_width=True):
                # Debug: Check what we got
                st.write(f"DEBUG: Essay length = {len(student_essay) if student_essay else 0}")
                st.write(f"DEBUG: Input method = {input_method}")
                st.write(f"DEBUG: Essay content: {student_essay[:100] if student_essay else 'EMPTY'}")
                
                if not student_essay or len(student_essay.split()) < 10:
                    st.error("Please write a proper essay before submitting (minimum 10 words).")
                else:
                    with st.spinner("Submitting and marking your essay... Please wait..."):
                        result, error = mark_essay_with_guide(
                            question,
                            marking_guide,
                            max_score,
                            student_essay,
                            st.session_state.matric
                        )
                    
                    if error:
                        st.error(f"Marking error: {error}")
                        st.info("Please try again or contact your lecturer for assistance.")
                    elif result:
                        parsed = parse_result(result, max_score)
                        
                        if save_result(
                            exam_id,
                            st.session_state.matric,
                            st.session_state.student_name,
                            student_essay,
                            parsed
                        ):
                            st.success("✅ Essay submitted and marked successfully!")
                            st.divider()
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Score", parsed["score"])
                            with col2:
                                st.metric("Grade", parsed["grade"])
                            with col3:
                                st.metric("Percentage", parsed["percentage"])
                            with col4:
                                try:
                                    pct = float(parsed["percentage"].replace("%", ""))
                                    status = "PASS" if pct >= 40 else "FAIL"
                                except:
                                    status = "N/A"
                                st.metric("Status", status)
                            
                            st.divider()
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("### ✅ Points Covered")
                                if parsed["points_covered"]:
                                    for point in parsed["points_covered"]:
                                        st.success(f"• {point}")
                                else:
                                    st.info("No specific points identified")
                            with col2:
                                st.markdown("### ❌ Points Missed")
                                if parsed["points_missed"]:
                                    for point in parsed["points_missed"]:
                                        st.error(f"• {point}")
                                else:
                                    st.success("All points covered!")
                            
                            st.divider()
                            st.markdown("### 💬 Feedback")
                            st.info(parsed["feedback"])
                            
                            st.info("📋 Results are subject to lecturer review and approval.")
                            
                            st.session_state.student_verified = False
                        else:
                            st.error("Failed to save result. Please try again.")

                            # ============================================================
## ============================================================
# LECTURER PANEL
# ============================================================
elif role == "👨‍🏫 Lecturer Panel":
    st.subheader("👨‍🏫 Lecturer Panel")
    
    tab1, tab2 = st.tabs(["📝 Setup Exam", "📊 Review Results"])
    
    with tab1:
        st.markdown("### Create New Exam")
        st.info("Set up your exam once. Students submit automatically and AI marks instantly.")
        
        col1, col2 = st.columns(2)
        with col1:
            course_code = st.text_input("Course Code", placeholder="e.g. CSC 301", key="lec_code")
            course_title = st.text_input("Course Title", placeholder="e.g. Artificial Intelligence", key="lec_title")
            lecturer_name = st.text_input("Your Name", placeholder="e.g. Dr. Abdullahi", key="lec_name")
            max_score = st.number_input("Maximum Score", min_value=1, max_value=100, value=20, key="lec_score")
        
        with col2:
            st.markdown("**Exam Question:**")
            q_method = st.radio("Input method:", ["Type", "Upload .txt file"], horizontal=True, key="q_m")
            if q_method == "Type":
                exam_question = st.text_area("Question", placeholder="Enter essay question...", height=120, key="q_text")
            else:
                q_file = st.file_uploader("Upload question (.txt)", type=["txt"], key="qf")
                exam_question = q_file.read().decode("utf-8", errors="ignore") if q_file else ""
                if q_file:
                    st.success(f"Loaded: {q_file.name}")
            
            st.markdown("**Marking Guide:**")
            g_method = st.radio("Input method:", ["Type", "Upload .txt file"], horizontal=True, key="g_m")
            if g_method == "Type":
                marking_guide = st.text_area(
                    "Marking Guide",
                    placeholder="""1. Definition (2 marks)
2. Benefits (6 marks)
3. Challenges (6 marks)
4. Recommendations (4 marks)
5. Conclusion (2 marks)""",
                    height=180,
                    key="g_text"
                )
            else:
                g_file = st.file_uploader("Upload marking guide (.txt)", type=["txt"], key="gf")
                marking_guide = g_file.read().decode("utf-8", errors="ignore") if g_file else ""
                if g_file:
                    st.success(f"Loaded: {g_file.name}")
        
        if st.button("💾 Activate Exam", type="primary", use_container_width=True):
            if course_code and exam_question and marking_guide:
                cursor = conn.cursor()
                cursor.execute("UPDATE exams SET is_active = 0")
                cursor.execute("""
                    INSERT INTO exams (course_code, course_title, lecturer_name, question, marking_guide, max_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (course_code, course_title, lecturer_name, exam_question, marking_guide, max_score))
                conn.commit()
                st.success(f"✅ Exam activated! Students can now submit their essays.")
                st.info("Students will see this exam immediately in the Student Panel.")
            else:
                st.error("Please fill in Course Code, Question, and Marking Guide.")
    
    with tab2:
        st.markdown("### Student Results")
        active_exam = get_active_exam()
        
        if not active_exam:
            st.info("No active exam found.")
        else:
            results = get_all_results(active_exam[0])
            
            if not results:
                st.info("No submissions yet. Waiting for students to submit.")
            else:
                st.metric("Total Submissions", len(results))
                st.divider()
                
                for r in results:
                    with st.expander(f"Student: {r[2]} | {r[3]} | Score: {r[5]} | Grade: {r[6]}", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Student ID:** {r[2]}")
                            st.markdown(f"**Name:** {r[3]}")
                            st.markdown(f"**Score:** {r[5]}")
                            st.markdown(f"**Grade:** {r[6]}")
                            st.markdown(f"**Percentage:** {r[7]}")
                            st.markdown(f"**Submitted:** {r[11]}")
                        with col2:
                            st.markdown(f"**Points Covered:** {r[8]}")
                            st.markdown(f"**Points Missed:** {r[9]}")
                            st.markdown(f"**Feedback:** {r[10]}")
                        
                        st.divider()
                        st.markdown("**Student Essay:**")
                        st.text_area(
                            "Essay Answer",
                            value=r[4],
                            height=200,
                            disabled=True,
                            key=f"essay_{r[0]}"
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"✅ Approve", key=f"approve_{r[0]}"):
                                cursor = conn.cursor()
                                cursor.execute("UPDATE results SET approved = 1 WHERE id = ?", (r[0],))
                                conn.commit()
                                st.success("Result approved!")
                                st.rerun()
                        with col2:
                            new_score = st.text_input(f"Override score:", key=f"override_{r[0]}", placeholder="e.g. 15/20")
                            if st.button(f"Update Score", key=f"update_{r[0]}"):
                                if new_score:
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE results SET score = ?, approved = 1 WHERE id = ?", (new_score, r[0]))
                                    conn.commit()
                                    st.success(f"Score updated to {new_score}")
                                    st.rerun()
                                else:
                                    st.error("Please enter a score")
                # ============================================================
# ADMIN PANEL
# ============================================================
elif role == "📊 Admin Panel":
    st.subheader("📊 Administration Panel")
    
    cursor = conn.cursor()
    
    col1, col2, col3 = st.columns(3)
    
    cursor.execute("SELECT COUNT(*) FROM exams")
    total_exams = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM results")
    total_results = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM results WHERE approved = 1")
    approved_results = cursor.fetchone()[0]
    
    with col1:
        st.metric("Total Exams Created", total_exams)
    with col2:
        st.metric("Total Essays Marked", total_results)
    with col3:
        st.metric("Results Approved", approved_results)
    
    st.divider()
    
    st.markdown("### All Exams")
    cursor.execute("SELECT * FROM exams ORDER BY created_at DESC")
    exams = cursor.fetchall()
    
    if exams:
        for exam in exams:
            status = "🟢 ACTIVE" if exam[7] == 1 else "🔴 Inactive"
            st.markdown(f"**{exam[1]}** - {exam[2]} | Lecturer: {exam[3]} | {status} | Created: {exam[8]}")
    else:
        st.info("No exams created yet.")

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("🎓 NSUK AI System")
    st.markdown("""
    **How It Works:**
    
    👨‍🏫 **Lecturer:**
    - Creates exam with question
    - Uploads marking guide
    - Activates exam for students
    - Reviews AI results
    - Approves or adjusts scores
    
    🎓 **Student:**
    - Logs in with matric number
    - Reads the question
    - Types or uploads essay
    - Submits for marking
    """)    

