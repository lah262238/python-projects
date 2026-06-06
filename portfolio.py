import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Abdulkadir Hassan | AI Engineer",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 48px;
        font-weight: bold;
        color: #1F4E79;
        text-align: center;
    }
    .sub-header {
        font-size: 24px;
        color: #2E75B6;
        text-align: center;
    }
    .section-header {
        font-size: 28px;
        font-weight: bold;
        color: #1F4E79;
        border-bottom: 2px solid #2E75B6;
        padding-bottom: 10px;
    }
    .project-card {
        background-color: #F0F4F8;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E75B6;
        margin-bottom: 20px;
    }
    .skill-badge {
        background-color: #1F4E79;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 5px;
        display: inline-block;
    }
    .metric-card {
        text-align: center;
        padding: 20px;
        background-color: #1F4E79;
        color: white;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<p class="main-header">Lawal Abdulkadir Hassan</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI Engineer | Python Developer | Automation Specialist</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666;">📍 Keffi, Nasarawa State, Nigeria | 🎯 Building AI solutions for African businesses</p>', unsafe_allow_html=True)

st.divider()

# Quick Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><h2>13</h2><p>Days Coding</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><h2>6+</h2><p>AI Projects Built</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><h2>1</h2><p>Live Deployment</p></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><h2>Oct</h2><p>2026 Target</p></div>', unsafe_allow_html=True)

st.divider()

# Navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 About Me",
    "🚀 Projects",
    "💻 Skills",
    "🎯 Services",
    "📞 Contact"
])

# Tab 1: About Me
with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("https://avatars.githubusercontent.com/u/lah262238", width=200)
        st.markdown("### Quick Info")
        st.markdown("📍 Keffi, Nasarawa State")
        st.markdown("🎓 NSUK Student")
        st.markdown("💼 AI Engineer in Training")
        st.markdown("📅 Started: May 29, 2026")
        st.markdown("🎯 Goal: October 2026")

    with col2:
        st.markdown('<p class="section-header">About Me</p>', unsafe_allow_html=True)
        st.markdown("""
        I am **Lawal Abdulkadir Hassan**, an aspiring AI Engineer from Keffi, 
        Nasarawa State, Nigeria. I started my programming journey on May 29, 2026 
        with zero prior experience.

        In just 13 days, I have built **6 working AI applications** including 
        chatbots, text summarizers, grade calculators, and an AI essay marking 
        system currently being evaluated by **Nasarawa State University Keffi**.

        My mission is to build **affordable AI solutions for African businesses** 
        that solve real local problems — from student examination systems to 
        business automation tools.

        I am committed to becoming a professional AI Engineer by **October 2026** 
        through consistent daily practice and real-world project building.
        """)

        st.markdown("### My Journey")
        progress_data = {
            "Python Fundamentals": 85,
            "AI Integration": 80,
            "Web Deployment": 75,
            "Database Management": 70,
            "OOP & Clean Code": 80,
            "API Development": 75,
        }

        for skill, progress in progress_data.items():
            st.markdown(f"**{skill}**")
            st.progress(progress / 100)

# Tab 2: Projects
with tab2:
    st.markdown('<p class="section-header">Projects Built</p>', unsafe_allow_html=True)

    projects = [
        {
            "title": "🤖 AI Chat Application",
            "description": "Multi-turn AI chatbot with conversation memory. Users can have natural conversations with AI that remembers context across messages.",
            "tech": ["Python", "Streamlit", "OpenRouter AI", "SQLite"],
            "features": ["Conversation memory", "Save chat history", "Real-time responses", "Custom AI persona"],
            "status": "✅ LIVE",
            "link": "https://abdulkadir-ai.streamlit.app"
        },
        {
            "title": "📝 AI Essay Marker",
            "description": "AI-powered essay marking system built for Nasarawa State University Keffi. Marks student essays instantly with detailed feedback.",
            "tech": ["Python", "Streamlit", "OpenRouter AI", "NLP"],
            "features": ["Instant marking", "Detailed feedback", "Grade assignment", "Printable report"],
            "status": "🔄 In Review (NSUK)",
            "link": "#"
        },
        {
            "title": "📄 AI Text Summarizer",
            "description": "Summarizes any text into a specified number of sentences using AI. Supports file input and custom output saving.",
            "tech": ["Python", "OpenRouter AI", "File I/O"],
            "features": ["Custom sentence count", "File input support", "Save summaries", "Error handling"],
            "status": "✅ Complete",
            "link": "https://github.com/lah262238/python-projects"
        },
        {
            "title": "💰 Expense Tracker",
            "description": "Professional expense tracking application with budget management, reporting, and OOP architecture.",
            "tech": ["Python", "OOP", "File Handling"],
            "features": ["Budget tracking", "Max expense finder", "Report generation", "Data persistence"],
            "status": "✅ Complete",
            "link": "https://github.com/lah262238/python-projects"
        },
        {
            "title": "🎓 Grade Calculator",
            "description": "Student grade calculation system with multiple score inputs, letter grades, and pass/fail determination.",
            "tech": ["Python", "OOP", "Input Validation"],
            "features": ["Multiple scores", "Letter grades", "Pass/Fail status", "Input validation"],
            "status": "✅ Complete",
            "link": "https://github.com/lah262238/python-projects"
        },
        {
            "title": "🗄️ Database Handler",
            "description": "Reusable database management system using SQLite. Handles conversations, expenses, and user data with full CRUD operations.",
            "tech": ["Python", "SQLite", "OOP"],
            "features": ["Multi-table support", "CRUD operations", "Logging", "Error handling"],
            "status": "✅ Complete",
            "link": "https://github.com/lah262238/python-projects"
        }
    ]

    for project in projects:
        with st.expander(f"{project['title']} — {project['status']}", expanded=False):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**Description:** {project['description']}")
                st.markdown("**Features:**")
                for feature in project['features']:
                    st.markdown(f"  • {feature}")

            with col2:
                st.markdown("**Tech Stack:**")
                for tech in project['tech']:
                    st.markdown(f"  🔧 {tech}")

                if project['link'] != "#":
                    st.markdown(f"[🔗 View Project]({project['link']})")

# Tab 3: Skills
with tab3:
    st.markdown('<p class="section-header">Technical Skills</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🐍 Python")
        skills_python = [
            "Variables & Data Types",
            "Loops & Functions",
            "Object-Oriented Programming",
            "Error Handling",
            "File I/O Operations",
            "List & Dictionary Operations"
        ]
        for skill in skills_python:
            st.markdown(f"✅ {skill}")

    with col2:
        st.markdown("### 🤖 AI & APIs")
        skills_ai = [
            "OpenRouter AI Integration",
            "Anthropic Claude API",
            "Google Gemini API",
            "REST API Calls",
            "JSON Data Handling",
            "Prompt Engineering"
        ]
        for skill in skills_ai:
            st.markdown(f"✅ {skill}")

    with col3:
        st.markdown("### 🛠️ Tools & Deployment")
        skills_tools = [
            "Git & GitHub",
            "Streamlit Deployment",
            "SQLite Databases",
            "Environment Variables",
            "VS Code",
            "PowerShell"
        ]
        for skill in skills_tools:
            st.markdown(f"✅ {skill}")

    st.divider()
    st.markdown("### 📈 Currently Learning")
    learning = [
        "Advanced Database Management",
        "Web Application Deployment",
        "User Authentication Systems",
        "Payment Integration (Paystack)",
        "Mobile App Development",
        "Machine Learning Fundamentals"
    ]
    cols = st.columns(3)
    for i, item in enumerate(learning):
        with cols[i % 3]:
            st.markdown(f"🔄 {item}")

# Tab 4: Services
with tab4:
    st.markdown('<p class="section-header">Services I Offer</p>', unsafe_allow_html=True)

    services = [
        {
            "icon": "🤖",
            "title": "AI Chatbot Development",
            "description": "Custom AI chatbots for customer support, education, or business automation.",
            "price": "$500 - $2,000",
            "timeline": "3-7 days"
        },
        {
            "icon": "📄",
            "title": "Document AI Tools",
            "description": "AI-powered tools for summarizing, analyzing, and processing documents.",
            "price": "$300 - $1,000",
            "timeline": "2-5 days"
        },
        {
            "icon": "📝",
            "title": "AI Assessment Systems",
            "description": "Automated essay marking and student assessment systems for educational institutions.",
            "price": "$1,000 - $5,000",
            "timeline": "1-2 weeks"
        },
        {
            "icon": "🔄",
            "title": "Python Automation",
            "description": "Automate repetitive business tasks using Python scripts and AI integration.",
            "price": "$200 - $800",
            "timeline": "1-3 days"
        },
        {
            "icon": "📊",
            "title": "Data Processing Tools",
            "description": "Custom tools for processing, analyzing, and visualizing business data.",
            "price": "$400 - $1,500",
            "timeline": "3-7 days"
        },
        {
            "icon": "🏫",
            "title": "Educational AI Tools",
            "description": "AI tutors, exam preparation systems, and learning management tools for schools.",
            "price": "$500 - $3,000",
            "timeline": "1-2 weeks"
        }
    ]

    col1, col2 = st.columns(2)
    for i, service in enumerate(services):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div class="project-card">
                <h3>{service['icon']} {service['title']}</h3>
                <p>{service['description']}</p>
                <p>💰 <strong>Price:</strong> {service['price']}</p>
                <p>⏱️ <strong>Timeline:</strong> {service['timeline']}</p>
            </div>
            """, unsafe_allow_html=True)

# Tab 5: Contact
with tab5:
    st.markdown('<p class="section-header">Get In Touch</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📬 Contact Information")
        st.markdown("📧 **Email:** lah262238@gmail.com")
        st.markdown("📍 **Location:** Keffi, Nasarawa State, Nigeria")
        st.markdown("🔗 **GitHub:** [github.com/lah262238](https://github.com/lah262238)")
        st.markdown("💼 **Upwork:** [View Profile](https://www.upwork.com)")
        st.markdown("🎓 **University:** Nasarawa State University Keffi (NSUK)")

        st.divider()
        st.markdown("### 🕐 Availability")
        st.success("✅ Available for new projects")
        st.markdown("- Response time: Within 24 hours")
        st.markdown("- Working hours: 6AM - 10PM WAT")
        st.markdown("- Open to: Freelance, Contract, Full-time")

    with col2:
        st.markdown("### 💌 Send a Message")
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        subject = st.selectbox("Subject", [
            "Project Inquiry",
            "Collaboration",
            "Job Opportunity",
            "NSUK Essay Marker",
            "JAMB/WAEC Tutor App",
            "Other"
        ])
        message = st.text_area("Message", height=150)

        if st.button("Send Message 📨", type="primary"):
            if name and email and message:
                st.success(f"Thank you {name}! Your message has been received. I will respond within 24 hours.")
                st.balloons()
            else:
                st.error("Please fill in all fields.")

# Footer
st.divider()
st.markdown("""
<p style="text-align:center; color:#888;">
    © 2026 Lawal Abdulkadir Hassan | AI Engineer | Keffi, Nigeria<br>
    Built with Python & Streamlit | 
    <a href="https://github.com/lah262238">GitHub</a> | 
    <a href="https://www.upwork.com">Upwork</a>
</p>
""", unsafe_allow_html=True)