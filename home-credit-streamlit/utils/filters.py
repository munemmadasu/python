import streamlit as st
def sidebar_filters(df):
    st.sidebar.header("Filters")
    target = st.sidebar.multiselect(
        "Target",
        df["TARGET"].unique(),
        default=df["TARGET"].unique()
    )
    gender = st.sidebar.multiselect(
        "Gender",
        df["CODE_GENDER"].dropna().unique(),
        default=df["CODE_GENDER"].dropna().unique()
    )
    education = st.sidebar.multiselect(
        "Education",
        df["NAME_EDUCATION_TYPE"].dropna().unique(),
        default=df["NAME_EDUCATION_TYPE"].dropna().unique()
    )
    contract = st.sidebar.multiselect(
        "Contract Type",
        df["NAME_CONTRACT_TYPE"].dropna().unique(),
        default=df["NAME_CONTRACT_TYPE"].dropna().unique()
    )
    filtered_df = df[
        (df["TARGET"].isin(target))
        &
        (df["CODE_GENDER"].isin(gender))
        &
        (df["NAME_EDUCATION_TYPE"].isin(education))
        &
        (df["NAME_CONTRACT_TYPE"].isin(contract))
    ]

    return filtered_df

#from utils.filters import sidebar_filters