# -*- coding: utf-8 -*-
import urlparse
import json
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

    
    
def clear_category(x):
    return x.rstrip("/")


def get_in_store(x):
    if x:
        return 1
    else:
        return 0
    

class StaplesComItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_input_processor = MapCompose(lambda x: x.strip())
    default_output_processor = Compose(TakeFirst(), lambda x: x.strip())
    default_selector_class = Selector
    menu_name_out = Compose(Join(), clear_category, lambda x: x.strip())
    category_name_out = Compose(Join(), clear_category, lambda x: x.strip())
    subcategory_name_out = Compose(Join(), clear_category, lambda x: x.strip())
    category_path_out = Compose(lambda path_list: filter(lambda x: "/" != x, path_list), Join(pipelines.DELIMITER_CATEGORY_PATH))
    in_store_out = Compose(TakeFirst(), get_in_store)



class StaplesComSpider(CrawlSpider):
    name = "staples_com"
    allowed_domains = ["staples.com"]
    start_urls = [
        "https://www.staples.com/",
#        "https://www.staples.com/Total-Defense-PC-Tune-Up-in-store-only/product_1564544",
#        "https://www.staples.com/hp-laserjet-pro-m15w-wireless-laser-printer-w2g51a/product_24323034",
#        "https://www.staples.com/Staples-One-Touch-Half-Strip-Compact-Stapler-Fastening-Capacity-20-Sheets-Black/product_1798849",
#        "https://www.staples.com/Snacks/cat_CL166198/7zuxr?icid=BREAKROOMSUPERCAT:LINKBOX3:VARIETYPACKS",
#        "https://www.staples.com/Domtar-Cover-Stock-8-1-2-x-11-ETTER-Size-Bright-White-96-US-Brightness-67-lb-250-Sheets-Pack-82880/product_759119",
#        "https://www.staples.com/N-Joy-Pure-Sugar-Value-Pack-20-oz-Canister-3-Pack/product_236240",
#        "https://www.staples.com/Green-Mountain-Coffee-Dark-Magic-Extra-Bold-Coffee-K-Cup-48-Count/product_1635472",
#        "https://www.staples.com/Folgers-Classic-Roast-Ground-Coffee-Regular-9-oz-40-Filter-Packets/product_495726",
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths=(".//div[@id='category-products-content']//li")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(".//div[contains(@id, 'products-flyout')]//div[contains(@class, 'links-container')]")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(".//div[@class='cwwbos_container_wrapper']")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(".//div[@id='pagination']")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(".//div[contains(@class, '__product_info')]")), callback="parse_item"),
    )
    custom_settings = {
        "DOWNLOAD_DELAY": .3,
        "CONCURRENT_REQUESTS": 3,
#        "PROXIES": []
    }


    def parse_item(self, response):
#    def parse(self, response):
        hxs = Selector(response)
        l = StaplesComItemLoader(item = ProductItem(), response = response)

        preload_data = hxs.xpath(".//script[contains(., 'window.__PRELOADED_STATE__')]/text()").extract_first()
        preload_json = utils.regex_extractor(ur".*__PRELOADED_STATE__\s*=(.*);", preload_data, 1)
        preload_json_data = json.loads(preload_json)
        
        if preload_json_data:
            sku_state = preload_json_data.get("skuState", None)
            
            if sku_state:
                sku_data = sku_state.get("skuData", None)
                
                if sku_data:

                    items = sku_data.get("items", None)
                    
                    if items:
                        item = items[0]

                        if item:
                            product = item.get("product", None)

                            if product:
                                l.add_value("url", response.url)
                                l.add_xpath("name", ".//h1[contains(@class, 'product_title')]/text()")
                                l.add_xpath("menu_name", ".//div[@id='breadcrumbs_container']/ul/li[2]//text()")
                                l.add_xpath("category_name", ".//div[@id='breadcrumbs_container']/ul/li[3]//text()")
                                l.add_xpath("subcategory_name", ".//div[@id='breadcrumbs_container']/ul/li[4]//text()")
                                l.add_xpath("category_path", ".//div[@id='breadcrumbs_container']/ul/li//span/text()")
                                l.add_xpath("in_store", ".//*[@id='bopis_title']")

                                l.add_value("brand", product.get("brandName", None))
                                l.add_value("sku", product.get("partNumber", None))
                                l.add_value("upc", product.get("upcCode", None))

                                images = product.get("images", None)
                                if images:
                                    standard = images.get("standard", None)

                                    if standard:
                                        image_url = standard[0]

                                        if image_url:
                                            l.add_value("orig_thumbnail_url", image_url)

                            price = item.get("price", None)

                            if price:
                                price_items = price.get("item", None)

                                if price_items:
                                    price_item = price_items[0]
                                    
                                    if price_item:
                                        data = price_item.get("data", None)

                                        if data:
                                            price_infos = data.get("priceInfo", None)
                                            
                                            if price_infos:
                                                one_time_purchases = filter(lambda x: "ONE_TIME_PURCHASE" == x.get("purchaseOptionType", None), price_infos)

                                                if one_time_purchases:
                                                    one_time_purchase = one_time_purchases[0] 
                                                    
                                                    if one_time_purchase:
                                                        final_price = one_time_purchase.get("finalPrice", None)

                                                        if final_price:
                                                            l.add_value("price", str(final_price))

                    # get links to child products
                    sku_select_arr = sku_data.get("skuSelectArr", None)
                    
                    if sku_select_arr:
                        child_products = sku_select_arr.get("childProducts", None)
                        
                        if child_products:
                            child_product_urls = map(lambda x: x.get("link", None), child_products)
                            child_product_urls = map(lambda x: urlparse.urljoin("https://www.staples.com/", x), child_product_urls)

                            for url in child_product_urls:
                                yield Request(url = url, callback=self.parse)

        yield l.load_item()

