import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show_credit_card_page(df):
    st.title("Page 18 – Credit Card Balance Analysis")
    if df is None or df.empty:
        st.warning("credit_card_balance.csv missing.")
        return

    # Calculations
    df['CREDIT_UTILIZATION'] = df['AMT_BALANCE'] / np.where(df['AMT_CREDIT_LIMIT_ACTUAL'] == 0, np.nan, df['AMT_CREDIT_LIMIT_ACTUAL'])

    # KPIs
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("CC Cust.", f"{df['SK_ID_CURR'].nunique():,}")
    c2.metric("Avg Bal.", f"${df['AMT_BALANCE'].mean():,.0f}")
    c3.metric("Avg Limit", f"${df['AMT_CREDIT_LIMIT_ACTUAL'].mean():,.0f}")
    c4.metric("Avg Util.", f"{(df['CREDIT_UTILIZATION'].mean()*100):.1f}%")
    c5.metric("Avg Pay.", f"${df['AMT_PAYMENT_CURRENT'].mean():,.0f}")
    c6.metric("Cust. w/ DPD", f"{df[df['SK_DPD'] > 0]['SK_ID_CURR'].nunique():,}")

    st.markdown("---")

    # Plots
    sample = df.sample(min(5000, len(df)))
    l, r = st.columns(2)
    with l:
        st.plotly_chart(px.histogram(sample, x='AMT_BALANCE', nbins=30, title="Balance Distribution"), use_container_width=True)
        st.plotly_chart(px.histogram(sample, x='CREDIT_UTILIZATION', nbins=30, title="Utilization Distribution"), use_container_width=True)
        st.plotly_chart(px.scatter(sample, x='AMT_BALANCE', y='AMT_PAYMENT_CURRENT', title="Balance vs Payment"), use_container_width=True)

    with r:
        st.plotly_chart(px.histogram(sample, x='AMT_CREDIT_LIMIT_ACTUAL', nbins=30, title="Credit Limit Distribution"), use_container_width=True)
        st.plotly_chart(px.scatter(sample, x='AMT_CREDIT_LIMIT_ACTUAL', y='AMT_BALANCE', title="Limit vs Balance"), use_container_width=True)
        st.plotly_chart(px.histogram(df[df['SK_DPD'] > 0], x='SK_DPD', nbins=30, log_y=True, title="DPD Distribution (DPD > 0)"), use_container_width=True)

    # Customer Aggregates
    st.subheader("Customer Aggregates")
    st.dataframe(df.groupby('SK_ID_CURR').agg(
        avg_balance=('AMT_BALANCE', 'mean'),
        max_balance=('AMT_BALANCE', 'max'),
        avg_credit_limit=('AMT_CREDIT_LIMIT_ACTUAL', 'mean'),
        avg_utilization=('CREDIT_UTILIZATION', 'mean'),
        max_utilization=('CREDIT_UTILIZATION', 'max'),
        total_drawings=('AMT_DRAWINGS_CURRENT', 'sum'),
        avg_payments=('AMT_PAYMENT_CURRENT', 'mean'),
        max_dpd=('SK_DPD', 'max')
    ).reset_index().head(10), use_container_width=True)