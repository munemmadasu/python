import streamlit as st, pandas as pd, numpy as np, plotly.express as px

st.set_page_config(page_title="Page 10 - Affordability", layout="wide")
st.title("Page 10 – Credit Affordability Analysis")

@st.cache_data
def load_data():
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        'AMT_INCOME_TOTAL': np.random.exponential(120000, n) + 30000,
        'AMT_CREDIT': np.random.exponential(400000, n) + 100000,
        'AMT_ANNUITY': np.random.exponential(20000, n) + 5000,
        'AMT_GOODS_PRICE': np.random.exponential(350000, n) + 90000,
        'CNT_FAM_MEMBERS': np.random.choice([1, 2, 3, 4, 5], n),
        'DAYS_BIRTH': np.random.randint(-25000, -7300, n),
        'TARGET': np.random.choice([0, 1], n, p=[0.92, 0.08])
    })
    # Mandatory Feature Engineering
    df['CREDIT_TO_INCOME'] = df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']
    df['ANNUITY_TO_INCOME'] = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']
    df['GOODS_TO_INCOME'] = df['AMT_GOODS_PRICE'] / df['AMT_INCOME_TOTAL']
    df['CREDIT_TO_GOODS'] = df['AMT_CREDIT'] / df['AMT_GOODS_PRICE']
    df['INCOME_PER_FAM_MEMBER'] = df['AMT_INCOME_TOTAL'] / df['CNT_FAM_MEMBERS']
    
    df['AGE'] = (df['DAYS_BIRTH'] / -365.25).astype(int)
    df['AGE_GROUP'] = pd.cut(df['AGE'], bins=[20, 31, 41, 51, 61, 100], labels=['20–30', '31–40', '41–50', '51–60', '60+'], right=False)
    df['INCOME_GROUP'] = pd.qcut(df['AMT_INCOME_TOTAL'], q=5, labels=['Very Low', 'Low', 'Middle', 'High', 'Very High'])
    return df

df = load_data()
high_cred = df['CREDIT_TO_INCOME'] > 3.0  # Industry standard: Principal > 3x annual income
high_ann = df['ANNUITY_TO_INCOME'] > 0.30  # Standard DTI cap: Debt payments > 30% income

# KPI Cards
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Avg Credit/Income", f"{df['CREDIT_TO_INCOME'].mean():.2f}x")
c2.metric("Med Credit/Income", f"{df['CREDIT_TO_INCOME'].median():.2f}x")
c3.metric("Avg Annuity/Income", f"{df['ANNUITY_TO_INCOME'].mean()*100:.1f}%")
c4.metric("High Credit Burden (>3x)", f"{high_cred.sum():,}")
c5.metric("High Annuity Burden (>30%)", f"{high_ann.sum():,}")

# Visualizations
r1, r2 = st.columns(2)
r1.plotly_chart(px.histogram(df[df['CREDIT_TO_INCOME'] < 10], x='CREDIT_TO_INCOME', nbins=20, title="Credit-to-Income Distribution"), use_container_width=True)
r2.plotly_chart(px.histogram(df[df['ANNUITY_TO_INCOME'] < 1.0], x='ANNUITY_TO_INCOME', nbins=20, title="Annuity-to-Income Distribution"), use_container_width=True)

r3, r4 = st.columns(2)
r3.plotly_chart(px.box(df[df['CREDIT_TO_INCOME'] < 10], x='TARGET', y='CREDIT_TO_INCOME', title="Credit-to-Income by Default Status"), use_container_width=True)
r4.plotly_chart(px.scatter(df, x='AMT_INCOME_TOTAL', y='AMT_CREDIT', color='CREDIT_TO_INCOME', opacity=0.6, title="Income vs Credit"), use_container_width=True)

r5, r6 = st.columns(2)
r5.plotly_chart(px.bar(df.groupby('INCOME_GROUP', observed=False)['CREDIT_TO_INCOME'].mean().reset_index(), x='INCOME_GROUP', y='CREDIT_TO_INCOME', title="Avg Credit Burden by Income Group"), use_container_width=True)
ann_age = df.groupby('AGE_GROUP', observed=False)['ANNUITY_TO_INCOME'].mean().reset_index()
ann_age['ANNUITY_TO_INCOME (%)'] = ann_age['ANNUITY_TO_INCOME'] * 100
r6.plotly_chart(px.bar(ann_age, x='AGE_GROUP', y='ANNUITY_TO_INCOME (%)', title="Avg Annuity Burden (%) by Age Group"), use_container_width=True)

# Recommendations & Threshold Justification
st.info("""
**Threshold Rationale:** High Credit Burden is set at **>3.0x** annual income (over-leveraging limit), while High Annuity Burden is set at **>30%** (debt service ratio ceiling).
**Risky Patterns:** Low-income earners carry disproportionately high credit-to-income burdens; households with multiple dependents face severely diluted per-capita disposable income.
""")