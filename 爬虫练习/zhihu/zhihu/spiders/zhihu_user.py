# -*- coding: utf-8 -*-
import scrapy

class ZhihuUserSpider(scrapy.Spider):
    name = "zhihu_user"
    allowed_domains = ["zhihu"]
    start_urls = ['http://zhihu/']

    def parse(self, response):
        pass
