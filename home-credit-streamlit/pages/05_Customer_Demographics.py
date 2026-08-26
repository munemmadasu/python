import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Customer Demographic Analysis", layout="wide")

st.title("Page 5 – Customer Demographic Analysis")
st.markdown("### Objective: Understand who the Home Credit customers are.")

# --- 1. DATA GENERATION / LOADING ---
@st.cache_data
def load_data():
    # Replace this block with: df = pd.read_csv('data/application_train.csv')
    np.random.seed(42)
    n = 1000
    
    data = {
        'DAYS_BIRTH': np.random.randint(-25000, -7300, n),
        'CODE_GENDER': np.random.choice(['F', 'M'], n, p=[0.65, 0.35]),
        'NAME_EDUCATION_TYPE': np.random.choice(
            ['Secondary / secondary special', 'Higher education', 'Incomplete higher', 'Lower secondary'], 
            n, p=[0.70, 0.20, 0.06, 0.04]
        ),
        'NAME_FAMILY_STATUS': np.random.choice(
            ['Married', 'Single / not married', 'Civil marriage', 'Separated', 'Widow'], 
            n, p=[0.60, 0.15, 0.10, 0.08, 0.07]
        ),
        'NAME_INCOME_TYPE': np.random.choice(
            ['Working', 'Commercial associate', 'Pensioner', 'State servant'], 
            n, p=[0.52, 0.23, 0.18, 0.07]
        ),
        'AMT_INCOME_TOTAL': np.random.exponential(scale=150000, size=n) + 30000,
        'CNT_CHILDREN': np.random.choice([0, 1, 2, 3], n, p=[0.7, 0.2, 0.08, 0.02]),
        'CNT_FAM_MEMBERS': np.random.choice([1, 2, 3, 4], n, p=[0.2, 0.5, 0.2, 0.1])
    }
    df = pd.DataFrame(data)
    
    # Feature Engineering: Age & Age Groups
    df['AGE'] = (df['DAYS_BIRTH'] / -365.25).astype(int)
    bins = [20, 31, 41, 51, 61, 100]
    labels = ['20–30', '31–40', '41–50', '51–60', '60+']
    df['AGE_GROUP'] = pd.cut(df['AGE'], bins=bins, labels=labels, right=False)
    
    return df

df = load_data()

# --- 2. KPI CARDS ---
st.subheader("Key Demographic Indicators")
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Average Age", f"{df['AGE'].mean():.1f} yrs")
col2.metric("Median Age", f"{int(df['AGE'].median())} yrs")
col3.metric("Top Gender", df['CODE_GENDER'].mode()[0])
col4.metric("Top Education", df['NAME_EDUCATION_TYPE'].mode()[0].split('/')[0])
col5.metric("Top Income Type", df['NAME_INCOME_TYPE'].mode()[0])
col6.metric("Top Family Status", df['NAME_FAMILY_STATUS'].mode()[0])

st.markdown("---")

# --- 3. GRAPHS SECTION ---
st.subheader("Demographic Distributions")

# Row 1: Age & Gender
r1_col1, r1_col2 = st.columns(2)

with r1_col1:
    fig_age = px.histogram(df, x='AGE', nbins=20, title="Age Distribution", labels={'AGE': 'Age (Years)'})
    st.plotly_chart(fig_age, use_container_width=True)

with r1_col2:
    fig_gender = px.pie(df, names='CODE_GENDER', hole=0.4, title="Gender Distribution")
    st.plotly_chart(fig_gender, use_container_width=True)

# Row 2: Education & Family Status
r2_col1, r2_col2 = st.columns(2)

with r2_col1:
    edu_counts = df['NAME_EDUCATION_TYPE'].value_counts().reset_index()
    edu_counts.columns = ['Education', 'Count']
    fig_edu = px.bar(edu_counts, x='Count', y='Education', orientation='h', title="Education Level Distribution")
    st.plotly_chart(fig_edu, use_container_width=True)

with r2_col2:
    fam_counts = df['NAME_FAMILY_STATUS'].value_counts().reset_index()
    fam_counts.columns = ['Family Status', 'Count']
    fig_fam = px.bar(fam_counts, x='Family Status', y='Count', title="Family Status Distribution")
    st.plotly_chart(fig_fam, use_container_width=True)

# Row 3: Income Type & Age Group by Gender
r3_col1, r3_col2 = st.columns(2)

with r3_col1:
    inc_counts = df['NAME_INCOME_TYPE'].value_counts().reset_index()
    inc_counts.columns = ['Income Type', 'Count']
    fig_inc = px.bar(inc_counts, x='Count', y='Income Type', orientation='h', title="Income Type Distribution")
    st.plotly_chart(fig_inc, use_container_width=True)

with r3_col2:
    fig_age_gender = px.histogram(
        df, x='AGE_GROUP', color='CODE_GENDER', barmode='group', 
        title="Age Group by Gender", category_orders={'AGE_GROUP': ['20–30', '31–40', '41–50', '51–60', '60+']}
    )
    st.plotly_chart(fig_age_gender, use_container_width=True)

# Row 4: Age vs Income Scatter Plot
st.subheader("Bivariate Analysis")
fig_scatter = px.scatter(
    df, x='AGE', y='AMT_INCOME_TOTAL', color='CODE_GENDER', 
    opacity=0.6, title="Age vs. Total Income", labels={'AGE': 'Age', 'AMT_INCOME_TOTAL': 'Total Income ($)'}
)
st.plotly_chart(fig_scatter, use_container_width=True)

# --- 4. INSIGHTS SECTION ---
st.markdown("---")
st.subheader("Key Demographic Insights")
st.info("""
* **Core Applicant Profile:** The typical applicant is a married female with secondary education, working in a non-state sector job.
* **Age Distribution:** The borrower population is predominantly concentrated in the **31–50 age range**.
* **Gender Skew:** Female applicants represent the larger proportion of loan seekers in this dataset.
""")