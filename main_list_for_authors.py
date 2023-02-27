import json

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.request import request_from_dict


class FindUrlsForAuthors(scrapy.Spider):
    name = "find_urls_for_authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]
    links_for_authors = set()
    find_all_links_for_authors = False
    custom_settings = {
        "FEED_FORMAT": "json", 
        "FEED_URI": "list_authors.json"
    }
    
    def parse(self, response):
        
        # count = 0
        
        next_page = ""
        
        if not self.find_all_links_for_authors:
            
            links = response.xpath("//div[@class='quote']/span/a/@href").extract()
            
            [self.links_for_authors.add(self.start_urls[0]+link) for link in links]
            
            # for link in links:
            #     self.new_start_urls.add(self.start_urls[0]+link)
        
            next_page = response.xpath("//li[@class='next']/a/@href").get()
        
        if next_page:
            yield scrapy.Request(url=self.start_urls[0]+next_page)
            
        else:
            
            self.find_all_links_for_authors = True
            
            for link_for_author in self.links_for_authors:
                yield scrapy.Request(url=link_for_author)                
                
            author = response.xpath("//h3[@class='author-title']/text()").get()
            
            if author:
                yield {
                    "fullname": author.strip(),
                    "born_date": response.xpath("//span[@class='author-born-date']/text()").get(),
                    "born_location": response.xpath("//span[@class='author-born-location']/text()").get(),
                    "description": response.xpath("//div[@class='author-description']/text()").get().strip()
                }


process = CrawlerProcess(settings=get_project_settings())
process.crawl(FindUrlsForAuthors)
process.start()

# import list_authors
# with open("list_authors.json", "r") as file:
#     list_authors = json.load(file)

# list_links = []

# for list_author in list_authors:
#     list_links += list_author.get("links")
    
# list_links1 = set(list_links)
# start_urls = []

# for list_ in list_links1:
#     start_urls.append("http://quotes.toscrape.com"+list_)
    
    
# class AuthorsSpider(scrapy.Spider):
#     name = "list_authors"
#     allowed_domains = ["quotes.toscrape.com"]
#     start_urls = start_urls
#     custom_settings = {
#         "FEED_FORMAT": "json", 
#         "FEED_URI": "authors_spider.json"
#     }
    
#     def parse(self, response):
            
#         yield {
#             # "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
#             "author": response.xpath("//h3[@class='author-title']/text()").get()
#             # "author": self.start_urls[0]+link
#             # "quote": quote.xpath("span[@class='text']/text()").get()
#         }
        
#         # next_link = response.xpath("//li[@class='next']/a/@href").get()
        
#         # if next_link:
#         #     yield scrapy.Request(url=self.start_urls[0]+next_link)
# # print(authors)


# # process1 = CrawlerProcess()
# process.crawl(AuthorsSpider)
# process.start()