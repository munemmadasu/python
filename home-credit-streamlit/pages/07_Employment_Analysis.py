import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show_employment_page(df):
    st.title("Page 7 – Employment Analysis")
    if df is None or df.empty:
        st.warning("application_train.csv missing.")
        return

    # Preprocessing (Handle 365243 anomaly)
    df['EMP_YEARS'] = df['DAYS_EMPLOYED'].replace(365243, np.nan).abs() / 365.25
    
    # Categorization
    df['EMP_GROUP'] = pd.cut(df['EMP_YEARS'], bins=[-1, 1, 3, 5, 10, 20, np.inf], 
                             labels=['<1 Year', '1–3 Years', '3–5 Years', '5–10 Years', '10–20 Years', '20+ Years'])
    df['EMP_GROUP'] = df['EMP_GROUP'].astype(str).fillna('Unemployed / Special')
    df.loc[df['DAYS_EMPLOYED'] == 365243, 'EMP_GROUP'] = 'Unemployed / Special'

    # KPIs
    grp_def = df.groupby('EMP_GROUP')['TARGET'].mean().reset_index() if 'TARGET' in df.columns else pd.DataFrame()
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Avg Emp Yrs", f"{df['EMP_YEARS'].mean():.1f}")
    c2.metric("Med Emp Yrs", f"{df['EMP_YEARS'].median():.1f}")
    c3.metric("Top Occupation", str(df['OCCUPATION_TYPE'].mode()[0]) if 'OCCUPATION_TYPE' in df.columns else "N/A")
    c4.metric("Top Org", str(df['ORGANIZATION_TYPE'].mode()[0]) if 'ORGANIZATION_TYPE' in df.columns else "N/A")
    c5.metric("High Risk Group", grp_def.sort_values(by='TARGET', ascending=False).iloc[0]['EMP_GROUP'] if not grp_def.empty else "N/A")

    st.markdown("---")

    # Plots
    sample = df.sample(min(5000, len(df)))
    l, r = st.columns(2)
    with l:
        st.plotly_chart(px.histogram(df['EMP_YEARS'].dropna(), nbins=30, title="Employment Years"), use_container_width=True)
        st.plotly_chart(px.bar(df['EMP_GROUP'].value_counts().reset_index(), x='EMP_GROUP', y='count', title="Group Distribution"), use_container_width=True)
        if 'TARGET' in df.columns:
            st.plotly_chart(px.bar(grp_def, x='EMP_GROUP', y='TARGET', title="Default Rate by Group"), use_container_width=True)
        st.plotly_chart(px.scatter(sample, x='EMP_YEARS', y='AMT_INCOME_TOTAL', title="Emp Years vs Income", log_y=True), use_container_width=True)

    with r:
        if 'TARGET' in df.columns and 'OCCUPATION_TYPE' in df.columns:
            st.plotly_chart(px.bar(df.groupby('OCCUPATION_TYPE')['TARGET'].mean().reset_index(), x='TARGET', y='OCCUPATION_TYPE', orientation='h', title="Occupation vs Default"), use_container_width=True)
        if 'TARGET' in df.columns and 'ORGANIZATION_TYPE' in df.columns:
            st.plotly_chart(px.bar(df.groupby('ORGANIZATION_TYPE')['TARGET'].mean().reset_index().head(15), x='TARGET', y='ORGANIZATION_TYPE', orientation='h', title="Org Type vs Default"), use_container_width=True)
        st.plotly_chart(px.scatter(sample, x='EMP_YEARS', y='AMT_CREDIT', title="Emp Years vs Credit"), use_container_width=True)