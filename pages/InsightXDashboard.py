import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from io import BytesIO

st.set_page_config(layout="wide")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1 { color: #1f4e79; font-size: 2.5rem; font-weight: 600; margin-bottom: 0.5rem; }
    .stSidebar h1, .stSidebar h2, .stSidebar h3 { color: #1f4e79; }
    .stMarkdown > h2 { color: #1f4e79; font-size: 1.3rem; margin-top: 1.5rem; }
    .css-6qob1r.e1fqkh3o3 { background-color: #f8f9fa; }
    </style>
""", unsafe_allow_html=True)

st.title("InsightX - Data Visualization Dashboard")

# Year Selection
st.sidebar.title("Select Placement Year")
year_option = st.sidebar.selectbox("Choose a year to analyze:", (
    "Placement Data - 2022", "Placement Data - 2023", "Placement Data - 2024"
))
file_paths = {
    "Placement Data - 2022": "data/placement_2022.csv",
    "Placement Data - 2023": "data/placement_2023.csv",
    "Placement Data - 2024": "data/placement_2024.csv"
}
df = pd.read_csv(file_paths[year_option])

# Filters
st.sidebar.markdown("### Optional Filters")
if "branch" in df.columns:
    selected_branches = st.sidebar.multiselect("Filter by Branch", sorted(df["branch"].dropna().unique()))
    if selected_branches:
        df = df[df["branch"].isin(selected_branches)]

if "company name" in df.columns:
    selected_companies = st.sidebar.multiselect("Filter by Company", sorted(df["company name"].dropna().unique()))
    if selected_companies:
        df = df[df["company name"].isin(selected_companies)]

# Student Search
st.sidebar.markdown("### 🔍 Search Student Details")
query = st.sidebar.text_input("Enter Student Name or Roll Number")
if query:
    res = df[df.apply(lambda r: query.lower() in str(r).lower(), axis=1)]
    if not res.empty:
        st.subheader("🎓 Student Details")
        st.dataframe(res[["s.no", "name", "roll number", "branch", "company name", "package"]])
    else:
        st.warning("No matching student found.")

# Auto Insights
st.subheader("📌 Smart Summary")
try:
    total, placed = len(df), df["company name"].notna().sum()
    st.success(f'''
    - Total Students: **{total}**
    - Placed: **{placed}** ({(placed/total)*100:.2f}%)
    - Avg Package: ₹**{df["package"].mean():.2f} LPA**
    - Top Company: **{df["company name"].mode().iloc[0]}**
    - Top Branch: **{df["branch"].mode().iloc[0]}**
    ''')
except:
    st.warning("Missing expected columns.")

# Multi-Year Trend
st.subheader("📈 Branch-wise Placement Trend")
trend_df = pd.DataFrame()
for yr, path in file_paths.items():
    temp = pd.read_csv(path)
    if {"branch", "company name"}.issubset(temp.columns):
        placed = temp[temp["company name"].notna()]["branch"].value_counts()
        trend_df[yr] = placed
trend_df = trend_df.fillna(0).astype(int).T
fig2, ax2 = plt.subplots(figsize=(10, 5))
for col in trend_df.columns:
    ax2.plot(trend_df.index, trend_df[col], marker='o', label=col)
ax2.set_title("Placements per Branch over Years")
ax2.set_ylabel("Placed Students")
ax2.legend()
st.pyplot(fig2)

# Heatmap
if {"branch", "company name", "package"}.issubset(df.columns):
    st.subheader("🧱 Avg Package Heatmap (Branch vs Company)")
    pivot = df.pivot_table(index="branch", columns="company name", values="package", aggfunc="mean")
    fig_hm, ax_hm = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot, cmap="YlGnBu", annot=True, fmt=".1f", ax=ax_hm)
    st.pyplot(fig_hm)

# Live Search
st.subheader("🔎 Live Search")
text = st.text_input("Type to filter rows:")
filtered = df[df.apply(lambda r: text.lower() in str(r).lower(), axis=1)] if text else df
st.dataframe(filtered, use_container_width=True)

# Graph Generator
st.subheader("📊 Graph Generator")
col1, col2 = st.columns(2)
with col1:
    col_x = st.selectbox("X-axis column", ["None"] + df.columns.tolist())
    col_hue = st.selectbox("Hue (Optional)", ["None"] + df.columns.tolist())
with col2:
    y_cols = df.select_dtypes(include="number").columns.tolist()
    col_y = st.selectbox("Y-axis column", y_cols)
    chart = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Pie Chart"])

use_sci = st.checkbox("Scientific Notation Y-axis", False)
palette = st.selectbox("Color Palette", ["viridis", "magma", "coolwarm", "pastel", "rocket"])
top_n = st.slider("Top N Categories", 1, 50, 10)
agg_mode = st.radio("Aggregation Mode", ["Count", "Sum", "Average"], horizontal=True)

# --- Chart Logic ---
if col_x != "None":
    col_hue = None if col_hue == "None" else col_hue
    fig3, ax3 = plt.subplots(figsize=(10, 5))

    if chart == "Pie Chart":
        counts = df[col_x].value_counts().head(top_n)
        colors = sns.color_palette(palette, len(counts))
        ax3.pie(counts.values, labels=counts.index, autopct="%1.1f%%", colors=colors)
        st.pyplot(fig3)

    else:
        group = df.groupby([col_x, col_hue]) if col_hue else df.groupby(col_x)
        if agg_mode == "Count":
            data = group.size().reset_index(name="value") if col_hue else group.size().nlargest(top_n)
        else:
            if col_hue:
                agg = df.groupby([col_x, col_hue])[col_y]
                data = (agg.mean() if agg_mode == "Average" else agg.sum()).reset_index(name="value")
            else:
                agg = df.groupby(col_x)[col_y]
                data = (agg.mean() if agg_mode == "Average" else agg.sum()).nlargest(top_n)

        if col_hue:
            if chart == "Bar Chart":
                sns.barplot(data=data, x=col_x, y="value", hue=col_hue, ax=ax3, palette=palette)
                for bar in ax3.patches:
                    height = bar.get_height()
                    if height > 0:
                        label = f"{height:.0e}" if use_sci and height > 9999 else f"{height:.0f}"
                        ax3.annotate(label, (bar.get_x() + bar.get_width()/2, height),
                                     ha='center', va='bottom', fontsize=9, fontweight='bold')
            else:
                for h in data[col_hue].unique():
                    sub = data[data[col_hue] == h]
                    ax3.plot(sub[col_x], sub["value"], label=h, marker='o')
                    for i, val in sub.iterrows():
                        label = f"{val['value']:.0e}" if use_sci and val['value'] > 9999 else f"{val['value']:.0f}"
                        ax3.annotate(label, (val[col_x], val['value']), ha='center', va='bottom', fontsize=9)
                ax3.legend()
        else:
            if chart == "Bar Chart":
                sns.barplot(x=data.index, y=data.values, ax=ax3, palette=palette)
                for i, val in enumerate(data.values):
                    label = f"{val:.0e}" if use_sci and val > 9999 else f"{val:.0f}"
                    ax3.annotate(label, (i, val), ha='center', va='bottom', fontsize=9, fontweight='bold')
            else:
                ax3.plot(data.index, data.values, marker='o')
                for i, (x_val, y_val) in enumerate(zip(data.index, data.values)):
                    label = f"{y_val:.0e}" if use_sci and y_val > 9999 else f"{y_val:.0f}"
                    ax3.annotate(label, (x_val, y_val), ha='center', va='bottom', fontsize=9)

        if use_sci:
            ax3.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
            ax3.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45, ha="right")
        st.pyplot(fig3)

        # 📌 Detailed AI Summary
        if chart != "Pie Chart":
          if agg_mode == "Count":
            top_category = df[col_x].value_counts().idxmax()
            top_value = df[col_x].value_counts().max()
            insight = f"**Insight:** The category **{top_category}** under **{col_x}** has the highest number of records, with a total of **{top_value} students**."
          else:
           grouped_vals = df.groupby(col_x)[col_y]
           summary_series = grouped_vals.mean() if agg_mode == "Average" else grouped_vals.sum()
           top_cat = summary_series.idxmax()
           top_val = summary_series.max()
           op = "average" if agg_mode == "Average" else "total"
           insight = f"**Insight:** The category **{top_cat}** under **{col_x}** has the highest {op} value of **{col_y}**, amounting to **{top_val:.2f}**."

          if col_hue:
           insight += f" This is further categorized by **{col_hue}**, providing deeper comparative insights."

          st.markdown(insight)


        # 📥 Download
        buf = BytesIO()
        fig3.savefig(buf, format="png")
        st.download_button("📥 Download Graph", buf.getvalue(), file_name="graph.png", mime="image/png")

else:
    st.warning("Please select a column for the X-axis.")
