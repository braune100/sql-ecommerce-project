📊 E-commerce SQL Analysis Project
🧾 Overview

This project analyzes an e-commerce dataset using SQLite and SQL queries to uncover business insights such as revenue trends, customer behavior, and product performance.

The goal is to demonstrate practical data analysis skills using SQL, data aggregation, and business-oriented thinking.

📁 Dataset

The dataset used is the Online Retail dataset, containing transaction-level data.

Key columns:
InvoiceNo
StockCode
Description
Quantity
InvoiceDate
UnitPrice
CustomerID
Country
Revenue
Date
Month
🗄️ Project Structure

sql-ecommerce-project/
│
├── ecommerce.db              # SQLite database
├── online_retail_small.csv   # Raw dataset
├── queries.sql               # SQL analysis queries
└── README.md                 # Project documentation

🔍 Key Analyses Performed
📈 Sales Performance
Total revenue calculation
Monthly revenue trends
Top-performing months
🌍 Geographic Insights
Revenue by country
Order distribution across regions
🛍️ Product Analysis
Best-selling products
Products with highest revenue contribution
👤 Customer Analysis
Top customers by spend
Repeat purchase behavior
🧠 Key SQL Techniques Used
GROUP BY aggregations
SUM(), COUNT(), AVG()
Date-based filtering
Sorting with ORDER BY
Basic business KPIs creation
🚀 How to Run This Project
1. Open SQLite
sqlite3 ecommerce.db
2. Run queries
.read queries.sql

OR copy/paste queries manually.

📊 Example Insights
Revenue is highly concentrated in a few high-value customers
Certain months show strong seasonal spikes
A small number of products drive most revenue
🧩 Skills Demonstrated
SQL data analysis
Business intelligence thinking
Data cleaning and transformation
KPI development
Git & GitHub project workflow
📌 Future Improvements
Add Power BI or Tableau dashboard
Create Python visualization layer
Perform customer segmentation (RFM analysis)
Add machine learning for demand prediction
👨‍💻 Author

Bruno Silveira
Aspiring Data Analyst | SQL • Python • Analytics
