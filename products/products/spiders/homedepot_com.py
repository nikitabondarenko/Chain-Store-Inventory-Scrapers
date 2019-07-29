# -*- coding: utf-8 -*-
import json
from urlparse import urljoin
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose, TakeFirst, Compose, Join, Identity
from scrapy.http import Request, HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.conf import settings
from products.items import ProductItem
from products import pipelines, utils



class HomedepotComItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_input_processor = MapCompose(lambda x: x.strip())
    default_output_processor = Compose(TakeFirst(), lambda x: x.strip())
    default_selector_class = Selector
    menu_name_out = Compose(lambda x: x[0] if 0 < len(x) else None, lambda x: x.strip())
    category_name_out = Compose(lambda x: x[1] if 1 < len(x) else None, lambda x: x.strip())
    subcategory_name_out = Compose(lambda x: x[2] if 2 < len(x) else None, lambda x: x.strip())
    category_path_out = Compose(Join(pipelines.DELIMITER_CATEGORY_PATH))
    in_store_in = Identity()
    in_store_out = Compose(TakeFirst())



class HomedepotComSpider(CrawlSpider):
    name = "homedepot_com"
    allowed_domains = ["homedepot.com"]
    start_urls = [
        "https://www.homedepot.com/c/site_map",
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths=(".//div[@class='content']//ul")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(".//div[@class='content']//p")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(".//div[@class='content']//h3")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(".//div[@class='content']//li")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(".//nav[@role='navigation']")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(".//div[@data-component='productpod']//div[contains(@class, 'description')]")), callback="parse_item"),
    )


    def parse_item(self, response):
#    def parse(self, response):
        hxs = Selector(response)
        l = HomedepotComItemLoader(item = ProductItem(), response = response)

        l.add_value("url", response.url)

        categories = []

        # getting categories
        breadcrumb_data = hxs.xpath(".//script[contains(., 'BREADCRUMB_JSON')]/text()").extract_first()
        breadcrumb_data = utils.regex_extractor(ur"BREADCRUMB_JSON\s*=(.+);", breadcrumb_data, 1)
        
        if breadcrumb_data:
            breadcrumb_json_data = json.loads(breadcrumb_data)

            if breadcrumb_json_data:
                bs_live_person_data = breadcrumb_json_data.get("bcLivePersonData", None)
            
                if bs_live_person_data:
                    categories = bs_live_person_data.split(">")
        else:
            categories = hxs.xpath(".//div[@id='breadcrumb']//li//text()").extract()
        
            if categories:
                categories = categories[1:]

        if categories:
            l.add_value("menu_name", categories)
            l.add_value("category_name", categories)
            l.add_value("subcategory_name", categories)
            l.add_value("category_path", categories)

        l.add_xpath("brand", ".//div[contains(@class, 'sticky_brand_info')]/text()")
        l.add_xpath("name", ".//h1[contains(@class, 'title')]/text()")
        l.add_xpath("sku", ".//*[@id='product_internet_number']/text()")
        l.add_xpath("upc", ".//upc/text()")
        l.add_xpath("orig_thumbnail_url", ".//img[@id='mainImage']/@src")
        l.add_xpath("price", ".//*[@id='ajaxPrice']/@content")


        availability_online = utils.regex_extractor(ur"(\"AvailabilityType\":\"Online\")", response.body, 1)
        if availability_online:
            l.add_value("in_store", 0)
        else:
            availability_browseonly = utils.regex_extractor(ur"(\"AvailabilityType\":\"Browse Only\")", response.body, 1)
            if availability_browseonly:
                l.add_value("in_store", 1)
            else:
                message_na = utils.regex_extractor(ur"(This product isn't currently sold in stores)", response.body, 1)
                if message_na:
                    l.add_value("in_store", 1)
        
        return l.load_item()

