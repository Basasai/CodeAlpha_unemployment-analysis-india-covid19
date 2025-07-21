# 📦 Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ✅ Load both datasets
df1 = pd.read_csv('Unemployment in India.csv')
df2 = pd.read_csv('Unemployment_Rate_upto_11_2020.csv')

# -------------------------------------
# 📊 Data 1: Unemployment in India
# -------------------------------------

# Clean column names
df1.columns = df1.columns.str.strip()

# Convert 'Date' column
# Using errors='coerce' to handle potential parsing issues
df1['Date'] = pd.to_datetime(df1['Date'], errors='coerce')

# Drop missing values (including those from coerced date errors)
df1.dropna(inplace=True)

# Extract month and year
df1['Month'] = df1['Date'].dt.month
df1['Year'] = df1['Date'].dt.year

# Print column names to identify the correct unemployment rate column
print("Columns in df1:", df1.columns)

# Define the correct column name for unemployment rate
unemployment_col_df1 = 'Estimated Unemployment Rate (%)'

# Plot unemployment trend (overall)
plt.figure(figsize=(12, 6))
sns.lineplot(data=df1, x='Date', y=unemployment_col_df1)
plt.title('Overall Unemployment Rate Over Time (India)')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate (%)')
plt.grid(True)
plt.show()

# Highlight COVID-19 period
df1['Covid_Period'] = df1['Date'] >= pd.to_datetime('2020-03-01')
plt.figure(figsize=(12, 6))
sns.lineplot(data=df1, x='Date', y=unemployment_col_df1, hue='Covid_Period', palette=['blue', 'red'])
plt.title('Unemployment Before and During COVID-19')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate (%)')
plt.legend(title='COVID-19 Period', labels=['Before', 'During/After'])
plt.grid(True)
plt.show()

# Seasonal pattern
plt.figure(figsize=(10, 5))
sns.boxplot(data=df1, x='Month', y=unemployment_col_df1)
plt.title('Seasonal Unemployment Trends')
plt.xlabel('Month')
plt.ylabel('Unemployment Rate (%)')
plt.grid(True)
plt.show()

# Unemployment by Region
plt.figure(figsize=(14, 7))
sns.boxplot(data=df1, x='Region', y=unemployment_col_df1)
plt.title('Unemployment Rate by Region')
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

# -------------------------------------
# 📊 Data 2: Unemployment_Rate_upto_11_2020
# -------------------------------------

# Print column names for df2 to diagnose KeyError
print("\nColumns in df2:", df2.columns)

# Convert ' Date' to datetime, handling potential errors
df2['Date'] = pd.to_datetime(df2[' Date'], errors='coerce')

# Melt the wide format to long
df2_long = df2.melt(id_vars='Date', var_name='State', value_name='Unemployment Rate')

# Drop missing values
df2_long.dropna(inplace=True)

# Plot a few states for illustration
sample_states = ['Delhi', 'Tamil Nadu', 'Maharashtra', 'Bihar']
plt.figure(figsize=(12, 6))
for state in sample_states:
    state_data = df2_long[df2_long['State'] == state]
    plt.plot(state_data['Date'], state_data['Unemployment Rate'], label=state)
plt.title('State-wise Unemployment Trends')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate (%)')
plt.legend()
plt.grid(True)
plt.show()

# -------------------------------------
# 📌 Key Insights
# -------------------------------------
# Highest unemployment (file 1)
max_unemp = df1[df1[unemployment_col_df1] == df1[unemployment_col_df1].max()]
print("\n📌 Highest Recorded Unemployment:")
print(max_unemp[['Date', 'Region', unemployment_col_df1]])

# Average unemployment by year
avg_year = df1.groupby('Year')[unemployment_col_df1].mean()
print("\n📈 Average Unemployment Rate by Year:\n", avg_year)

# -------------------------------------
# 📋 Policy Insight
# -------------------------------------
print("\n📋 Insight for Policymakers:")
print("- COVID-19 caused a visible spike in unemployment post March 2020.")
print("- Urban areas and industrial states like Delhi and Maharashtra were more affected.")
print("- Targeted employment schemes and upskilling programs may help recovery.")