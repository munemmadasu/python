import pandas as pd
import plotly.express as px

# 1. Load Data
df = pd.read_csv("data/application_train.csv")

# 2. KPI Calculations
kpis = {
    "Total Customers": df['SK_ID_CURR'].nunique(),
    "Total Applications": len(df),
    "Default Customers": (df['TARGET'] == 1).sum(),
    "Non-Default Customers": (df['TARGET'] == 0).sum(),
    "Default Rate (%)": round((df['TARGET'] == 1).mean() * 100, 2),
    "Total Credit Exposure": df['AMT_CREDIT'].sum(),
    "Average Credit": df['AMT_CREDIT'].mean(),
    "Average Income": df['AMT_INCOME_TOTAL'].mean(),
    "Average Annuity": df['AMT_ANNUITY'].mean(),
    "Average Goods Price": df['AMT_GOODS_PRICE'].mean(),
    "Median Income": df['AMT_INCOME_TOTAL'].median(),
    "Median Credit": df['AMT_CREDIT'].median()
}

print("=== EXECUTIVE PORTFOLIO KPIS ===")
for metric, value in kpis.items():
    print(f"{metric}: {value:,.2f}" if isinstance(value, float) else f"{metric}: {value:,}")

# 3. Generating Core Visualizations
# Default vs Non-Default Count
fig_bar = px.bar(df['TARGET'].value_counts().reset_index(), x='TARGET', y='count', title='Default vs Non-Default Count')
fig_bar.show()

# Default Percentage (Donut Chart)
fig_donut = px.pie(df, names='TARGET', hole=0.4, title='Default Percentage')
fig_donut.show()

# Credit Amount Distribution
fig_hist_credit = px.histogram(df, x='AMT_CREDIT', nbins=50, title='Credit Amount Distribution')
fig_hist_credit.show()

# Income Distribution (Filtered to 99th percentile for display clarity)
fig_hist_income = px.histogram(df[df['AMT_INCOME_TOTAL'] <= df['AMT_INCOME_TOTAL'].quantile(0.99)], 
                               x='AMT_INCOME_TOTAL', nbins=50, title='Income Distribution')
fig_hist_income.show()

# Credit by Income Type (Treemap)
income_credit = df.groupby('NAME_INCOME_TYPE')['AMT_CREDIT'].sum().reset_index()
fig_treemap = px.treemap(income_credit, path=['NAME_INCOME_TYPE'], values='AMT_CREDIT', title='Credit by Income Type')
fig_treemap.show()

# Default Rate by Income Type
def_by_income = df.groupby('NAME_INCOME_TYPE')['TARGET'].mean().reset_index()
def_by_income['Default Rate (%)'] = def_by_income['TARGET'] * 100
fig_def_rate = px.bar(def_by_income.sort_values('Default Rate (%)'), y='NAME_INCOME_TYPE', x='Default Rate (%)', orientation='h', title='Default Rate by Income Type')
fig_def_rate.show()

# Income vs Credit (Scatter Plot - Subsampled for performance)
fig_scatter = px.scatter(df.sample(min(2000, len(df))), x='AMT_INCOME_TOTAL', y='AMT_CREDIT', color='TARGET', title='Income vs Credit')
fig_scatter.show()
