# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from HTMLParser import HTMLParser
import unicodedata
import logging
from twisted.enterprise import adbapi
import psycopg2
import psycopg2.extras
import logging
from scrapy.conf import settings
from scrapy.exceptions import DropItem


DELIMITER_CATEGORY_PATH = " / "

SITE_ID_TARGET_COM = 6
SITE_ID_STAPLES_COM = 7
SITE_ID_HOMEDEPOT_COM = 8
SITE_ID_BEDBATHANDBEYOND_COM = 9
SITE_ID_BARNESANDNOBLE_COM = 10
SITE_ID_PETCO_COM = 11

        
SPIDERS_UNESCAPE_NAME = ["target_com", "bedbathandbeyond_com"]

VARCHAR_COLUMNS = ["name", "subcategory_name", "category_name", "menu_name", "sku", "url", "upc", "orig_thumbnail_url",
    "s3_thumbnail_url", "orig_hero_url", "s3_hero_url", "orig_image_misc_url", "s3_image_misc_url",
    "brand", "grocery_attrs", "price", "price_unit", "category_path", "gender"
]



class PreProductsPipeline(object):
    def process_item(self, item, spider):
        return item



class UnescapeNamePipeline(object):
    htmlparser = HTMLParser()

    def process_item(self, item, spider):
        if spider.name in SPIDERS_UNESCAPE_NAME:
            name = item.get("name", None)
            
            if name:
                name_unescaped = self.htmlparser.unescape(name)

                item["name"] = name_unescaped

        return item



class TargetComPipeline(object):
    htmlparser = HTMLParser()

    def process_item(self, item, spider):
        if "target_com" == spider.name:
            # we scrape only in store records
            # which doesn't have "Not in stores" label
            item["in_store"] = 1
            item["site_type_id"] = SITE_ID_TARGET_COM

        return item


class StaplesComPipeline(object):
    def process_item(self, item, spider):
        if "staples_com" == spider.name:
            in_store = item.get("in_store", None)
            
            # if in_store is empyt - in_store=0
            if None == in_store:
                item["in_store"] = 0

            item["site_type_id"] = SITE_ID_STAPLES_COM

        return item


class HomedepotComPipeline(object):
    def process_item(self, item, spider):
        if "homedepot_com" == spider.name:
            item["site_type_id"] = SITE_ID_HOMEDEPOT_COM

        return item



class BedbathandbeyondComPipeline(object):
    htmlparser = HTMLParser()

    def process_item(self, item, spider):
        if "bedbathandbeyond_com" == spider.name:
            item["site_type_id"] = SITE_ID_BEDBATHANDBEYOND_COM

        return item


class BarnesandnobleComPipeline(object):
    def process_item(self, item, spider):
        if "barnesandnoble_com" == spider.name:
            item["site_type_id"] = SITE_ID_BARNESANDNOBLE_COM
            item["in_store"] = 1

        return item


class PetcoComPipeline(object):
    def process_item(self, item, spider):
        if "petco_com" == spider.name:
            item["site_type_id"] = SITE_ID_PETCO_COM

        return item


class PostProductsPipeline(object):
    def process_item(self, item, spider):
        url = item.get("url", None)
        price = item.get("price", None)
        name = item.get("name", None)
        sku = item.get("sku", None)
        unique_attrs = item.get("unique_attrs", None)

        if not sku:
            raise DropItem("SKU not found")

        if price:
            try:
                price_float_value = float(price)
                item["price"] = "{:.2f}".format(price_float_value)
            except Exception as e:
                item["price"] = None
                logging.warning(u"Error during price formatting {} ->  (url: {}): {}".format(price, url, e))
        
        if name:
            unicode_name = None

            if type(name) is str:
                unicode_name = unicode(name, "utf-8")
            elif type(name) is unicode:
                unicode_name = name
            
            if unicode_name:
                # remove umlauts (etc) and non ascii characters
                normalized_name = unicodedata.normalize("NFKD", unicode_name).encode("ASCII", "ignore")
                
                item["name"] = normalized_name
        

        if unique_attrs:
            hstore_values = []
            for key, value in unique_attrs.iteritems():
                hstore_value = "\"" + key + "\" => \"" + value + "\""
                hstore_values.append(hstore_value)
            
            if hstore_values:
                item["unique_attrs"] = ", ".join(hstore_values)


        """
        # add double quotes to varchar elements
        for column_name in VARCHAR_COLUMNS:
            column_value = item.get(column_name, None)

            if column_value:
                item[column_name] = "\"" + column_value + "\""
        """

        return item



class PostgreSqlPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool("psycopg2",
        host = settings["DB_HOST"],
        database = settings["DB_NAME"],
        user = settings["DB_USER"],
        password = settings["DB_PASSWD"])


    def process_item(self, item, spider):
        site_type_id = item.get("site_type_id", None)
        sku = item.get("sku", None)

        logging.debug("SQL processing item with sku={} and site_type_id={}".format(sku, site_type_id))

        query = self.dbpool.runInteraction(self.process_record, item)
        query.addErrback(self.handle_error)
        return item


    def process_record(self, cursor, item):
        site_type_id = item.get("site_type_id", None)
        sku = item.get("sku", None)

        if site_type_id and sku:
            existing_record = self._select_by_site_id_and_sku(cursor, site_type_id, sku)
            
            if existing_record:
                logging.debug("Item sku={} and site_type_id={} already exists".format(sku, site_type_id))
            
                record_id = existing_record[0]
                self._update_record(cursor, record_id, item)
            else:
                self._insert_record(cursor, item)


    def _select_by_site_id_and_sku(self, cursor, site_id, sku):
        sql = """SELECT id, in_store, name, subcategory_name, category_name, menu_name, gpc_product_id, sku,
            url, site_type_id, created_at, updated_at, upc, inventory_last_seen_at, orig_thumbnail_url,
            s3_thumbnail_url, orig_hero_url, s3_hero_url, orig_image_misc_url, s3_image_misc_url,
            brand, external_product_id, grocery_attrs, store_appearance, price, price_unit, 
            category_path, gender, unique_attrs
        FROM cw_products WHERE site_type_id = %s AND sku = %s"""
            
        cursor.execute(sql, (site_id, sku))
        result = cursor.fetchone()
        return result


    def _insert_record(self, cursor, item):
        sql_keys = []
        sql_values = []

        for key, value in item.iteritems():
            sql_keys.append(key)

            if isinstance(value, str) or isinstance(value, unicode):
                sql_values.append(value.encode("utf-8"))
            else:
                sql_values.append(value)
        
        if sql_keys and sql_values:
            sql = "INSERT INTO cw_products (created_at, " + ", ".join(sql_keys)  + ") VALUES (CURRENT_TIMESTAMP, " + ", ".join(["%s"] * len(sql_values)) + ");"

            logging.debug(u"Insert new record: {} (values: {})".format(sql, sql_values))

            cursor.execute(sql, sql_values)
            cursor.execute("commit;")


    def _update_record(self, cursor, record_id, item):
        sql_keys = []
        sql_values = []

        for key, value in item.iteritems():
            sql_keys.append(key)

            if isinstance(value, str) or isinstance(value, unicode):
                sql_values.append(value.encode("utf-8"))
            else:
                sql_values.append(value)
                
        if sql_keys and sql_values:
            sql = "UPDATE cw_products SET (inventory_last_seen_at, updated_at, " + ", ".join(sql_keys)  + ") = (CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, " + ", ".join(["%s"] * len(sql_values)) + ") WHERE id = %s;"
        
            sql_values.append(record_id)
            
            logging.debug(u"Update record: {} (values: {})".format(sql, sql_values))
            
            cursor.execute(sql, sql_values)
            cursor.execute("commit;")



    def handle_error(self, e):
        if e.check(psycopg2.errors.UniqueViolation):
            logging.info(u"Item already exists: {}".format(e.getErrorMessage()))
        else:
            logging.warning(u"Error during storing data into DB: {}".format(e))

