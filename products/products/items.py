# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    menu_name = scrapy.Field()
    category_name = scrapy.Field()
    subcategory_name = scrapy.Field()
    in_store = scrapy.Field()
    gpc_product_id = scrapy.Field()
    sku = scrapy.Field()
    site_type_id = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    upc = scrapy.Field()
    unique_attrs = scrapy.Field()
    inventory_last_seen_at = scrapy.Field()
    orig_thumbnail_url = scrapy.Field()
    s3_thumbnail_url = scrapy.Field()
    orig_hero_url = scrapy.Field()
    s3_hero_url = scrapy.Field()
    orig_image_misc_url = scrapy.Field()
    s3_image_misc_url = scrapy.Field()
    brand = scrapy.Field()
    external_product_id = scrapy.Field()
    grocery_attrs = scrapy.Field()
    store_appearance = scrapy.Field()
    price = scrapy.Field()
    price_unit = scrapy.Field()
    category_path = scrapy.Field()
    gender = scrapy.Field()

