#Business Overview
TOTAL_REVENUE="""
;with cte as(select order_id from olist_orders_dataset o where o.order_status='delivered')
 SELECT
    SUM(oi.price + oi.freight_value) AS total_revenue
FROM dbo.olist_order_items_dataset oi(nolock)
INNER JOIN cte o
    ON o.order_id = oi.order_id """

TOTAL_ORDERS="""
SELECT
    COUNT(*) AS total_orders
FROM dbo.olist_orders_dataset(nolock)
WHERE order_status = 'delivered';"""

TOTAL_CUSTOMERS="""
SELECT
    COUNT(DISTINCT c.customer_unique_id) AS total_customers
FROM dbo.olist_orders_dataset o
INNER JOIN dbo.olist_customers_dataset c
    ON c.customer_id = o.customer_id
WHERE o.order_status = 'delivered';
"""

TOTAL_SELLERS="""
SELECT
    COUNT(DISTINCT oi.seller_id) AS total_sellers
FROM dbo.olist_order_items_dataset oi
INNER JOIN dbo.olist_orders_dataset o
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered';
"""
AVERAGE_ORDER_VALUE="""
WITH OrderRevenue AS (
    SELECT
        oi.order_id,
        SUM(oi.price + oi.freight_value) AS order_revenue
    FROM dbo.olist_order_items_dataset oi
    INNER JOIN dbo.olist_orders_dataset o
        ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY oi.order_id
)
SELECT
    AVG(order_revenue) AS average_order_value
FROM OrderRevenue;
"""

AVERAGE_REVIEW_SCORE="""
WITH OrderReviews AS (
    SELECT
        r.order_id,
        AVG(CAST(r.review_score AS FLOAT)) AS avg_review
    FROM dbo.olist_order_reviews_dataset r
    GROUP BY r.order_id
)
SELECT
    AVG(r.avg_review) AS average_review_score
FROM dbo.olist_orders_dataset o
INNER JOIN OrderReviews r
    ON r.order_id = o.order_id
WHERE o.order_status = 'delivered';
"""

YEARLY_REVENUE_ORDERS="""
SELECT
    cast(YEAR(o.order_purchase_timestamp) as varchar) AS order_year,
    SUM(oi.price + oi.freight_value) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM dbo.olist_orders_dataset o
INNER JOIN dbo.olist_order_items_dataset oi
    ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY YEAR(o.order_purchase_timestamp)
ORDER BY order_year;
"""

LOAD_YEAR="""
 SELECT DISTINCT YEAR(order_purchase_timestamp) AS order_year
 FROM dbo.olist_orders_dataset(nolock)
 WHERE order_purchase_timestamp IS NOT NULL
 ORDER BY order_year DESC;
"""

TOP_SELLING_PRODUCT="""
select top 15 product_category_name 'Product',convert(decimal(10,2),sum(price)) 'SaleValue'
from olist_products_dataset a(nolock) 
join olist_order_items_dataset b (nolock) 
on a.product_id=b.product_id
group by product_category_name
order by SaleValue desc
"""

QUERIES = {
 "TOTAL_REVENUE":TOTAL_REVENUE,
 "TOTAL_ORDERS":TOTAL_ORDERS,
 "TOTAL_CUSTOMERS":TOTAL_CUSTOMERS,
 "TOTAL_SELLERS":TOTAL_SELLERS,
 "AVERAGE_ORDER_VALUE":AVERAGE_ORDER_VALUE,
 "AVERAGE_REVIEW_SCORE":AVERAGE_REVIEW_SCORE,
 "YEARLY_REVENUE_ORDERS":YEARLY_REVENUE_ORDERS,
 "LOAD_YEAR":LOAD_YEAR,
 "TOP_SELLING_PRODUCT":TOP_SELLING_PRODUCT
}

def get_category_revenue(SelectedYear):
 query = f"""
         ;WITH cte AS (
             SELECT DISTINCT
                 o.order_id                 
             FROM dbo.olist_orders_dataset o(nolock)
             WHERE o.order_status = 'delivered'
               AND YEAR(o.order_purchase_timestamp) = {int(SelectedYear)}
         )
         SELECT
           COALESCE(p.product_category_name, 'Unknown') AS [Product Category],
           SUM(oi.price + oi.freight_value) AS Revenue
         FROM  dbo.olist_order_items_dataset oi (nolock)
         JOIN dbo.olist_products_dataset p 
         ON p.product_id = oi.product_id
         where exists(select '*' from cte o where oi.order_id=o.order_id)
         GROUP BY COALESCE(p.product_category_name, 'Unknown')
         ORDER BY SUM(oi.price + oi.freight_value) DESC;
     """
 return query

def get_monthly_revenue(SelectedYear):
  query = f"""
         ;WITH cte AS (
             SELECT DISTINCT
                 o.order_id,
                 LEFT(DATENAME(MONTH, o.order_purchase_timestamp), 3) AS MONTHNAME,
                 MONTH(o.order_purchase_timestamp) AS MONTH
             FROM dbo.olist_orders_dataset o
             WHERE o.order_status = 'delivered'
               AND YEAR(o.order_purchase_timestamp) = {int(SelectedYear)}
         )
         SELECT
             o.MONTHNAME AS MonthName,
             SUM(oi.price + oi.freight_value) AS revenue
         FROM cte o
         JOIN dbo.olist_order_items_dataset oi
             ON oi.order_id = o.order_id
         GROUP BY
             o.MONTH,
             o.MONTHNAME
         ORDER BY
             o.MONTH;
     """
  return query


def get_top_selling_product(SelectedYear):
 query = f"""
         ;WITH cte AS (
             SELECT DISTINCT
                 o.order_id                 
             FROM dbo.olist_orders_dataset o(nolock)
             WHERE o.order_status = 'delivered'
               AND YEAR(o.order_purchase_timestamp) = {int(SelectedYear)}
         )
         select top 15 product_category_name 'Product',convert(decimal(10,2),sum(price+freight_value)) 'SaleValue'
         from olist_products_dataset a(nolock) 
         join olist_order_items_dataset b (nolock) 
         on a.product_id=b.product_id
         join cte c on b.order_id=c.order_id
         group by product_category_name
         order by SaleValue desc
     """
 return query

def get_location_sales(SelectedYear):
 query = f"""
         ;with CTE as(select  a.order_id,b.customer_state
             from olist_orders_dataset a(nolock) 
             join olist_customers_dataset b(nolock)
             on a.customer_id=b.customer_id
             WHERE a.order_status = 'delivered'
                        AND YEAR(a.order_purchase_timestamp) = {int(SelectedYear)})
         select b.customer_state 'State',
                 convert(decimal(10,2),sum(price+freight_value) )'SaleValue'
         from olist_order_items_dataset a(nolock) 
         join CTE b 
         on a.order_id=b.order_id
         group by customer_state
         order by SaleValue desc
     """
 return query

def get_customer_distribution(SelectedYear):
 query = f"""
         SELECT COALESCE(c.customer_state, 'Unknown') AS state,
               COUNT(DISTINCT c.customer_unique_id) AS customers
        FROM dbo.olist_orders_dataset o
        JOIN dbo.olist_customers_dataset c ON c.customer_id = o.customer_id
        WHERE YEAR(o.order_purchase_timestamp) = {int(SelectedYear)}
          AND o.order_status = 'delivered'
        GROUP BY COALESCE(c.customer_state, 'Unknown')
        ORDER BY customers DESC
     """
 return query

def get_customer_spending(SelectedYear):
 query = f"""
          SELECT c.customer_unique_id,
               SUM(oi.price + oi.freight_value) AS total_spending,
               COUNT(DISTINCT o.order_id) AS order_count
        FROM dbo.olist_orders_dataset o
        JOIN dbo.olist_order_items_dataset oi ON oi.order_id = o.order_id
        JOIN dbo.olist_customers_dataset c ON c.customer_id = o.customer_id
        WHERE YEAR(o.order_purchase_timestamp) = {int(SelectedYear)}
          AND o.order_status = 'delivered'
        GROUP BY c.customer_unique_id
     """
 return query


def get_one_time_vs_repeat_custcount(SelectedYear):
 query = f"""
          WITH delivered_orders AS (
                SELECT c.customer_unique_id, o.order_purchase_timestamp
                FROM dbo.olist_orders_dataset o
                JOIN dbo.olist_customers_dataset c ON c.customer_id = o.customer_id
                WHERE o.order_status = 'delivered'
                  AND o.order_purchase_timestamp IS NOT NULL
            ),
            year_customers AS (
                SELECT DISTINCT customer_unique_id
                FROM delivered_orders
                WHERE order_purchase_timestamp >= DATEFROMPARTS({int(SelectedYear)}, 1, 1)
                  AND order_purchase_timestamp < DATEFROMPARTS({int(SelectedYear)} + 1, 1, 1)
            ),
            previous_customers AS (
                SELECT DISTINCT customer_unique_id
                FROM delivered_orders
                WHERE order_purchase_timestamp < DATEFROMPARTS({int(SelectedYear)}, 1, 1)
            )
            SELECT CASE WHEN p.customer_unique_id IS NULL THEN 'New'
                        ELSE 'Repeat' END AS customer_type,
                   COUNT('*') AS customers,
                   CAST(
                        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER()
                        AS DECIMAL(5,2)
                    ) AS CustomerPercentage
            FROM year_customers y
            LEFT JOIN previous_customers p
              ON p.customer_unique_id = y.customer_unique_id
            GROUP BY CASE WHEN p.customer_unique_id IS NULL THEN 'New'
                          ELSE 'Repeat' END
     """
 return query

def get_top_seller(SelectedYear):
    query = f"""  
            WITH delivered_orders AS (
                            SELECT o.order_id
                            FROM dbo.olist_orders_dataset o
                            WHERE o.order_status = 'delivered'
                              AND o.order_purchase_timestamp IS NOT NULL
                              and year(order_purchase_timestamp)={int(SelectedYear)}
                        )
            SELECT top 15
                seller_id AS SellerID,
                COUNT(DISTINCT a.order_id) AS SellerOrderCount,
                SUM(price+freight_value) AS SellerRevenue
            FROM olist_order_items_dataset(nolock) a
            join delivered_orders b
            on a.order_id=b.order_id
            GROUP BY seller_id
            ORDER BY SellerRevenue DESC;
    """
    return query

def get_seller_revenue(SelectedYear):
    query = f"""  
            WITH delivered_orders AS (
                            SELECT o.order_id
                            FROM dbo.olist_orders_dataset o(nolock)
                            WHERE o.order_status = 'delivered'
                              AND o.order_purchase_timestamp IS NOT NULL
                              and year(order_purchase_timestamp)={int(SelectedYear)}
                        )
            SELECT top 15
                seller_id AS SellerID,
                SUM(price+freight_value) AS SellerRevenue
            FROM olist_order_items_dataset(nolock) a
            join delivered_orders b
            on a.order_id=b.order_id
            GROUP BY seller_id
            ORDER BY SellerRevenue DESC;
    """
    return query

def get_seller_count(SelectedYear):
    query = f"""  
            WITH delivered_orders AS (
                            SELECT o.order_id
                            FROM dbo.olist_orders_dataset o(nolock)
                            WHERE o.order_status = 'delivered'
                              AND o.order_purchase_timestamp IS NOT NULL
                              and year(order_purchase_timestamp)={int(SelectedYear)}
                        )
            SELECT top 15
                seller_id AS SellerID,
                COUNT(DISTINCT a.order_id) AS TotalOrderCount
            FROM olist_order_items_dataset(nolock) a
            join delivered_orders b
            on a.order_id=b.order_id
            GROUP BY seller_id
            ORDER BY TotalOrderCount DESC;
    """
    return query
def get_category_yearly_revenue(SelectedYear):
    query = f"""  
             WITH delivered_orders AS (
                            SELECT o.order_id
                            FROM dbo.olist_orders_dataset o
                            WHERE o.order_status = 'delivered'
                              AND o.order_purchase_timestamp IS NOT NULL
                              and year(order_purchase_timestamp)={int(SelectedYear)}
                        )
            SELECT top 15
                COALESCE(p.product_category_name, 'Unknown') AS category,
                SUM(oi.price + oi.freight_value) AS revenue,
                COUNT(DISTINCT o.order_id) AS total_orders
            FROM delivered_orders o
            JOIN dbo.olist_order_items_dataset oi
                ON o.order_id = oi.order_id
            JOIN dbo.olist_products_dataset p
                ON oi.product_id = p.product_id
            GROUP BY p.product_category_name
            ORDER BY revenue DESC;
    """
    return query

def get_seller_rating(SelectedYear):
    query = f""" 
             WITH delivered_orders AS (
                SELECT o.order_id
                FROM dbo.olist_orders_dataset o
                WHERE o.order_status = 'delivered'
                  AND o.order_purchase_timestamp IS NOT NULL
                  and year(order_purchase_timestamp)={int(SelectedYear)}
            )
            SELECT
                oi.seller_id,
                SUM(oi.price + oi.freight_value) AS revenue,
                AVG(CAST(r.review_score AS FLOAT)) AS avg_rating,
                COUNT(DISTINCT r.review_id) AS review_count
            FROM delivered_orders o
            JOIN dbo.olist_order_items_dataset oi(nolock)
                ON o.order_id = oi.order_id
            JOIN dbo.olist_order_reviews_dataset r(nolock)
                ON o.order_id = r.order_id
            GROUP BY oi.seller_id
            ORDER BY avg_rating DESC;
    """
    return query

def get_avg_delivery_day(SelectedYear):
    query = f""" 
             SELECT
                AVG(
                    CAST(
                        DATEDIFF(
                            SECOND,
                            order_purchase_timestamp,
                            order_delivered_customer_date
                        ) / 86400.0 AS FLOAT
                    )
                ) AS avg_delivery_days
            FROM dbo.olist_orders_dataset
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date IS NOT NULL
              and year(order_purchase_timestamp)={int(SelectedYear)}
    """
    return query

def get_monthly_avg_delivery_day(SelectedYear):
    query = f""" 
             SELECT
                MONTH(order_purchase_timestamp) AS order_month,
                LEFT(DATENAME(MONTH, order_purchase_timestamp), 3) AS month_name,            
                AVG(
                    DATEDIFF(
                        SECOND,
                        order_purchase_timestamp,
                        order_delivered_customer_date
                    ) / 86400.0
                ) AS avg_delivery_days,            
                COUNT(*) AS total_orders            
            FROM dbo.olist_orders_dataset            
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date IS NOT NULL
              and year(order_purchase_timestamp)={int(SelectedYear)}
            GROUP BY
                MONTH(order_purchase_timestamp),
                LEFT(DATENAME(MONTH, order_purchase_timestamp), 3)
            ORDER BY    order_month;
    """
    return query

def get_on_time_delayed_delivery(SelectedYear):
    query = f""" 
             SELECT
                CASE
                    WHEN order_delivered_customer_date
                         <= order_estimated_delivery_date
                    THEN 'On-Time'
                    ELSE 'Delayed'
                END AS delivery_status,
                COUNT(*) AS order_count
            FROM dbo.olist_orders_dataset
            WHERE order_status = 'delivered'
              AND order_delivered_customer_date IS NOT NULL
              AND order_estimated_delivery_date IS NOT NULL
              and year(order_purchase_timestamp)={int(SelectedYear)}
            GROUP BY
                CASE
                    WHEN order_delivered_customer_date
                         <= order_estimated_delivery_date
                    THEN 'On-Time'
                    ELSE 'Delayed'
                END;
    """
    return query

def get_location_delivery(SelectedYear):
    query = f""" 
            SELECT
                c.customer_state,
                COUNT(*) AS total_orders,
            
                AVG(
                    DATEDIFF(
                        SECOND,
                        o.order_purchase_timestamp,
                        o.order_delivered_customer_date
                    ) / 86400.0
                ) AS avg_delivery_days,
            
                AVG(
                    CASE
                        WHEN o.order_delivered_customer_date
                             > o.order_estimated_delivery_date
                        THEN 1.0
                        ELSE 0.0
                    END
                ) * 100 AS delayed_rate
            
            FROM dbo.olist_orders_dataset o
            JOIN dbo.olist_customers_dataset c
                ON o.customer_id = c.customer_id
            
            WHERE o.order_status = 'delivered'
              AND o.order_delivered_customer_date IS NOT NULL
              AND o.order_estimated_delivery_date IS NOT NULL
              AND year(o.order_purchase_timestamp)={int(SelectedYear)}
            GROUP BY c.customer_state
            ORDER BY delayed_rate DESC;
    """
    return query

def get_delay_vs_review_score(SelectedYear):
    query = f""" 
             WITH ReviewByOrder AS (
                SELECT
                    order_id,
                    AVG(CAST(review_score AS FLOAT)) AS avg_review_score
                FROM dbo.olist_order_reviews_dataset
                GROUP BY order_id
            ),
            DeliveryData AS (
                SELECT
                    o.order_id,
                    DATEDIFF(
                        SECOND,
                        o.order_estimated_delivery_date,
                        o.order_delivered_customer_date
                    ) / 86400.0 AS delay_days,
                    r.avg_review_score
                FROM dbo.olist_orders_dataset o
                JOIN ReviewByOrder r
                    ON o.order_id = r.order_id
                WHERE o.order_status = 'delivered'
                  AND o.order_delivered_customer_date IS NOT NULL
                  AND o.order_estimated_delivery_date IS NOT NULL
                  AND year(o.order_purchase_timestamp)={int(SelectedYear)}
            )
            SELECT
                CASE
                    WHEN delay_days <= 0 THEN 'On-Time / Early'
                    WHEN delay_days <= 3 THEN '1-3 Days Late'
                    WHEN delay_days <= 7 THEN '4-7 Days Late'
                    ELSE 'More than 7 Days Late'
                END AS delay_group,
                COUNT(*) AS order_count,
                AVG(avg_review_score) AS avg_review_score
            FROM DeliveryData
            GROUP BY
                CASE
                    WHEN delay_days <= 0 THEN 'On-Time / Early'
                    WHEN delay_days <= 3 THEN '1-3 Days Late'
                    WHEN delay_days <= 7 THEN '4-7 Days Late'
                    ELSE 'More than 7 Days Late'
                END;
    """
    return query

def get_customer_review_data(SelectedYear):
    query = f""" 
             WITH ReviewData AS
            (
                SELECT
                    r.review_id,
                    r.review_score
                FROM dbo.olist_order_reviews_dataset r
                INNER JOIN dbo.olist_orders_dataset o
                    ON r.order_id = o.order_id
                WHERE r.review_score BETWEEN 1 AND 5
                  AND  YEAR(o.order_purchase_timestamp) = {int(SelectedYear)}
                  
            )
            SELECT
                COUNT(DISTINCT review_id) AS total_reviews,
                CAST(AVG(CAST(review_score AS FLOAT))
                     AS DECIMAL(4,2)) AS avg_review_score,
            
                CAST(
                    100.0 * SUM(CASE WHEN review_score IN (4,5)
                                     THEN 1 ELSE 0 END)
                    / NULLIF(COUNT(*),0)
                    AS DECIMAL(5,2)
                ) AS positive_review_pct,
            
                CAST(
                    100.0 * SUM(CASE WHEN review_score IN (1,2)
                                     THEN 1 ELSE 0 END)
                    / NULLIF(COUNT(*),0)
                    AS DECIMAL(5,2)
                ) AS negative_review_pct
            FROM ReviewData;
    """
    return query

def get_category_review(SelectedYear):
    query = f""" 
             WITH OrderReviews AS
            (
                SELECT
                    r.order_id,
                    AVG(CAST(r.review_score AS FLOAT)) AS avg_score
                FROM dbo.olist_order_reviews_dataset r
                INNER JOIN dbo.olist_orders_dataset o
                    ON r.order_id = o.order_id
                WHERE r.review_score BETWEEN 1 AND 5
                  AND  YEAR(o.order_purchase_timestamp) = {int(SelectedYear)}      
                GROUP BY r.order_id
            )
                SELECT
                    COALESCE(p.product_category_name, 'Unknown') AS category,
                    COUNT(*) AS review_count,
                    AVG(orv.avg_score) AS avg_review_score
                FROM OrderReviews orv
                INNER JOIN dbo.olist_order_items_dataset oi
                    ON orv.order_id = oi.order_id
                INNER JOIN dbo.olist_products_dataset p
                    ON oi.product_id = p.product_id   
                GROUP BY p.product_category_name
                HAVING COUNT(*) >= 10
    """
    return query

def get_review_cust_count(SelectedYear):
    query = f""" 
             WITH DeliveryData AS (
                SELECT
                    order_id,
                    DATEDIFF(
                        DAY,
                        order_purchase_timestamp,
                        order_delivered_customer_date
                    ) AS DeliveryDays,
                    DATEDIFF(
                        DAY,
                        order_estimated_delivery_date,
                        order_delivered_customer_date
                    ) AS DeliveryDelay,
                    CASE
                        WHEN order_delivered_customer_date
                             <= order_estimated_delivery_date
                            THEN 'On-Time / Early'
                        WHEN DATEDIFF(
                                SECOND,
                                order_estimated_delivery_date,
                                order_delivered_customer_date
                             ) / 86400.0 <= 3
                            THEN '1-3 Days Late'
                        WHEN DATEDIFF(
                                SECOND,
                                order_estimated_delivery_date,
                                order_delivered_customer_date
                             ) / 86400.0 <= 7
                            THEN '4-7 Days Late'
                        ELSE 'More than 7 Days Late'
                    END  AS DeliveryStatus
                FROM olist_orders_dataset
                WHERE order_status = 'delivered'
                  AND order_delivered_customer_date IS NOT NULL
                  AND order_estimated_delivery_date IS NOT NULL
                  AND YEAR(order_purchase_timestamp) = {int(SelectedYear)}
            )
            SELECT
                d.DeliveryStatus,
                r.review_score AS ReviewScore,
                COUNT(*) AS ReviewCount,
                AVG(CAST(d.DeliveryDays AS FLOAT)) AS AvgDeliveryDays,
                AVG(CAST(d.DeliveryDelay AS FLOAT)) AS AvgDeliveryDelay
            FROM DeliveryData d
            JOIN olist_order_reviews_dataset r
                ON d.order_id = r.order_id
            GROUP BY
                d.DeliveryStatus,
                r.review_score
            ORDER BY
                CASE DeliveryStatus
                    WHEN 'On-Time / Early' THEN 1
                    WHEN '1-3 Days Late' THEN 2
                    WHEN '4-7 Days Late' THEN 3
                    ELSE 4
                END,
                r.review_score;

    """
    return query