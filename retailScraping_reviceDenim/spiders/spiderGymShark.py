#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 14:27:08 2018

@author: RacquelFygenson
"""
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from tutorial2.items import ReviceSampleItem
from urllib.parse import urljoin
import json


class MySpider(CrawlSpider):
    name = "gymsharkCrawl"
    allowed_domains: ["gymshark.com"]
    start_urls = ["https://www.gymshark.com/collections/all-products/womens?page=1"]
    
#    rules = (
#        Rule(LinkExtractor(restrict_xpaths="//a[@title='Next Page']"), follow=True),
##        Rule(LinkExtractor(allow=r"/collections/everything?page=\d+$"), callback='parse')
##         Rule(LinkExtractor(allow=r"/collections/everything?page=\d+$"), callback='parse')
#
#    )

    
    def parse(self, response):
        
#        name = response.css(".ProductItem__Title.Heading a::text").extract()
#        price = response.css('.money::text').extract()
        link = response.css("div.prod-image-wrap > a").xpath('@href').extract()
        linkFull =[]
        for lnk in link:
             newLink = response.urljoin(lnk)
             linkFull.append(newLink)
             yield scrapy.Request(url = newLink, callback=self.parse_link)
#        for entry in linkFull: 
#            scraped = {
#                    'link' : entry
#                    }
            #yield scraped 
                   
            
#        for item in zip(name, price, linkFull):
#            scraped_info = {
#                    'name' : item[0],
#                    'price' : item[1],
#                    'link' : item[2]
#                    } 
#            
#            yield scraped_info
            
            
        #follow pagination links
        next_page_url = response.css('div.Pagination__Nav > a[rel="next"]').xpath('@href').extract()
        
        if next_page_url:           
           next_page_url = response.urljoin(next_page_url[0])  
           yield scrapy.Request(url = next_page_url, callback=self.parse)
           
    
    def parse_link(self, response):
        # continue parsing (aka your second spider) 
        name = response.css(".product-details>h1::text").extract()
        #price = response.css(".ProductMeta__Price.Price.Text--subdued.u-h4 > .money::text").extract()
        json_info= response.css("script[type='application/json']").extract()
        sizes = json_info[2]
        sizes = sizes.split('variants":')
        sizes = sizes[1]
        sizes = sizes.split(',"images":[')
        sizes = sizes[0]
        sizesJson = json.loads(sizes)
        
        number_of_sizes = len(sizesJson)
        for size in range(0,number_of_sizes):
            scraped_info = {
                    'name' :  name,
                    'price' : sizesJson[size]['price'],
                    'size' : sizesJson[size]['title'],
                    'qA' : sizesJson[size]['inventory_quantity'],
                    'available' : sizesJson[size]['available']
                    }
            yield scraped_info
        

 #       for #number of options in json# in json
        #take out size, price, qA, zip with name, price, yield, do again
#        for item in zip(name, price):
#            scraped_info = {
#                    'name' : item[0],
#                    'afterpay' : item[1],
#                    
#                    }
        
            
        
        
        