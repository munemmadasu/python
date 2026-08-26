import streamlit as st
import pandas as pd
import plotly.express as px

def show_pos_cash_page(df):
    st.title("Page 16 – POS/CASH Loan Analysis")
    if df is None or df.empty:
        st.warning("POS_CASH_balance.csv missing.")
        return

    # Metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Records", f"{len(df):,}")
    c2.metric("Active", f"{(df['NAME_CONTRACT_STATUS'] == 'Active').sum():,}")
    c3.metric("Completed", f"{(df['NAME_CONTRACT_STATUS'] == 'Completed').sum():,}")
    c4.metric("Avg Rem. Inst.", f"{df['CNT_INSTALMENT_FUTURE'].mean():.1f}")
    c5.metric("Cust. w/ DPD", f"{df[df['SK_DPD'] > 0]['SK_ID_CURR'].nunique():,}")

    st.markdown("---")

    # Plots
    l, r = st.columns(2)
    with l:
        st.plotly_chart(px.bar(df['NAME_CONTRACT_STATUS'].value_counts().reset_index(), x='NAME_CONTRACT_STATUS', y='count', title="Status Distribution"), use_container_width=True)
        st.plotly_chart(px.histogram(df, x='CNT_INSTALMENT_FUTURE', nbins=30, title="Installments Remaining"), use_container_width=True)
        st.plotly_chart(px.line(df.groupby('MONTHS_BALANCE').size().reset_index(name='Count'), x='MONTHS_BALANCE', y='Count', title="Monthly Balance Trend"), use_container_width=True)

    with r:
        st.plotly_chart(px.histogram(df[df['SK_DPD'] > 0], x='SK_DPD', nbins=30, log_y=True, title="Days Past Due (DPD > 0)"), use_container_width=True)
        st.plotly_chart(px.box(df.sample(min(5000, len(df))), x='NAME_CONTRACT_STATUS', y='SK_DPD', log_y=True, title="DPD by Status"), use_container_width=True)

    # Aggregates
    st.subheader("Customer Aggregates")
    st.dataframe(df.groupby('SK_ID_CURR').agg(
        avg_dpd=('SK_DPD', 'mean'),
        max_dpd=('SK_DPD', 'max'),
        dpd_events=('SK_DPD', lambda x: (x > 0).sum()),
        avg_inst_rem=('CNT_INSTALMENT_FUTURE', 'mean'),
        completed_contracts=('NAME_CONTRACT_STATUS', lambda x: (x == 'Completed').sum())
    ).reset_index().head(10), use_container_width=True)