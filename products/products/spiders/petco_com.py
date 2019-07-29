# -*- coding: utf-8 -*-
import json
from urlparse import urljoin
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose, TakeFirst, Compose, Join, Identity
from scrapy.http import Request, HtmlResponse
from scrapy.spiders import SitemapSpider, CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.conf import settings
from products.items import ProductItem
from products import pipelines, utils



def get_in_store(x):
    if "no" == x:
        return 1
    else:
        return 0


class PetcoComItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_input_processor = MapCompose(lambda x: x.strip())
    default_output_processor = Compose(TakeFirst(), lambda x: x.strip())
    default_selector_class = Selector
    menu_name_out = Compose(lambda x: x[1] if 1 < len(x) else None, lambda x: x.strip())
    category_name_out = Compose(lambda x: x[2] if 2 < len(x) else None, lambda x: x.strip())
    subcategory_name_out = Compose(lambda x: x[3] if 3 < len(x) else None, lambda x: x.strip())
    category_path_out = Compose(lambda x: x[1:], Join(pipelines.DELIMITER_CATEGORY_PATH))
    price_out = Compose(TakeFirst(), lambda x: x.replace("$", "").strip())
    in_store_out = Compose(TakeFirst(), get_in_store)


class PetcoComSpider(SitemapSpider):
    name = "petco_com"
    allowed_domains = ["petco.com"]
    start_urls = [
#        "https://www.petco.com/shop/ShopAllBrandsView?catalogId=10051&langId=-1&storeId=10151&langId=-1"
#        "https://www.petco.com/shop/en/petcostore/brand/a-pets-life"
#        "https://www.petco.com/shop/en/petcostore/product/a-pets-life-personalized-small-photo-frame-cremation-urn-honeynut-pet-memorial-for-pet-weight-up-to-195-lbs",
#        "https://www.petco.com/shop/en/petcostore/product/dog/dog-food/wet-dog-food/wholehearted-grain-free-lamb-and-carrot-canned-adult-dog-food",
#        "https://www.petco.com/shop/en/petcostore/product/dog/dog-treats-and-chews/dog-dental-treats-and-chews/star-mark-everlasting-bacon-dog-dental-chew",
    ]
    sitemap_urls = ["https://www.petco.com/sitemap_10151.xml"]
    sitemap_rules = [("/petcostore/product/", "parse_item")]


    def parse_item(self, response):
        hxs = Selector(response)

        store_id = hxs.xpath(".//meta[@name='CommerceSearch']/@content").extract_first()
        if store_id:
            store_id = store_id.replace("storeId_", "")

        catalog_id = hxs.xpath(".//input[@id='es_parent_category_rn']/@value").extract_first()
        if not catalog_id:
            catalog_id = utils.regex_extractor(ur"params\.catalogId\s?=\s?'(.+?)';", response.body, 1)

        catalog_entry_ids = hxs.xpath(".//input[@id='catEntryIdList']/@value").extract_first()
        if not catalog_entry_ids:
            catalog_entry_ids = hxs.xpath(".//input[@id='catalogEntryIdToUse_request']/@value").extract_first()
        if catalog_entry_ids:
            catalog_entry_ids = catalog_entry_ids.split(",")

        product_id = hxs.xpath(".//input[@id='es_productId']/@value").extract_first()

        if store_id and catalog_id and catalog_entry_ids and product_id:
            url = "https://www.petco.com/shop/GetCatalogEntryDetailsByIDView?"
            
            for catalog_entry_id in catalog_entry_ids:
                l = PetcoComItemLoader(item = ProductItem(), response = response)

                l.add_value("url", response.url)

                l.add_xpath("menu_name", ".//ol[@class='breadcrumb']//li//text()")
                l.add_xpath("category_name", ".//ol[@class='breadcrumb']//li//text()")
                l.add_xpath("subcategory_name", ".//ol[@class='breadcrumb']//li//text()")
                l.add_xpath("category_path", ".//ol[@class='breadcrumb']//li//text()")
                l.add_xpath("brand", ".//div[contains(@class, 'product-brand')]//span[@itemprop='name']/text()")

                url = utils.add_params_to_url(url, storeId = store_id, langId = -1, catalogId = catalog_id, catalogEntryId = catalog_entry_id, productId = product_id)
                request = Request(url, callback = self.parse_variation_data)
                request.meta["loader"] = l
                yield request
            

             
    def parse_variation_data(self, response):
        loader = response.meta["loader"]
        hxs = Selector(response)
        extracted_json = utils.regex_extractor(ur"/\*(.+)\*/", response.body, 1)

        details_data = json.loads(extracted_json)
        if details_data:
            catalog_entry = details_data.get("catalogEntry", None)
            
            if catalog_entry:
                catalog_entry_identifier = catalog_entry.get("catalogEntryIdentifier", None)

                if catalog_entry_identifier:
                    external_identifier = catalog_entry_identifier.get("externalIdentifier", None)
                    
                    if external_identifier:
                        loader.add_value("sku", external_identifier.get("partNumber", None))

                descriptions = catalog_entry.get("description", None)

                if descriptions:
                    description = descriptions[0]
                    
                    if description:
                        loader.add_value("name", description.get("name", None))
                        loader.add_value("orig_thumbnail_url", description.get("fullImage", None))

                loader.add_value("price", catalog_entry.get("offerPrice", None))

                in_store_only = catalog_entry.get("InStoreOnly", None)
                if in_store_only:
                    loader.add_value("in_store", in_store_only)

        return loader.load_item()

