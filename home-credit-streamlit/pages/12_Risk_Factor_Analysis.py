import streamlit as st, pandas as pd, numpy as np, plotly.express as px

st.set_page_config(page_title="Page 12 - Risk Factors", layout="wide")
st.title("Page 12 – Risk Factor Exploration")

@st.cache_data
def load_data():
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        'TARGET': np.random.choice([0, 1], n, p=[0.92, 0.08]),
        'DAYS_BIRTH': np.random.randint(-25000, -7300, n),
        'AMT_INCOME_TOTAL': np.random.exponential(120000, n) + 30000,
        'AMT_CREDIT': np.random.exponential(400000, n) + 100000,
        'AMT_ANNUITY': np.random.exponential(20000, n) + 5000,
        'DAYS_EMPLOYED': np.random.choice([365243] + list(np.random.randint(-10000, -50, n-150)), size=n),
        'CNT_FAM_MEMBERS': np.random.choice([1, 2, 3, 4, 5], n)
    })
    df['AGE'] = (df['DAYS_BIRTH'] / -365.25).astype(int)
    emp = np.where(df['DAYS_EMPLOYED'] == 365243, np.nan, df['DAYS_EMPLOYED'] / -365.25)
    df['CREDIT_TO_INCOME'] = df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']
    df['ANNUITY_TO_INCOME'] = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']
    
    # Binned Bands
    df['Age Band'] = pd.cut(df['AGE'], bins=[20, 31, 41, 51, 61, 100], labels=['20–30', '31–40', '41–50', '51–60', '60+'], right=False)
    df['Credit Band'] = pd.qcut(df['AMT_CREDIT'], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    df['Income Band'] = pd.qcut(df['AMT_INCOME_TOTAL'], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    df['Employment Band'] = pd.cut(emp, bins=[0, 1, 3, 5, 10, 20, 100], labels=['<1 Yr', '1–3 Yrs', '3–5 Yrs', '5–10 Yrs', '10–20 Yrs', '20+ Yrs'], right=False).astype(str)
    df.loc[df['DAYS_EMPLOYED'] == 365243, 'Employment Band'] = 'Unemployed / Special'
    df['Credit-to-Income Band'] = pd.qcut(df['CREDIT_TO_INCOME'], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    df['Annuity-to-Income Band'] = pd.qcut(df['ANNUITY_TO_INCOME'], q=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    return df

df = load_data()
risk_bar = lambda col, title: px.bar(df.groupby(col, observed=False)['TARGET'].mean().reset_index().assign(**{'Default Rate (%)': lambda x: x['TARGET']*100}), x=col, y='Default Rate (%)', title=title)

# Binned Risk Charts
r1, r2 = st.columns(2)
r1.plotly_chart(risk_bar('Age Band', "Age Group vs Default Rate"), use_container_width=True)
r2.plotly_chart(risk_bar('Credit Band', "Credit Band vs Default Rate"), use_container_width=True)

r3, r4 = st.columns(2)
r3.plotly_chart(risk_bar('Income Band', "Income Band vs Default Rate"), use_container_width=True)
r4.plotly_chart(risk_bar('Employment Band', "Employment Band vs Default Rate"), use_container_width=True)

r5, r6 = st.columns(2)
r5.plotly_chart(risk_bar('Credit-to-Income Band', "Credit-to-Income Band vs Default"), use_container_width=True)
r6.plotly_chart(risk_bar('Annuity-to-Income Band', "Annuity-to-Income Band vs Default"), use_container_width=True)

# Correlation Heatmap
st.subheader("Correlation Heatmap")
num_cols = ['TARGET', 'AGE', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 'CREDIT_TO_INCOME', 'ANNUITY_TO_INCOME']
st.plotly_chart(px.imshow(df[num_cols].corr(), text_auto='.2f', aspect="auto", color_continuous_scale='RdBu_r'), use_container_width=True)

# Important Rule Notice
st.warning("**Correlation ≠ Causation:** These charts show **observed statistical relationships** only. Individual factors (e.g., age or employment duration) do not directly cause default.")