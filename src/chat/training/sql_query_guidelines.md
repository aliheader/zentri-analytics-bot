# SQL Query Generation Guidelines for E-commerce Data Analysis

## 1. Schema Overview

### Core Tables and Relationships
The database consists of several interconnected tables that store e-commerce data. The main tables are:
- Orders table: Contains all order information
- Customers table: Stores customer details
- Line items table: Contains individual items in orders
- Shipping address table: Stores delivery information
- Products table: Contains product information
- Variants table: Contains Product Variants
- Categories table: Contains product categorization
- For analysis on inventory, refer to variants table.

### Key Relationships
The tables are connected through specific fields:
- Orders are linked to customers through a customer_id
- Orders are linked to shipping addresses through an order_id
- Line items are connected to orders through an order_id
- Use LineItems.product_id and Products.source_product_id, to join line_items and products
- Use LineItems.variant_id and Products.source_variant_id, to join line_items and variants
- Variants are associated with Products through product_id.
- Query Sample for Product and LineItem Joins
    SELECT 
    p.title, 
    SUM(oli.quantity) AS total_quantity_sold
    FROM 
    public.order_lineitems oli
    INNER JOIN public.order_orders oo ON oli.order_id = oo.id
    INNER JOIN public.product_products p ON oli.product_id = p.source_product_id
    GROUP BY 
    p.title
    ORDER BY 
    total_quantity_sold DESC
    LIMIT 10;

## 2. Query Generation Rules

### 2.1 Table Joins
When combining data from multiple tables:
- Always specify the type of join explicitly
- Use left joins when the relationship might not exist
- Use inner joins when the relationship must exist
- Ensure proper join conditions are specified

### 2.2 Aggregation Functions
When calculating metrics:
- Use distinct counting for unique items
- Use sum for monetary values
- Use average with proper rounding for averages
- Handle null values appropriately

### 2.3 Date/Time Handling
When working with timestamps:
- Always convert timezone to UTC
- Use proper date truncation for grouping
- Handle time differences correctly
- Consider timezone in all calculations

### 2.4 Numeric Operations
When performing calculations:
- Use proper rounding with type casting
- Handle null values in calculations
- Ensure correct decimal precision
- Use appropriate numeric types

### 2.5 Ordering and limit
- Always apply limit
- Maxmimum limit is 1000
- Applying ordering in desc order.
- If user specifically asked for ordering, then apply that ordering.

## 3. Common Query Patterns

### 3.1 Customer Analysis
Typical customer analysis includes:
- Customer distribution by location
- Customer count and order frequency
- Revenue per customer
- Customer segmentation

### 3.2 Order Analysis
Common order analysis includes:
- Order volume by location
- Revenue analysis
- Average order value
- Order status distribution

### 3.3 Product Analysis
Standard product analysis includes:
- Product performance metrics
- Revenue by product
- Quantity analysis
- Product category performance

## 4. Best Practices

### 4.1 Query Structure
Follow this sequence when writing queries:
1. Start with data selection
2. Define table relationships
3. Add filtering conditions
4. Include grouping
5. Add post-aggregation filters
6. Specify result ordering

### 4.2 Performance Considerations
Consider these factors for query performance:
- Use appropriate indexes
- Limit result sets
- Optimize join conditions
- Consider query execution plan

### 4.3 Error Prevention
Prevent errors by:
- Using clear table aliases
- Checking for null values
- Using proper type casting
- Handling edge cases

## 5. Common Metrics

### 5.1 Customer Metrics
Key customer metrics include:
- Customer count
- Order frequency
- Customer lifetime value
- Repeat purchase rate

### 5.2 Order Metrics
Important order metrics include:
- Order count
- Total revenue
- Average order value
- Shipping costs

### 5.3 Product Metrics
Essential product metrics include:
- Quantity sold
- Revenue per product
- Average price
- Return rate

### 6.4 Important Considerations
Key points to remember:
- Always use UTC timezone conversion
- Use consistent time grouping
- Handle null timestamp values
- Consider timezone differences
- Use proper time difference calculations

### 6.5 Common Mistakes to Avoid
Avoid these common errors:
- Using local timestamps instead of source timestamps
- Incorrect timezone conversion
- Missing null checks
- Incorrect time difference calculations
- Ignoring timezone in comparisons

## 7. Common Pitfalls to Avoid

1. Incorrect table relationships
2. Missing null value handling
3. Improper aggregation
4. Incorrect timestamp handling
5. Missing type casting
6. Not using distinct when needed
7. Forgetting edge cases

## 8. Query Validation Checklist

1. Verify table relationships
2. Check null handling
3. Validate aggregations
4. Confirm timestamp handling
5. Test numeric operations
6. Verify result limits
7. Check indexing
8. Validate performance 

## 9. Customer Name Handling

### 9.1 Customer Name Fields
The customer table uses separate fields for name components:
- `first_name`: Customer's first name
- `last_name`: Customer's last name
- There is no single name column, names must be constructed from these fields
