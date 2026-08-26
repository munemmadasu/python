import streamlit as st, pandas as pd, numpy as np, plotly.express as px

st.set_page_config(page_title="Page 11 - Default Risk EDA", layout="wide")
st.title("Page 11 – Default Risk EDA")

@st.cache_data
def load_data():
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        'TARGET': np.random.choice([0, 1], n, p=[0.92, 0.08]),
        'DAYS_BIRTH': np.random.randint(-25000, -7300, n),
        'AMT_INCOME_TOTAL': np.random.exponential(120000, n) + 30000,
        'DAYS_EMPLOYED': np.random.choice([365243] + list(np.random.randint(-10000, -50, n-150)), size=n),
        'NAME_EDUCATION_TYPE': np.random.choice(['Secondary', 'Higher', 'Incomplete higher', 'Lower secondary'], n, p=[0.7, 0.2, 0.06, 0.04]),
        'OCCUPATION_TYPE': np.random.choice(['Laborers', 'Sales staff', 'Core staff', 'Managers', 'Drivers'], n),
        'NAME_CONTRACT_TYPE': np.random.choice(['Cash loans', 'Revolving loans'], n, p=[0.9, 0.1])
    })
    df['AGE_GROUP'] = pd.cut((df['DAYS_BIRTH'] / -365.25).astype(int), bins=[20, 31, 41, 51, 61, 100], labels=['20–30', '31–40', '41–50', '51–60', '60+'], right=False)
    df['INCOME_GROUP'] = pd.qcut(df['AMT_INCOME_TOTAL'], q=5, labels=['Very Low', 'Low', 'Middle', 'High', 'Very High'])
    emp = np.where(df['DAYS_EMPLOYED'] == 365243, np.nan, df['DAYS_EMPLOYED'] / -365.25)
    df['EMP_GROUP'] = pd.cut(emp, bins=[0, 1, 3, 5, 10, 20, 100], labels=['<1 Yr', '1–3 Yrs', '3–5 Yrs', '5–10 Yrs', '10–20 Yrs', '20+ Yrs'], right=False).astype(str)
    df.loc[df['DAYS_EMPLOYED'] == 365243, 'EMP_GROUP'] = 'Unemployed / Special'
    return df

df = load_data()
risk = lambda col: df.groupby(col, observed=False)['TARGET'].mean().idxmax()

# KPI Cards
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Defaults", f"{int(df['TARGET'].sum()):,}")
c2.metric("Non-Defaults", f"{int((df['TARGET']==0).sum()):,}")
c3.metric("Default Rate", f"{df['TARGET'].mean()*100:.2f}%")
c4.metric("Risk Age", risk('AGE_GROUP'))
c5.metric("Risk Income", risk('INCOME_GROUP'))
c6.metric("Risk Employment", risk('EMP_GROUP'))

# Visualizations
r1, r2 = st.columns(2)
r1.plotly_chart(px.bar(df['TARGET'].map({0:'Non-Default',1:'Default'}).value_counts().reset_index(), x='TARGET', y='count', title="TARGET Distribution"), use_container_width=True)
r2.plotly_chart(px.pie(df, names=df['TARGET'].map({0:'Non-Default',1:'Default'}), hole=0.5, title="Default Percentage"), use_container_width=True)

calc_risk = lambda col: df.groupby(col, observed=False)['TARGET'].mean().reset_index().assign(**{'Default Rate (%)': lambda x: x['TARGET']*100})

r3, r4 = st.columns(2)
r3.plotly_chart(px.bar(calc_risk('AGE_GROUP'), x='AGE_GROUP', y='Default Rate (%)', title="Default Rate by Age Group"), use_container_width=True)
r4.plotly_chart(px.bar(calc_risk('INCOME_GROUP'), x='INCOME_GROUP', y='Default Rate (%)', title="Default Rate by Income Group"), use_container_width=True)

r5, r6 = st.columns(2)
r5.plotly_chart(px.bar(calc_risk('EMP_GROUP'), x='EMP_GROUP', y='Default Rate (%)', title="Default Rate by Employment Group"), use_container_width=True)
r6.plotly_chart(px.bar(calc_risk('NAME_EDUCATION_TYPE').sort_values('Default Rate (%)'), x='Default Rate (%)', y='NAME_EDUCATION_TYPE', orientation='h', title="Default by Education"), use_container_width=True)

r7, r8 = st.columns(2)
r7.plotly_chart(px.bar(calc_risk('OCCUPATION_TYPE').sort_values('Default Rate (%)'), x='Default Rate (%)', y='OCCUPATION_TYPE', orientation='h', title="Default by Occupation"), use_container_width=True)
ctr = df.groupby(['NAME_CONTRACT_TYPE', 'TARGET']).size().reset_index(name='Count').assign(TARGET=lambda x: x['TARGET'].map({0:'Non-Default', 1:'Default'}))
r8.plotly_chart(px.bar(ctr, x='NAME_CONTRACT_TYPE', y='Count', color='TARGET', barmode='group', title="Default by Contract Type"), use_container_width=True)

# Required Insight
st.info("**Key Insight — Count vs. Rate:** Large groups yield high default *counts* due to sample size. Always evaluate *Default Rate (%)* to isolate true risk.")