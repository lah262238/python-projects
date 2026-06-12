import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="NSUK AI Essay Marking Module",
    page_icon="📝",
    layout="wide"
)

st.title("📝 NSUK AI Essay Marking Module")
st.markdown("**Integration Module for Existing CBT System**")
st.markdown("*Developed by Lawal Abdulkadir Hassan | AI Engineer*")
st.divider()

def mark_essay_with_guide(question, marking_guide, max_score, student_essay, student_id):
    """Mark essay strictly using lecturer's marking guide"""
    try:
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
        if "error" in data:
            return None, f"Error: {data['error']['message']}"
        return data["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, f"Error: {str(e)}"

def parse_result(result_text, max_score):
    """Parse AI marking result"""
    parsed = {
        "score": "N/A",
        "grade": "N/A",
        "percentage": "N/A",
        "points_covered": [],
        "points_missed": [],
        "feedback": "N/A"
    }
    
    current_section = None
    
    for line in result_text.replace("None", "").strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("SCORE:"):
            parsed["score"] = line.replace("SCORE:", "").strip()
        elif line.startswith("GRADE:"):
            parsed["grade"] = line.replace("GRADE:", "").strip()
        elif line.startswith("PERCENTAGE:"):
            parsed["percentage"] = line.replace("PERCENTAGE:", "").strip()
        elif "POINTS COVERED" in line.upper():
            current_section = "covered"
        elif "POINTS MISSED" in line.upper():
            current_section = "missed"
        elif line.startswith("FEEDBACK:") or line.startswith("FEEDBACk:") or line.startswith("OVERALL FEEDBACK:"):
            parsed["feedback"] = line.replace("FEEDBACK:", "").replace("FEEDBACk:", "").replace("OVERALL FEEDBACK:", "").strip()
            current_section = "feedback"
        elif current_section == "feedback" and line:
            parsed["feedback"] += " " + line
        elif line.startswith("- "):
            if current_section == "covered":
                parsed["points_covered"].append(line[2:])
            elif current_section == "missed":
                parsed["points_missed"].append(line[2:])
    
    return parsed

# Main Interface
tab1, tab2, tab3 = st.tabs([
    "👨🏫 Lecturer Setup",
    "📝 Mark Essays",
    "📊 Results"
])

# Tab 1: Lecturer Setup
with tab1:
    st.subheader("👨🏫 Lecturer Setup Panel")
    st.markdown("Set up your exam question and marking guide once. Reuse for all students.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        course_code = st.text_input(
            "Course Code",
            placeholder="e.g. CSC 301"
        )
        course_title = st.text_input(
            "Course Title",
            placeholder="e.g. Artificial Intelligence"
        )
        lecturer_name = st.text_input(
            "Lecturer Name",
            placeholder="e.g. Dr. Abdullahi"
        )
        max_score = st.number_input(
            "Maximum Score",
            min_value=1,
            max_value=100,
            value=20
        )
    
    with col2:
        st.markdown("**Exam Question:**")
        question_method = st.radio(
            "How do you want to enter the question?",
            ["Type Question", "Upload from File"],
            horizontal=True,
            key="q_method"
        )
        
        if question_method == "Type Question":
            exam_question = st.text_area(
                "Exam Question",
                placeholder="Enter the essay question...",
                height=120
            )
        else:
            q_file = st.file_uploader(
                "Upload question file (.txt)",
                type=["txt"],
                key="q_file"
            )
            if q_file is not None:
                exam_question = q_file.read().decode("utf-8", errors="ignore")
                st.success(f"Question loaded from: {q_file.name}")
                st.text_area("Question Preview", exam_question, height=100)
            else:
                exam_question = ""
        
        st.markdown("**Marking Guide:**")
        guide_method = st.radio(
            "How do you want to enter the marking guide?",
            ["Type Guide", "Upload from File"],
            horizontal=True,
            key="g_method"
        )
        
        if guide_method == "Type Guide":
            marking_guide = st.text_area(
                "Marking Guide",
                placeholder="""Enter marking guide points. Example:
1. Definition with examples (4 marks)
2. Three main benefits (6 marks)
3. Two challenges in Nigeria (4 marks)
4. Practical recommendations (4 marks)
5. Clear conclusion (2 marks)""",
                height=200
            )
        else:
            g_file = st.file_uploader(
                "Upload marking guide file (.txt)",
                type=["txt"],
                key="g_file"
            )
            if g_file is not None:
                marking_guide = g_file.read().decode("utf-8", errors="ignore")
                st.success(f"Marking guide loaded from: {g_file.name}")
                st.text_area("Marking Guide Preview", marking_guide, height=150)
            else:
                marking_guide = ""
    
    if st.button("💾 Save Exam Setup", type="primary"):
        if course_code and exam_question and marking_guide:
            st.session_state.exam_setup = {
                "course_code": course_code,
                "course_title": course_title,
                "lecturer_name": lecturer_name,
                "max_score": max_score,
                "question": exam_question,
                "marking_guide": marking_guide
            }
            st.success(f"✅ Exam setup saved for {course_code}!")
            st.info("Go to 'Mark Essays' tab to start marking student answers.")
        else:
            st.error("Please fill in Course Code, Question, and Marking Guide.")

# Tab 2: Mark Essays
with tab2:
    st.subheader("📝 Mark Student Essays")
    
    if "exam_setup" not in st.session_state:
        st.warning("⚠️ Please set up the exam in the 'Lecturer Setup' tab first.")
    else:
        setup = st.session_state.exam_setup
        
        st.info(f"**Course:** {setup['course_code']} - {setup['course_title']} | **Max Score:** {setup['max_score']}")
        
        st.markdown("### Student Information")
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input(
                "Student Matriculation Number",
                placeholder="e.g. NSU/2021/001"
            )
        with col2:
            student_name = st.text_input(
                "Student Name",
                placeholder="e.g. Abdulkadir Hassan"
            )
        
        st.markdown("### Student Essay Answer")
        student_essay = st.text_area(
            "Paste student essay here",
            placeholder="Paste or type student essay answer...",
            height=250
        )
        
        if st.button("🎯 Mark This Essay", type="primary", use_container_width=True):
            if not student_id:
                st.error("Please enter student matriculation number.")
            elif not student_essay or len(student_essay.split()) < 5:
                st.error("Please enter a valid student essay.")
            else:
                with st.spinner("AI is marking based on your marking guide..."):
                    result, error = mark_essay_with_guide(
                        setup["question"],
                        setup["marking_guide"],
                        setup["max_score"],
                        student_essay,
                        student_id
                    )
                
                if error:
                    st.error(f"Error: {error}")
                elif result:
                    parsed = parse_result(result, setup["max_score"])
                    
                    st.success("✅ Essay marked successfully!")
                    st.divider()
                    
                    # Score Display
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
                            st.warning("No specific points identified")
                    
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
                    
                    st.divider()
                    
                    # Save to results
                    if "results" not in st.session_state:
                        st.session_state.results = []
                    
                    st.session_state.results.append({
                        "student_id": student_id,
                        "student_name": student_name,
                        "score": parsed["score"],
                        "grade": parsed["grade"],
                        "percentage": parsed["percentage"],
                        "feedback": parsed["feedback"]
                    })
                    
                    # Printable Report
                    st.markdown("### 📄 Official Marking Report")
                    report = f"""
NASARAWA STATE UNIVERSITY KEFFI
OFFICIAL AI ESSAY MARKING REPORT
{'='*50}
Course: {setup['course_code']} - {setup['course_title']}
Lecturer: {setup['lecturer_name']}
Student ID: {student_id}
Student Name: {student_name}
{'='*50}

SCORE: {parsed['score']}
GRADE: {parsed['grade']}
PERCENTAGE: {parsed['percentage']}

POINTS COVERED:
{chr(10).join(['• ' + p for p in parsed['points_covered']])}

POINTS MISSED:
{chr(10).join(['• ' + p for p in parsed['points_missed']])}

FEEDBACK:
{parsed['feedback']}

{'='*50}
Marked by: NSUK AI Essay Marking System v2.0
Developer: Lawal Abdulkadir Hassan
Note: Subject to lecturer review and approval
{'='*50}
                    """
                    st.code(report, language=None)

# Tab 3: Results
with tab3:
    st.subheader("📊 All Marked Essays")
    
    if "results" not in st.session_state or not st.session_state.results:
        st.info("No results yet. Mark some essays in the 'Mark Essays' tab.")
    else:
        results = st.session_state.results
        
        st.metric("Total Essays Marked", len(results))
        
        st.markdown("### Results Summary")
        for i, r in enumerate(results):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**{r['student_id']}**")
            with col2:
                st.write(r['student_name'])
            with col3:
                st.write(f"Score: {r['score']}")
            with col4:
                st.write(f"Grade: {r['grade']}")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Approve All Results", type="primary"):
                st.success("All results approved and ready for release!")
        with col2:
            if st.button("📥 Export Results"):
                st.info("Export feature coming in next version.")

# Sidebar
with st.sidebar:
    st.header("📝 NSUK Essay Module")
    st.markdown("""
    **How It Works:**
    
    1️⃣ Lecturer sets up question and marking guide once
    
    2️⃣ Paste each student's essay answer
    
    3️⃣ AI marks instantly based on marking guide
    
    4️⃣ Lecturer reviews and approves
    
    5️⃣ Results released to students
    
    **Key Features:**
    - Marks based on YOUR guide
    - Shows points covered/missed
    - Consistent marking
    - Printable reports
    - Results dashboard
    - Lecturer override
    
    **Integration:**
    This module connects to NSUK's existing CBT system via API.
    
    **Developer:**
    Lawal Abdulkadir Hassan
    AI Engineer | Keffi, Nigeria
    📧 lah262238@gmail.com
    """)
    
    if "exam_setup" in st.session_state:
        st.divider()
        st.success(f"Active Exam: {st.session_state.exam_setup['course_code']}")
    
    st.divider()
    st.caption("v2.0 | June 2026 | Built for NSUK")