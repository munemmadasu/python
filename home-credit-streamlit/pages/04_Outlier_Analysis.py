import pandas as pd
import numpy as np
import plotly.express as px

# 1. Load Data
df = pd.read_csv("data/application_train.csv")

# Key numerical columns to analyze
target_cols = ['AMT_INCOME_TOTAL', 'AMT_CREDIT', 'AMT_ANNUITY', 
               'AMT_GOODS_PRICE', 'DAYS_BIRTH', 'DAYS_EMPLOYED', 
               'CNT_CHILDREN', 'CNT_FAM_MEMBERS']

# 2. KPI Calculations
num_cols = len(df.select_dtypes(include=[np.number]).columns)

# Calculate variables with outliers using 1.5 * IQR rule
outlier_vars_count = 0
for col in target_cols:
    if col in df.columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        if ((df[col] < (q1 - 1.5 * iqr)) | (df[col] > (q3 + 1.5 * iqr))).sum() > 0:
            outlier_vars_count += 1

kpis = {
    "Number of Numerical Columns": num_cols,
    "Variables with Outliers (IQR Method)": outlier_vars_count,
    "Maximum Income": df['AMT_INCOME_TOTAL'].max(),
    "Maximum Credit": df['AMT_CREDIT'].max(),
    "Maximum Annuity": df['AMT_ANNUITY'].max()
}

print("=== OUTLIER & DISTRIBUTION KPIS ===")
for k, v in kpis.items():
    print(f"{k}: {v:,.2f}" if isinstance(v, float) else f"{k}: {v:,}")

# 3. Generating Recommended Visualizations
# Income Distribution (Histogram up to 99th percentile)
p99_income = df['AMT_INCOME_TOTAL'].quantile(0.99)
fig_inc_hist = px.histogram(df[df['AMT_INCOME_TOTAL'] <= p99_income], x='AMT_INCOME_TOTAL', 
                            nbins=50, title='Income Distribution (Filtered to 99th Percentile)')
fig_inc_hist.show()

# Income Outliers (Box Plot)
fig_inc_box = px.box(df, y='AMT_INCOME_TOTAL', title='Income Outliers Box Plot')
fig_inc_box.show()

# Credit Outliers (Box Plot)
fig_cred_box = px.box(df, y='AMT_CREDIT', title='Credit Outliers Box Plot')
fig_cred_box.show()

# Annuity Outliers (Box Plot)
fig_ann_box = px.box(df, y='AMT_ANNUITY', title='Annuity Outliers Box Plot')
fig_ann_box.show()

# Income vs Credit (Scatter Plot sampled for visual clarity)
sample_df = df.sample(min(2000, len(df)), random_state=42)
fig_scatter = px.scatter(sample_df, x='AMT_INCOME_TOTAL', y='AMT_CREDIT', 
                         color='TARGET', title='Income vs Credit Scatter Plot')
fig_scatter.show()

# 4. Outlier Evaluation & Preprocessing Strategy
print("\n=== OUTLIER ANALYSIS & TECHNIQUES ===")
print("* Data Entry Issue / Invalid Value: DAYS_EMPLOYED contains 365,243 (~1,000 years), which is an anomalous placeholder and must be converted to NaN.")
print("* True Extreme Customers: Unusually high income or credit amounts represent legitimate high-net-worth borrowers rather than errors.")
print("* Outlier Handling Techniques:")
print("  1. Percentile Capping / Winsorization: Cap extreme values at the 1st and 99th percentiles to preserve sample size while muting extreme skewness.")
print("  2. Log Transformation: Apply np.log1p() to skewed monetary fields (e.g., AMT_INCOME_TOTAL) to normalize distributions for analysis.")
print("  3. Business-Rule Validation: Retain legitimate extreme profiles rather than automatically dropping rows.")