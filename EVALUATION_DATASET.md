# Text-to-SQL Evaluation Dataset
## 20 Questions for AI Model Evaluation (Easy to Hard)

---

## EASY LEVEL (Questions 1-5)

### Question 1
**Difficulty:** Easy  
**Category:** Simple Selection

**NLP Query:**  
"How many stores do we have?"

**SQL Query:**
```sql
SELECT COUNT(*) as total_stores
FROM stores;
```

**Expected Answer:** 3

---

### Question 2
**Difficulty:** Easy  
**Category:** Simple Selection

**NLP Query:**  
"List all brand names in our catalog."

**SQL Query:**
```sql
SELECT brand_name
FROM brands
ORDER BY brand_name;
```

**Expected Answer:**  
| brand_name |
|---|
| Electra |
| Haro |
| Heller |
| Kona |
| Pure Cycles |
| Ritchey |
| Strider |
| Sun Bicycles |
| Trek |
| Windsor |
| Huffy |

---

### Question 3
**Difficulty:** Easy  
**Category:** Simple Selection with WHERE

**NLP Query:**  
"What is the email address of the Santa Cruz Bikes store?"

**SQL Query:**
```sql
SELECT email
FROM stores
WHERE store_name = 'Santa Cruz Bikes';
```

**Expected Answer:** santacruz@bikes.shop

---

### Question 4
**Difficulty:** Easy  
**Category:** Aggregation

**NLP Query:**  
"How many customers do we have in total?"

**SQL Query:**
```sql
SELECT COUNT(*) as total_customers
FROM customers;
```

**Expected Answer:** 1446

---

### Question 5
**Difficulty:** Easy  
**Category:** Simple Selection with LIMIT

**NLP Query:**  
"Show me the first 3 products in our catalog."

**SQL Query:**
```sql
SELECT product_id, product_name, list_price
FROM products
ORDER BY product_id
LIMIT 3;
```

**Expected Answer:**  
| product_id | product_name | list_price |
|---|---|---|
| 1 | Trek 820 - 2016 | 379.99 |
| 2 | Ritchey Timberwolf Frameset - 2016 | 749.99 |
| 3 | Surly Wednesday Frameset - 2016 | 999.99 |

---

## MEDIUM LEVEL (Questions 6-13)

### Question 6
**Difficulty:** Medium  
**Category:** JOIN with WHERE

**NLP Query:**  
"Get all products from the Trek brand with their prices."

**SQL Query:**
```sql
SELECT p.product_id, p.product_name, p.list_price
FROM products p
JOIN brands b ON p.brand_id = b.brand_id
WHERE b.brand_name = 'Trek'
ORDER BY p.product_name;
```

**Expected Answer:**  
| product_id | product_name | list_price |
|---|---|---|
| 1 | Trek 820 - 2016 | 379.99 |
| 4 | Trek Fuel EX 8 29 - 2016 | 2899.99 |
| 5 | Trek Slash 8 27.5 - 2016 | 1799.99 |
| (and more Trek products) |

---

### Question 7
**Difficulty:** Medium  
**Category:** JOIN and Aggregation

**NLP Query:**  
"How many orders were placed by each customer? Show customer name and order count."

**SQL Query:**
```sql
SELECT c.customer_id, c.first_name, c.last_name, COUNT(o.order_id) as order_count
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY order_count DESC
LIMIT 5;
```

**Expected Answer:**  
| customer_id | first_name | last_name | order_count |
|---|---|---|---|
| 118 | Lavina | Frazier | 13 |
| 150 | Nita | Schorr | 12 |
| 195 | Traci | Hauch | 11 |
| (top 5 customers by order count) |

---

### Question 8
**Difficulty:** Medium  
**Category:** JOIN with Aggregation and HAVING

**NLP Query:**  
"Which categories have more than 20 products?"

**SQL Query:**
```sql
SELECT c.category_id, c.category_name, COUNT(p.product_id) as product_count
FROM categories c
JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name
HAVING COUNT(p.product_id) > 20
ORDER BY product_count DESC;
```

**Expected Answer:**  
| category_id | category_name | product_count |
|---|---|---|
| 6 | Mountain Bikes | 43 |
| 7 | Road Bikes | 40 |
| (and possibly others) |

---

### Question 9
**Difficulty:** Medium  
**Category:** JOIN with Multiple Conditions

**NLP Query:**  
"List customers from New York state and their total spending."

**SQL Query:**
```sql
SELECT c.customer_id, c.first_name, c.last_name, c.state,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE c.state = 'NY'
GROUP BY c.customer_id, c.first_name, c.last_name, c.state
ORDER BY total_spent DESC
LIMIT 5;
```

**Expected Answer:**  
| customer_id | first_name | last_name | state | total_spent |
|---|---|---|---|---|
| (Top NY customers by spending) |

---

### Question 10
**Difficulty:** Medium  
**Category:** Multiple JOINs

**NLP Query:**  
"Show me all orders placed at the Baldwin Bikes store with customer names and order dates."

**SQL Query:**
```sql
SELECT o.order_id, c.first_name, c.last_name, o.order_date, s.store_name
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN stores s ON o.store_id = s.store_id
WHERE s.store_name = 'Baldwin Bikes'
ORDER BY o.order_date DESC
LIMIT 10;
```

**Expected Answer:**  
| order_id | first_name | last_name | order_date | store_name |
|---|---|---|---|---|
| (Orders from Baldwin Bikes store with customer info) |

---

### Question 11
**Difficulty:** Medium  
**Category:** Calculation with JOIN

**NLP Query:**  
"What is the total revenue from each product (quantity * list_price minus discount)?"

**SQL Query:**
```sql
SELECT p.product_id, p.product_name, 
       SUM(oi.quantity) as total_quantity_sold,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_revenue DESC
LIMIT 10;
```

**Expected Answer:**  
| product_id | product_name | total_quantity_sold | total_revenue |
|---|---|---|---|---|
| (Top 10 products by revenue) |

---

### Question 12
**Difficulty:** Medium  
**Category:** String Filtering

**NLP Query:**  
"Show all products that contain 'Trek' in their name."

**SQL Query:**
```sql
SELECT product_id, product_name, list_price
FROM products
WHERE product_name LIKE '%Trek%'
ORDER BY product_name;
```

**Expected Answer:**  
| product_id | product_name | list_price |
|---|---|---|---|
| (All Trek products) |

---

### Question 13
**Difficulty:** Medium  
**Category:** Date Filtering

**NLP Query:**  
"How many orders were placed in January 2016?"

**SQL Query:**
```sql
SELECT COUNT(*) as orders_in_january
FROM orders
WHERE YEAR(order_date) = 2016 AND MONTH(order_date) = 1;
```

**Expected Answer:** (Numeric count of January 2016 orders)

---

## HARD LEVEL (Questions 14-20)

### Question 14
**Difficulty:** Hard  
**Category:** Subquery with Aggregation

**NLP Query:**  
"Find customers who have spent more than the average order value."

**SQL Query:**
```sql
SELECT c.customer_id, c.first_name, c.last_name,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as customer_total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING SUM(oi.quantity * oi.list_price * (1 - oi.discount)) > 
       (SELECT AVG(order_value) FROM (
           SELECT SUM(quantity * list_price * (1 - discount)) as order_value
           FROM order_items
           GROUP BY order_id
       ) AS order_values)
ORDER BY customer_total_spent DESC
LIMIT 5;
```

**Expected Answer:**  
| customer_id | first_name | last_name | customer_total_spent |
|---|---|---|---|
| (Top customers above average spending) |

---

### Question 15
**Difficulty:** Hard  
**Category:** Complex JOIN with Window Functions

**NLP Query:**  
"Show the top-selling product in each category with its total revenue."

**SQL Query:**
```sql
SELECT c.category_name, p.product_id, p.product_name,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as category_product_revenue
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY c.category_name, p.product_id, p.product_name
ORDER BY c.category_name, category_product_revenue DESC;
```

**Expected Answer:**  
| category_name | product_id | product_name | category_product_revenue |
|---|---|---|---|
| (Top product per category) |

---

### Question 16
**Difficulty:** Hard  
**Category:** Multiple Aggregations with JOIN

**NLP Query:**  
"For each staff member, show their store, total orders handled, and total revenue from those orders."

**SQL Query:**
```sql
SELECT st.staff_id, st.first_name, st.last_name, s.store_name,
       COUNT(DISTINCT o.order_id) as total_orders,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as total_revenue
FROM staffs st
JOIN stores s ON st.store_id = s.store_id
LEFT JOIN orders o ON st.staff_id = o.staff_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY st.staff_id, st.first_name, st.last_name, s.store_name
ORDER BY total_revenue DESC;
```

**Expected Answer:**  
| staff_id | first_name | last_name | store_name | total_orders | total_revenue |
|---|---|---|---|---|---|
| (Each staff member's performance metrics) |

---

### Question 17
**Difficulty:** Hard  
**Category:** Complex Subquery

**NLP Query:**  
"Find products that have never been ordered."

**SQL Query:**
```sql
SELECT p.product_id, p.product_name, p.list_price
FROM products p
WHERE p.product_id NOT IN (
    SELECT DISTINCT oi.product_id
    FROM order_items oi
)
ORDER BY p.product_name;
```

**Expected Answer:**  
| product_id | product_name | list_price |
|---|---|---|
| (Products never ordered) |

---

### Question 18
**Difficulty:** Hard  
**Category:** Complex JOIN with CASE Statement

**NLP Query:**  
"Show inventory status for each product in each store (stock level, status as Low/Medium/High based on quantity)."

**SQL Query:**
```sql
SELECT s.store_name, p.product_id, p.product_name, st.quantity,
       CASE 
           WHEN st.quantity <= 10 THEN 'Low'
           WHEN st.quantity BETWEEN 11 AND 30 THEN 'Medium'
           ELSE 'High'
       END as stock_status
FROM stores s
CROSS JOIN products p
LEFT JOIN stocks st ON s.store_id = st.store_id AND p.product_id = st.product_id
WHERE st.quantity IS NOT NULL
ORDER BY s.store_name, st.quantity
LIMIT 15;
```

**Expected Answer:**  
| store_name | product_id | product_name | quantity | stock_status |
|---|---|---|---|---|
| (Inventory levels with status) |

---

### Question 19
**Difficulty:** Hard  
**Category:** Multi-level Aggregation

**NLP Query:**  
"What is the monthly revenue trend for 2016? Show month and total revenue."

**SQL Query:**
```sql
SELECT DATE_FORMAT(o.order_date, '%Y-%m') as month,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as monthly_revenue,
       COUNT(DISTINCT o.order_id) as orders_count
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE YEAR(o.order_date) = 2016
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month;
```

**Expected Answer:**  
| month | monthly_revenue | orders_count |
|---|---|---|
| 2016-01 | (January revenue) | (January orders) |
| 2016-02 | (February revenue) | (February orders) |
| (and so on for each month) |

---

### Question 20
**Difficulty:** Hard  
**Category:** Complex Analysis with Multiple Conditions

**NLP Query:**  
"Find customers who bought from multiple stores, show their total spending per store, and calculate their overall customer lifetime value."

**SQL Query:**
```sql
SELECT c.customer_id, c.first_name, c.last_name, 
       COUNT(DISTINCT o.store_id) as stores_shopped,
       COUNT(DISTINCT o.order_id) as total_orders,
       SUM(oi.quantity * oi.list_price * (1 - oi.discount)) as lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(DISTINCT o.store_id) > 1
ORDER BY lifetime_value DESC
LIMIT 10;
```

**Expected Answer:**  
| customer_id | first_name | last_name | stores_shopped | total_orders | lifetime_value |
|---|---|---|---|---|---|
| (Customers who shopped at multiple stores with their CLV) |

---

## Summary Statistics

- **Total Questions:** 20
- **Easy Questions:** 5 (Questions 1-5)
- **Medium Questions:** 8 (Questions 6-13)
- **Hard Questions:** 7 (Questions 14-20)

### Skills Covered:

**Easy Level:**
- Simple SELECT statements
- Basic WHERE clauses
- COUNT aggregation
- ORDER BY and LIMIT

**Medium Level:**
- INNER and LEFT JOINs
- Multiple table joins
- GROUP BY and HAVING
- SUM and COUNT with calculations
- LIKE pattern matching
- Date filtering with WHERE

**Hard Level:**
- Subqueries and nested queries
- Complex multi-level JOINs
- Window functions and ranking
- CASE statements
- Multiple aggregations
- Complex filtering logic
- Date grouping and formatting
- Customer lifetime value calculations

---

## Notes for Evaluation:

1. **Expected Answers:** The numeric values and exact result sets may vary slightly depending on the exact state of your database. Run the SQL queries against your database to get the definitive expected answers.

2. **Variations:** AI models might generate functionally equivalent SQL queries with different syntax. For example:
   - `INNER JOIN` vs `JOIN`
   - Different order of joins
   - Equivalent WHERE conditions
   - Different but equivalent aggregation methods

3. **Testing Criteria:** Evaluate the AI model on:
   - SQL Syntax correctness
   - Semantic correctness (does it answer the question?)
   - Query optimization
   - Result accuracy
