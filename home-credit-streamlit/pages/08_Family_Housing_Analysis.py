import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Family & Housing Analysis", layout="wide")

st.title("Page 8 – Family & Housing Analysis")
st.markdown("### Objective: Study household characteristics.")

# 1. Load Data & Derived Feature
@st.cache_data
def load_data():
    # Replace mock data with: df = pd.read_csv('data/application_train.csv')
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        'CNT_FAM_MEMBERS': np.random.choice([1, 2, 3, 4, 5], n, p=[0.2, 0.5, 0.2, 0.07, 0.03]),
        'CNT_CHILDREN': np.random.choice([0, 1, 2, 3], n, p=[0.65, 0.22, 0.10, 0.03]),
        'NAME_FAMILY_STATUS': np.random.choice(['Married', 'Single / not married', 'Civil marriage', 'Separated', 'Widow'], n),
        'NAME_HOUSING_TYPE': np.random.choice(['House / apartment', 'With parents', 'Municipal apartment', 'Rented apartment'], n, p=[0.85, 0.07, 0.05, 0.03]),
        'FLAG_OWN_CAR': np.random.choice(['Y', 'N'], n, p=[0.34, 0.66]),
        'FLAG_OWN_REALTY': np.random.choice(['Y', 'N'], n, p=[0.69, 0.31]),
        'AMT_INCOME_TOTAL': np.random.exponential(scale=120000, size=n) + 30000,
        'TARGET': np.random.choice([0, 1], n, p=[0.92, 0.08])
    })
    # Derived Feature
    df['INCOME_PER_FAM_MEMBER'] = df['AMT_INCOME_TOTAL'] / df['CNT_FAM_MEMBERS']
    return df

df = load_data()

# 2. KPI Cards
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Avg Family Size", f"{df['CNT_FAM_MEMBERS'].mean():.1f}")
c2.metric("Avg Children", f"{df['CNT_CHILDREN'].mean():.1f}")
c3.metric("Home Ownership", f"{(df['FLAG_OWN_REALTY'] == 'Y').mean()*100:.1f}%")
c4.metric("Car Ownership", f"{(df['FLAG_OWN_CAR'] == 'Y').mean()*100:.1f}%")
c5.metric("Top Housing Type", df['NAME_HOUSING_TYPE'].mode()[0])

st.markdown("---")

# 3. Graphs
# Row 1: Distributions
r1c1, r1c2, r1c3 = st.columns(3)
with r1c1:
    st.plotly_chart(px.histogram(df, x='CNT_FAM_MEMBERS', title="Family Size Distribution"), use_container_width=True)
with r1c2:
    st.plotly_chart(px.bar(df['CNT_CHILDREN'].value_counts().reset_index(), x='CNT_CHILDREN', y='count', title="Children Distribution"), use_container_width=True)
with r1c3:
    st.plotly_chart(px.bar(df['NAME_HOUSING_TYPE'].value_counts().reset_index(), x='count', y='NAME_HOUSING_TYPE', orientation='h', title="Housing Type Distribution"), use_container_width=True)

# Row 2: Donut Charts
r2c1, r2c2 = st.columns(2)
with r2c1:
    st.plotly_chart(px.pie(df, names='FLAG_OWN_REALTY', hole=0.5, title="Property Ownership"), use_container_width=True)
with r2c2:
    st.plotly_chart(px.pie(df, names='FLAG_OWN_CAR', hole=0.5, title="Car Ownership"), use_container_width=True)

# Row 3: Income & Default Relationships
r3c1, r3c2 = st.columns(2)
with r3c1:
    st.plotly_chart(px.box(df, x='CNT_FAM_MEMBERS', y='AMT_INCOME_TOTAL', log_y=True, title="Family Size vs Income"), use_container_width=True)
with r3c2:
    fam_def = df.groupby('CNT_FAM_MEMBERS')['TARGET'].mean().reset_index()
    fam_def['Default Rate (%)'] = fam_def['TARGET'] * 100
    st.plotly_chart(px.line(fam_def, x='CNT_FAM_MEMBERS', y='Default Rate (%)', markers=True, title="Family Size vs Default Rate"), use_container_width=True)

# Row 4: Derived Feature Analysis
st.subheader("Affordability: Income per Family Member")
st.plotly_chart(px.box(df, x='CNT_FAM_MEMBERS', y='INCOME_PER_FAM_MEMBER', color='NAME_HOUSING_TYPE', log_y=True, title="Income per Family Member by Housing Type"), use_container_width=True)