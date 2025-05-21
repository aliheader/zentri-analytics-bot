questions = [
    {
        "question": "What is the monthly order volume?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC') AS month,
                COUNT(*) AS order_count
            FROM order_orders o
            WHERE o.source_created_at IS NOT NULL
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the monthly revenue trend?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC') AS month,
                SUM(o.total_price) AS total_revenue,
                COUNT(*) AS order_count,
                ROUND(CAST(SUM(o.total_price) AS numeric), 2) AS rounded_revenue
            FROM order_orders o
            WHERE o.source_created_at IS NOT NULL
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "How frequently are products updated?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', p.source_updated_at AT TIME ZONE 'UTC') AS month,
                COUNT(*) AS update_count
            FROM product_products p
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the monthly customer acquisition trend?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.source_created_at AT TIME ZONE 'UTC') AS month,
                COUNT(*) AS new_customers
            FROM order_customers c
            WHERE c.source_created_at IS NOT NULL
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "How frequently are collections updated?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.source_updated_at AT TIME ZONE 'UTC') AS month,
                COUNT(*) AS update_count
            FROM product_collections c
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the average time between order creation and status changes?",
        "sql_query": """
            SELECT 
                o.status,
                ROUND(CAST(AVG(EXTRACT(EPOCH FROM (o.source_updated_at - o.source_created_at))/3600) AS numeric), 2) AS avg_hours_to_status_change
            FROM order_orders o
            WHERE o.source_created_at IS NOT NULL
            GROUP BY o.status
            ORDER BY avg_hours_to_status_change;
        """,
    },
    {
        "question": "How frequently are product variants updated?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', v.source_updated_at AT TIME ZONE 'UTC') AS month,
                COUNT(*) AS update_count
            FROM product_variants v
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "How frequently are customer records updated?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.source_updated_at AT TIME ZONE 'UTC') AS month,
                COUNT(*) AS update_count
            FROM order_customers c
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the average time between order creation and processing?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC') AS month,
                ROUND(CAST(AVG(EXTRACT(EPOCH FROM (o.source_updated_at - o.source_created_at))/3600) AS numeric), 2) AS avg_hours_to_process
            FROM order_orders o
            WHERE o.source_created_at IS NOT NULL
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "How many orders were placed each month?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', o.created_at AT TIME ZONE 'UTC') AS month,
                COUNT(*) AS order_count
            FROM order_orders o
            WHERE o.is_deleted = false
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "How many total customers do we have?",
        "sql_query": """
            SELECT 
                COUNT(*) AS total_customers
            FROM order_customers c
            WHERE c.is_deleted = false;
        """,
    },
    {
        "question": "How many active products are in each category?",
        "sql_query": """
            SELECT 
                pc.category_name,
                COUNT(DISTINCT p.id) AS product_count
            FROM product_productcategories pc
            JOIN product_products p ON pc.id = p.category_id
            WHERE p.is_deleted = false
            GROUP BY pc.category_name
            ORDER BY product_count DESC;
        """,
    },
    {
        "question": "What is the distribution of orders by status?",
        "sql_query": """
            SELECT 
                o.status,
                COUNT(*) AS order_count
            FROM order_orders o
            WHERE o.is_deleted = false
            GROUP BY o.status
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "What is the total revenue by month?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', o.created_at AT TIME ZONE 'UTC') AS month,
                SUM(o.total_price) AS total_revenue
            FROM order_orders o
            WHERE o.is_deleted = false
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the average order value?",
        "sql_query": """
            SELECT 
                AVG(o.total_price) AS avg_order_value
            FROM order_orders o
            WHERE o.is_deleted = false;
        """,
    },
    {
        "question": "How many products does each vendor have?",
        "sql_query": """
            SELECT 
                v.name AS vendor_name,
                COUNT(DISTINCT p.id) AS product_count
            FROM product_vendor v
            JOIN product_products p ON v.id = p.vendor_id
            WHERE p.is_deleted = false
            GROUP BY v.name
            ORDER BY product_count DESC;
        """,
    },
    {
        "question": "How many orders are from each state?",
        "sql_query": """
            SELECT 
                c.state,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_customers c
            JOIN order_orders o ON c.id = o.customer_id
            WHERE c.is_deleted = false 
                AND o.is_deleted = false
                AND c.state IS NOT NULL
            GROUP BY c.state
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "How many products are in each collection?",
        "sql_query": """
            SELECT 
                c.title AS collection_name,
                COUNT(DISTINCT pc.product_id) AS product_count
            FROM product_collections c
            JOIN product_productcollections pc ON c.id = pc.collection_id
            WHERE c.is_deleted = false
            GROUP BY c.title
            ORDER BY product_count DESC;
        """,
    },
    {
        "question": "How many orders do customers typically place?",
        "sql_query": """
            SELECT 
                COUNT(DISTINCT o.id) AS order_count,
                COUNT(DISTINCT c.id) AS customer_count
            FROM order_customers c
            JOIN order_orders o ON c.id = o.customer_id
            WHERE c.is_deleted = false 
                AND o.is_deleted = false
            GROUP BY c.id
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "What is the average order value by month?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', o.created_at) AS month,
                AVG(o.total_price) AS avg_order_value,
                COUNT(*) AS order_count
            FROM order_orders o
            WHERE o.is_deleted = false
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "Which product categories have the highest number of products?",
        "sql_query": """
            SELECT 
                pc.category_name,
                COUNT(DISTINCT p.id) AS product_count
            FROM product_productcategories pc
            JOIN product_products p ON pc.id = p.category_id
            WHERE p.is_deleted = false
            GROUP BY pc.category_name
            ORDER BY product_count DESC;
        """,
    },
    {
        "question": "What is the customer retention rate by month?",
        "sql_query": """
            WITH customer_orders AS (
                SELECT 
                    c.id AS customer_id,
                    DATE_TRUNC('month', o.created_at) AS order_month,
                    COUNT(DISTINCT o.id) AS order_count
                FROM order_customers c
                JOIN order_orders o ON c.id = o.customer_id
                WHERE c.is_deleted = false AND o.is_deleted = false
                GROUP BY c.id, order_month
            )
            SELECT 
                order_month,
                COUNT(DISTINCT CASE WHEN order_count > 1 THEN customer_id END) * 100.0 / 
                COUNT(DISTINCT customer_id) AS retention_rate
            FROM customer_orders
            GROUP BY order_month
            ORDER BY order_month DESC;
        """,
    },
    {
        "question": "What is the average time between orders for repeat customers?",
        "sql_query": """
            WITH order_times AS (
                SELECT 
                    o.customer_id,
                    o.created_at,
                    LAG(o.created_at) OVER (PARTITION BY o.customer_id ORDER BY o.created_at) AS prev_order_time
                FROM order_orders o
                WHERE o.is_deleted = false
            )
            SELECT 
                AVG(EXTRACT(EPOCH FROM (created_at - prev_order_time))/86400) AS avg_days_between_orders
            FROM order_times
            WHERE prev_order_time IS NOT NULL;
        """,
    },
    {
        "question": "Which vendors have the highest average product price?",
        "sql_query": """
            SELECT 
                v.name AS vendor_name,
                AVG(pv.price) AS avg_product_price,
                COUNT(DISTINCT p.id) AS product_count
            FROM product_vendor v
            JOIN product_products p ON v.id = p.vendor_id
            JOIN product_variants pv ON p.id = pv.product_id
            WHERE v.is_deleted = false 
                AND p.is_deleted = false 
                AND pv.is_deleted = false
            GROUP BY v.name
            ORDER BY avg_product_price DESC;
        """,
    },
    {
        "question": "What is the distribution of order statuses?",
        "sql_query": """
            SELECT 
                o.status,
                COUNT(*) AS order_count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
            FROM order_orders o
            WHERE o.is_deleted = false
            GROUP BY o.status
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Who are the top 10 customers by total spend?",
        "sql_query": """
            SELECT 
                c.first_name,
                c.last_name,
                c.email,
                SUM(o.total_price) AS total_spent,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_customers c
            JOIN order_orders o ON c.id = o.customer_id
            WHERE c.is_deleted = false AND o.is_deleted = false
            GROUP BY c.id, c.first_name, c.last_name, c.email
            ORDER BY total_spent DESC
            LIMIT 10;
        """,
    },
    {
        "question": "What is the average order value by customer state?",
        "sql_query": """
            SELECT 
                c.state,
                AVG(o.total_price) AS avg_order_value,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_customers c
            JOIN order_orders o ON c.id = o.customer_id
            WHERE c.is_deleted = false 
                AND o.is_deleted = false 
                AND c.state IS NOT NULL
            GROUP BY c.state
            ORDER BY avg_order_value DESC;
        """,
    },
    {
        "question": "What is the total revenue trend over the last 12 months?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', o.created_at) AS month,
                SUM(o.total_price) AS total_revenue
            FROM order_orders o
            WHERE o.is_deleted = false 
                AND o.created_at >= NOW() - INTERVAL '12 months'
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the daily revenue trend for the last 30 days?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('day', o.created_at) AS day,
                SUM(o.total_price) AS daily_revenue
            FROM order_orders o
            WHERE o.is_deleted = false 
                AND o.created_at >= NOW() - INTERVAL '30 days'
            GROUP BY day
            ORDER BY day DESC;
        """,
    },
    {
        "question": "What is the average order value trend over time?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', o.created_at) AS month,
                AVG(o.total_price) AS avg_order_value,
                COUNT(*) AS order_count
            FROM order_orders o
            WHERE o.is_deleted = false
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the customer acquisition trend by month?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.created_at) AS month,
                COUNT(*) AS new_customers
            FROM order_customers c
            WHERE c.is_deleted = false
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the customer lifetime value by acquisition month?",
        "sql_query": """
            WITH customer_lifetime AS (
                SELECT 
                    c.id,
                    DATE_TRUNC('month', c.created_at) AS acquisition_month,
                    SUM(o.total_price) AS lifetime_value
                FROM order_customers c
                JOIN order_orders o ON c.id = o.customer_id
                WHERE c.is_deleted = false AND o.is_deleted = false
                GROUP BY c.id, acquisition_month
            )
            SELECT 
                acquisition_month,
                AVG(lifetime_value) AS avg_lifetime_value,
                COUNT(*) AS customer_count
            FROM customer_lifetime
            GROUP BY acquisition_month
            ORDER BY acquisition_month DESC;
        """,
    },
    {
        "question": "What is the distribution of customer order frequency?",
        "sql_query": """
            SELECT 
                order_count,
                COUNT(*) AS customer_count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
            FROM (
                SELECT 
                    customer_id,
                    COUNT(*) AS order_count
                FROM order_orders
                WHERE is_deleted = false
                GROUP BY customer_id
            ) customer_orders
            GROUP BY order_count
            ORDER BY order_count;
        """,
    },
    {
        "question": "What is the average time to first repeat purchase?",
        "sql_query": """
            WITH repeat_purchases AS (
                SELECT 
                    customer_id,
                    created_at,
                    LAG(created_at) OVER (PARTITION BY customer_id ORDER BY created_at) AS prev_order_time
                FROM order_orders
                WHERE is_deleted = false
            )
            SELECT 
                AVG(EXTRACT(EPOCH FROM (created_at - prev_order_time))/86400) AS avg_days_to_repeat
            FROM repeat_purchases
            WHERE prev_order_time IS NOT NULL;
        """,
    },
    {
        "question": "What is the conversion rate by marketing channel?",
        "sql_query": """
            SELECT 
                o.source,
                COUNT(DISTINCT o.id) AS order_count,
                COUNT(DISTINCT c.id) AS visitor_count,
                ROUND(COUNT(DISTINCT o.id) * 100.0 / COUNT(DISTINCT c.id), 2) AS conversion_rate
            FROM order_orders o
            JOIN order_customers c ON o.customer_id = c.id
            WHERE o.is_deleted = false AND c.is_deleted = false
            GROUP BY o.source
            ORDER BY conversion_rate DESC;
        """,
    },
    {
        "question": "What is the email marketing opt-in rate by month?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.created_at) AS month,
                COUNT(CASE WHEN c.accept_email_marketing THEN 1 END) AS opted_in,
                COUNT(*) AS total_customers,
                ROUND(COUNT(CASE WHEN c.accept_email_marketing THEN 1 END) * 100.0 / COUNT(*), 2) AS opt_in_rate
            FROM order_customers c
            WHERE c.is_deleted = false
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the SMS marketing opt-in rate by month?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.created_at) AS month,
                COUNT(CASE WHEN c.accept_sms_marketing THEN 1 END) AS opted_in,
                COUNT(*) AS total_customers,
                ROUND(COUNT(CASE WHEN c.accept_sms_marketing THEN 1 END) * 100.0 / COUNT(*), 2) AS opt_in_rate
            FROM order_customers c
            WHERE c.is_deleted = false
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the impact of marketing campaigns on order value?",
        "sql_query": """
            SELECT 
                o.source,
                o.discount_code,
                AVG(o.total_price) AS avg_order_value,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_orders o
            WHERE o.is_deleted = false
            GROUP BY o.source, o.discount_code
            ORDER BY avg_order_value DESC;
        """,
    },
    {
        "question": "What is the average order value by city?",
        "sql_query": """
            SELECT 
                sa.city,
                sa.country,
                AVG(o.total_price) AS avg_order_value,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_orders o
            JOIN order_shippingaddress sa ON o.id = sa.order_id
            WHERE o.is_deleted = false AND sa.is_deleted = false
            GROUP BY sa.city, sa.country
            HAVING COUNT(DISTINCT o.id) > 10
            ORDER BY avg_order_value DESC;
        """,
    },
    {
        "question": "What is the customer density by region?",
        "sql_query": """
            SELECT 
                sa.province,
                sa.country,
                COUNT(DISTINCT o.customer_id) AS customer_count,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_orders o
            JOIN order_shippingaddress sa ON o.id = sa.order_id
            WHERE o.is_deleted = false AND sa.is_deleted = false
            GROUP BY sa.province, sa.country
            ORDER BY customer_count DESC;
        """,
    },
    {
        "question": "What is the delivery time analysis by region?",
        "sql_query": """
            SELECT 
                sa.country,
                sa.province,
                AVG(EXTRACT(EPOCH FROM (oli.delivered_at - o.created_at))/86400) AS avg_delivery_days,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_orders o
            JOIN order_shippingaddress sa ON o.id = sa.order_id
            JOIN order_lineitems oli ON o.id = oli.order_id
            WHERE o.is_deleted = false 
                AND sa.is_deleted = false 
                AND oli.is_deleted = false
                AND oli.delivered_at IS NOT NULL
            GROUP BY sa.country, sa.province
            ORDER BY avg_delivery_days;
        """,
    },
    {
        "question": "What is the refund analysis by reason?",
        "sql_query": """
            SELECT 
                oli.return_reason,
                COUNT(DISTINCT oli.id) AS return_count,
                SUM(oli.price * oli.quantity) AS refund_amount,
                ROUND(COUNT(DISTINCT oli.id) * 100.0 / SUM(COUNT(DISTINCT oli.id)) OVER (), 2) AS return_percentage
            FROM order_lineitems oli
            WHERE oli.is_deleted = false AND oli.return_reason IS NOT NULL
            GROUP BY oli.return_reason
            ORDER BY return_count DESC;
        """,
    },
    {
        "question": "What is the out-of-stock analysis by category?",
        "sql_query": """
            SELECT 
                pc.category_name,
                COUNT(CASE WHEN pv.quantity = 0 THEN 1 END) AS out_of_stock_count,
                COUNT(*) AS total_products,
                ROUND(COUNT(CASE WHEN pv.quantity = 0 THEN 1 END) * 100.0 / COUNT(*), 2) AS out_of_stock_percentage
            FROM product_productcategories pc
            JOIN product_products p ON pc.id = p.category_id
            JOIN product_variants pv ON p.id = pv.product_id
            WHERE p.is_deleted = false AND pv.is_deleted = false
            GROUP BY pc.category_name
            ORDER BY out_of_stock_percentage DESC;
        """,
    },
    {
        "question": "What is the inventory value by category?",
        "sql_query": """
            SELECT 
                pc.category_name,
                SUM(pv.quantity * pv.cost_per_item) AS inventory_value,
                COUNT(DISTINCT p.id) AS product_count
            FROM product_productcategories pc
            JOIN product_products p ON pc.id = p.category_id
            JOIN product_variants pv ON p.id = pv.product_id
            WHERE p.is_deleted = false AND pv.is_deleted = false
            GROUP BY pc.category_name
            ORDER BY inventory_value DESC;
        """,
    },
    {
        "question": "What is the order fulfillment time analysis?",
        "sql_query": """
            SELECT 
                o.status,
                AVG(EXTRACT(EPOCH FROM (oli.delivered_at - o.created_at))/86400) AS avg_fulfillment_days,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_orders o
            JOIN order_lineitems oli ON o.id = oli.order_id
            WHERE o.is_deleted = false 
                AND oli.is_deleted = false
                AND oli.delivered_at IS NOT NULL
            GROUP BY o.status
            ORDER BY avg_fulfillment_days;
        """,
    },
    {
        "question": "What is the seasonal sales pattern by month?",
        "sql_query": """
            SELECT 
                EXTRACT(MONTH FROM o.created_at) AS month,
                SUM(o.total_price) AS total_revenue,
                COUNT(DISTINCT o.id) AS order_count,
                AVG(o.total_price) AS avg_order_value
            FROM order_orders o
            WHERE o.is_deleted = false
            GROUP BY month
            ORDER BY month;
        """,
    },
    {
        "question": "What is the holiday season performance analysis?",
        "sql_query": """
            SELECT 
                CASE 
                    WHEN EXTRACT(MONTH FROM o.created_at) = 12 THEN 'December'
                    WHEN EXTRACT(MONTH FROM o.created_at) = 11 THEN 'November'
                    ELSE 'Other'
                END AS season,
                SUM(o.total_price) AS total_revenue,
                COUNT(DISTINCT o.id) AS order_count,
                AVG(o.total_price) AS avg_order_value
            FROM order_orders o
            WHERE o.is_deleted = false
            GROUP BY season
            ORDER BY total_revenue DESC;
        """,
    },
    {
        "question": "What is the promotional campaign effectiveness by season?",
        "sql_query": """
            SELECT 
                CASE 
                    WHEN EXTRACT(MONTH FROM o.created_at) IN (12, 1, 2) THEN 'Winter'
                    WHEN EXTRACT(MONTH FROM o.created_at) IN (3, 4, 5) THEN 'Spring'
                    WHEN EXTRACT(MONTH FROM o.created_at) IN (6, 7, 8) THEN 'Summer'
                    ELSE 'Fall'
                END AS season,
                o.discount_code,
                COUNT(DISTINCT o.id) AS order_count,
                SUM(o.total_price) AS total_revenue,
                SUM(o.total_discounts) AS total_discounts
            FROM order_orders o
            WHERE o.is_deleted = false AND o.discount_code IS NOT NULL
            GROUP BY season, o.discount_code
            ORDER BY season, total_revenue DESC;
        """,
    },
    {
        "question": "What are the top 10 best-selling products by revenue?",
        "sql_query": """
            SELECT 
                p.title,
                SUM(oli.price * oli.quantity) AS total_revenue,
                SUM(oli.quantity) AS total_quantity
            FROM product_products p
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            GROUP BY p.title
            ORDER BY total_revenue DESC
            LIMIT 10;
        """,
    },
    {
        "question": "What are the top performing product variants?",
        "sql_query": """
            SELECT 
                p.title AS product_name,
                pv.title AS variant_name,
                SUM(oli.quantity) AS total_quantity,
                SUM(oli.price * oli.quantity) AS total_revenue
            FROM product_products p
            JOIN product_variants pv ON p.source_product_id = pv.source_product_id
            JOIN order_lineitems oli ON pv.source_variant_id = oli.variant_id
            GROUP BY p.title, pv.title
            ORDER BY total_revenue DESC
            LIMIT 10;
        """,
    },
    {
        "question": "What is the revenue by product category?",
        "sql_query": """
            SELECT 
                pc.category_name,
                SUM(oli.price * oli.quantity) AS category_revenue,
                ROUND(CAST(SUM(oli.price * oli.quantity) * 100.0 / 
                    SUM(SUM(oli.price * oli.quantity)) OVER () AS numeric), 2) AS revenue_percentage
            FROM product_productcategories pc
            JOIN product_products p ON pc.id = p.category_id
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            GROUP BY pc.category_name
            ORDER BY category_revenue DESC;
        """,
    },
    {
        "question": "What is the return rate by product?",
        "sql_query": """
            SELECT 
                p.title,
                COUNT(DISTINCT CASE WHEN oli.return_reason IS NOT NULL THEN oli.id END) AS returned_items,
                COUNT(DISTINCT oli.id) AS total_items,
                ROUND(CAST(COUNT(DISTINCT CASE WHEN oli.return_reason IS NOT NULL THEN oli.id END) * 100.0 / 
                    COUNT(DISTINCT oli.id) AS numeric), 2) AS return_rate
            FROM product_products p
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            GROUP BY p.title
            HAVING COUNT(DISTINCT oli.id) > 10
            ORDER BY return_rate DESC;
        """,
    },
    {
        "question": "What is the inventory turnover by product?",
        "sql_query": """
            SELECT 
                p.title,
                pv.quantity AS current_inventory,
                COUNT(DISTINCT oli.order_id) AS order_count,
                SUM(oli.quantity) AS total_sold,
                ROUND(CAST(SUM(oli.quantity) * 1.0 / NULLIF(pv.quantity, 0) AS numeric), 2) AS turnover_rate
            FROM product_products p
            JOIN product_variants pv ON p.source_product_id = pv.source_product_id
            LEFT JOIN order_lineitems oli ON pv.source_variant_id = oli.variant_id
            GROUP BY p.title, pv.quantity
            ORDER BY turnover_rate DESC;
        """,
    },
    {
        "question": "What is the average price and quantity sold by product?",
        "sql_query": """
            SELECT 
                p.title,
                ROUND(CAST(AVG(oli.price) AS numeric), 2) AS avg_price,
                SUM(oli.quantity) AS total_quantity,
                SUM(oli.price * oli.quantity) AS total_revenue
            FROM product_products p
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            GROUP BY p.title
            ORDER BY total_revenue DESC;
        """,
    },
    {
        "question": "What is the price distribution by product variant?",
        "sql_query": """
            SELECT 
                p.title AS product_name,
                pv.title AS variant_name,
                ROUND(CAST(AVG(oli.price) AS numeric), 2) AS avg_price,
                MIN(oli.price) AS min_price,
                MAX(oli.price) AS max_price,
                SUM(oli.quantity) AS total_quantity
            FROM product_products p
            JOIN product_variants pv ON p.source_product_id = pv.source_product_id
            JOIN order_lineitems oli ON pv.source_variant_id = oli.variant_id
            GROUP BY p.title, pv.title
            ORDER BY total_quantity DESC;
        """,
    },
    {
        "question": "What is the revenue by product collection?",
        "sql_query": """
            SELECT 
                c.title AS collection_name,
                SUM(oli.price * oli.quantity) AS collection_revenue,
                COUNT(DISTINCT p.id) AS product_count
            FROM product_collections c
            JOIN product_productcollections pc ON c.id = pc.collection_id
            JOIN product_products p ON pc.product_id = p.id
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            GROUP BY c.title
            ORDER BY collection_revenue DESC;
        """,
    },
    {
        "question": "What is the revenue by vendor?",
        "sql_query": """
            SELECT 
                v.name AS vendor_name,
                SUM(oli.price * oli.quantity) AS vendor_revenue,
                COUNT(DISTINCT p.id) AS product_count
            FROM product_vendor v
            JOIN product_products p ON v.id = p.vendor_id
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            GROUP BY v.name
            ORDER BY vendor_revenue DESC;
        """,
    },
    {
        "question": "What is the discount impact on product sales?",
        "sql_query": """
            SELECT 
                p.title,
                ROUND(CAST(AVG(oli.total_discounts) AS numeric), 2) AS avg_discount,
                ROUND(CAST(AVG(oli.total_discounts) * 100.0 / AVG(oli.price) AS numeric), 2) AS discount_percentage,
                SUM(oli.quantity) AS total_quantity
            FROM product_products p
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            WHERE oli.total_discounts > 0
            GROUP BY p.title
            ORDER BY total_quantity DESC;
        """,
    },
    {
        "question": "What is the seasonal performance of products?",
        "sql_query": """
            SELECT 
                p.title,
                EXTRACT(MONTH FROM o.source_created_at AT TIME ZONE 'UTC') AS month,
                SUM(oli.quantity) AS total_quantity,
                SUM(oli.price * oli.quantity) AS total_revenue
            FROM product_products p
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            JOIN order_orders o ON oli.order_id = o.id
            GROUP BY p.title, month
            ORDER BY p.title, month;
        """,
    },
    {
        "question": "What is the availability status of product variants?",
        "sql_query": """
            SELECT 
                p.title AS product_name,
                pv.title AS variant_name,
                pv.quantity AS current_stock,
                COUNT(DISTINCT oli.order_id) AS recent_orders,
                SUM(oli.quantity) AS recent_sales
            FROM product_products p
            JOIN product_variants pv ON p.source_product_id = pv.source_product_id
            LEFT JOIN order_lineitems oli ON pv.source_variant_id = oli.variant_id
                AND oli.created_at >= NOW() - INTERVAL '30 days'
            GROUP BY p.title, pv.title, pv.quantity
            ORDER BY current_stock;
        """,
    },
    {
        "question": "What is the growth rate of product categories?",
        "sql_query": """
            SELECT 
                pc.category_name,
                DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC') AS month,
                SUM(oli.price * oli.quantity) AS monthly_revenue,
                LAG(SUM(oli.price * oli.quantity)) OVER (PARTITION BY pc.category_name ORDER BY DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC')) AS prev_month_revenue,
                ROUND(CAST((SUM(oli.price * oli.quantity) - LAG(SUM(oli.price * oli.quantity)) OVER (PARTITION BY pc.category_name ORDER BY DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC'))) * 100.0 / 
                    NULLIF(LAG(SUM(oli.price * oli.quantity)) OVER (PARTITION BY pc.category_name ORDER BY DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC')), 0) AS numeric), 2) AS growth_rate
            FROM product_productcategories pc
            JOIN product_products p ON pc.id = p.category_id
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            JOIN order_orders o ON oli.order_id = o.id
            GROUP BY pc.category_name, month
            ORDER BY pc.category_name, month;
        """,
    },
    {
        "question": "What products are frequently purchased together?",
        "sql_query": """
            SELECT 
                p1.title AS product1,
                p2.title AS product2,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_orders o
            JOIN order_lineitems oli1 ON o.id = oli1.order_id
            JOIN product_products p1 ON p1.source_product_id = oli1.product_id
            JOIN order_lineitems oli2 ON o.id = oli2.order_id
            JOIN product_products p2 ON p2.source_product_id = oli2.product_id
            WHERE p1.id < p2.id
            GROUP BY p1.title, p2.title
            HAVING COUNT(DISTINCT o.id) > 5
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "How effective are product collections?",
        "sql_query": """
            SELECT 
                c.title AS collection_name,
                COUNT(DISTINCT p.id) AS total_products,
                COUNT(DISTINCT oli.order_id) AS order_count,
                SUM(oli.price * oli.quantity) AS total_revenue,
                ROUND(CAST(SUM(oli.price * oli.quantity) / COUNT(DISTINCT p.id) AS numeric), 2) AS revenue_per_product
            FROM product_collections c
            JOIN product_productcollections pc ON c.id = pc.collection_id
            JOIN product_products p ON pc.product_id = p.id
            LEFT JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            GROUP BY c.title
            ORDER BY revenue_per_product DESC;
        """,
    },
    {
        "question": "What is the performance trend of vendors?",
        "sql_query": """
            SELECT 
                v.name AS vendor_name,
                DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC') AS month,
                COUNT(DISTINCT p.id) AS active_products,
                SUM(oli.price * oli.quantity) AS monthly_revenue
            FROM product_vendor v
            JOIN product_products p ON v.id = p.vendor_id
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            JOIN order_orders o ON oli.order_id = o.id
            GROUP BY v.name, month
            ORDER BY v.name, month;
        """,
    },
    {
        "question": "What are the main reasons for product returns?",
        "sql_query": """
            SELECT 
                p.title,
                oli.return_reason,
                COUNT(*) AS return_count,
                ROUND(CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY p.title) AS numeric), 2) AS return_percentage
            FROM product_products p
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            WHERE oli.return_reason IS NOT NULL
            GROUP BY p.title, oli.return_reason
            ORDER BY p.title, return_count DESC;
        """,
    },
    {
        "question": "What is the shipping cost analysis by product?",
        "sql_query": """
            SELECT 
                p.title,
                AVG(o.shipping_charge) AS avg_shipping_cost,
                AVG(oli.price * oli.quantity) AS avg_order_value,
                ROUND(CAST(AVG(o.shipping_charge) * 100.0 / AVG(oli.price * oli.quantity) AS numeric), 2) AS shipping_percentage
            FROM product_products p
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            JOIN order_orders o ON oli.order_id = o.id
            GROUP BY p.title
            ORDER BY shipping_percentage DESC;
        """,
    },
    {
        "question": "What is the tax analysis by product?",
        "sql_query": """
            SELECT 
                p.title,
                SUM(oli.tax) AS total_tax,
                SUM(oli.price * oli.quantity) AS total_revenue,
                ROUND(CAST(SUM(oli.tax) * 100.0 / SUM(oli.price * oli.quantity) AS numeric), 2) AS tax_percentage
            FROM product_products p
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            GROUP BY p.title
            ORDER BY tax_percentage DESC;
        """,
    },
    {
        "question": "How effective are discounts on products?",
        "sql_query": """
            SELECT 
                p.title,
                AVG(oli.total_discounts) AS avg_discount,
                AVG(oli.price * oli.quantity) AS avg_order_value,
                SUM(oli.quantity) AS total_quantity,
                ROUND(CAST(AVG(oli.total_discounts) * 100.0 / AVG(oli.price * oli.quantity) AS numeric), 2) AS discount_percentage
            FROM product_products p
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            WHERE oli.total_discounts > 0
            GROUP BY p.title
            ORDER BY total_quantity DESC;
        """,
    },
    {
        "question": "What is the fulfillment status of products?",
        "sql_query": """
            SELECT 
                p.title,
                oli.fulfillment_status,
                COUNT(*) AS item_count,
                SUM(oli.quantity) AS total_quantity
            FROM product_products p
            JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            GROUP BY p.title, oli.fulfillment_status
            ORDER BY p.title, item_count DESC;
        """,
    },
    {
        "question": "What is the weight distribution of products?",
        "sql_query": """
            SELECT 
                p.title,
                pv.weight,
                pv.weight_unit,
                COUNT(DISTINCT oli.order_id) AS order_count,
                SUM(oli.quantity) AS total_quantity
            FROM product_products p
            JOIN product_variants pv ON p.source_product_id = pv.source_product_id
            JOIN order_lineitems oli ON pv.source_variant_id = oli.variant_id
            GROUP BY p.title, pv.weight, pv.weight_unit
            ORDER BY total_quantity DESC;
        """,
    },
    {
        "question": "What is the barcode coverage of products?",
        "sql_query": """
            SELECT 
                p.title,
                COUNT(DISTINCT CASE WHEN pv.barcode IS NOT NULL THEN pv.id END) AS barcoded_variants,
                COUNT(DISTINCT pv.id) AS total_variants,
                ROUND(CAST(COUNT(DISTINCT CASE WHEN pv.barcode IS NOT NULL THEN pv.id END) * 100.0 / 
                    COUNT(DISTINCT pv.id) AS numeric), 2) AS barcode_coverage
            FROM product_products p
            JOIN product_variants pv ON p.source_product_id = pv.source_product_id
            GROUP BY p.title
            ORDER BY barcode_coverage DESC;
        """,
    },
    {
        "question": "What is the category distribution by vendor?",
        "sql_query": """
            SELECT 
                v.name AS vendor_name,
                pc.category_name,
                COUNT(DISTINCT p.id) AS product_count,
                SUM(oli.price * oli.quantity) AS total_revenue
            FROM product_vendor v
            JOIN product_products p ON v.id = p.vendor_id
            JOIN product_productcategories pc ON p.category_id = pc.id
            LEFT JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            GROUP BY v.name, pc.category_name
            ORDER BY v.name, total_revenue DESC;
        """,
    },
    {
        "question": "How effective are product tags?",
        "sql_query": """
            SELECT 
                t.name AS tag_name,
                COUNT(DISTINCT p.id) AS product_count,
                COUNT(DISTINCT oli.order_id) AS order_count,
                SUM(oli.price * oli.quantity) AS total_revenue
            FROM product_tags t
            JOIN product_producttags pt ON t.id = pt.tag_id
            JOIN product_products p ON pt.product_id = p.id
            LEFT JOIN order_lineitems oli ON p.source_product_id = oli.product_id
            GROUP BY t.name
            ORDER BY total_revenue DESC;
        """,
    },
    {
        "question": "What are the most popular product variant options?",
        "sql_query": """
            SELECT 
                p.title AS product_name,
                po.name AS option_name,
                po.value AS option_value,
                COUNT(DISTINCT oli.order_id) AS order_count,
                SUM(oli.quantity) AS total_quantity
            FROM product_products p
            JOIN product_options po ON p.id = po.product_id
            JOIN product_variants pv ON p.source_product_id = pv.source_product_id
            JOIN order_lineitems oli ON pv.source_variant_id = oli.variant_id
            GROUP BY p.title, po.name, po.value
            ORDER BY total_quantity DESC;
        """,
    },
    {
        "question": "What is the cost analysis of products?",
        "sql_query": """
            SELECT 
                p.title,
                AVG(pv.cost_per_item) AS avg_cost,
                AVG(oli.price) AS avg_selling_price,
                ROUND(CAST((AVG(oli.price) - AVG(pv.cost_per_item)) * 100.0 / AVG(oli.price) AS numeric), 2) AS margin_percentage
            FROM product_products p
            JOIN product_variants pv ON p.source_product_id = pv.source_product_id
            JOIN order_lineitems oli ON pv.source_variant_id = oli.variant_id
            GROUP BY p.title
            ORDER BY margin_percentage DESC;
        """,
    },
    {
        "question": "What is the warranty distribution of products?",
        "sql_query": """
            SELECT 
                p.title,
                pv.warranty,
                COUNT(DISTINCT oli.order_id) AS order_count,
                SUM(oli.quantity) AS total_quantity
            FROM product_products p
            JOIN product_variants pv ON p.source_product_id = pv.source_product_id
            JOIN order_lineitems oli ON pv.source_variant_id = oli.variant_id
            GROUP BY p.title, pv.warranty
            ORDER BY total_quantity DESC;
        """,
    },
    {
        "question": "What are the top shipping cities by order volume?",
        "sql_query": """
            SELECT 
                sa.city,
                COUNT(DISTINCT o.id) AS order_count,
                SUM(o.total_price) AS total_revenue,
                ROUND(CAST(AVG(o.total_price) AS numeric), 2) AS avg_order_value
            FROM order_orders o
            JOIN order_shippingaddress sa ON o.id = sa.order_id
            GROUP BY sa.city
            ORDER BY order_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "What is the customer distribution by state?",
        "sql_query": """
            SELECT 
                c.state,
                COUNT(DISTINCT c.id) AS customer_count,
                COUNT(DISTINCT o.id) AS order_count,
                SUM(o.total_price) AS total_revenue
            FROM order_customers c
            LEFT JOIN order_orders o ON c.id = o.customer_id
            WHERE c.state IS NOT NULL
            GROUP BY c.state
            ORDER BY customer_count DESC;
        """,
    },
    {
        "question": "What is the distribution of customer order frequency?",
        "sql_query": """
            SELECT 
                order_count_range,
                COUNT(*) AS customer_count,
                ROUND(CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS numeric), 2) AS percentage
            FROM (
                SELECT 
                    c.id,
                    CASE 
                        WHEN COUNT(DISTINCT o.id) = 1 THEN '1 order'
                        WHEN COUNT(DISTINCT o.id) <= 3 THEN '2-3 orders'
                        WHEN COUNT(DISTINCT o.id) <= 5 THEN '4-5 orders'
                        ELSE '6+ orders'
                    END AS order_count_range
                FROM order_customers c
                LEFT JOIN order_orders o ON c.id = o.customer_id
                GROUP BY c.id
            ) AS customer_orders
            GROUP BY order_count_range
            ORDER BY customer_count DESC;
        """,
    },
    {
        "question": "What is the customer acquisition by source?",
        "sql_query": """
            SELECT 
                c.source,
                COUNT(DISTINCT c.id) AS customer_count,
                COUNT(DISTINCT o.id) AS order_count,
                SUM(o.total_price) AS total_revenue
            FROM order_customers c
            LEFT JOIN order_orders o ON c.id = o.customer_id
            GROUP BY c.source
            ORDER BY customer_count DESC;
        """,
    },
    {
        "question": "What is the email marketing opt-in rate by month?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.accept_email_marketing_at AT TIME ZONE 'UTC') AS month,
                COUNT(DISTINCT CASE WHEN c.accept_email_marketing THEN c.id END) AS opted_in,
                COUNT(DISTINCT c.id) AS total_customers,
                ROUND(CAST(COUNT(DISTINCT CASE WHEN c.accept_email_marketing THEN c.id END) * 100.0 / 
                    COUNT(DISTINCT c.id) AS numeric), 2) AS opt_in_rate
            FROM order_customers c
            WHERE c.accept_email_marketing_at IS NOT NULL
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the SMS marketing opt-in rate by month?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.accept_sms_marketing_at AT TIME ZONE 'UTC') AS month,
                COUNT(DISTINCT CASE WHEN c.accept_sms_marketing THEN c.id END) AS opted_in,
                COUNT(DISTINCT c.id) AS total_customers,
                ROUND(CAST(COUNT(DISTINCT CASE WHEN c.accept_sms_marketing THEN c.id END) * 100.0 / 
                    COUNT(DISTINCT c.id) AS numeric), 2) AS opt_in_rate
            FROM order_customers c
            WHERE c.accept_sms_marketing_at IS NOT NULL
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the order distribution by province?",
        "sql_query": """
            SELECT 
                sa.province,
                COUNT(DISTINCT o.id) AS order_count,
                SUM(o.total_price) AS total_revenue,
                ROUND(CAST(AVG(o.total_price) AS numeric), 2) AS avg_order_value
            FROM order_orders o
            JOIN order_shippingaddress sa ON o.id = sa.order_id
            WHERE sa.province IS NOT NULL
            GROUP BY sa.province
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "What is the order distribution by country?",
        "sql_query": """
            SELECT 
                sa.country,
                COUNT(DISTINCT o.id) AS order_count,
                SUM(o.total_price) AS total_revenue,
                ROUND(CAST(AVG(o.total_price) AS numeric), 2) AS avg_order_value
            FROM order_orders o
            JOIN order_shippingaddress sa ON o.id = sa.order_id
            GROUP BY sa.country
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "What is the customer lifetime value by acquisition month?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.source_created_at AT TIME ZONE 'UTC') AS acquisition_month,
                COUNT(DISTINCT c.id) AS customer_count,
                SUM(o.total_price) AS total_revenue,
                ROUND(CAST(SUM(o.total_price) / COUNT(DISTINCT c.id) AS numeric), 2) AS avg_lifetime_value
            FROM order_customers c
            LEFT JOIN order_orders o ON c.id = o.customer_id
            GROUP BY acquisition_month
            ORDER BY acquisition_month DESC;
        """,
    },
    {
        "question": "What is the customer repeat purchase rate by month?",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC') AS month,
                COUNT(DISTINCT CASE WHEN order_count > 1 THEN c.id END) AS repeat_customers,
                COUNT(DISTINCT c.id) AS total_customers,
                ROUND(CAST(COUNT(DISTINCT CASE WHEN order_count > 1 THEN c.id END) * 100.0 / 
                    COUNT(DISTINCT c.id) AS numeric), 2) AS repeat_purchase_rate
            FROM order_orders o
            JOIN order_customers c ON o.customer_id = c.id
            JOIN (
                SELECT customer_id, COUNT(*) AS order_count
                FROM order_orders
                GROUP BY customer_id
            ) AS customer_orders ON c.id = customer_orders.customer_id
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "What is the distribution of shipping address types?",
        "sql_query": """
            SELECT 
                CASE 
                    WHEN sa.company IS NOT NULL THEN 'Business'
                    WHEN sa.address2 IS NOT NULL THEN 'Complex'
                    ELSE 'Residential'
                END AS address_type,
                COUNT(DISTINCT o.id) AS order_count,
                SUM(o.total_price) AS total_revenue,
                ROUND(CAST(AVG(o.total_price) AS numeric), 2) AS avg_order_value
            FROM order_orders o
            JOIN order_shippingaddress sa ON o.id = sa.order_id
            GROUP BY address_type
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "What is the customer verification status distribution?",
        "sql_query": """
            SELECT 
                c.verified_email,
                COUNT(DISTINCT c.id) AS customer_count,
                COUNT(DISTINCT o.id) AS order_count,
                SUM(o.total_price) AS total_revenue
            FROM order_customers c
            LEFT JOIN order_orders o ON c.id = o.customer_id
            GROUP BY c.verified_email
            ORDER BY customer_count DESC;
        """,
    },
    {
        "question": "What is the distribution of customer tags?",
        "sql_query": """
            SELECT 
                tag,
                COUNT(DISTINCT c.id) AS customer_count,
                COUNT(DISTINCT o.id) AS order_count,
                SUM(o.total_price) AS total_revenue
            FROM order_customers c
            CROSS JOIN UNNEST(c.tags) AS tag
            LEFT JOIN order_orders o ON c.id = o.customer_id
            GROUP BY tag
            ORDER BY customer_count DESC;
        """,
    },
    {
        "question": "What is the average time between order creation and delivery?",
        "sql_query": """
            SELECT 
                sa.city,
                ROUND(CAST(AVG(EXTRACT(EPOCH FROM (oli.delivered_at - o.source_created_at))/86400) AS numeric), 2) AS avg_delivery_days,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_orders o
            JOIN order_lineitems oli ON o.id = oli.order_id
            JOIN order_shippingaddress sa ON o.id = sa.order_id
            WHERE oli.delivered_at IS NOT NULL
            GROUP BY sa.city
            HAVING COUNT(DISTINCT o.id) > 10
            ORDER BY avg_delivery_days;
        """,
    },
    {
        "question": "What is the distribution of customer spend tiers?",
        "sql_query": """
            SELECT 
                c."predictedSpendTier",
                COUNT(DISTINCT c.id) AS customer_count,
                COUNT(DISTINCT o.id) AS order_count,
                SUM(o.total_price) AS total_revenue,
                ROUND(CAST(AVG(o.total_price) AS numeric), 2) AS avg_order_value
            FROM order_customers c
            LEFT JOIN order_orders o ON c.id = o.customer_id
            WHERE c."predictedSpendTier" IS NOT NULL
            GROUP BY c."predictedSpendTier"
            ORDER BY customer_count DESC;
        """,
    },
    {
        "question": "What is the shipping cost distribution by region?",
        "sql_query": """
            SELECT 
                sa.country,
                sa.province,
                ROUND(CAST(AVG(o.shipping_charge) AS numeric), 2) AS avg_shipping_cost,
                ROUND(CAST(AVG(o.total_price) AS numeric), 2) AS avg_order_value,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_orders o
            JOIN order_shippingaddress sa ON o.id = sa.order_id
            GROUP BY sa.country, sa.province
            HAVING COUNT(DISTINCT o.id) > 10
            ORDER BY avg_shipping_cost DESC;
        """,
    },
    {
        "question": "What is the trend of average order value by customer state?",
        "sql_query": """
            SELECT 
                c.state,
                DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC') AS month,
                ROUND(CAST(AVG(o.total_price) AS numeric), 2) AS avg_order_value,
                COUNT(DISTINCT o.id) AS order_count
            FROM order_customers c
            JOIN order_orders o ON c.id = o.customer_id
            WHERE c.state IS NOT NULL
            GROUP BY c.state, month
            ORDER BY c.state, month DESC;
        """,
    },
    {
        "question": "What is the completeness of shipping addresses?",
        "sql_query": """
            SELECT 
                CASE 
                    WHEN sa.address1 IS NULL THEN 'Missing Address'
                    WHEN sa.city IS NULL THEN 'Missing City'
                    WHEN sa.province IS NULL THEN 'Missing Province'
                    WHEN sa.country IS NULL THEN 'Missing Country'
                    WHEN sa.zip IS NULL THEN 'Missing ZIP'
                    ELSE 'Complete'
                END AS address_status,
                COUNT(DISTINCT o.id) AS order_count,
                SUM(o.total_price) AS total_revenue
            FROM order_orders o
            JOIN order_shippingaddress sa ON o.id = sa.order_id
            GROUP BY address_status
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Show basic order information with customer details",
        "sql_query": """
            SELECT 
                o.id AS order_id,
                o.source_created_at AT TIME ZONE 'UTC' AS order_date,
                o.total_price,
                o.status,
                c.first_name,
                c.last_name,
                c.email
            FROM order_orders o
            LEFT JOIN order_customers c ON o.customer_id = c.id
            WHERE o.source_created_at IS NOT NULL
            LIMIT 5;
        """,
    },
    {
        "question": "Show order items with product details",
        "sql_query": """
            SELECT 
                oli.id AS line_item_id,
                oli.quantity,
                oli.price,
                p.title AS product_title,
                pv.title AS variant_title
            FROM order_lineitems oli
            JOIN product_products p ON oli.product_id = p.source_product_id
            LEFT JOIN product_variants pv ON p.source_product_id = pv.source_product_id 
                AND oli.variant_id = pv.source_variant_id
            LIMIT 5;
        """,
    },
    {
        "question": "Show shipping address details for orders",
        "sql_query": """
            SELECT 
                o.id AS order_id,
                sa.first_name,
                sa.last_name,
                sa.address1,
                sa.city,
                sa.province,
                sa.country
            FROM order_orders o
            JOIN order_shippingaddress sa ON o.id = sa.order_id
            LIMIT 5;
        """,
    },
    {
        "question": "Show products with their categories",
        "sql_query": """
            SELECT 
                p.title AS product_title,
                pc.category_name
            FROM product_products p
            LEFT JOIN product_productcategories pc ON p.category_id = pc.id
            LIMIT 5;
        """,
    },
    {
        "question": "Show products with their variants",
        "sql_query": """
            SELECT 
                p.title AS product_title,
                pv.title AS variant_title,
                pv.price,
                pv.quantity
            FROM product_products p
            JOIN product_variants pv ON p.source_product_id = pv.source_product_id
            LIMIT 5;
        """,
    },
    {
        "question": "Show customer basic information",
        "sql_query": """
            SELECT 
                c.first_name,
                c.last_name,
                c.email,
                c.phone,
                c.state
            FROM order_customers c
            LIMIT 5;
        """,
    },
    {
        "question": "Show order status distribution",
        "sql_query": """
            SELECT 
                status,
                COUNT(*) AS order_count
            FROM order_orders
            GROUP BY status
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Show product categories distribution",
        "sql_query": """
            SELECT 
                pc.category_name,
                COUNT(DISTINCT p.id) AS product_count
            FROM product_productcategories pc
            LEFT JOIN product_products p ON pc.id = p.category_id
            GROUP BY pc.category_name
            ORDER BY product_count DESC;
        """,
    },
    {
        "question": "Show customer state distribution",
        "sql_query": """
            SELECT 
                state,
                COUNT(*) AS customer_count
            FROM order_customers
            WHERE state IS NOT NULL
            GROUP BY state
            ORDER BY customer_count DESC;
        """,
    },
    {
        "question": "Show shipping city distribution",
        "sql_query": """
            SELECT 
                city,
                COUNT(DISTINCT order_id) AS order_count
            FROM order_shippingaddress
            WHERE city IS NOT NULL
            GROUP BY city
            ORDER BY order_count DESC
            LIMIT 10;
        """,
    },
    {
        "question": "Show customer acquisition by month",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.source_created_at AT TIME ZONE 'UTC') AS month,
                COUNT(*) AS new_customers
            FROM order_customers c
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "Show customer email marketing opt-in rate by month",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.source_created_at AT TIME ZONE 'UTC') AS month,
                COUNT(CASE WHEN c.accept_email_marketing THEN 1 END) AS opted_in,
                COUNT(*) AS total_customers,
                ROUND(CAST(COUNT(CASE WHEN c.accept_email_marketing THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS opt_in_rate
            FROM order_customers c
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "Show customer SMS marketing opt-in rate by month",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', c.source_created_at AT TIME ZONE 'UTC') AS month,
                COUNT(CASE WHEN c.accept_sms_marketing THEN 1 END) AS opted_in,
                COUNT(*) AS total_customers,
                ROUND(CAST(COUNT(CASE WHEN c.accept_sms_marketing THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS opt_in_rate
            FROM order_customers c
            GROUP BY month
            ORDER BY month DESC;
        """,
    },
    {
        "question": "Show customer verification status distribution",
        "sql_query": """
            SELECT 
                verified_email,
                COUNT(*) AS customer_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_customers) AS numeric), 2) AS percentage
            FROM order_customers
            GROUP BY verified_email;
        """,
    },
    {
        "question": "Show customer tag distribution",
        "sql_query": """
            SELECT 
                UNNEST(tags) AS tag,
                COUNT(*) AS customer_count
            FROM order_customers
            GROUP BY tag
            ORDER BY customer_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "Show customer spend tier distribution",
        "sql_query": """
            SELECT 
                "predictedSpendTier",
                COUNT(*) AS customer_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_customers) AS numeric), 2) AS percentage
            FROM order_customers
            GROUP BY "predictedSpendTier"
            ORDER BY customer_count DESC;
        """,
    },
    {
        "question": "Show customer order frequency distribution",
        "sql_query": """
            SELECT 
                orders_count,
                COUNT(*) AS customer_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_customers) AS numeric), 2) AS percentage
            FROM order_customers
            GROUP BY orders_count
            ORDER BY orders_count;
        """,
    },
    {
        "question": "Show customer total spend distribution",
        "sql_query": """
            SELECT 
                CASE 
                    WHEN total_spent <= 100 THEN '0-100'
                    WHEN total_spent <= 500 THEN '101-500'
                    WHEN total_spent <= 1000 THEN '501-1000'
                    WHEN total_spent <= 5000 THEN '1001-5000'
                    ELSE '5000+'
                END AS spend_range,
                COUNT(*) AS customer_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_customers) AS numeric), 2) AS percentage
            FROM order_customers
            GROUP BY spend_range
            ORDER BY MIN(total_spent);
        """,
    },
    {
        "question": "Show customer state distribution with average spend",
        "sql_query": """
            SELECT 
                state,
                COUNT(*) AS customer_count,
                ROUND(CAST(AVG(total_spent) AS numeric), 2) AS avg_spend,
                ROUND(CAST(SUM(total_spent) AS numeric), 2) AS total_spend
            FROM order_customers
            WHERE state IS NOT NULL
            GROUP BY state
            ORDER BY customer_count DESC;
        """,
    },
    {
        "question": "Show customer currency distribution",
        "sql_query": """
            SELECT 
                currency,
                COUNT(*) AS customer_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_customers) AS numeric), 2) AS percentage
            FROM order_customers
            GROUP BY currency
            ORDER BY customer_count DESC;
        """,
    },
    {
        "question": "Show order status distribution by month",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC') AS month,
                status,
                COUNT(*) AS order_count,
                ROUND(CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY DATE_TRUNC('month', o.source_created_at AT TIME ZONE 'UTC')) AS numeric), 2) AS percentage
            FROM order_orders o
            GROUP BY month, status
            ORDER BY month DESC, order_count DESC;
        """,
    },
    {
        "question": "Show order financial status distribution",
        "sql_query": """
            SELECT 
                financial_status,
                COUNT(*) AS order_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_orders) AS numeric), 2) AS percentage
            FROM order_orders
            GROUP BY financial_status
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Show order fulfillment status distribution",
        "sql_query": """
            SELECT 
                fulfillment_status,
                COUNT(*) AS order_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_orders) AS numeric), 2) AS percentage
            FROM order_orders
            GROUP BY fulfillment_status
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Show order return status distribution",
        "sql_query": """
            SELECT 
                return_status,
                COUNT(*) AS order_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_orders) AS numeric), 2) AS percentage
            FROM order_orders
            GROUP BY return_status
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Show order risk status distribution",
        "sql_query": """
            SELECT 
                risk_status,
                COUNT(*) AS order_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_orders) AS numeric), 2) AS percentage
            FROM order_orders
            GROUP BY risk_status
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Show order verification status distribution",
        "sql_query": """
            SELECT 
                verification,
                COUNT(*) AS order_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_orders) AS numeric), 2) AS percentage
            FROM order_orders
            GROUP BY verification
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Show order discount code usage",
        "sql_query": """
            SELECT 
                discount_code,
                COUNT(*) AS order_count,
                ROUND(CAST(AVG(total_discounts) AS numeric), 2) AS avg_discount,
                ROUND(CAST(SUM(total_discounts) AS numeric), 2) AS total_discounts
            FROM order_orders
            WHERE discount_code IS NOT NULL
            GROUP BY discount_code
            ORDER BY order_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "Show order shipping name analysis",
        "sql_query": """
            SELECT 
                shipping_name,
                COUNT(*) AS order_count
            FROM order_orders
            WHERE shipping_name IS NOT NULL
            GROUP BY shipping_name
            ORDER BY order_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "Show order automatic discount analysis",
        "sql_query": """
            SELECT 
                automatic_discount,
                COUNT(*) AS order_count,
                ROUND(CAST(AVG(total_discounts) AS numeric), 2) AS avg_discount,
                ROUND(CAST(SUM(total_discounts) AS numeric), 2) AS total_discounts
            FROM order_orders
            WHERE automatic_discount IS NOT NULL
            GROUP BY automatic_discount
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Show order buy X get Y analysis",
        "sql_query": """
            SELECT 
                is_bxgy,
                COUNT(*) AS order_count,
                ROUND(CAST(AVG(total_discounts) AS numeric), 2) AS avg_discount,
                ROUND(CAST(SUM(total_discounts) AS numeric), 2) AS total_discounts
            FROM order_orders
            GROUP BY is_bxgy
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Show product status distribution",
        "sql_query": """
            SELECT 
                status,
                COUNT(*) AS product_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM product_products) AS numeric), 2) AS percentage
            FROM product_products
            GROUP BY status
            ORDER BY product_count DESC;
        """,
    },
    {
        "question": "Show product type distribution",
        "sql_query": """
            SELECT 
                product_type,
                COUNT(*) AS product_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM product_products) AS numeric), 2) AS percentage
            FROM product_products
            GROUP BY product_type
            ORDER BY product_count DESC;
        """,
    },
    {
        "question": "Show product launch date analysis",
        "sql_query": """
            SELECT 
                DATE_TRUNC('month', launch_date AT TIME ZONE 'UTC') AS launch_month,
                COUNT(*) AS product_count
            FROM product_products
            WHERE launch_date IS NOT NULL
            GROUP BY launch_month
            ORDER BY launch_month DESC;
        """,
    },
    {
        "question": "Show product quantity limit analysis",
        "sql_query": """
            SELECT 
                quantity_limit,
                COUNT(*) AS product_count
            FROM product_products
            WHERE quantity_limit IS NOT NULL
            GROUP BY quantity_limit
            ORDER BY quantity_limit;
        """,
    },
    {
        "question": "Show product quantity limit expiry analysis",
        "sql_query": """
            SELECT 
                quantity_limit_expiry_hours,
                COUNT(*) AS product_count
            FROM product_products
            WHERE quantity_limit_expiry_hours IS NOT NULL
            GROUP BY quantity_limit_expiry_hours
            ORDER BY quantity_limit_expiry_hours;
        """,
    },
    {
        "question": "Show variant option1 distribution",
        "sql_query": """
            SELECT 
                option1,
                COUNT(*) AS variant_count
            FROM product_variants
            WHERE option1 IS NOT NULL
            GROUP BY option1
            ORDER BY variant_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "Show variant option2 distribution",
        "sql_query": """
            SELECT 
                option2,
                COUNT(*) AS variant_count
            FROM product_variants
            WHERE option2 IS NOT NULL
            GROUP BY option2
            ORDER BY variant_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "Show variant option3 distribution",
        "sql_query": """
            SELECT 
                option3,
                COUNT(*) AS variant_count
            FROM product_variants
            WHERE option3 IS NOT NULL
            GROUP BY option3
            ORDER BY variant_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "Show variant barcode coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN barcode IS NOT NULL THEN 1 END) AS with_barcode,
                COUNT(*) AS total_variants,
                ROUND(CAST(COUNT(CASE WHEN barcode IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM product_variants;
        """,
    },
    {
        "question": "Show variant SKU coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN sku IS NOT NULL THEN 1 END) AS with_sku,
                COUNT(*) AS total_variants,
                ROUND(CAST(COUNT(CASE WHEN sku IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM product_variants;
        """,
    },
    {
        "question": "Show variant weight unit distribution",
        "sql_query": """
            SELECT 
                weight_unit,
                COUNT(*) AS variant_count
            FROM product_variants
            WHERE weight_unit IS NOT NULL
            GROUP BY weight_unit
            ORDER BY variant_count DESC;
        """,
    },
    {
        "question": "Show variant weight distribution",
        "sql_query": """
            SELECT 
                CASE 
                    WHEN weight <= 100 THEN '0-100'
                    WHEN weight <= 500 THEN '101-500'
                    WHEN weight <= 1000 THEN '501-1000'
                    WHEN weight <= 5000 THEN '1001-5000'
                    ELSE '5000+'
                END AS weight_range,
                COUNT(*) AS variant_count
            FROM product_variants
            GROUP BY weight_range
            ORDER BY MIN(weight);
        """,
    },
    {
        "question": "Show variant fulfillment service distribution",
        "sql_query": """
            SELECT 
                fulfillment_service,
                COUNT(*) AS variant_count
            FROM product_variants
            WHERE fulfillment_service IS NOT NULL
            GROUP BY fulfillment_service
            ORDER BY variant_count DESC;
        """,
    },
    {
        "question": "Show variant inventory management status",
        "sql_query": """
            SELECT 
                inventory_management,
                COUNT(*) AS variant_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM product_variants) AS numeric), 2) AS percentage
            FROM product_variants
            GROUP BY inventory_management
            ORDER BY variant_count DESC;
        """,
    },
    {
        "question": "Show variant taxable status",
        "sql_query": """
            SELECT 
                taxable,
                COUNT(*) AS variant_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM product_variants) AS numeric), 2) AS percentage
            FROM product_variants
            GROUP BY taxable
            ORDER BY variant_count DESC;
        """,
    },
    {
        "question": "Show shipping country distribution",
        "sql_query": """
            SELECT 
                country,
                COUNT(DISTINCT order_id) AS order_count,
                ROUND(CAST(COUNT(DISTINCT order_id) * 100.0 / (SELECT COUNT(*) FROM order_orders) AS numeric), 2) AS percentage
            FROM order_shippingaddress
            GROUP BY country
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Show shipping province distribution",
        "sql_query": """
            SELECT 
                province,
                COUNT(DISTINCT order_id) AS order_count,
                ROUND(CAST(COUNT(DISTINCT order_id) * 100.0 / (SELECT COUNT(*) FROM order_orders) AS numeric), 2) AS percentage
            FROM order_shippingaddress
            GROUP BY province
            ORDER BY order_count DESC;
        """,
    },
    {
        "question": "Show shipping city distribution",
        "sql_query": """
            SELECT 
                city,
                COUNT(DISTINCT order_id) AS order_count,
                ROUND(CAST(COUNT(DISTINCT order_id) * 100.0 / (SELECT COUNT(*) FROM order_orders) AS numeric), 2) AS percentage
            FROM order_shippingaddress
            GROUP BY city
            ORDER BY order_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "Show shipping company distribution",
        "sql_query": """
            SELECT 
                company,
                COUNT(DISTINCT order_id) AS order_count
            FROM order_shippingaddress
            WHERE company IS NOT NULL
            GROUP BY company
            ORDER BY order_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "Show shipping phone coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN phone IS NOT NULL THEN 1 END) AS with_phone,
                COUNT(*) AS total_addresses,
                ROUND(CAST(COUNT(CASE WHEN phone IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM order_shippingaddress;
        """,
    },
    {
        "question": "Show shipping secondary phone coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN secondary_phone IS NOT NULL THEN 1 END) AS with_secondary_phone,
                COUNT(*) AS total_addresses,
                ROUND(CAST(COUNT(CASE WHEN secondary_phone IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM order_shippingaddress;
        """,
    },
    {
        "question": "Show shipping address completeness",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN address1 IS NOT NULL AND city IS NOT NULL AND province IS NOT NULL AND country IS NOT NULL THEN 1 END) AS complete_addresses,
                COUNT(*) AS total_addresses,
                ROUND(CAST(COUNT(CASE WHEN address1 IS NOT NULL AND city IS NOT NULL AND province IS NOT NULL AND country IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS completeness_percentage
            FROM order_shippingaddress;
        """,
    },
    {
        "question": "Show shipping address type distribution",
        "sql_query": """
            SELECT 
                CASE 
                    WHEN company IS NOT NULL THEN 'Business'
                    ELSE 'Residential'
                END AS address_type,
                COUNT(*) AS address_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_shippingaddress) AS numeric), 2) AS percentage
            FROM order_shippingaddress
            GROUP BY address_type
            ORDER BY address_count DESC;
        """,
    },
    {
        "question": "Show shipping recommended city coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN recommended_city IS NOT NULL THEN 1 END) AS with_recommended_city,
                COUNT(*) AS total_addresses,
                ROUND(CAST(COUNT(CASE WHEN recommended_city IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM order_shippingaddress;
        """,
    },
    {
        "question": "Show shipping MS city coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN ms_city IS NOT NULL THEN 1 END) AS with_ms_city,
                COUNT(*) AS total_addresses,
                ROUND(CAST(COUNT(CASE WHEN ms_city IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM order_shippingaddress;
        """,
    },
    {
        "question": "Show line item quantity distribution",
        "sql_query": """
            SELECT 
                CASE 
                    WHEN quantity <= 1 THEN '1'
                    WHEN quantity <= 2 THEN '2'
                    WHEN quantity <= 5 THEN '3-5'
                    WHEN quantity <= 10 THEN '6-10'
                    ELSE '10+'
                END AS quantity_range,
                COUNT(*) AS line_item_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_lineitems) AS numeric), 2) AS percentage
            FROM order_lineitems
            GROUP BY quantity_range
            ORDER BY MIN(quantity);
        """,
    },
    {
        "question": "Show line item price distribution",
        "sql_query": """
            SELECT 
                CASE 
                    WHEN price <= 10 THEN '0-10'
                    WHEN price <= 50 THEN '11-50'
                    WHEN price <= 100 THEN '51-100'
                    WHEN price <= 500 THEN '101-500'
                    ELSE '500+'
                END AS price_range,
                COUNT(*) AS line_item_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_lineitems) AS numeric), 2) AS percentage
            FROM order_lineitems
            GROUP BY price_range
            ORDER BY MIN(price);
        """,
    },
    {
        "question": "Show line item compare at price coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN compare_at_price IS NOT NULL THEN 1 END) AS with_compare_price,
                COUNT(*) AS total_line_items,
                ROUND(CAST(COUNT(CASE WHEN compare_at_price IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM order_lineitems;
        """,
    },
    {
        "question": "Show line item SKU coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN sku IS NOT NULL THEN 1 END) AS with_sku,
                COUNT(*) AS total_line_items,
                ROUND(CAST(COUNT(CASE WHEN sku IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM order_lineitems;
        """,
    },
    {
        "question": "Show line item barcode coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN barcode IS NOT NULL THEN 1 END) AS with_barcode,
                COUNT(*) AS total_line_items,
                ROUND(CAST(COUNT(CASE WHEN barcode IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM order_lineitems;
        """,
    },
    {
        "question": "Show line item vendor distribution",
        "sql_query": """
            SELECT 
                vendor,
                COUNT(*) AS line_item_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_lineitems) AS numeric), 2) AS percentage
            FROM order_lineitems
            WHERE vendor IS NOT NULL
            GROUP BY vendor
            ORDER BY line_item_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "Show line item fulfillment service distribution",
        "sql_query": """
            SELECT 
                fulfillment_service,
                COUNT(*) AS line_item_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_lineitems) AS numeric), 2) AS percentage
            FROM order_lineitems
            WHERE fulfillment_service IS NOT NULL
            GROUP BY fulfillment_service
            ORDER BY line_item_count DESC;
        """,
    },
    {
        "question": "Show line item product exists status",
        "sql_query": """
            SELECT 
                product_exists,
                COUNT(*) AS line_item_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_lineitems) AS numeric), 2) AS percentage
            FROM order_lineitems
            GROUP BY product_exists
            ORDER BY line_item_count DESC;
        """,
    },
    {
        "question": "Show line item requires shipping status",
        "sql_query": """
            SELECT 
                requires_shipping,
                COUNT(*) AS line_item_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_lineitems) AS numeric), 2) AS percentage
            FROM order_lineitems
            GROUP BY requires_shipping
            ORDER BY line_item_count DESC;
        """,
    },
    {
        "question": "Show line item fulfillable quantity distribution",
        "sql_query": """
            SELECT 
                CASE 
                    WHEN fulfillable_quantity <= 1 THEN '1'
                    WHEN fulfillable_quantity <= 2 THEN '2'
                    WHEN fulfillable_quantity <= 5 THEN '3-5'
                    WHEN fulfillable_quantity <= 10 THEN '6-10'
                    ELSE '10+'
                END AS quantity_range,
                COUNT(*) AS line_item_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_lineitems) AS numeric), 2) AS percentage
            FROM order_lineitems
            GROUP BY quantity_range
            ORDER BY MIN(fulfillable_quantity);
        """,
    },
    {
        "question": "Show collection type distribution",
        "sql_query": """
            SELECT 
                is_smart,
                COUNT(*) AS collection_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM product_collections) AS numeric), 2) AS percentage
            FROM product_collections
            GROUP BY is_smart
            ORDER BY collection_count DESC;
        """,
    },
    {
        "question": "Show collection publication count distribution",
        "sql_query": """
            SELECT 
                publication_count,
                COUNT(*) AS collection_count
            FROM product_collections
            GROUP BY publication_count
            ORDER BY publication_count;
        """,
    },
    {
        "question": "Show collection sort order distribution",
        "sql_query": """
            SELECT 
                sort_order,
                COUNT(*) AS collection_count
            FROM product_collections
            WHERE sort_order IS NOT NULL
            GROUP BY sort_order
            ORDER BY collection_count DESC;
        """,
    },
    {
        "question": "Show collection SEO title coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN seo_title IS NOT NULL THEN 1 END) AS with_seo_title,
                COUNT(*) AS total_collections,
                ROUND(CAST(COUNT(CASE WHEN seo_title IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM product_collections;
        """,
    },
    {
        "question": "Show collection SEO handle coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN seo_handle IS NOT NULL THEN 1 END) AS with_seo_handle,
                COUNT(*) AS total_collections,
                ROUND(CAST(COUNT(CASE WHEN seo_handle IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM product_collections;
        """,
    },
    {
        "question": "Show collection SEO description coverage",
        "sql_query": """
            SELECT 
                COUNT(CASE WHEN seo_description IS NOT NULL THEN 1 END) AS with_seo_description,
                COUNT(*) AS total_collections,
                ROUND(CAST(COUNT(CASE WHEN seo_description IS NOT NULL THEN 1 END) * 100.0 / COUNT(*) AS numeric), 2) AS coverage_percentage
            FROM product_collections;
        """,
    },
    {
        "question": "Show collection sub vendor distribution",
        "sql_query": """
            SELECT 
                sub_vendor,
                COUNT(*) AS collection_count
            FROM product_collections
            WHERE sub_vendor IS NOT NULL
            GROUP BY sub_vendor
            ORDER BY collection_count DESC;
        """,
    },
    {
        "question": "Show collection condition criteria distribution",
        "sql_query": """
            SELECT 
                condition_criteria,
                COUNT(*) AS collection_count
            FROM product_collections
            WHERE condition_criteria IS NOT NULL
            GROUP BY condition_criteria
            ORDER BY collection_count DESC;
        """,
    },
    {
        "question": "Show collection sorting1 distribution",
        "sql_query": """
            SELECT 
                sorting1,
                COUNT(*) AS collection_count
            FROM product_collections
            WHERE sorting1 IS NOT NULL
            GROUP BY sorting1
            ORDER BY collection_count DESC;
        """,
    },
    {
        "question": "Show collection sorting2 distribution",
        "sql_query": """
            SELECT 
                sorting2,
                COUNT(*) AS collection_count
            FROM product_collections
            WHERE sorting2 IS NOT NULL
            GROUP BY sorting2
            ORDER BY collection_count DESC;
        """,
    },
    {
        "question": "Show category name distribution",
        "sql_query": """
            SELECT 
                category_name,
                COUNT(*) AS category_count
            FROM product_productcategories
            GROUP BY category_name
            ORDER BY category_count DESC;
        """,
    },
    {
        "question": "Show category source ID distribution",
        "sql_query": """
            SELECT 
                source_category_id,
                COUNT(*) AS category_count
            FROM product_productcategories
            WHERE source_category_id IS NOT NULL
            GROUP BY source_category_id
            ORDER BY category_count DESC;
        """,
    },
    {
        "question": "Show category client distribution",
        "sql_query": """
            SELECT 
                client_id,
                COUNT(*) AS category_count
            FROM product_productcategories
            WHERE client_id IS NOT NULL
            GROUP BY client_id
            ORDER BY category_count DESC;
        """,
    },
    {
        "question": "Show tag name distribution",
        "sql_query": """
            SELECT 
                name,
                COUNT(*) AS tag_count
            FROM product_tags
            GROUP BY name
            ORDER BY tag_count DESC;
        """,
    },
    {
        "question": "Show tag client distribution",
        "sql_query": """
            SELECT 
                client_id,
                COUNT(*) AS tag_count
            FROM product_tags
            GROUP BY client_id
            ORDER BY tag_count DESC;
        """,
    },
    {
        "question": "Show vendor name distribution",
        "sql_query": """
            SELECT 
                name,
                COUNT(*) AS vendor_count
            FROM product_vendor
            GROUP BY name
            ORDER BY vendor_count DESC;
        """,
    },
    {
        "question": "Show vendor client distribution",
        "sql_query": """
            SELECT 
                client_id,
                COUNT(*) AS vendor_count
            FROM product_vendor
            GROUP BY client_id
            ORDER BY vendor_count DESC;
        """,
    },
]
