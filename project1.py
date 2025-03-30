import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import pymysql

# Database Connection Settings
HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
PORT = 4000
USER = "jynBzNA54kSWeXs.root"
PASSWORD = "iLlH6q8wVdsYWZQ9"
DATABASE = "project"
SSL_CERT = r"C:\Users\LENOVO\Desktop\DataScience\streamlit\env\CA cert from Tibd cloud.pem"

# Create SQLAlchemy Engine
engine = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?ssl_ca={SSL_CERT}"
)

# Function to Fetch Data
def get_data(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)  # Using SQLAlchemy for compatibility
    return df

# Streamlit App
st.set_page_config(page_title="SQL Dashboard", layout="wide")
st.title("Retail Order Data Analysis ")

# Sidebar Menu
option = st.sidebar.radio("Select Category", ["SQL Queries", "Joins", "Analysis"])

# Query dictionary
queries = {
    "SQL Queries": {
        "1. Find top 10 highest revenue generating products":
    """ select product_id,sub_category,sum(sale_price*quantity) as highest_revenue
from project.orders
group by product_id,sub_category
order by highest_revenue desc
limit 10
""",

    "2. Find the top 5 cities with the highest profit margins":
    """ SELECT
city,
SUM(sale_price * quantity) AS total_revenue,
SUM(profit) AS total_profit,
    CASE
        WHEN SUM(sale_price * quantity) > 0
        THEN ROUND((SUM(profit) / SUM(sale_price * quantity)) * 100, 2)
        ELSE 0
     END AS profit_margin
FROM project.orders
GROUP BY city
HAVING total_revenue > 0
ORDER BY profit_margin DESC
LIMIT 5
""",

    "3. Calculate the total discount given for each category":
    """
    select category,sum(discount_amount) as total_discount
from project.orders
group by category
order by total_discount desc
    """,

    "4. Find the average sale price per product category":
    """
    select category,avg(sale_price) as avg_sale_price
from project.orders
group by category
order by avg_sale_price desc
    """,

    "5. Find the region with the highest average sale price":
    """
    select region,avg(sale_price) as highest_average_sale_price
from project.orders
group by region
order by highest_average_sale_price desc
    """,

    "6. Find the total profit per category":
    """
    select category,sum(profit) as total_profit
from project.orders
group by category
order by total_profit desc
    """
    ,

    "7. Identify the top 3 segments with the highest quantity of orders":
    """
    select segment,sum(quantity) as highest_quantity
from project.orders
group by segment
order by highest_quantity desc
    """
    ,

    "8. Determine the average discount percentage given per region":
    """
   select region,avg(discount_percent) as avg_discount_percent
from project.orders
group by region
order by avg_discount_percent desc
    """
    ,

    "9. Find the product category with the highest total profit":
    """
    select category,sum(profit) as highest_total_profit
from project.orders
group by category
order by highest_total_profit desc
    """
    ,

    "10. Calculate the total revenue generated per year":
    """
    select year(order_date) as year,sum(sale_price*quantity) as total_revenue
from project.orders
group by year
order by total_revenue
    """
    },

    "Joins": {
        "1. Get all order details with product info":
        """SELECT o.order_id, o.order_date, o.ship_mode, 
       p.product_id, p.category, p.sub_category, 
       op.quantity, op.sale_price, op.profit
FROM project.order_product op
JOIN project.order o ON op.order_id = o.order_id
JOIN project.product p ON op.product_id = p.product_id limit 10""",
           
        "2. Total sales for each category":
        """SELECT p.category, SUM(op.sale_price) AS total_sales
FROM project.order_product op
JOIN project.product p ON op.product_id = p.product_id
GROUP BY p.category""",

         "3. Top 5 products with highest profit":
        """SSELECT p.product_id, p.category,p.sub_category, SUM(op.profit) AS total_profit
FROM project.order_product op
JOIN project.product p ON op.product_id = p.product_id
GROUP BY p.product_id, p.sub_category
ORDER BY total_profit DESC
LIMIT 5""",
               
          "4. Number of orders placed in each region":
        """SELECT o.region, COUNT(DISTINCT o.order_id) AS total_orders
FROM project.orders o
JOIN project.order_product op ON o.order_id = op.order_id
GROUP BY o.region""",

           "5.  Find the top 5 cities with the highest total sales.":
        """SELECT o.city, 
       SUM(op.sale_price) AS total_sales
FROM project.order_product op
JOIN project.order o ON op.order_id = o.order_id
GROUP BY o.city
ORDER BY total_sales DESC
LIMIT 5""",

            "6.Total discount given for each category":
        """SELECT p.category, SUM(op.discount_amount) AS total_discount
FROM project.order_product op
JOIN project.product p ON op.product_id = p.product_id
GROUP BY p.category""",

           "7. Orders with the highest discount percentage":
        """SELECT o.order_id,p.category,op.product_id, op.discount_percent
FROM project.order_product op
JOIN project.orders o ON op.order_id = o.order_id
JOIN project.product p ON op.product_id = p.product_id
ORDER BY op.discount_percent DESC
LIMIT 10""",

            "8. Average sale price for each sub-category":
        """SELECT p.sub_category, AVG(op.sale_price) AS avg_sale_price
FROM project.order_product op
JOIN project.product p ON op.product_id = p.product_id
GROUP BY p.sub_category""",

           "9. Most popular product (ordered most times)":
        """SELECT p.product_id, p.sub_category, COUNT(op.order_id) AS order_count
FROM project.order_product op
JOIN project.product p ON op.product_id = p.product_id
GROUP BY p.product_id, p.sub_category
ORDER BY order_count desc
limit 10""",

            "10. Total revenue, profit, and discount given for each region":
        """SELECT o.region, SUM(op.sale_price) AS total_revenue, 
       SUM(op.profit) AS total_profit, SUM(op.discount_amount) AS total_discount
FROM project.orders o
JOIN project.order_product op ON o.order_id = op.order_id
GROUP BY o.region""",
    },

    "Analysis": {
        "1. Top-Selling Products: Identify the products that generate the highest revenue based on sale prices":
        """SELECT product_id, 
       SUM(sale_price * quantity) AS total_revenue
FROM project.orders
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 5""",

        "2. Monthly Sales Analysis: Compare year-over-year sales to identify growth or decline in certain months":
        """SELECT YEAR(order_date) AS year, 
       MONTH(order_date) AS month, 
       SUM(sale_price * quantity) AS total_sales
FROM project.orders
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year, month""",

           "3. Product Performance: Use functions like GROUP BY, HAVING, ROW_NUMBER(), and CASE WHEN to categorize and rank products by their revenue, profit margin, etc":
        """SELECT product_id, 
       SUM(sale_price * quantity) AS total_revenue,
       SUM(profit) AS total_profit,
       RANK() OVER (ORDER BY SUM(sale_price * quantity) DESC) AS revenue_rank,
       RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
FROM project.orders
GROUP BY product_id limit 10""",

           "4. Regional Sales Analysis: Query sales data by region to identify which areas are performing best":
        """SELECT region, 
       SUM(sale_price * quantity) AS total_sales
FROM project.orders
GROUP BY region
ORDER BY total_sales DESC""",

           "5. Discount Analysis: Identify products with discounts greater than 20% and calculate the impact of discounts on sales":
        """SELECT product_id, 
       discount_percent, 
       SUM(sale_price * quantity) AS total_sales,
       CASE 
           WHEN discount_percent > 20 THEN 'High Discount'
           WHEN discount_percent BETWEEN 10 AND 20 THEN 'Medium Discount'
           ELSE 'Low Discount'
       END AS discount_category
FROM project.orders
GROUP BY product_id, discount_percent
ORDER BY discount_percent DESC limit 10"""
    }
}

# Display Query Options Based on Sidebar Selection
if option in queries:
    st.header(f"{option} Results")

    # Dropdown for query selection
    selected_query = st.selectbox("Choose a query:", list(queries[option].keys()))

    if st.button("Run Query"):
        df = get_data(queries[option][selected_query])  # Execute selected query
        st.dataframe(df)
