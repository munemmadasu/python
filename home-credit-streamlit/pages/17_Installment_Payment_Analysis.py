import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show_installment_payment_page(df):
    st.title("Page 17 – Installment Payment Analysis")
    if df is None or df.empty:
        st.warning("installments_payments.csv missing.")
        return

    # Calculations & Classifications
    df['PAYMENT_DELAY'] = df['DAYS_ENTRY_PAYMENT'] - df['DAYS_INSTALMENT']
    df['PAYMENT_DIFF'] = df['AMT_PAYMENT'] - df['AMT_INSTALMENT']
    df['PAYMENT_RATIO'] = df['AMT_PAYMENT'] / np.where(df['AMT_INSTALMENT'] == 0, np.nan, df['AMT_INSTALMENT'])

    df['TIMING_STATUS'] = np.select([df['PAYMENT_DELAY'] < 0, df['PAYMENT_DELAY'] == 0, df['PAYMENT_DELAY'] > 0], ['Early', 'On-Time', 'Late'], default='Unknown')

    tot = len(df)
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    c1.metric("Total Inst.", f"{tot:,}")
    c2.metric("Avg Inst.", f"${df['AMT_INSTALMENT'].mean():,.0f}")
    c3.metric("Avg Pay.", f"${df['AMT_PAYMENT'].mean():,.0f}")
    c4.metric("On-Time %", f"{((df['PAYMENT_DELAY'] <= 0).sum()/tot*100):.1f}%" if tot else "0%")
    c5.metric("Late %", f"{((df['PAYMENT_DELAY'] > 0).sum()/tot*100):.1f}%" if tot else "0%")
    c6.metric("Underpay %", f"{((df['PAYMENT_DIFF'] < -1).sum()/tot*100):.1f}%" if tot else "0%")
    c7.metric("Avg Delay", f"{df['PAYMENT_DELAY'].mean():.1f} d")

    st.markdown("---")

    # Plots
    sample = df.sample(min(5000, len(df)))
    l, r = st.columns(2)
    with l:
        st.plotly_chart(px.histogram(sample, x='PAYMENT_DELAY', nbins=30, title="Delay Distribution"), use_container_width=True)
        st.plotly_chart(px.scatter(sample, x='AMT_INSTALMENT', y='AMT_PAYMENT', color='TIMING_STATUS', title="Scheduled vs Actual Payment"), use_container_width=True)
        
        top_late = df[df['PAYMENT_DELAY'] > 0]['SK_ID_CURR'].value_counts().head(10).reset_index(name='Late_Count')
        st.plotly_chart(px.bar(top_late, x='Late_Count', y='SK_ID_CURR', orientation='h', title="Late Payments by Customer"), use_container_width=True)

    with r:
        st.plotly_chart(px.pie(df, names='TIMING_STATUS', title="On-Time vs Late", hole=0.4), use_container_width=True)
        st.plotly_chart(px.histogram(sample, x='PAYMENT_DIFF', nbins=30, title="Payment Difference Distribution"), use_container_width=True)
        st.plotly_chart(px.scatter(sample, x='PAYMENT_DELAY', y='AMT_PAYMENT', title="Delay Days vs Payment Amount"), use_container_width=True)

    # Customer Aggregates
    st.subheader("Customer Aggregates")
    st.dataframe(df.groupby('SK_ID_CURR').agg(
        total_installments=('NUM_INSTALMENT_NUMBER', 'count'),
        late_payment_count=('PAYMENT_DELAY', lambda x: (x > 0).sum()),
        late_payment_pct=('PAYMENT_DELAY', lambda x: (x > 0).sum() / len(x) * 100),
        avg_payment_delay=('PAYMENT_DELAY', 'mean'),
        max_payment_delay=('PAYMENT_DELAY', 'max'),
        avg_payment_ratio=('PAYMENT_RATIO', 'mean'),
        underpayment_count=('PAYMENT_DIFF', lambda x: (x < -1).sum())
    ).reset_index().head(10), use_container_width=True)