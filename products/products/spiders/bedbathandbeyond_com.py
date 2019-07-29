# -*- coding: utf-8 -*-
import re
import json
from urlparse import urljoin
import logging
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

        
MESSAGE_SERVER_ERROR = "Technical boo-boo right here. We'll get it fixed up."
MESSAGE_INCIDENT_ERROR = "Incident Number"

ITEMS_PER_PAGE = 24


def correct_image_url(x):
    return urljoin("https://b3h2.scene7.com/is/image/BedBathandBeyond/", x)


def get_in_store(x):
    if x:
        return 0
    else:
        return 1


class BedbathandbeyondComItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_input_processor = MapCompose(lambda x: x.strip())
    default_output_processor = Compose(TakeFirst(), lambda x: x.strip())
    default_selector_class = Selector
    category_path_out = Compose(Join(pipelines.DELIMITER_CATEGORY_PATH))
    orig_thumbnail_url_out = Compose(TakeFirst(), correct_image_url, lambda x: x.strip())
    in_store_out = Compose(TakeFirst(), get_in_store)
    
    

class BedbathandbeyondComSpider(CrawlSpider):
    name = "bedbathandbeyond_com"
    allowed_domains = ["bedbathandbeyond.com"]
    start_urls = [
        "https://www.bedbathandbeyond.com/store/category/clearance-savings/10009/",
        "https://www.bedbathandbeyond.com/store/category/bedding/10001/",
        "https://www.bedbathandbeyond.com/store/category/bath/13432/",
        "https://www.bedbathandbeyond.com/store/category/kitchen/10002/",
        "https://www.bedbathandbeyond.com/store/category/dining/10003/",
        "https://www.bedbathandbeyond.com/store/category/personalized-gifts/13807/",
        "https://www.bedbathandbeyond.com/store/category/furniture/13492/",
        "https://www.bedbathandbeyond.com/store/category/home-decor/10004/",
        "https://www.bedbathandbeyond.com/store/category/curtains-window/15588/",
        "https://www.bedbathandbeyond.com/store/category/storage-cleaning/10005/",
        "https://www.bedbathandbeyond.com/store/category/smart-home-home-improvement/14880/",
        "https://www.bedbathandbeyond.com/store/category/outdoor/10018/",
        "https://www.bedbathandbeyond.com/store/category/baby-kids/10006/",
        "https://www.bedbathandbeyond.com/store/category/health-beauty/13493/",
        "https://www.bedbathandbeyond.com/store/category/more/10007/",
        "https://www.bedbathandbeyond.com/store/category/gifts/13806/",
        "https://www.bedbathandbeyond.com/store/category/clearance-savings/10009/",
        "https://www.bedbathandbeyond.com/store/category/new-arrivals/10008/",
        "https://www.bedbathandbeyond.com/store/category/holiday/12792/",


#        "https://www.bedbathandbeyond.com/store/category/bath/bath-towels-rugs/13433/3-24",
        #"https://www.bedbathandbeyond.com/store/product/7-inch-grabber-mini-oven-mitt/3255156",
        #"https://www.bedbathandbeyond.com/store/product/sure-fit-reg-stretch-stripe-ottoman-slipcover/3246898",
#        "https://www.bedbathandbeyond.com/store/product/bridge-street-3-piece-marble-twist-lamp-set-with-cfl-bulbs/1017229630",
    ]
#    custom_settings = {
#        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64…) Gecko/20100101 Firefox/60.0",
#        "COOKIES_ENABLED": False,
#        "DOWNLOAD_DELAY": 10,
#        "CONCURRENT_REQUESTS": 1,
#        "DOWNLOADER_MIDDLEWARES": {
#            'products.basic_middlewares.user_agent_middleware.RandomUserAgentMiddleware': 400,
#            'products.basic_middlewares.proxy_middleware.ProxyMiddleware': 410,
#            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
#         }
#    }
    
    
#    """
    def parse(self, response):
        hxs = Selector(response)

#        if MESSAGE_SERVER_ERROR in response.body:
#            logging.error("Sever error during getting page: {}".format(response.url))
#        if MESSAGE_INCIDENT_ERROR in response.body:
#            logging.error("Unknown error during getting page: {}".format(response.url))
#        else:
        # process items
        item_urls = hxs.xpath(".//div[@class='grid-container']//article//div[contains(@id, 'tile')]/a/@href").extract()
        item_urls = map(lambda x: urljoin("https://www.bedbathandbeyond.com", x), item_urls)

        for item_url in item_urls:
            yield Request(url = item_url, callback=self.parse_item)

        # process pagination
        pagination_page_numbers = hxs.xpath(".//ul[contains(@class, 'Pagination')]//a/text()").extract()
        for pagination_page_number in pagination_page_numbers:
            if pagination_page_number:
                listing_url = None
                match = re.search(r"/store/category/.+?/\d+?/\d+(-\d+)", response.url)

                if match:
                    listing_url = re.sub(r"(/store/category/.+?/\d+?)/\d+(-\d+)", r"\1/" + str(pagination_page_number) + r"\2", response.url)
                else:
                    listing_url = re.sub(r"(/store/category/.+?/\d+?)/?$", r"\1/" + str(pagination_page_number) + "-" + str(ITEMS_PER_PAGE), response.url)
    
                if listing_url:
                    yield Request(url = listing_url, callback=self.parse)

        # process subcategories
        category_urls = hxs.xpath(".//li[contains(@class, 'SubCategoryList')]//a/@href").extract()

        if category_urls:
            for category_url in category_urls:
                if category_url:
                    category_url = urljoin("https://www.bedbathandbeyond.com/", category_url)
                    yield Request(url = category_url, callback=self.parse)
#    """


    def parse_item(self, response):
#    def parse(self, response):
        hxs = Selector(response)
        
        item_data = hxs.xpath(".//script[contains(., 'window.__INITIAL_STATE__')]/text()").extract_first()
        item_data = utils.regex_extractor(ur"window.__INITIAL_STATE__\s*=(.+?);\n", item_data, 1)

        if item_data:
            item_json_data = json.loads(item_data)
            
            if item_json_data:
                pdp = item_json_data.get("PDP", None)

                if pdp:
                    product_details = pdp.get("productDetails", None)
                    
                    if product_details:
                        """
                        brand = None

                        data = product_details.get("data", None)

                        if data:
                            brand = data.get("BRAND_NAME", None)
                        """

                        sku_details = product_details.get("skuDetails", None)

                        if sku_details:
                            for sku_detail in sku_details:
                                l = BedbathandbeyondComItemLoader(item = ProductItem(), response = response)
                                
                                l.add_value("url", response.url)
                                l.add_xpath("menu_name", "(.//ul[contains(@class, 'Breadcrumbs')]//a)[1]//text()")
                                l.add_xpath("category_name", "(.//ul[contains(@class, 'Breadcrumbs')]//a)[2]//text()")
                                l.add_xpath("subcategory_name", "(.//ul[contains(@class, 'Breadcrumbs')]//a)[3]//text()")
                                l.add_xpath("category_path", ".//ul[contains(@class, 'Breadcrumbs')]//a/*[@itemprop='name']/text()")
                                l.add_xpath("brand", ".//*[@itemprop='brand']//text()")
                                l.add_xpath("in_store", ".//*[contains(@class, 'Delivery') and normalize-space(.)='In-Store Pickup']/text()")

                                l.add_value("name", sku_detail.get("DISPLAY_NAME", None))
                                l.add_value("sku", sku_detail.get("SKU_ID", None))
                                l.add_value("upc", sku_detail.get("UPC", None))
                                l.add_value("price", sku_detail.get("IS_PRICE_VALUE", None))
                                l.add_value("orig_thumbnail_url", sku_detail.get("SCENE7_URL", None))
                                
                                yield l.load_item()

