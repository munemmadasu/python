def calculate_kpis(df):
    total_applications=len(df)
    default_customers=(
        df["TARGET"]==1
    ).sum()

    non_default_customers=(
        df["TARGET"]==0
    ).sum()

    default_rate=(default_customers/total_applications*100)

    avg_income=(df["AMT_INCOME_TOTAL"].mean())

    avg_credit=(df["AMT_CREDIT"].mean())

    avg_annuity=(df["AMT_ANNUITY"].mean())

    return{
        "total_applications":total_applications,
        "default_customers":default_customers,
        "non_default_customers":non_default_customers,
        "default_rate":default_rate,
        "avg_income":avg_income,
        "avg_credit":avg_credit,
        "avg_annuity":avg_annuity
        }