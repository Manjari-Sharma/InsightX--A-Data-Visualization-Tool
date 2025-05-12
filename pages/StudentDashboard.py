import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Dashboard", layout="centered")
st.title("🎓 Student Dashboard - InsightX")

# 🔐 Check Login Status
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("⚠️ Access denied. Please login through login.py first.")
    st.stop()

# 👤 Get Logged-in Roll Number
student_roll = st.session_state.student_roll
student_name = st.session_state.student_name

# 📅 Select Year
year = st.selectbox("Select Year", ["2022", "2023", "2024"])
file_path = f"data/placement_{year}.csv"

# 📁 Load Year-specific Placement Data
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error(f"Data file for {year} not found.")
    st.stop()

# 🔍 Filter by Student
student_data = df[df["roll number"].astype(str) == student_roll]

if not student_data.empty:
    st.success(f"Welcome, {student_name}!")
    st.subheader(f"📄 Your Placement Details - {year}")
    st.dataframe(student_data, use_container_width=True)

    # Optional: Show company + package as a highlight
    if "company name" in student_data.columns and "package" in student_data.columns:
        company = student_data.iloc[0]["company name"]
        package = student_data.iloc[0]["package"]
        if pd.notna(company):
            st.info(f"✅ You are placed in **{company}** with a package of **₹{package} LPA**.")
        else:
            st.warning("😕 You have not been placed yet.")
else:
    st.warning("No placement data found for your roll number in this year.")
