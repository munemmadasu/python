import pandas as pd
import numpy as np
import plotly.express as px

# 1. Load Data
df = pd.read_csv("data/application_train.csv")
num_rows, num_cols = df.shape

# 2. KPI Calculations
missing_series = df.isnull().sum()
total_missing = missing_series.sum()
missing_pct = round((total_missing / (num_rows * num_cols)) * 100, 2)
cols_missing = (missing_series > 0).sum()
cols_above_30 = ((missing_series / num_rows) > 0.30).sum()
cols_above_50 = ((missing_series / num_rows) > 0.50).sum()

print("=== MISSING VALUE ANALYSIS KPIS ===")
print(f"Total Missing Values: {total_missing:,}")
print(f"Missing Percentage: {missing_pct}%")
print(f"Columns with Missing Data: {cols_missing}")
print(f"Columns > 30% Missing: {cols_above_30}")
print(f"Columns > 50% Missing: {cols_above_50}")

# 3. DataFrame for Column Missing Info & Categorization
missing_df = pd.DataFrame({
    'Column': df.columns,
    'Data_Type': df.dtypes.astype(str),
    'Missing_Count': missing_series.values,
    'Missing_Pct': (missing_series.values / num_rows) * 100
})

bins = [-0.1, 5, 20, 40, 60, 100]
labels = ['0–5% Missing', '5–20% Missing', '20–40% Missing', '40–60% Missing', '60%+ Missing']
missing_df['Missing_Group'] = pd.cut(missing_df['Missing_Pct'], bins=bins, labels=labels)

print("\n=== COLUMNS BY MISSING CATEGORY ===")
print(missing_df['Missing_Group'].value_counts().sort_index())

# 4. Recommended Graphs

# Top 20 Columns by Missing Percentage (Horizontal Bar Chart)
top20 = missing_df.sort_values(by='Missing_Pct', ascending=False).head(20)
fig_top20 = px.bar(top20, x='Missing_Pct', y='Column', orientation='h', 
                   title='Top 20 Columns by Missing Percentage', text_auto='.1f')
fig_top20.update_layout(yaxis={'categoryorder': 'total ascending'})
fig_top20.show()

# Missing Percentage Distribution (Histogram)
fig_hist = px.histogram(missing_df[missing_df['Missing_Count'] > 0], x='Missing_Pct', 
                       nbins=20, title='Missing Percentage Distribution')
fig_hist.show()

# Missingness Heatmap (Top 30 missing columns sampled for performance)
sample_df = df[missing_df.sort_values('Missing_Pct', ascending=False).head(30)['Column']].sample(min(1000, num_rows), random_state=42)
fig_heatmap = px.imshow(sample_df.isnull().T.astype(int), 
                        title="Missingness Heatmap (Top 30 Columns)",
                        color_continuous_scale=['#1f77b4', '#d62728'])
fig_heatmap.show()

# Missing Values by Data Type (Bar Chart)
missing_by_dtype = missing_df.groupby('Data_Type')['Missing_Count'].sum().reset_index()
fig_dtype = px.bar(missing_by_dtype, x='Data_Type', y='Missing_Count', 
                   title='Missing Values by Data Type', text_auto=True)
fig_dtype.show()

# 5. Preprocessing Strategy Explanations
print("\n=== PREPROCESSING STRATEGY & EXPLANATIONS ===")
print("1. Drop Columns (>50% Missing): Drop normalized building parameters (e.g., COMMONAREA_AVG, OWN_CAR_AGE) due to heavy noise and insufficient signal.")
print("2. Fill using Median (<20% Missing Numeric): Impute skewed continuous variables like AMT_ANNUITY and EXT_SOURCE_2/3 using the median.")
print("3. Fill using Mode (<5% Missing Categorical): Impute low-missingness categorical fields like NAME_TYPE_SUITE using the mode.")
print("4. Create Missing Indicator: Add binary flags (e.g., EXT_SOURCE_1_IS_MISSING) prior to imputation, as missing external scores carry predictive signal.")