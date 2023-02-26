import json

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class FindUrlsForAuthors(scrapy.Spider):
    name = "find_urls_for_authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]
    new_start_urls = set()
    custom_settings = {
        "FEED_FORMAT": "json", 
        "FEED_URI": "list_authors.json"
    }
    
    def parse(self, response):
        links = response.xpath("//div[@class='quote']/span/a/@href").extract()
        
        for link in links:
            self.new_start_urls.add()
        # yield {
        #     # "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
        #     "links": links
        #     # "author": self.start_urls[0]+link
        #     # "quote": quote.xpath("span[@class='text']/text()").get()
        # }
        
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        
        if next_link:
            yield scrapy.Request(url=self.start_urls[0]+next_link)
# print(authors)


process = CrawlerProcess(settings=get_project_settings())
process.crawl(FindUrlsForAuthors)
process.start()
process.stop()

print("--------------------")
print("End spyder")

# import list_authors
with open("list_authors.json", "r") as file:
    list_authors = json.load(file)

list_links = []

for list_author in list_authors:
    list_links += list_author.get("links")
    
list_links1 = set(list_links)
start_urls = []

for list_ in list_links1:
    start_urls.append("http://quotes.toscrape.com"+list_)
    
    
class AuthorsSpider(scrapy.Spider):
    name = "list_authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = start_urls
    custom_settings = {
        "FEED_FORMAT": "json", 
        "FEED_URI": "authors_spider.json"
    }
    
    def parse(self, response):
            
        yield {
            # "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
            "author": response.xpath("//h3[@class='author-title']/text()").get()
            # "author": self.start_urls[0]+link
            # "quote": quote.xpath("span[@class='text']/text()").get()
        }
        
        # next_link = response.xpath("//li[@class='next']/a/@href").get()
        
        # if next_link:
        #     yield scrapy.Request(url=self.start_urls[0]+next_link)
# print(authors)


# process1 = CrawlerProcess()
process.crawl(AuthorsSpider)
process.start()