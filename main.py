
# Pharma Sales Performance Project - Python + SQL

# Step 1: Import Libraries
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Step 2: Load Datasets (Simulated CSVs)
sales_data = pd.DataFrame({
    'region': ['East', 'West', 'East', 'South', 'North', 'West', 'South'],
    'sales_rep_id': [101, 102, 101, 103, 104, 102, 103],
    'product': ['A', 'B', 'C', 'A', 'C', 'B', 'A'],
    'sales_amount': [2000, 1500, 3000, 2500, 1000, 1800, 2700],
    'date': pd.to_datetime(['2024-01-10', '2024-01-12', '2024-02-05', '2024-02-10', '2024-03-15', '2024-03-18', '2024-04-01'])
})

rep_info = pd.DataFrame({
    'sales_rep_id': [101, 102, 103, 104],
    'rep_name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'region': ['East', 'West', 'South', 'North'],
    'target': [7000, 6000, 8000, 5000]
})

product_master = pd.DataFrame({
    'product': ['A', 'B', 'C'],
    'product_name': ['PainRelief', 'Antibiotic', 'Supplement'],
    'category': ['OTC', 'Rx', 'OTC']
})

# Step 3: Create SQLite DB and Upload Data
conn = sqlite3.connect('pharma_sales.db')
sales_data.to_sql('sales_data', conn, if_exists='replace', index=False)
rep_info.to_sql('rep_info', conn, if_exists='replace', index=False)
product_master.to_sql('product_master', conn, if_exists='replace', index=False)

# Step 4: SQL Queries for Analysis
print("\n--- Total Sales by Region ---")
query1 = """
SELECT region, SUM(sales_amount) AS total_sales
FROM sales_data
GROUP BY region;
"""
print(pd.read_sql(query1, conn))

print("\n--- Top Performing Reps ---")
query2 = """
SELECT r.rep_name, SUM(s.sales_amount) AS total_sales
FROM sales_data s
JOIN rep_info r ON s.sales_rep_id = r.sales_rep_id
GROUP BY r.rep_name
ORDER BY total_sales DESC
LIMIT 5;
"""
print(pd.read_sql(query2, conn))

print("\n--- Monthly Sales by Category ---")
query3 = """
SELECT strftime('%Y-%m', s.date) AS month, p.category, SUM(s.sales_amount) AS total
FROM sales_data s
JOIN product_master p ON s.product = p.product
GROUP BY month, p.category
ORDER BY month;
"""
monthly_sales = pd.read_sql(query3, conn)
print(monthly_sales)

# Step 5: Visualization
plt.figure(figsize=(10,6))
sns.barplot(data=monthly_sales, x='month', y='total', hue='category')
plt.title('Monthly Sales by Product Category')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.tight_layout()
plt.show()

# Step 6: Performance Comparison
query4 = """
SELECT r.rep_name, SUM(s.sales_amount) AS achieved, r.target
FROM sales_data s
JOIN rep_info r ON s.sales_rep_id = r.sales_rep_id
GROUP BY r.rep_name;
"""
performance = pd.read_sql(query4, conn)
performance['% Achievement'] = round((performance['achieved'] / performance['target']) * 100, 2)
print("\n--- Performance vs Target ---")
print(performance)

# Close the connection
conn.close()
