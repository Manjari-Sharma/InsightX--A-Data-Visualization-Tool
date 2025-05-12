import streamlit as st
import pandas as pd

# Load student login credentials 
users_df = pd.read_csv("users.csv")  # name,roll_number,password

# Init session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.student_roll = None
    st.session_state.student_name = None

st.title("🎓 Student Login - InsightX")

roll = st.text_input("Enter your Roll Number")
pwd = st.text_input("Enter your Password", type="password")
if st.button("Login"):
    user = users_df[
        (users_df["roll number"].astype(str) == roll) &
        (users_df["password"] == pwd)
    ]
    if not user.empty:
        st.session_state.logged_in = True
        st.session_state.student_roll = user.iloc[0]["roll number"]
        st.session_state.student_name = user.iloc[0]["name"]
        st.success(f"Welcome, {st.session_state.student_name}!")
        st.markdown("✅ Go to the top-left menu and select **Student View** to continue.")
    else:
        st.error("Invalid credentials. Please try again.")
