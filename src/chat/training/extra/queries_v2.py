questions = [
    # Top selling products by revenue
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
    # Product variant performance
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
    # Product category revenue
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
    # Product return analysis
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
    # Product inventory analysis
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
    # Product price analysis
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
    # Product variant price analysis
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
    # Product collection performance
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
    # Product vendor performance
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
    # Product discount analysis
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
    # Product seasonal performance
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
    # Product variant availability
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
    # Product category growth
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
    # Product bundle analysis
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
    # Product price elasticity
    {
        "question": "What is the price elasticity of products?",
        "sql_query": """
            WITH price_changes AS (
                SELECT 
                    p.id,
                    p.title,
                    oli.price,
                    oli.created_at,
                    LAG(oli.price) OVER (PARTITION BY p.id ORDER BY oli.created_at) AS prev_price,
                    SUM(oli.quantity) AS quantity_sold
                FROM product_products p
                JOIN order_lineitems oli ON p.source_product_id = oli.product_id
                GROUP BY p.id, p.title, oli.price, oli.created_at
            )
            SELECT 
                title,
                AVG((quantity_sold - LAG(quantity_sold) OVER (PARTITION BY id ORDER BY created_at)) * 100.0 / 
                    NULLIF(LAG(quantity_sold) OVER (PARTITION BY id ORDER BY created_at), 0) /
                    (price - prev_price) * 100.0 / NULLIF(prev_price, 0)) AS avg_price_elasticity
            FROM price_changes
            WHERE prev_price IS NOT NULL
            GROUP BY title
            ORDER BY avg_price_elasticity;
        """,
    },
    # Product collection effectiveness
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
    # Product vendor performance trend
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
    # Product return reason analysis
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
    # Product shipping analysis
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
    # Product tax analysis
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
    # Product discount effectiveness
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
    # Product fulfillment analysis
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
    # Product weight analysis
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
    # Product barcode analysis
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
    # Product vendor category analysis
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
    # Product tag effectiveness
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
    # Product variant option analysis
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
    # Product cost analysis
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
    # Product warranty analysis
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
    # Shipping city analysis
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
    # Customer state analysis
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
    # Customer order frequency
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
    # Customer acquisition channel
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
    # Customer email marketing
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
    # Customer SMS marketing
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
    # Shipping province analysis
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
    # Shipping country analysis
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
    # Customer lifetime value
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
    # Customer repeat purchase rate
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
    # Shipping address analysis
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
    # Customer verification analysis
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
    # Customer tag analysis
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
    # Shipping time analysis
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
    # Customer spend tier analysis
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
    # Shipping cost analysis
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
    # Customer order value trend
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
    # Shipping address completeness
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
]
