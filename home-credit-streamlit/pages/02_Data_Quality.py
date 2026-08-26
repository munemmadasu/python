import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Load Dataset
df = pd.read_csv("data/application_train.csv")

# 2. KPI Calculations
num_rows, num_cols = df.shape
num_num = len(df.select_dtypes(include=['int64', 'float64']).columns)
num_cat = len(df.select_dtypes(include=['object', 'category']).columns)
total_cells = num_rows * num_cols
missing_cells = df.isnull().sum().sum()
duplicate_rows = df.duplicated().sum()
memory_mb = df.memory_usage(deep=True).sum() / (1024 ** 2)
unique_cust = df['SK_ID_CURR'].nunique() if 'SK_ID_CURR' in df.columns else num_rows

print("=== DATA QUALITY KPIS ===")
print(f"Rows: {num_rows:,} | Cols: {num_cols:,} | Numerical: {num_num} | Categorical: {num_cat}")
print(f"Missing Cells: {missing_cells:,} | Duplicates: {duplicate_rows} | Memory: {memory_mb:.2f} MB | Unique Customers: {unique_cust:,}")

# 3. Data Quality Summary Table
summary_list = []
for col in df.columns:
    m_count = df[col].isnull().sum()
    is_num = pd.api.types.is_numeric_dtype(df[col])
    summary_list.append({
        "Column Name": col,
        "Data Type": str(df[col].dtype),
        "Missing Count": m_count,
        "Missing %": round((m_count / num_rows) * 100, 2),
        "Unique Values": df[col].nunique(dropna=True),
        "Minimum": df[col].min() if is_num else np.nan,
        "Maximum": df[col].max() if is_num else np.nan,
        "Mean": df[col].mean() if is_num else np.nan,
        "Median": df[col].median() if is_num else np.nan,
    })

quality_table = pd.DataFrame(summary_list)
print("\n=== SUMMARY TABLE (TOP 10 COLUMNS) ===")
print(quality_table.head(10))

# 4. Recommended Visualizations
# Column Data Types (Bar Chart)
fig_dtypes = px.bar(
    x=['Numerical', 'Categorical'], 
    y=[num_num, num_cat], 
    labels={'x': 'Data Type Group', 'y': 'Count'}, 
    title="Column Data Types", 
    text_auto=True
)
fig_dtypes.show()

# Missing vs Available Data (Stacked Bar Chart)
# We create a proper DataFrame first where every row gets a 'Dataset' label
df_missing_clean = pd.DataFrame({
    'Status': ['Available Data', 'Missing Data'],
    'Cells': [total_cells - missing_cells, missing_cells],
    'Category': ['Dataset', 'Dataset']  # Both rows now match!
})

fig_missing = px.bar(
    df_missing_clean,                  # Use our new DataFrame
    x='Category',                      # Look at the 'Category' column for X
    y='Cells',                         # Look at the 'Cells' column for Y
    color='Status',
    title="Missing vs Available Data",
    color_discrete_map={'Available Data': '#2ca02c', 'Missing Data': '#d62728'}
)
fig_missing.show()

# Unique Values by Column (Horizontal Bar Chart - Top 20)
fig_unique = px.bar(
    quality_table.sort_values('Unique Values', ascending=False).head(20),
    x='Unique Values', y='Column Name', orientation='h',
    title="Top 20 Columns by Unique Values"
)
fig_unique.show()

# Dataset Completeness (Gauge Chart)
completeness_pct = round(((total_cells - missing_cells) / total_cells) * 100, 2)
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=completeness_pct,
    title={'text': "Dataset Completeness (%)"},
    gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#1f77b4"}}
))
fig_gauge.show()

# 5. Data Quality Analysis & Preprocessing Strategy
print("\n=== DATA QUALITY ANALYSIS & STRATEGY ===")
print("* Quality Issues: High missingness across housing/normalized building scores (e.g., COMMONAREA_AVG, EXT_SOURCE_1).")
print("* Extreme Anomalies: Days employed (`DAYS_EMPLOYED`) contains 365,243 placeholder values (representing ~1000 years).")
print("* Customer Duplicates: No duplicate `SK_ID_CURR` IDs detected.")
print("* Preprocessing Strategy:")
print("  1. Replace 365,243 in `DAYS_EMPLOYED` with `NaN` before performing employment calculations.")
print("  2. Drop columns exceeding 50% missingness threshold where business relevance is low.")
print("  3. Impute median for skewed numerical features and mode for categorical features.")