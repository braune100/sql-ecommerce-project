-- ==============================
-- E-COMMERCE SQL ANALYSIS PROJECT
-- ==============================

-- TOTAL REVENUE
SELECT SUM(Quantity * UnitPrice) AS total_revenue
FROM ecommerce;

-- TOP COUNTRIES BY REVENUE
SELECT Country,
       SUM(Quantity * UnitPrice) AS revenue
FROM ecommerce
GROUP BY Country
ORDER BY revenue DESC;

-- TOP CUSTOMERS
SELECT CustomerID,
       SUM(Quantity * UnitPrice) AS total_spent
FROM ecommerce
WHERE CustomerID IS NOT NULL
GROUP BY CustomerID
ORDER BY total_spent DESC
LIMIT 10;

-- MONTHLY REVENUE
SELECT strftime('%Y-%m', InvoiceDate) AS month,
       SUM(Quantity * UnitPrice) AS revenue
FROM ecommerce
GROUP BY month
ORDER BY month;

-- CUSTOMER RANKING (WINDOW FUNCTION)
SELECT CustomerID,
       SUM(Quantity * UnitPrice) AS total_spent,
       RANK() OVER (ORDER BY SUM(Quantity * UnitPrice) DESC) AS rank
FROM ecommerce
WHERE CustomerID IS NOT NULL
GROUP BY CustomerID;