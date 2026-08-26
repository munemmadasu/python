import streamlit as st
import pandas as pd
import plotly.express as px

def show_previous_application_page(df):
    st.title("Page 15 – Previous Application Analysis")

    if df is None or df.empty:
        st.warning("Previous applications dataset missing.")
        return

    # --- KPIs ---
    tot = len(df)
    appr = (df['NAME_CONTRACT_STATUS'] == 'Approved').sum()
    ref = (df['NAME_CONTRACT_STATUS'] == 'Refused').sum()
    canc = (df['NAME_CONTRACT_STATUS'] == 'Canceled').sum()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Apps", f"{tot:,}")
    c2.metric("Approved", f"{appr:,}")
    c3.metric("Refused", f"{ref:,}")
    c4.metric("Cancelled", f"{canc:,}")
    c5.metric("Approval %", f"{(appr/tot*100):.1f}%" if tot else "0%")
    c6.metric("Rejection %", f"{(ref/tot*100):.1f}%" if tot else "0%")

    st.markdown("---")

    # --- Charts ---
    c_left, c_right = st.columns(2)
    with c_left:
        st.plotly_chart(px.bar(df['NAME_CONTRACT_STATUS'].value_counts().reset_index(), x='NAME_CONTRACT_STATUS', y='count', title="Application Status"), use_container_width=True)
        
        sample_df = df.sample(min(5000, len(df)))
        st.plotly_chart(px.scatter(sample_df, x='AMT_APPLICATION', y='AMT_CREDIT', color='NAME_CONTRACT_STATUS', title="App vs Credit Amount"), use_container_width=True)
        
        st.plotly_chart(px.bar(df['NAME_CLIENT_TYPE'].value_counts().reset_index(), x='NAME_CLIENT_TYPE', y='count', title="Client Types"), use_container_width=True)

    with c_right:
        st.plotly_chart(px.pie(df, names='NAME_CONTRACT_STATUS', title="Approval Percentage", hole=0.4), use_container_width=True)
        st.plotly_chart(px.bar(df['NAME_CONTRACT_TYPE'].value_counts().reset_index(), x='NAME_CONTRACT_TYPE', y='count', title="Contract Types"), use_container_width=True)
        st.plotly_chart(px.bar(df['NAME_PRODUCT_TYPE'].value_counts().reset_index(), x='count', y='NAME_PRODUCT_TYPE', orientation='h', title="Product Types"), use_container_width=True)

    # Rejection Reasons
    if 'CODE_REJECT_REASON' in df.columns:
        rejects = df[df['CODE_REJECT_REASON'] != 'XAP']['CODE_REJECT_REASON'].value_counts().reset_index()
        st.plotly_chart(px.bar(rejects, x='count', y='CODE_REJECT_REASON', orientation='h', title="Rejection Reasons"), use_container_width=True)

    # --- Customer Features ---
    st.subheader("Customer Aggregates")
    agg_df = df.groupby('SK_ID_CURR').agg(
        num_apps=('SK_ID_PREV', 'count'),
        num_approved=('NAME_CONTRACT_STATUS', lambda x: (x == 'Approved').sum()),
        num_refused=('NAME_CONTRACT_STATUS', lambda x: (x == 'Refused').sum()),
        approval_rate=('NAME_CONTRACT_STATUS', lambda x: (x == 'Approved').sum() / len(x)),
        avg_credit=('AMT_CREDIT', 'mean'),
        max_credit=('AMT_CREDIT', 'max')
    ).reset_index()

    st.dataframe(agg_df.head(10), use_container_width=True)