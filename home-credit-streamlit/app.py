
import streamlit as st

from utils.data_loader import load_data

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Home Credit Default Risk Dashboard",
    page_icon="🏦",
    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("🏦 Home Credit Default Risk Dashboard")

st.markdown("""
Welcome to the **Home Credit Default Risk Analytics Dashboard**.

This project analyzes loan applicants and identifies patterns associated with customer default risk.

The dashboard helps understand customer profiles, financial characteristics, credit behavior, and factors influencing payment difficulties.
""")

# =====================================================
# DASHBOARD OVERVIEW
# =====================================================

with st.expander("📋 Dashboard Overview", expanded=True):

    st.write("""
### Available Pages

1. Executive Overview
2. Default Analysis
3. Demographic Analysis
4. Age Analysis
5. Gender Analysis
6. Income Analysis
7. Credit Analysis
8. Annuity Analysis
9. Education Analysis
10. Employment Analysis
11. Family Analysis
12. Housing Analysis
13. Contract Type Analysis
14. External Score Analysis
15. Regional Analysis
16. Missing Value Analysis
17. Correlation Analysis
18. Customer Risk Explorer
19. Advanced Insights
20. Data Explorer
""")

# =====================================================
# DATASET INFORMATION
# =====================================================

with st.expander("📊 Dataset Information"):

    st.write("""
### Dataset

**Source:** Home Credit Default Risk Dataset

### Target Variable

- TARGET = 0 → Customer repaid loan successfully
- TARGET = 1 → Customer faced payment difficulties

### Dataset Categories

- Customer Demographics
- Income Information
- Credit Information
- Annuity Information
- Employment Information
- Education Information
- Family Information
- Housing Information
- External Credit Scores
- Regional Characteristics
""")

# =====================================================
# BUSINESS PROBLEM
# =====================================================

with st.expander("🎯 Business Problem"):

    st.write("""
Home Credit provides loans to individuals with limited credit history.

The objective is to analyze applicant characteristics and identify customers who may face payment difficulties.

This dashboard helps:

✅ Understand customer demographics

✅ Explore financial behavior

✅ Analyze loan portfolio characteristics

✅ Identify high-risk customer groups

✅ Support data-driven lending decisions
""")

# =====================================================
# TECHNOLOGY STACK
# =====================================================

with st.expander("⚙️ Technology Stack"):

    st.write("""
### Tools Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- Scikit-Learn
- Data Visualization
- Exploratory Data Analysis (EDA)
""")

# =====================================================
# DATASET SUMMARY
# =====================================================

st.header("📈 Dataset Summary")

try:

    df = load_data("Data/application_train.csv")

    total_records = len(df)

    total_features = len(df.columns)

    default_rate = (
        df["TARGET"].mean() * 100
    )

    missing_rate = (
        df.isnull().sum().sum()
        /
        (df.shape[0] * df.shape[1])
        * 100
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Records",
        f"{total_records:,}"
    )

    col2.metric(
        "Total Features",
        total_features
    )

    col3.metric(
        "Default Rate %",
        f"{default_rate:.2f}%"
    )

    col4.metric(
        "Missing Values %",
        f"{missing_rate:.2f}%"
    )

except Exception as e:

    st.error(f"Error Loading Dataset: {e}")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Home Credit Default Risk Dashboard • Built using Streamlit and Python"
)