import streamlit as st
from auth_system import AuthSystem

st.set_page_config(
    page_title="NSUK Auth System",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 NSUK Authentication System")
st.markdown("**Secure Login Portal | Nasarawa State University Keffi**")
st.divider()

auth = AuthSystem()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None

# Show dashboard if logged in
if st.session_state.logged_in:
    user = st.session_state.user
    
    st.success(f"Welcome, {user['full_name']}! 👋")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("User ID", user['user_id'])
    with col2:
        st.metric("Role", user['role'].upper())
    with col3:
        st.metric("Department", user['department'] or "N/A")
    
    st.divider()
    
    if user['role'] == 'admin':
        st.subheader("👑 Admin Dashboard")
        
        tab1, tab2, tab3 = st.tabs([
            "👥 All Users",
            "➕ Register User",
            "📜 Login History"
        ])
        
        with tab1:
            users = auth.get_all_users()
            st.metric("Total Users", len(users))
            st.divider()
            for u in users:
                status = "✅ Active" if u[5] == 1 else "❌ Inactive"
                with st.expander(f"{u[0]} — {u[1]} ({u[3]}) {status}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Email:** {u[2] or 'N/A'}")
                        st.markdown(f"**Department:** {u[4] or 'N/A'}")
                        st.markdown(f"**Joined:** {u[6]}")
                        st.markdown(f"**Last Login:** {u[7] or 'Never'}")
                    with col2:
                        if u[3] != 'admin':
                            if st.button(f"Deactivate", key=f"deact_{u[0]}"):
                                auth.deactivate_user(u[0])
                                st.success(f"{u[0]} deactivated")
                                st.rerun()
                            new_pass = st.text_input(
                                "New Password",
                                key=f"pass_{u[0]}",
                                type="password"
                            )
                            if st.button("Reset Password", key=f"reset_{u[0]}"):
                                if new_pass:
                                    success, msg = auth.reset_password(u[0], new_pass)
                                    st.success(msg) if success else st.error(msg)
        
        with tab2:
            st.markdown("### Register New User")
            col1, col2 = st.columns(2)
            with col1:
                new_id = st.text_input("User ID (Matric/Staff ID)")
                new_name = st.text_input("Full Name")
                new_email = st.text_input("Email")
            with col2:
                new_role = st.selectbox("Role", ["student", "lecturer", "admin"])
                new_dept = st.text_input("Department")
                new_pass = st.text_input("Password", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
            
            if st.button("Register User", type="primary"):
                if new_pass != confirm_pass:
                    st.error("Passwords do not match")
                elif new_id and new_name and new_pass:
                    success, msg = auth.register_user(
                        new_id, new_name, new_email,
                        new_pass, new_role, new_dept
                    )
                    st.success(msg) if success else st.error(msg)
                else:
                    st.error("Please fill all required fields")
        
        with tab3:
            st.markdown("### Recent Login History")
            history = auth.get_login_history()
            for h in history:
                icon = "✅" if h[2] == "success" else "❌"
                st.markdown(f"{icon} **{h[0]}** — {h[1]} — {h[2].upper()}")
    
    elif user['role'] == 'lecturer':
        st.subheader("👨‍🏫 Lecturer Dashboard")
        st.success("✅ You have access to the Essay Marking System")
        st.markdown("Click below to go to the exam management system:")
        st.link_button(
            "Go to Essay Marking System",
            "https://nsuk-essay-marker.streamlit.app"
        )
    
    elif user['role'] == 'student':
        st.subheader("🎓 Student Portal")
        st.info("Welcome to your student portal")
        st.markdown("Click below to access your exam:")
        st.link_button(
            "Go to Exam Portal",
            "https://nsuk-essay-marker.streamlit.app"
        )
    
    st.divider()
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

else:
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        user_id = st.text_input(
            "Matriculation Number / Staff ID",
            placeholder="e.g. NSU/2021/001 or STAFF/001"
        )
        password = st.text_input(
            "Password",
            type="password"
        )
        
        if st.button("Login", type="primary", use_container_width=True):
            if user_id and password:
                success, result = auth.login(user_id, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user = result
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.error("Please enter your ID and password")
        
        st.divider()
        st.info("""
        **Default Admin Account:**
        - ID: ADMIN001
        - Password: admin123
        """)
    
    with tab2:
        st.subheader("Create Student Account")
        col1, col2 = st.columns(2)
        with col1:
            reg_id = st.text_input(
                "Matriculation Number",
                placeholder="e.g. NSU/2021/001"
            )
            reg_name = st.text_input(
                "Full Name",
                placeholder="e.g. Abdulkadir Hassan"
            )
            reg_email = st.text_input(
                "Email Address",
                placeholder="e.g. abdulkadir@nsuk.edu.ng"
            )
        with col2:
            reg_dept = st.text_input(
                "Department",
                placeholder="e.g. Computer Science"
            )
        with col2:
            reg_dept = st.text_input(
                "Department",
                placeholder="e.g. Computer Science",
                key="reg_dept"
            )
            reg_pass = st.text_input(
                "Password",
                type="password",
                key="reg_pass"
            )
            reg_confirm = st.text_input(
                "Confirm Password",
                type="password",
                key="reg_confirm"
            )
        
        if st.button("Create Account", type="primary", use_container_width=True):
            if reg_pass != reg_confirm:
                st.error("Passwords do not match")
            elif reg_id and reg_name and reg_pass:
                success, msg = auth.register_user(
                    reg_id, reg_name, reg_email,
                    reg_pass, "student", reg_dept
                )
                st.success(msg) if success else st.error(msg)
                if success:
                    st.info("Account created! Go to Login tab to sign in.")
            else:
                st.error("Please fill all required fields")

with st.sidebar:
    st.header("🔐 Auth System")
    st.markdown("""
    **Features:**
    - Secure password hashing
    - Role-based access control
    - Login history tracking
    - Admin user management
    - Password reset
    - Account deactivation
    
    **Roles:**
    - 👑 Admin: Full access
    - 👨‍🏫 Lecturer: Exam management
    - 🎓 Student: Exam portal
    """)
    counts = auth.get_user_count()
    for role, count in counts:
        st.metric(f"{role.capitalize()}s", count)