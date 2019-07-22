/*
CREATE SEQUENCE cw_products_id_seq;

CREATE TABLE cw_products (
    id bigint NOT NULL PRIMARY KEY DEFAULT NEXTVAL('cw_products_id_seq'),
    in_store smallint,
    name varchar(500), 
    subcategory_name varchar(300),
    category_name varchar(300),
    menu_name varchar(100),
    gpc_product_id integer,
    sku varchar(100) NOT NULL,
    url varchar(1000),
    site_type_id smallint NOT NULL,
    created_at timestamp,
    updated_at timestamp,
    upc varchar(25),
    inventory_last_seen_at timestamp,
    orig_thumbnail_url varchar(700),
    s3_thumbnail_url varchar(200),
    orig_hero_url varchar(700),
    s3_hero_url varchar(200),
    orig_image_misc_url varchar(700),
    s3_image_misc_url varchar(200),
    brand varchar(100),
    external_product_id bigint,
    grocery_attrs varchar(100),
    store_appearance text[],
    price varchar(70),
    price_unit varchar(50),
    category_path varchar(1000),
    gender varchar(50),
    unique_attrs varchar(10000),
    CONSTRAINT unique_product_constraint UNIQUE (sku, site_type_id)
);
*/

CREATE TABLE cw_products (
    id bigint NOT NULL,
    in_store smallint,
    name character varying(500),
    subcategory_name character varying(300),
    category_name character varying(300),
    menu_name character varying(100),
    gpc_product_id integer,
    sku character varying NOT NULL,
    url character varying(1000),
    site_type_id smallint NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    upc character varying(25),
    unique_attrs hstore,
--    unique_attrs varchar(10000),
    inventory_last_seen_at timestamp without time zone,
    orig_thumbnail_url character varying(700),
    s3_thumbnail_url character varying(200),
    orig_hero_url character varying(700),
    s3_hero_url character varying(200),
    orig_image_misc_url character varying(700),
    s3_image_misc_url character varying(200),
    brand character varying DEFAULT ''::character varying,
    external_product_id bigint,
    grocery_attrs character varying(100),
    store_appearance integer[],
    price character varying(70),
    price_unit character varying(50),
    category_path character varying,
    gender character varying(50)
);


CREATE SEQUENCE cw_products_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE cw_products_id_seq OWNED BY cw_products.id;


ALTER TABLE ONLY cw_products ALTER COLUMN id SET DEFAULT nextval('cw_products_id_seq'::regclass);


