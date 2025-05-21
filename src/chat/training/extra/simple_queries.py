questions = [
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
        "question": "Show product vendor distribution",
        "sql_query": """
            SELECT 
                vendor,
                COUNT(*) AS product_count,
                ROUND(CAST(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM product_products) AS numeric), 2) AS percentage
            FROM product_products
            GROUP BY vendor
            ORDER BY product_count DESC;
        """,
    },
    {
        "question": "Show product tag distribution",
        "sql_query": """
            SELECT 
                UNNEST(tags) AS tag,
                COUNT(*) AS product_count
            FROM product_products
            GROUP BY tag
            ORDER BY product_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "Show product collection distribution",
        "sql_query": """
            SELECT 
                UNNEST(collections) AS collection,
                COUNT(*) AS product_count
            FROM product_products
            GROUP BY collection
            ORDER BY product_count DESC
            LIMIT 20;
        """,
    },
    {
        "question": "Show product category distribution",
        "sql_query": """
            SELECT 
                UNNEST(categories) AS category,
                COUNT(*) AS product_count
            FROM product_products
            GROUP BY category
            ORDER BY product_count DESC
            LIMIT 20;
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
        "question": "Show product addon templates distribution",
        "sql_query": """
            SELECT 
                UNNEST(addon_templates) AS addon_template,
                COUNT(*) AS product_count
            FROM product_products
            GROUP BY addon_template
            ORDER BY product_count DESC
            LIMIT 20;
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
