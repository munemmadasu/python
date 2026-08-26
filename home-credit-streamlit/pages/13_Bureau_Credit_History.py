import streamlit as st
import pandas as pd
import plotly.express as px

def show_bureau_page(df):
    st.title("Page 13 – Bureau Credit History Analysis")
    if df is None or df.empty:
        st.warning("bureau.csv missing.")
        return

    # --- KPIs ---
    tot_acc = len(df)
    cust_cnt = df['SK_ID_CURR'].nunique() if 'SK_ID_CURR' in df.columns else 0
    act_cnt = (df['CREDIT_ACTIVE'] == 'Active').sum()
    cls_cnt = (df['CREDIT_ACTIVE'] == 'Closed').sum()
    tot_debt = df['AMT_CREDIT_SUM_DEBT'].sum() if 'AMT_CREDIT_SUM_DEBT' in df.columns else 0
    tot_overdue = df['AMT_CREDIT_SUM_OVERDUE'].sum() if 'AMT_CREDIT_SUM_OVERDUE' in df.columns else 0

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Bureau Accounts", f"{tot_acc:,}")
    c2.metric("Cust. w/ History", f"{cust_cnt:,}")
    c3.metric("Active Credits", f"{act_cnt:,}")
    c4.metric("Closed Credits", f"{cls_cnt:,}")
    c5.metric("Total Bureau Debt", f"${tot_debt:,.0f}")
    c6.metric("Total Overdue", f"${tot_overdue:,.0f}")

    st.markdown("---")

    # --- Visualizations ---
    sample = df.sample(min(5000, len(df)))
    l, r = st.columns(2)

    with l:
        # Active vs Closed Loans
        st.plotly_chart(px.bar(df['CREDIT_ACTIVE'].value_counts().reset_index(), x='CREDIT_ACTIVE', y='count', title="Active vs Closed Loans"), use_container_width=True)
        # Credit Amount Distribution
        st.plotly_chart(px.histogram(sample, x='AMT_CREDIT_SUM', nbins=30, log_y=True, title="Bureau Credit Amount Distribution"), use_container_width=True)
        # Overdue Amount Distribution
        st.plotly_chart(px.histogram(df[df['AMT_CREDIT_SUM_OVERDUE'] > 0], x='AMT_CREDIT_SUM_OVERDUE', nbins=30, log_y=True, title="Overdue Amount Distribution (Overdue > 0)"), use_container_width=True)

    with r:
        # Credit Type Distribution (Horizontal Bar)
        st.plotly_chart(px.bar(df['CREDIT_TYPE'].value_counts().reset_index(), x='count', y='CREDIT_TYPE', orientation='h', title="Credit Type Distribution"), use_container_width=True)
        # Bureau Debt Distribution
        st.plotly_chart(px.histogram(sample, x='AMT_CREDIT_SUM_DEBT', nbins=30, log_y=True, title="Bureau Debt Distribution"), use_container_width=True)
        # Credit Type vs Total Debt
        debt_by_type = df.groupby('CREDIT_TYPE')['AMT_CREDIT_SUM_DEBT'].sum().reset_index()
        st.plotly_chart(px.bar(debt_by_type, x='CREDIT_TYPE', y='AMT_CREDIT_SUM_DEBT', title="Credit Type vs Total Debt"), use_container_width=True)

    # --- Customer Aggregates ---
    st.subheader("Customer Aggregates")
    st.dataframe(df.groupby('SK_ID_CURR').agg(
        num_bureau_accounts=('SK_ID_BUREAU', 'count'),
        num_active_accounts=('CREDIT_ACTIVE', lambda x: (x == 'Active').sum()),
        num_closed_accounts=('CREDIT_ACTIVE', lambda x: (x == 'Closed').sum()),
        total_bureau_credit=('AMT_CREDIT_SUM', 'sum'),
        total_bureau_debt=('AMT_CREDIT_SUM_DEBT', 'sum'),
        avg_bureau_credit=('AMT_CREDIT_SUM', 'mean'),
        max_overdue_amount=('AMT_CREDIT_SUM_OVERDUE', 'max')
    ).reset_index().head(10), use_container_width=True)