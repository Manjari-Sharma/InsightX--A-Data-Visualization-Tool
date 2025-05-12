# 🚀 InsightX - Data Visualization & Analytics Dashboard

InsightX is a Streamlit-based interactive dashboard designed to analyze and visualize student placement data over multiple academic years.

> 📈 Built to empower colleges and students with powerful placement data insights!

---

## 🔥 Key Features

- 📊 **Interactive Graphs:** Bar, Line, and Pie charts with customizable axes and hues
- 🧠 **Auto Insights:** Highlights top hiring company, highest package, and placement ratios
- 🧪 **Graph Controls:**
  - X/Y Axis Selector
  - Hue Selector
  - Chart Type (Bar, Line, Pie)
  - Aggregation (Count, Sum, Average)
  - Scientific Notation Toggle
  - Top-N Categories Filter
  - Color Palette Selection
- 📅 **Multi-Year Data Analysis:** Analyze placement trends for 2022, 2023, and 2024
- 🔍 **Live Search & Filters:** Filter by Branch, Company, Student Name/Roll
- 🔐 **Student Login System:** Each student can log in and view their own data securely
- 🧱 **Heatmaps & Trends:** Avg. package heatmap by Branch & Company, multi-year trendline
- 📥 **Export Charts:** Download any graph as a PNG file

---

## How to Run

# 1. Clone the repo
- git clone https://github.com/yourusername/insightx.git
- cd insightx

# 2. Create a virtual environment
- python -m venv venv
- venv\Scripts\activate   # for Windows
- source venv/bin/activate   # for macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Streamlit app
streamlit run Home.py

---

## 🔐 Student Login System
users.csv should contain: name, roll number, password

Students log in via login.py

Their view is restricted to their own placement details in StudentDashboard.py

---

## ✨ Author
Made with ❤️ by Manjari Sharma

GitHub: https://github.com/Manjari-Sharma

