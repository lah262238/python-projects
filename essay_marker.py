import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="NSUK AI Essay Marker",
    page_icon="📝",
    layout="wide"
)

# Header
st.title("📝 NSUK AI Essay Marking System")
st.markdown("**Prototype v1.0 | Developed by Lawal Abdulkadir Hassan | AI Engineer**")
st.markdown("*Nasarawa State University Keffi — Intelligent Assessment Platform*")
st.divider()

def mark_essay(question, rubric, max_score, student_essay):
    """Send essay to AI for marking"""
    try:
        prompt = f"""
You are an expert university examiner at Nasarawa State University Keffi, Nigeria.

Your task is to mark a student's essay fairly and professionally.

EXAM QUESTION:
{question}

MARKING RUBRIC:
{rubric}

MAXIMUM SCORE: {max_score} marks

STUDENT ESSAY:
{student_essay}

Please evaluate the essay and provide:
1. SCORE: A number out of {max_score}
2. GRADE: A, B, C, D, or F
3. OVERALL FEEDBACK: 2-3 sentences summary
4. STRENGTHS: 3 specific things the student did well
5. AREAS FOR IMPROVEMENT: 3 specific areas to improve
6. DETAILED COMMENTS: Line by line feedback on key points

Be fair, constructive, and professional. 
Consider: Content accuracy, Depth of analysis, Structure, Grammar, Relevance to question.

Format your response EXACTLY like this:
SCORE: [number]/{max_score}
GRADE: [letter]
OVERALL FEEDBACK: [feedback]
STRENGTHS:
- [strength 1]
- [strength 2]
- [strength 3]
AREAS FOR IMPROVEMENT:
- [area 1]
- [area 2]
- [area 3]
DETAILED COMMENTS: [detailed feedback]
"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": "Bearer " + os.getenv("OPENROUTER_KEY")},
            json={
                "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=120,
            verify=False
        )

        data = response.json()

        if "error" in data:
            return None, f"API Error: {data['error']['message']}"

        return data["choices"][0]["message"]["content"], None

    except Exception as e:
        return None, f"Error: {str(e)}"

def parse_result(result_text, max_score):
    """Parse AI response into structured data"""
    result_text = result_text.replace("None", "").strip()
    lines = result_text.splitlines('\n')
    parsed = {
        "score": "N/A",
        "grade": "N/A",
        "overall": "N/A",
        "strengths": [],
        "improvements": [],
        "detailed": "N/A",
        "percentage": 0
    }

    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("SCORE:"):
            try:
                score_part = line.replace("SCORE:", "").strip()
                score_num = score_part.split("/")[0].strip()
                parsed["score"] = score_num
                parsed["percentage"] = round(
                    (float(score_num) / float(max_score)) * 100, 1
                )
            except:
                parsed["score"] = line.replace("SCORE:", "").strip()

        elif line.startswith("GRADE:"):
            parsed["grade"] = line.replace("GRADE:", "").strip()

        elif line.startswith("OVERALL FEEDBACK:"):
            parsed["overall"] = line.replace("OVERALL FEEDBACK:", "").strip()
            current_section = "overall"

        elif line.startswith("STRENGTHS:") or line.startswith("STRENGTHS"):
            current_section = "strengths"

        elif "IMPROVEMENT" in line.upper() or "AREAS FOR" in line.upper():
            current_section = "improvements"

        elif line.startswith("DETAILED COMMENTS:"):
            parsed["detailed"] = line.replace("DETAILED COMMENTS:", "").strip()
            current_section = "detailed"

        elif line.startswith("- "):
            if current_section == "strengths":
                parsed["strengths"].append(line[2:])
            elif current_section == "improvements":              
                parsed["improvements"].append(line[2:])

        elif line.startswith("- ") and current_section == "improvements":
            parsed["improvements"].append(line[2:])

        elif current_section == "detailed" and line:
            parsed["detailed"] += " " + line

    return parsed

# Main Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Examiner Panel")

    question = st.text_area(
        "Exam Question",
        placeholder="Enter the exam question here...",
        height=100
    )

    rubric = st.text_area(
        "Marking Rubric / Criteria",
        placeholder="e.g., Content (40%), Analysis (30%), Structure (20%), Grammar (10%)",
        height=100,
        value="Content accuracy (40%), Depth of analysis (30%), Essay structure (20%), Grammar and clarity (10%)"
    )

    max_score = st.number_input(
        "Maximum Score",
        min_value=1,
        max_value=100,
        value=20
    )

    course_code = st.text_input(
        "Course Code (optional)",
        placeholder="e.g., CSC 301"
    )

with col2:
    st.subheader("✍️ Student Answer")

    student_id = st.text_input(
        "Student ID (optional)",
        placeholder="e.g., NSU/2021/001"
    )

    student_essay = st.text_area(
        "Student Essay",
        placeholder="Paste or type student essay here...",
        height=250
    )

st.divider()

# Mark Button
if st.button("🎯 Mark Essay", type="primary", use_container_width=True):
    if not question:
        st.error("Please enter the exam question.")
    elif not student_essay:
        st.error("Please enter the student essay.")
    elif len(student_essay.split()) < 10:
        st.error("Essay is too short. Please enter a proper essay.")
    else:
        with st.spinner("AI is marking the essay... Please wait..."):
            result, error = mark_essay(question, rubric, max_score, student_essay)
            

        if error:
            st.error(f"Error: {error}")
        elif result:
            parsed = parse_result(result, max_score)

            st.success("✅ Essay marked successfully!")
            st.divider()

            # Results Header
            st.subheader("📊 Marking Results")

            # Score Display
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Score",
                    f"{parsed['score']}/{max_score}"
                )

            with col2:
                st.metric(
                    "Grade",
                    parsed['grade']
                )

            with col3:
                st.metric(
                    "Percentage",
                    f"{parsed['percentage']}%"
                )

            with col4:
                status = "PASS" if parsed['percentage'] >= 40 else "FAIL"
                st.metric(
                    "Status",
                    status
                )

            st.divider()

            # Detailed Results
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("💬 Overall Feedback")
                st.info(parsed['overall'])

                st.subheader("✅ Strengths")
                for strength in parsed['strengths']:
                    st.success(f"• {strength}")

            with col2:
                st.subheader("📈 Areas for Improvement")
                for improvement in parsed['improvements']:
                    st.warning(f"• {improvement}")

                st.subheader("📝 Detailed Comments")
                st.write(parsed['detailed'])

            st.divider()

            # Student Report
            st.subheader("📄 Printable Report")
            report = f"""
NASARAWA STATE UNIVERSITY KEFFI
AI ESSAY MARKING REPORT
{'='*50}
Course Code: {course_code or 'N/A'}
Student ID: {student_id or 'N/A'}
{'='*50}

QUESTION:
{question}

SCORE: {parsed['score']}/{max_score} ({parsed['percentage']}%)
GRADE: {parsed['grade']}
STATUS: {'PASS' if parsed['percentage'] >= 40 else 'FAIL'}

OVERALL FEEDBACK:
{parsed['overall']}

STRENGTHS:
{chr(10).join(['• ' + s for s in parsed['strengths']])}

AREAS FOR IMPROVEMENT:
{chr(10).join(['• ' + i for i in parsed['improvements']])}

DETAILED COMMENTS:
{parsed['detailed']}

{'='*50}
Marked by: NSUK AI Essay Marking System v1.0
Developer: Lawal Abdulkadir Hassan
Note: This is an AI-assisted marking. 
Lecturer review is recommended.
{'='*50}
            """
            st.code(report, language=None)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About This System")
    st.markdown("""
    **NSUK AI Essay Marker**
    
    This prototype demonstrates how AI can 
    automatically mark student essays for 
    university examinations.
    
    **Features:**
    - Instant AI marking
    - Detailed feedback
    - Score and grade
    - Printable report
    - CBT integration ready
    
    **How It Works:**
    1. Examiner enters question
    2. Enters marking rubric
    3. Pastes student essay
    4. AI marks instantly
    5. Lecturer reviews result
    
    **Benefits for NSUK:**
    - Save marking time
    - Consistent grading
    - Instant student feedback
    - Works with CBT system
    - Scalable to all departments
    """)

    st.divider()
    st.markdown("**Developer:**")
    st.markdown("Lawal Abdulkadir Hassan")
    st.markdown("AI Engineer | Keffi, Nigeria")
    st.markdown("📧 lah262238@gmail.com")
    st.markdown("🔗 [GitHub](https://github.com/lah262238)")

    st.divider()
    st.caption("Prototype v1.0 | June 2026")
    st.caption("Built for NSUK Administration")
