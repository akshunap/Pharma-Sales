# Pharma Sales Performance Project - Using Real CSV Data

# Step 1: Import Libraries
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Load Dataset from CSV
sales_data = pd.read_csv("pharma_sales.csv")
sales_data.columns = sales_data.columns.str.strip().str.lower()  # Normalize column names
print("Columns in CSV:", sales_data.columns.tolist())

# Step 3: Create SQLite DB and Upload Data
conn = sqlite3.connect('pharma_sales.db')
sales_data.to_sql('pharma_sales', conn, if_exists='replace', index=False)

# Step 4: SQL Queries for Analysis
print("\n--- Total Usage of Each Drug Category ---")
drug_columns = ['m01ab', 'm01ae', 'n02ba', 'n02be', 'n05b', 'n05c', 'r03', 'r06']
drug_usage = sales_data[drug_columns].sum().reset_index()
drug_usage.columns = ['drug_category', 'total_usage']
print(drug_usage)

# Step 5: Monthly Total Drug Usage
print("\n--- Monthly Total Drug Usage ---")
query = """
SELECT month, 
       SUM(m01ab + m01ae + n02ba + n02be + n05b + n05c + r03 + r06) AS total_usage
FROM pharma_sales
GROUP BY month
ORDER BY month;
"""
monthly_usage = pd.read_sql(query, conn)
print(monthly_usage)

# Step 6: Visualization - Total Usage by Drug Category
plt.figure(figsize=(10,6))
sns.barplot(data=drug_usage, x='drug_category', y='total_usage')
plt.title('Total Usage by Drug Category')
plt.xlabel('Drug Category')
plt.ylabel('Total Usage')
plt.tight_layout()
plt.show()

# Step 7: Monthly Trend of Total Drug Usage
plt.figure(figsize=(10,6))
sns.lineplot(data=monthly_usage, x='month', y='total_usage', marker='o')
plt.title('Monthly Total Drug Usage')
plt.xlabel('Month')
plt.ylabel('Total Usage')
plt.tight_layout()
plt.show()

# Close the connection
conn.close()

