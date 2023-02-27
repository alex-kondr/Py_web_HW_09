import json

import scrapy
from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from scrapy.utils.request import request_from_dict


authors = []


class FindUrlsForAuthors(scrapy.Spider):
    name = "find_urls_for_authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]
    links_for_authors = set()
    find_all_links_for_authors = False
    custom_settings = {
        "FEED_FORMAT": "json", 
        "FEED_URI": "quotes.json"
    }
    
    def parse(self, response):
        global authors
        
        # count = 0
        
        next_page = ""
        
        if not self.find_all_links_for_authors:
            
            for quote in response.xpath("/html//div[@class='quote']"):
                yield {
                    "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                    "author": quote.xpath("span/small[@class='author']/text()").get(),
                    "quote": quote.xpath("span[@class='text']/text()").get().strip()
                }
            
            
            links = response.xpath("//div[@class='quote']/span/a/@href").extract()
            
            [self.links_for_authors.add(self.start_urls[0]+link) for link in links]
            
            next_page = response.xpath("//li[@class='next']/a/@href").get()
        
        if next_page:
            yield scrapy.Request(url=self.start_urls[0]+next_page)
            
        else:
            
            # self.custom_settings = {
            #     "FEED_FORMAT": "json", 
            #     "FEED_URI": "list_authors1.json"
            # }
            
            self.find_all_links_for_authors = True
            
            for link_for_author in self.links_for_authors:
                yield scrapy.Request(url=link_for_author)                
                
            author = response.xpath("//h3[@class='author-title']/text()").get()
            
            if author:
                authors.append({
                    "fullname": author.strip(),
                    "born_date": response.xpath("//span[@class='author-born-date']/text()").get(),
                    "born_location": response.xpath("//span[@class='author-born-location']/text()").get(),
                    "description": response.xpath("//div[@class='author-description']/text()").get().strip()
                })


process = CrawlerProcess()
process.crawl(FindUrlsForAuthors)
process.start()

with open("authors.json", "w") as file:
    json.dump(authors, file)

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