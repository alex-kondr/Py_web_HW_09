import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "quotes_spider.json"}
    
    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small[@class='author']/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
            
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        
        if next_link:
            yield scrapy.Request(url=self.start_urls[0]+next_link)
        


process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()