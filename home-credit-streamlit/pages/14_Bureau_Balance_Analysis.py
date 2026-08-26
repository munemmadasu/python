import streamlit as st
import pandas as pd
import plotly.express as px

def show_bureau_balance_page(df):
    st.title("Page 14 – Bureau Balance Analysis")

    if df is None or df.empty:
        st.warning("Bureau Balance dataset (`bureau_balance.csv`) is missing.")
        return

    delinq_codes = ['1', '2', '3', '4', '5']

    # --- KPIs ---
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Records", f"{len(df):,}")
    c2.metric("Unique Accounts", f"{df['SK_ID_BUREAU'].nunique():,}")
    c3.metric("Top Status", str(df['STATUS'].mode()[0]))
    c4.metric("Delinquencies", f"{df['STATUS'].isin(delinq_codes).sum():,}")
    c5.metric("Closed Records", f"{(df['STATUS'] == 'C').sum():,}")

    st.markdown("---")

    # --- Charts ---
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(px.bar(df['STATUS'].value_counts().reset_index(), x='STATUS', y='count', title="Status Distribution"), use_container_width=True)
        
        # Monthly Delinquency Trend
        delinq_trend = df[df['STATUS'].isin(delinq_codes)].groupby('MONTHS_BALANCE').size().reset_index(name='Count')
        st.plotly_chart(px.line(delinq_trend, x='MONTHS_BALANCE', y='Count', title="Monthly Delinquency Trend"), use_container_width=True)

    with col2:
        st.plotly_chart(px.pie(df, names='STATUS', title="Status Percentage", hole=0.4), use_container_width=True)
        
        # Status Heatmap
        heatmap_data = pd.crosstab(df['STATUS'], df['MONTHS_BALANCE'])
        st.plotly_chart(px.imshow(heatmap_data, title="Status Heatmap across Months", aspect="auto"), use_container_width=True)

    # --- Feature Engineering ---
    st.subheader("Customer-Level Features")
    num_map = {'C': 0, 'X': 0, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5}
    df['STATUS_NUM'] = df['STATUS'].map(num_map).fillna(0)

    agg_df = df.groupby('SK_ID_BUREAU').agg(
        months_with_delinquency=('STATUS', lambda x: x.isin(delinq_codes).sum()),
        max_delinquency_level=('STATUS_NUM', 'max'),
        num_closed_months=('STATUS', lambda x: (x == 'C').sum()),
        num_active_months=('STATUS', lambda x: (x == '0').sum())
    ).reset_index()

    st.dataframe(agg_df.head(10), use_container_width=True)