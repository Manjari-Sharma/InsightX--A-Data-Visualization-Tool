import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Dashboard", layout="centered")
st.title("🎓 Student Dashboard - InsightX")

# 🔐 Check Login Status
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("⚠️ Access denied. Please login first!")
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

st.subheader("🔐 Change Password")

with st.form("change_password_form"):
    old_pwd = st.text_input("Current Password", type="password")
    new_pwd = st.text_input("New Password", type="password")
    confirm_pwd = st.text_input("Confirm New Password", type="password")
    submitted = st.form_submit_button("Update Password")

    if submitted:
        users_df = pd.read_csv("users.csv")

        user_index = users_df[users_df["roll number"].astype(str) == student_roll].index

        if not user_index.empty:
            current_pwd = users_df.loc[user_index[0], "password"]

            if old_pwd == current_pwd:
                if new_pwd == confirm_pwd:
                    users_df.loc[user_index[0], "password"] = new_pwd
                    users_df.to_csv("users.csv", index=False)
                    st.success("✅ Password updated successfully!")
                else:
                    st.error("❌ New passwords do not match.")
            else:
                st.error("❌ Current password is incorrect.")
        else:
            st.error("❌ Student record not found.")

