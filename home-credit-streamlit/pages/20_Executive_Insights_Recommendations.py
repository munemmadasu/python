import streamlit as st
import pandas as pd
import numpy as np

def show_executive_insights_page(app_df, bureau_df=None, inst_df=None, cc_df=None):
    st.title("Page 20 – Executive Insights & Business Recommendations")
    if app_df is None or app_df.empty:
        st.warning("data/application_train.csv missing.")
        return

    # Metrics Calculations
    tot_cust = len(app_df)
    def_rate = (app_df['TARGET'].mean() * 100) if 'TARGET' in app_df.columns else 0.0
    high_burden = ((app_df['AMT_CREDIT'] / np.where(app_df['AMT_INCOME_TOTAL'] == 0, np.nan, app_df['AMT_INCOME_TOTAL'])) > 4).sum()
    late_pay = inst_df[inst_df['DAYS_ENTRY_PAYMENT'] > inst_df['DAYS_INSTALMENT']]['SK_ID_CURR'].nunique() if inst_df is not None else 0
    bureau_debt = bureau_df[bureau_df['AMT_CREDIT_SUM_DEBT'] > 0]['SK_ID_CURR'].nunique() if bureau_df is not None else 0

    high_cc = 0
    if cc_df is not None:
        cc_util = cc_df.groupby('SK_ID_CURR').apply(lambda x: (x['AMT_BALANCE'] / np.where(x['AMT_CREDIT_LIMIT_ACTUAL'] == 0, np.nan, x['AMT_CREDIT_LIMIT_ACTUAL'])).mean())
        high_cc = (cc_util > 0.7).sum()

    # Executive KPIs
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Cust.", f"{tot_cust:,}")
    c2.metric("Default Rate", f"{def_rate:.2f}%")
    c3.metric("Total Credit Exp.", f"${app_df['AMT_CREDIT'].sum():,.0f}")
    c4.metric("Avg Credit", f"${app_df['AMT_CREDIT'].mean():,.0f}")
    c5.metric("Avg Income", f"${app_df['AMT_INCOME_TOTAL'].mean():,.0f}")

    c6, c7, c8, c9, c10 = st.columns(5)
    c6.metric("High Burden", f"{high_burden:,}")
    c7.metric("Late Pay Cust.", f"{late_pay:,}")
    c8.metric("Bureau Debt", f"{bureau_debt:,}")
    c9.metric("High CC Util", f"{high_cc:,}")
    c10.metric("Elevated Risk", f"{(high_burden + late_pay) // 2:,}")

    st.markdown("---")

    # Top 10 Insights
    st.subheader("Top 10 Portfolio Insights")
    insights = [
        "**1. Employment History:** Customers with short employment (<2 yrs) show higher observed default rates.",
        "**2. Debt-Burden Risk:** Credit-to-Income ratios > 4.0 correlate with elevated default likelihood.",
        "**3. Repayment Behaviour:** Repeated late installment payments form a primary risk-monitoring group.",
        "**4. External Debt Pressure:** High CC utilization (>70%) with bureau debt signals increased financial strain.",
        "**5. Income Segment Risk:** Low-income tiers display higher default rates despite lower average credit amounts.",
        "**6. Bureau History:** Customers with multiple active external loans show higher overall portfolio exposure.",
        "**7. Contract Types:** Cash loans demonstrate higher default rates compared to revolving or POS loans.",
        "**8. Age Profile:** Younger applicants (<30 yrs) consistently exhibit higher risk than mature applicants.",
        "**9. Occupation Impact:** Laborers and low-skill service workers account for higher relative delinquencies.",
        "**10. Cash-Flow Anomalies:** Underpayment and payment delays highlight critical household cash-flow volatility."
    ]

    for i in range(0, 10, 2):
        l, r = st.columns(2)
        l.info(insights[i])
        r.info(insights[i+1])

    # Recommendations
    st.subheader("Business Recommendations")
    st.markdown("""
    * **Affordability:** Cap Credit-to-Income ratios at 4.0 to limit over-leveraging.
    * **Early Warning:** Auto-flag accounts accumulating 2+ consecutive late payments.
    * **Bureau Integration:** Adjust credit limits dynamically based on external bureau debt levels.
    * **Underwriting:** Apply stricter verification for tenures under 2 years.
    """)
