import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show_risk_segmentation_page(app_df, bureau_df=None, inst_df=None, cc_df=None):
    st.title("Page 19 – Customer Risk Segmentation Using EDA Rules")
    if app_df is None or app_df.empty:
        st.warning("application_train.csv missing.")
        return

    df = app_df.copy()

    # Derived Features & Aggregations
    df['CREDIT_INCOME_RATIO'] = df['AMT_CREDIT'] / np.where(df['AMT_INCOME_TOTAL'] == 0, np.nan, df['AMT_INCOME_TOTAL'])
    df['ANNUITY_INCOME_RATIO'] = df['AMT_ANNUITY'] / np.where(df['AMT_INCOME_TOTAL'] == 0, np.nan, df['AMT_INCOME_TOTAL'])
    
    df['TOTAL_BUREAU_DEBT'] = bureau_df.groupby('SK_ID_CURR')['AMT_CREDIT_SUM_DEBT'].sum().reindex(df['SK_ID_CURR']).fillna(0).values if bureau_df is not None else 0
    df['LATE_PAYMENTS'] = inst_df[inst_df['DAYS_ENTRY_PAYMENT'] > inst_df['DAYS_INSTALMENT']].groupby('SK_ID_CURR').size().reindex(df['SK_ID_CURR']).fillna(0).values if inst_df is not None else 0
    
    if cc_df is not None:
        cc_df['UTIL'] = cc_df['AMT_BALANCE'] / np.where(cc_df['AMT_CREDIT_LIMIT_ACTUAL'] == 0, np.nan, cc_df['AMT_CREDIT_LIMIT_ACTUAL'])
        df['AVG_CC_UTIL'] = cc_df.groupby('SK_ID_CURR')['UTIL'].mean().reindex(df['SK_ID_CURR']).fillna(0).values
    else:
        df['AVG_CC_UTIL'] = 0

    # Rule-based Scoring
    risk_score = (
        (df['CREDIT_INCOME_RATIO'] > 4).astype(int) +
        (df['ANNUITY_INCOME_RATIO'] > 0.3).astype(int) +
        (df['LATE_PAYMENTS'] >= 3).astype(int) +
        (df['TOTAL_BUREAU_DEBT'] > df['AMT_INCOME_TOTAL']).astype(int) +
        (df['AVG_CC_UTIL'] > 0.7).astype(int)
    )

    df['RISK_SEGMENT'] = np.select(
        [risk_score == 0, risk_score == 1, risk_score == 2, risk_score >= 3],
        ['Low Observed Risk', 'Moderate Observed Risk', 'Elevated Observed Risk', 'High Observed Risk'],
        default='Low Observed Risk'
    )

    st.info("**Segmentation Logic:** High Credit-to-Income (>4) + High Annuity (>0.3) + Late Payments (≥3) + High Bureau Debt (>Income) + High CC Utilization (>70%)")

    # KPIs
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Low Risk", f"{(df['RISK_SEGMENT'] == 'Low Observed Risk').sum():,}")
    c2.metric("Moderate Risk", f"{(df['RISK_SEGMENT'] == 'Moderate Observed Risk').sum():,}")
    c3.metric("Elevated Risk", f"{(df['RISK_SEGMENT'] == 'Elevated Observed Risk').sum():,}")
    c4.metric("High Risk", f"{(df['RISK_SEGMENT'] == 'High Observed Risk').sum():,}")
    c5.metric("High-Risk Exposure", f"${df[df['RISK_SEGMENT'] == 'High Observed Risk']['AMT_CREDIT'].sum():,.0f}")

    st.markdown("---")

    # Plots
    sample = df.sample(min(5000, len(df)))
    l, r = st.columns(2)
    with l:
        st.plotly_chart(px.bar(df['RISK_SEGMENT'].value_counts().reset_index(), x='RISK_SEGMENT', y='count', title="Customer Count by Segment"), use_container_width=True)
        st.plotly_chart(px.bar(df.groupby('RISK_SEGMENT')['AMT_INCOME_TOTAL'].mean().reset_index(), x='RISK_SEGMENT', y='AMT_INCOME_TOTAL', title="Avg Income by Segment"), use_container_width=True)
        st.plotly_chart(px.box(sample, x='RISK_SEGMENT', y='CREDIT_INCOME_RATIO', title="Credit-to-Income by Segment"), use_container_width=True)
        st.plotly_chart(px.bar(df.groupby('RISK_SEGMENT')['TOTAL_BUREAU_DEBT'].mean().reset_index(), x='RISK_SEGMENT', y='TOTAL_BUREAU_DEBT', title="Avg Bureau Debt by Segment"), use_container_width=True)

    with r:
        st.plotly_chart(px.pie(df, names='RISK_SEGMENT', values='AMT_CREDIT', title="Portfolio Exposure by Segment", hole=0.4), use_container_width=True)
        st.plotly_chart(px.bar(df.groupby('RISK_SEGMENT')['AMT_CREDIT'].mean().reset_index(), x='RISK_SEGMENT', y='AMT_CREDIT', title="Avg Credit by Segment"), use_container_width=True)
        st.plotly_chart(px.bar(df.groupby('RISK_SEGMENT')['LATE_PAYMENTS'].mean().reset_index(), x='RISK_SEGMENT', y='LATE_PAYMENTS', title="Avg Late Payments by Segment"), use_container_width=True)

    # Segment Sample Table
    st.dataframe(df[['SK_ID_CURR', 'RISK_SEGMENT', 'AMT_INCOME_TOTAL', 'AMT_CREDIT', 'CREDIT_INCOME_RATIO', 'LATE_PAYMENTS', 'TOTAL_BUREAU_DEBT']].head(10), use_container_width=True)