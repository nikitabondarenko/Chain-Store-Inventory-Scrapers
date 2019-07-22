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


STORE_ID = 893
ITEMS_PER_PAGE = 24


class TargetComItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_input_processor = MapCompose(lambda x: x.strip())
    default_output_processor = Compose(TakeFirst(), lambda x: x.strip())
    default_selector_class = Selector
    orig_thumbnail_url_in = MapCompose(lambda x: "https:" + x.strip())
    price_in = Identity()
    price_out = Compose(TakeFirst())
    category_path_out = Compose(lambda x: x[1:], Join(pipelines.DELIMITER_CATEGORY_PATH))


class TargetComSpider(scrapy.Spider):
    name = "target_com"
    allowed_domains = ["target.com"]
    start_urls = [
        "https://www.target.com/",
#        "https://www.target.com/p/wrangler-174-men-s-5-star-regular-fit-jeans-rinse-40x32/-/A-14797384",
#        "https://www.target.com/c/outdoor-heating-accessories-fire-pits-patio-heaters-garden/-/N-5xtpj?Nao=24",
#        "https://www.target.com/p/kirk-franklin-long-live-love-cd/-/A-76472491",
#        "https://www.target.com/p/standish-2pk-patio-club-chair-black-gray-project-62-153/-/A-21499072",
#        "https://www.target.com/p/avocet-rattan-fan-back-accent-chair-opalhouse-153/-/A-53015665",
#        "https://www.target.com/p/boudreaux-s-butt-paste-diaper-rash-ointment-maximum-strength-preservative-free-4oz-tube/-/A-13923635",
#        "https://www.target.com/p/linen-lamp-shade-shell-threshold-153/-/A-16527279?preselect=15394670#lnk=sametab",
#        "https://www.target.com/p/women-s-5-pocket-denim-mini-skirt-wild-fable-153-medium-blue-wash/-/A-54185844?preselect=54008199#lnk=sametab"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url = url, callback = self.parse_listing_page)
#            yield Request(url = url, callback = self.parse_item)


    def parse_listing_page(self, response):
        hxs = Selector(response)

        category_urls = hxs.xpath(".//ul[@data-test='pictureNavigationFeatured']/li//a/@href").extract()
        category_urls = map(lambda x: urljoin("https://www.target.com/", x), category_urls)
        
        for category_url in category_urls:
            yield Request(url = category_url, callback = self.parse_listing_page)

        category = utils.regex_extractor(ur".+/c/.+/N-(.+?)($|\?)", response.url, 1)

        preload_data = hxs.xpath(".//script[contains(., 'window.__PRELOADED_STATE__')]/text()").extract_first()
        preload_json = utils.regex_extractor(ur".*__PRELOADED_STATE__=(.*)", preload_data, 1)

        api_key = None

        try:
            preload_json_data = json.loads(preload_json)

            if preload_json_data:
                config = preload_json_data.get("config", None)
                
                if config:
                    firefly = config.get("firefly", None)

                    if firefly:
                        api_key = firefly.get("apiKey", None)

                        if api_key:
                            yield self.create_listing_request(category, api_key, STORE_ID, 0, ITEMS_PER_PAGE)
        except:
            pass


    def create_listing_request(self, category, api_key, store_id, offset, count):
        metadata = {
            "category": category,
            "api_key": api_key,
            "store_id": store_id,
            "offset": offset
        }
        #url = "https://redsky.target.com/v2/plp/search/?count=24&offset=0&category=5xtpj&brand_id=&default_purchasability_filter=true&include_sponsored_search=true&ppatok=AOxT33a&platform=desktop&useragent=Mozilla%2F5.0+%28X11%3B+Linux+x86_64%3B+rv%3A60.0%29+Gecko%2F20100101+Firefox%2F60.0&pageId=%2Fc%2F5xtpj&channel=web&visitorId=016B23972EDE0201B9F6BF0295F5B450&store_ids=893%2C957%2C1342%2C836%2C880&scheduled_delivery_store_id=880&pricing_store_id=893&key=eb2551e4accc14f38cc42d32fbc2b2ea"
       # url = "https://redsky.target.com/v2/plp/search/?count=24&offset=0&category=5xtpj&default_purchasability_filter=true&include_sponsored_search=true&ppatok=AOxT33a&platform=desktop&pageId=%2Fc%2F5xtpj&channel=web&pricing_store_id=893&key=eb2551e4accc14f38cc42d32fbc2b2ea"
       # url = "https://redsky.target.com/v2/plp/search/?count=24&offset=0&category=5xtpj&default_purchasability_filter=true&include_sponsored_search=true&platform=desktop&channel=web&pricing_store_id=893&key=eb2551e4accc14f38cc42d32fbc2b2ea"
        url = "https://redsky.target.com/v2/plp/search/?count=" + str(count) + "&offset=" + str(offset) + "&category=" + str(category) + "&default_purchasability_filter=true&include_sponsored_search=true&channel=web&pricing_store_id=" + str(store_id) + "&key=" + str(api_key)
        return Request(url = url, callback = self.parse_listing, meta = metadata)


    def parse_listing(self, response):
        metadata = response.meta
        category = metadata.get("category", None)
        api_key = metadata.get("api_key", None)
        store_id = metadata.get("store_id", None)
        offset = metadata.get("offset", None)
        listing_json_data = json.loads(response.body)
        
        if listing_json_data:
            search_response = listing_json_data.get("search_response", None)
            
            if search_response:
                items = search_response.get("items", None)

                if items:
                    items = items.get("Item", None)

                    if items:
                        for item in items:
                            title = item.get("title", None)
                            url = item.get("url", None)
                            url = urljoin("https://www.target.com/", url)
                            pick_up_in_store = item.get("pick_up_in_store", None)
                            ship_to_store = item.get("ship_to_store", None)
                            ship_from_store = item.get("ship_from_store", None)
                            rush_delivery = item.get("rush_delivery", None)
                            is_out_of_stock_in_all_store_locations = item.get("is_out_of_stock_in_all_store_locations", "false")
                            is_out_of_stock_in_all_online_locations = item.get("is_out_of_stock_in_all_online_locations", None)

                        #    print(pick_up_in_store)
                            if (not (False == pick_up_in_store and \
                                    False == ship_to_store and \
                                    False == ship_from_store and \
                                    False == rush_delivery and \
                                    True == is_out_of_stock_in_all_store_locations and \
                                    False == is_out_of_stock_in_all_online_locations)):
                                yield Request(url = url, callback = self.parse_item)

                        if ITEMS_PER_PAGE == len(items):
                            yield self.create_listing_request(category, api_key, STORE_ID, offset + ITEMS_PER_PAGE, ITEMS_PER_PAGE)


    def parse_item(self, response):
        hxs = Selector(response)

        menu_name = hxs.xpath("(.//div[@data-test='breadcrumb']//span[@itemprop='name'])[2]/text()").extract_first()
        category_name = hxs.xpath("(.//div[@data-test='breadcrumb']//span[@itemprop='name'])[3]/text()").extract_first()
        subcategory_name = hxs.xpath("(.//div[@data-test='breadcrumb']//span[@itemprop='name'])[4]/text()").extract_first()
        category_path = hxs.xpath("(.//div[@data-test='breadcrumb']//span[@itemprop='name'])/text()").extract()

        preload_data = hxs.xpath(".//script[contains(., 'window.__PRELOADED_STATE__')]/text()").extract_first()
        preload_json = utils.regex_extractor(ur".*__PRELOADED_STATE__=(.*)", preload_data, 1)

        api_key = None

        preload_json_data = json.loads(preload_json)
        #print(preload_json_data)

        if preload_json_data:
            config = preload_json_data.get("config", None)
            
            if config:
                firefly = config.get("firefly", None)

                if firefly:
                    api_key = firefly.get("apiKey", None)

            product = preload_json_data.get("product", None)
            
            if product:
                product_details = product.get("productDetails", None)
                
                if product_details:
                    item = product_details.get("item", None)

                    if item:
                        brand = item.get("brand", None)

                        # check different types
                        children = item.get("children", None)

                        if children:
                            for child_key, child in children.iteritems():
                                l = TargetComItemLoader(item = ProductItem(), response = response)

                                title = child.get("title", None)
                                product_id = child.get("productId", None)

                                l.add_value("url", response.url)
                                l.add_value("menu_name", menu_name)
                                l.add_value("category_name", category_name)
                                l.add_value("subcategory_name", subcategory_name)
                                l.add_value("category_path", category_path)
                                l.add_value("brand", brand)
                                l.add_value("name", title)
                                l.add_value("sku", product_id)

                                item_details = child.get("itemDetails", None)

                                if item_details:
                                    upc = item_details.get("upc", None)
                                    l.add_value("upc", upc)

                                images = child.get("images", None)

                                if images:
                                    image_url = images.get("imageUrl", None)
                                    l.add_value("orig_thumbnail_url", image_url)

                                yield self.create_price_request(api_key, STORE_ID, product_id, l)
                        else:
                            l = TargetComItemLoader(item = ProductItem(), response = response)

                            title = item.get("title", None)
                            product_id = item.get("productId", None)

                            l.add_value("url", response.url)
                            l.add_value("menu_name", menu_name)
                            l.add_value("category_name", category_name)
                            l.add_value("subcategory_name", subcategory_name)
                            l.add_value("category_path", category_path)
                            l.add_value("brand", brand)
                            l.add_value("name", title)
                            l.add_value("sku", product_id)

                            item_details = item.get("itemDetails", None)

                            if item_details:
                                upc = item_details.get("upc", None)
                                l.add_value("upc", upc)

                            images = item.get("images", None)

                            if images:
                                image_url = images.get("imageUrl", None)
                                l.add_value("orig_thumbnail_url", image_url)

                            yield self.create_price_request(api_key, STORE_ID, product_id, l)

        
    def create_price_request(self, api_key, store_id, sku, loader):
        if api_key and store_id and sku:
            url = "https://redsky.target.com/web/pdp_location/v1/tcin/" + str(sku) + "?pricing_store_id=" + str(store_id) + "&key=" + str(api_key)
            request = Request(url, callback = self.parse_price)
            request.meta["loader"] = loader
            return request
        return loader.load_item()


    def parse_price(self, response):
        loader = response.meta["loader"]
        json_data = json.loads(response.body)
        
        if json_data:
            price = json_data.get("price", None)

            if price:
                current_retail = price.get("current_retail", None)
                loader.add_value("price", current_retail)

        return loader.load_item()

