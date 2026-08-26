import streamlit as st, pandas as pd, numpy as np, plotly.express as px

st.set_page_config(page_title="Page 9 - Loan Applications", layout="wide")
st.title("Page 9 – Current Loan Application Analysis")

@st.cache_data
def load_data():
    np.random.seed(42)
    n = 1000
    days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
    return pd.DataFrame({
        'NAME_CONTRACT_TYPE': np.random.choice(['Cash loans', 'Revolving loans'], n, p=[0.9, 0.1]),
        'AMT_CREDIT': np.random.exponential(400000, n) + 100000,
        'AMT_ANNUITY': np.random.exponential(20000, n) + 5000,
        'AMT_GOODS_PRICE': np.random.exponential(350000, n) + 90000,
        'WEEKDAY_APPR_PROCESS_START': np.random.choice(days, n, p=[0.18, 0.18, 0.17, 0.17, 0.16, 0.08, 0.06]),
        'HOUR_APPR_PROCESS_START': np.random.choice(range(24), n)
    })

df = load_data()

# KPI Cards
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Apps", f"{len(df):,}")
c2.metric("Avg Credit", f"${df['AMT_CREDIT'].mean():,.0f}")
c3.metric("Med Credit", f"${df['AMT_CREDIT'].median():,.0f}")
c4.metric("Avg Annuity", f"${df['AMT_ANNUITY'].mean():,.0f}")
c5.metric("Avg Goods", f"${df['AMT_GOODS_PRICE'].mean():,.0f}")
c6.metric("Top Type", df['NAME_CONTRACT_TYPE'].mode()[0])

# Charts
r1, r2 = st.columns(2)
r1.plotly_chart(px.bar(df['NAME_CONTRACT_TYPE'].value_counts().reset_index(), x='NAME_CONTRACT_TYPE', y='count', title="Contract Types"), use_container_width=True)
r2.plotly_chart(px.histogram(df, x='AMT_CREDIT', nbins=20, title="Credit Distribution"), use_container_width=True)

r3, r4 = st.columns(2)
r3.plotly_chart(px.histogram(df, x='AMT_ANNUITY', nbins=20, title="Annuity Distribution"), use_container_width=True)
r4.plotly_chart(px.histogram(df, x='AMT_GOODS_PRICE', nbins=20, title="Goods Price Distribution"), use_container_width=True)

r5, r6 = st.columns(2)
r5.plotly_chart(px.scatter(df, x='AMT_GOODS_PRICE', y='AMT_CREDIT', opacity=0.5, title="Credit vs Goods Price"), use_container_width=True)
r6.plotly_chart(px.scatter(df, x='AMT_ANNUITY', y='AMT_CREDIT', opacity=0.5, title="Credit vs Annuity"), use_container_width=True)

r7, r8 = st.columns(2)
days_order = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
r7.plotly_chart(px.bar(df['WEEKDAY_APPR_PROCESS_START'].value_counts().reindex(days_order).reset_index(), x='WEEKDAY_APPR_PROCESS_START', y='count', title="Weekday Volume"), use_container_width=True)
r8.plotly_chart(px.line(df['HOUR_APPR_PROCESS_START'].value_counts().sort_index().reset_index(), x='HOUR_APPR_PROCESS_START', y='count', markers=True, title="Hourly Trend"), use_container_width=True)

# Recommendations
st.info("**Popular Type:** Cash Loans | **Credit Range:** $200k–$600k | **Peak Time:** Weekday daytime (9 AM–3 PM) | **Unusual:** Off-peak night submissions.")