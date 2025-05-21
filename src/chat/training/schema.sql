CREATE TABLE public.order_customers (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    source character varying(50) NOT NULL,
    source_created_at timestamp with time zone,
    source_updated_at timestamp with time zone,
    source_customer_id bigint,
    first_name character varying(200),
    last_name character varying(200),
    phone character varying(200),
    email character varying(254),
    state character varying(200),
    accept_email_marketing boolean,
    accept_email_marketing_at timestamp with time zone,
    accept_sms_marketing boolean,
    accept_sms_marketing_at timestamp with time zone,
    verified_email boolean,
    tags character varying(100)[],
    total_spent integer,
    orders_count integer,
    currency character varying(100),
    client_id uuid NOT NULL
);

CREATE TABLE public.order_lineitems (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    source_order_id bigint,
    title character varying(300),
    quantity double precision,
    price double precision,
    compare_at_price double precision,
    sku character varying(150),
    shopify_barcode character varying(200),
    barcode character varying(200),
    vendor character varying(200),
    fulfillment_service character varying(200),
    requires_shipping boolean,
    product_exists boolean,
    fulfillable_quantity integer,
    grams double precision,
    total_discounts numeric(10,2),
    fulfillment_status character varying(200),
    tax double precision,
    tax_percentage double precision,
    description character varying(150),
    product_type character varying(200),
    tags character varying(100)[],
    variant_title character varying(200),
    collections character varying(100)[],
    cost_price double precision,
    category character varying(200),
    shipping_charge double precision,
    status character varying(50) NOT NULL,
    delivered_at timestamp with time zone,
    display_status character varying(50),
    return_reason text,
    returned_at timestamp with time zone,
    cancelled_at timestamp with time zone,
    order_id uuid NOT NULL
);


CREATE TABLE public.order_orders (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    source_id bigint,
    source character varying(50) NOT NULL,
    email character varying(150),
    source_created_at timestamp with time zone,
    source_updated_at timestamp with time zone NOT NULL,
    total_price double precision,
    subtotal_price double precision,
    price_conversion_rate double precision,
    checkout_price double precision,
    total_weight double precision,
    shipping_charge double precision,
    currency character varying(100),
    total_discounts double precision,
    name character varying(255),
    cancel_reason character varying(255),
    tags character varying(2000)[],
    status character varying(200),
    financial_status character varying(100),
    fulfillment_status character varying(100),
    discount_code character varying(150),
    shipping_name character varying(5000),
    source_customer_id bigint,
    automatic_discount character varying(200),
    total_tax double precision,
    donation_amount double precision,
    store_id character varying(255),
    gift_card_transaction_number character varying(200),
    gift_card_discount double precision,
    total_refunded double precision,
    cart_discount double precision,
    cancelled_at timestamp with time zone,
    client_id uuid NOT NULL,
    customer_id uuid
);


CREATE TABLE public.order_shippingaddress (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    source_order_id character varying(300),
    country character varying(300),
    phone character varying(300),
    secondary_phone character varying(300),
    company character varying(300),
    first_name character varying(300),
    last_name character varying(300),
    address1 character varying(300),
    address2 character varying(300),
    city character varying(300),
    province character varying(300),
    zip character varying(300),
    country_code character varying(300),
    name character varying(300),
    recommended_city character varying(300),
    ms_city character varying(300),
    customer_cnic character varying(50),
    latitude double precision,
    longitude double precision,
    order_id uuid NOT NULL
);


CREATE TABLE public.product_collections (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    source_created_at timestamp with time zone,
    source_updated_at timestamp with time zone,
    source character varying(50) NOT NULL,
    source_collection_id bigint,
    collection_id bigint,
    title character varying(200),
    description text,
    is_smart boolean,
    image text,
    handle character varying,
    publication_count integer,
    sort_order character varying(200),
    sub_vendor character varying(100),
    client_id uuid NOT NULL
);

CREATE TABLE public.product_options (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    name character varying(200),
    value character varying(200),
    product_id uuid NOT NULL
);

CREATE TABLE public.product_productcategories (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    category_name character varying(300),
    source_category_id character varying(100),
    client_id uuid
);


CREATE TABLE public.product_productcollections (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    source_product_id bigint,
    source_collection_id bigint,
    collection_id uuid NOT NULL,
    product_id uuid NOT NULL
);


CREATE TABLE public.product_products (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    source_created_at timestamp with time zone,
    source_updated_at timestamp with time zone,
    source character varying(50) NOT NULL,
    sub_vendor character varying(100),
    brand character varying(100),
    product_type character varying(100),
    title character varying(500),
    display_name character varying(500),
    description text,
    source_product_id bigint,=
    handle character varying(100),
    parent_sku character varying(100),
    tags text,
    category_id uuid,
    client_id uuid NOT NULL,
    vendor_id uuid NOT NULL
);


CREATE TABLE public.product_producttags (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    product_id uuid NOT NULL,
    tag_id uuid NOT NULL
);

CREATE TABLE public.product_tags (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    name character varying(255) NOT NULL,
    client_id uuid NOT NULL,
);

CREATE TABLE public.product_variants (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    source_created_at timestamp with time zone,
    source_updated_at timestamp with time zone,
    source character varying(50) NOT NULL,
    source_variant_id bigint,
    title character varying(200),
    source_product_id bigint,
    option1 character varying(200),
    option2 character varying(200),
    option3 character varying(200),
    barcode character varying(200),
    sku character varying(200),
    weight_unit character varying(200),
    weight double precision NOT NULL,
    quantity integer NOT NULL,
    price double precision,
    compare_at_price double precision,
    image character varying(200),
    client_id uuid NOT NULL,
    product_id uuid
);

CREATE TABLE public.product_vendor (
    id uuid NOT NULL,
    is_deleted boolean NOT NULL,
    name character varying(255),
    client_id uuid NOT NULL
);


ALTER TABLE ONLY public.order_orders
    ADD CONSTRAINT order_orders_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.order_orders
    ADD CONSTRAINT order_orders_source_id_key UNIQUE (source_id);



ALTER TABLE ONLY public.order_orders
    ADD CONSTRAINT order_orders_source_source_id_14244ff2_uniq UNIQUE (source, source_id);

ALTER TABLE ONLY public.order_billingaddress
    ADD CONSTRAINT order_billingaddress_order_id_b8273c33_fk_order_orders_id FOREIGN KEY (order_id) REFERENCES public.order_orders(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.order_orders
    ADD CONSTRAINT order_orders_customer_id_b0b78213_fk_order_customers_id FOREIGN KEY (customer_id) REFERENCES public.order_customers(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.order_shippingaddress
    ADD CONSTRAINT order_shippingaddress_order_id_2030a3eb_fk_order_orders_id FOREIGN KEY (order_id) REFERENCES public.order_orders(id) DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE ONLY public.product_collections
ADD CONSTRAINT product_collections_client_id_source_collect_adcf632d_uniq UNIQUE (
    client_id,
    source_collection_id,
    collection_id
);


ALTER TABLE ONLY public.product_collections
ADD CONSTRAINT product_collections_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.product_options
ADD CONSTRAINT product_options_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.product_productcategories
ADD CONSTRAINT product_productcategories_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.product_productcollections
ADD CONSTRAINT product_productcollectio_product_id_collection_id_bb0ecfcf_uniq UNIQUE (product_id, collection_id);

ALTER TABLE ONLY public.product_productcollections
ADD CONSTRAINT product_productcollections_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.product_productimages
ADD CONSTRAINT product_productimages_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.product_products
ADD CONSTRAINT product_products_client_id_source_product_id_f972c4ea_uniq UNIQUE (client_id, source_product_id);


ALTER TABLE ONLY public.product_products
ADD CONSTRAINT product_products_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.product_productstatusenums
ADD CONSTRAINT product_productstatusenums_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.product_producttags
ADD CONSTRAINT product_producttags_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.product_producttags
ADD CONSTRAINT product_producttags_product_id_tag_id_b91ab13d_uniq UNIQUE (product_id, tag_id);


ALTER TABLE ONLY public.product_tags
ADD CONSTRAINT product_tags_name_client_id_1bc0102a_uniq UNIQUE (name, client_id);


ALTER TABLE ONLY public.product_tags
ADD CONSTRAINT product_tags_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.product_variants
ADD CONSTRAINT product_variants_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.product_variants
ADD CONSTRAINT product_variants_product_id_source_variant_id_04a1a165_uniq UNIQUE (product_id, source_variant_id);


ALTER TABLE ONLY public.product_vendor
ADD CONSTRAINT product_vendor_client_id_name_42d846ac_uniq UNIQUE (client_id, name);


ALTER TABLE ONLY public.product_vendor
ADD CONSTRAINT product_vendor_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.product_collections
ADD CONSTRAINT product_collections_client_id_3f576ca8_fk_client_client_id FOREIGN KEY (client_id) REFERENCES public.client_client (id) DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE ONLY public.product_options
ADD CONSTRAINT product_options_product_id_5452622a_fk_product_products_id FOREIGN KEY (product_id) REFERENCES public.product_products (id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.product_productcategories
ADD CONSTRAINT product_productcateg_client_id_c6527226_fk_client_cl FOREIGN KEY (client_id) REFERENCES public.client_client (id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.product_productcollections
ADD CONSTRAINT product_productcolle_collection_id_fbaad429_fk_product_c FOREIGN KEY (collection_id) REFERENCES public.product_collections (id) DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE ONLY public.product_productcollections
ADD CONSTRAINT product_productcolle_product_id_9b04ef42_fk_product_p FOREIGN KEY (product_id) REFERENCES public.product_products (id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.product_productimages
ADD CONSTRAINT product_productimage_product_id_03f02217_fk_product_p FOREIGN KEY (product_id) REFERENCES public.product_products (id) DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE ONLY public.product_products
ADD CONSTRAINT product_products_category_id_82802e2d_fk_product_p FOREIGN KEY (category_id) REFERENCES public.product_productcategories (id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.product_products
ADD CONSTRAINT product_products_client_id_ecfc9e45_fk_client_client_id FOREIGN KEY (client_id) REFERENCES public.client_client (id) DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE ONLY public.product_products
ADD CONSTRAINT product_products_vendor_id_c3779557_fk_product_vendor_id FOREIGN KEY (vendor_id) REFERENCES public.product_vendor (id) DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE ONLY public.product_producttags
ADD CONSTRAINT product_producttags_product_id_d5917d9a_fk_product_products_id FOREIGN KEY (product_id) REFERENCES public.product_products (id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.product_producttags
ADD CONSTRAINT product_producttags_tag_id_495dfd95_fk_product_tags_id FOREIGN KEY (tag_id) REFERENCES public.product_tags (id) DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE ONLY public.product_tags
ADD CONSTRAINT product_tags_client_id_e81eadf8_fk_client_client_id FOREIGN KEY (client_id) REFERENCES public.client_client (id) DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE ONLY public.product_variants
ADD CONSTRAINT product_variants_client_id_b312c6df_fk_client_client_id FOREIGN KEY (client_id) REFERENCES public.client_client (id) DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE ONLY public.product_variants
ADD CONSTRAINT product_variants_product_id_019d9f04_fk_product_products_id FOREIGN KEY (product_id) REFERENCES public.product_products (id) DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE ONLY public.product_vendor
ADD CONSTRAINT product_vendor_client_id_4d4e22ed_fk_client_client_id FOREIGN KEY (client_id) REFERENCES public.client_client (id) DEFERRABLE INITIALLY DEFERRED;
