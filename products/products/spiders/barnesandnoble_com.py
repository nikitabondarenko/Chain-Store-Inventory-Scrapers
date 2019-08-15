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



class BarnesandnobleComItemLoader(ItemLoader):
    default_item_class = ProductItem
    default_input_processor = MapCompose(lambda x: x.strip())
    default_output_processor = Compose(TakeFirst(), lambda x: x.strip())
    default_selector_class = Selector
    category_path_out = Compose(Join(pipelines.DELIMITER_CATEGORY_PATH))
    brand_out = Compose(Join(), lambda x: x.strip())
    orig_thumbnail_url_out = Compose(TakeFirst(), lambda x: "https:" + x.strip())
    unique_attrs_in = Identity()
    unique_attrs_out = Compose(TakeFirst())



class BarnesandnobleComSpider(CrawlSpider):
    name = "barnesandnoble_com"
    allowed_domains = ["barnesandnoble.com"]
    start_urls = [
        "https://www.barnesandnoble.com/b/books/_/N-29Z8q8",
        "https://www.barnesandnoble.com/b/textbooks/_/N-8q9",
        "https://www.barnesandnoble.com/b/books/teens/_/N-29Z8q8Z19r4",
        "https://www.barnesandnoble.com/b/books/kids/_/N-29Z8q8Ztu1",
        "https://www.barnesandnoble.com/b/toys/_/N-8qf",
        "https://www.barnesandnoble.com/b/games-collectibles/_/N-1gls",
        "https://www.barnesandnoble.com/b/gift-home-office/_/N-8qg",
        "https://www.barnesandnoble.com/b/movies-tv/_/N-8qh",
        "https://www.barnesandnoble.com/b/music/_/N-8qi",
#        "https://www.barnesandnoble.com/w/bluest-eye-toni-morrison/1100608830"
    ]
    rules = (
        Rule(LinkExtractor(restrict_xpaths=(".//div[@id='refinements']")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(".//ul[@role='navigation']")), follow=True),
        Rule(LinkExtractor(restrict_xpaths=(".//div[contains(@class, 'product-shelf-title')]")), callback="parse_item"),
    )


    def parse_item(self, response):
#    def parse(self, response):
        hxs = Selector(response)
        l = BarnesandnobleComItemLoader(item = ProductItem(), response = response)

        l.add_value("url", response.url)


        categories_data = hxs.xpath(".//input[@id='gptAdsVal']/@value").extract_first()
        
        if categories_data:
            menu_name = utils.regex_extractor(ur"cat1:(.+?);", categories_data, 1)
            category_name = utils.regex_extractor(ur"cat2:(.+?);", categories_data, 1)
            subcategory_name = utils.regex_extractor(ur"cat3:(.+?);", categories_data, 1)
  
            l.add_value("menu_name", menu_name)
            l.add_value("category_name", category_name)
            l.add_value("subcategory_name", subcategory_name)

            l.add_value("category_path", menu_name)
            l.add_value("category_path", category_name)
            l.add_value("category_path", subcategory_name)
        
        l.add_xpath("name", ".//h1[@itemprop='name']/text()")
        l.add_xpath("price", ".//span[@id='pdp-cur-price']/text()")
        l.add_xpath("brand", ".//div[@id='ProductDetailsTab']//th[normalize-space(.)='Publisher:']/parent::tr/td//text()")
        l.add_xpath("sku", ".//div[@id='prodPromo']//a/@data-sku-id")
        l.add_xpath("upc", ".//div[@id='prodPromo']//a/@data-sku-id")
        l.add_xpath("orig_thumbnail_url", ".//div[@class='pdp-product-image-container']//img[@id='pdpMainImage']/@src")

        authors = hxs.xpath(".//span[@itemprop='author']/text()").extract()
        publishers = hxs.xpath(".//div[@id='ProductDetailsTab']//th[normalize-space(.)='Publisher:']/parent::tr/td//text()").extract()

        unique_attrs = {}

        if authors:
            authors = filter(lambda x: x and x.strip(), authors)
            if authors:
                authors = ", ".join(authors)
                unique_attrs["authors"] = authors

        if publishers:
            publishers = filter(lambda x: x and x.strip(), publishers)
            if publishers:
                publishers = ", ".join(publishers)
                unique_attrs["publishers"] = publishers

        if unique_attrs:
            l.add_value("unique_attrs", unique_attrs)
    
        return l.load_item()

