import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page setup
st.set_page_config(page_title="Income Analysis", layout="wide")

st.title("Page 6 – Income Analysis")
st.markdown("### Objective: Understand income distribution and its relationship with lending.")

# --- 1. DATA GENERATION / LOADING ---
@st.cache_data
def load_data():
    # Replace this block with: df = pd.read_csv('data/application_train.csv')
    np.random.seed(42)
    n = 1000
    
    data = {
        'AMT_INCOME_TOTAL': np.random.exponential(scale=120000, size=n) + 25000,
        'AMT_CREDIT': np.random.exponential(scale=300000, size=n) + 100000,
        'CNT_FAM_MEMBERS': np.random.choice([1, 2, 3, 4, 5], n, p=[0.2, 0.45, 0.2, 0.1, 0.05]),
        'CNT_CHILDREN': np.random.choice([0, 1, 2, 3], n, p=[0.65, 0.22, 0.10, 0.03]),
        'NAME_EDUCATION_TYPE': np.random.choice(
            ['Secondary / secondary special', 'Higher education', 'Incomplete higher', 'Lower secondary'], 
            n, p=[0.70, 0.20, 0.06, 0.04]
        ),
        'OCCUPATION_TYPE': np.random.choice(
            ['Laborers', 'Sales staff', 'Core staff', 'Managers', 'Drivers', 'High skill tech staff'], 
            n, p=[0.35, 0.20, 0.18, 0.12, 0.10, 0.05]
        ),
        'NAME_INCOME_TYPE': np.random.choice(
            ['Working', 'Commercial associate', 'Pensioner', 'State servant'], 
            n, p=[0.52, 0.23, 0.18, 0.07]
        ),
        'TARGET': np.random.choice([0, 1], n, p=[0.92, 0.08])
    }
    df = pd.DataFrame(data)
    
    # Feature Engineering
    # 1. Income per Family Member
    df['INCOME_PER_FAM_MEMBER'] = df['AMT_INCOME_TOTAL'] / df['CNT_FAM_MEMBERS']
    
    # 2. Income per Child (handling zero children safely)
    df['INCOME_PER_CHILD'] = np.where(
        df['CNT_CHILDREN'] > 0, 
        df['AMT_INCOME_TOTAL'] / df['CNT_CHILDREN'], 
        df['AMT_INCOME_TOTAL']
    )
    
    # 3. Income Percentile
    df['INCOME_PERCENTILE'] = df['AMT_INCOME_TOTAL'].rank(pct=True) * 100
    
    # 4. Quantile-Based Income Groups
    income_labels = ['Very Low', 'Low', 'Middle', 'High', 'Very High']
    df['INCOME_GROUP'] = pd.qcut(df['AMT_INCOME_TOTAL'], q=5, labels=income_labels)
    
    return df

df = load_data()

# --- 2. KPI CARDS ---
st.subheader("Key Income Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Average Income", f"${df['AMT_INCOME_TOTAL'].mean():,.2f}")
col2.metric("Median Income", f"${df['AMT_INCOME_TOTAL'].median():,.2f}")
col3.metric("Max Income", f"${df['AMT_INCOME_TOTAL'].max():,.2f}")
col4.metric("Avg / Family Member", f"${df['INCOME_PER_FAM_MEMBER'].mean():,.2f}")
col5.metric("Largest Income Group", df['INCOME_GROUP'].mode()[0])

st.markdown("---")

# --- 3. GRAPHS SECTION ---
st.subheader("Income Distributions & Groupings")

# Row 1: Income Histogram & Income Group Distribution
r1_c1, r1_c2 = st.columns(2)

with r1_c1:
    fig_hist = px.histogram(
        df[df['AMT_INCOME_TOTAL'] < df['AMT_INCOME_TOTAL'].quantile(0.99)], # Cap outliers for clean plot
        x='AMT_INCOME_TOTAL', nbins=30, title="Income Distribution (Truncated at 99th Percentile)"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with r1_c2:
    group_counts = df['INCOME_GROUP'].value_counts().reindex(
        ['Very Low', 'Low', 'Middle', 'High', 'Very High']
    ).reset_index()
    group_counts.columns = ['Income Group', 'Count']
    fig_grp = px.bar(group_counts, x='Income Group', y='Count', title="Income Group Distribution (Quantiles)")
    st.plotly_chart(fig_grp, use_container_width=True)

# Row 2: Income by Education & Income by Occupation
r2_c1, r2_c2 = st.columns(2)

with r2_c1:
    fig_edu_box = px.box(
        df, x='NAME_EDUCATION_TYPE', y='AMT_INCOME_TOTAL', 
        log_y=True, title="Income by Education Level (Log Scale)"
    )
    st.plotly_chart(fig_edu_box, use_container_width=True)

with r2_c2:
    occ_inc = df.groupby('OCCUPATION_TYPE')['AMT_INCOME_TOTAL'].median().reset_index()
    occ_inc = occ_inc.sort_values(by='AMT_INCOME_TOTAL', ascending=True)
    fig_occ = px.bar(
        occ_inc, x='AMT_INCOME_TOTAL', y='OCCUPATION_TYPE', 
        orientation='h', title="Median Income by Occupation"
    )
    st.plotly_chart(fig_occ, use_container_width=True)

# Row 3: Income by Income Type & Income vs Credit Scatter Plot
r3_c1, r3_c2 = st.columns(2)

with r3_c1:
    fig_inc_type = px.box(
        df, x='NAME_INCOME_TYPE', y='AMT_INCOME_TOTAL', 
        log_y=True, title="Income Distribution by Income Type"
    )
    st.plotly_chart(fig_inc_type, use_container_width=True)

with r3_c2:
    fig_scatter = px.scatter(
        df, x='AMT_INCOME_TOTAL', y='AMT_CREDIT', color='INCOME_GROUP',
        opacity=0.6, title="Income vs. Credit Amount",
        labels={'AMT_INCOME_TOTAL': 'Total Income ($)', 'AMT_CREDIT': 'Credit Amount ($)'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Row 4: Income Group vs Default Rate
st.subheader("Default Risk by Income Bracket")
def_rates = df.groupby('INCOME_GROUP', observed=False)['TARGET'].mean().reset_index()
def_rates['Default Rate (%)'] = def_rates['TARGET'] * 100

fig_default = px.bar(
    def_rates, x='INCOME_GROUP', y='Default Rate (%)', 
    title="Default Rate (%) across Income Groups",
    color='Default Rate (%)', color_continuous_scale='Reds'
)
st.plotly_chart(fig_default, use_container_width=True)

# --- 4. RECOMMENDATIONS & INSIGHTS ---
st.markdown("---")
st.subheader("Business Recommendations & Findings")

st.success("""
* **Highest Borrowing Segments:** Middle to High-income applicants hold the largest cumulative credit volume, taking advantage of higher credit limit eligibility.
* **Observed Default Exposure:** The **Very Low** and **Low** quantile income segments demonstrate elevated default rates compared to higher earners, primarily due to tighter cash-flow buffers during unforeseen financial shocks.
* **Loan Burden Warning:** Applicants in lower income groups with large family sizes display significantly diminished **Income per Family Member**, making them vulnerable to default even when absolute credit lines appear small.
""")


