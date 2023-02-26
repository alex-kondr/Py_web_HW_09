import scrapy
from scrapy.crawler import CrawlerProcess


class AuthorsSpider(scrapy.Spider):
    name = "list_authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]
    custom_settings = {
        "FEED_FORMAT": "json", 
        "FEED_URI": "list_authors.json"
    }
    
    def parse(self, response):
        
        # authors = response.xpath("/html//small[@class='author']/text()").extract()
        # yield authors
        links = response.xpath("//div[@class='quote']/span/a/@href").extract()
        # print(f"{links=}")
        # for link in links:
        # if links:
        #     yield scrapy.Request(url=self.start_urls[0]+links)
        # self.start_urls = []
        
        # for link in links:
        #     self.start_urls.append("http://quotes.toscrape.com"+link)
            # yield scrapy.Request(url=self.start_urls[0]+link)
            # scrapy.Request(url=self.start_urls[0]+link)
        # print("author: ", response.xpath("//h3[@class='author-title']/text()").get())
        # for author in response.xpath("/html//div[@class='author-details']"):
                
        
        # for link_ in self.start_urls:
        #     yield scrapy.Request(url=link_)
            
            # print(f"{response=}")
            
        # author =  response.xpath("//h3[@class='author-title']/text()").get()
        
        # if author:
            
        yield {
            # "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
            "links": links
            # "author": self.start_urls[0]+link
            # "quote": quote.xpath("span[@class='text']/text()").get()
        }
        
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        
        if next_link:
            yield scrapy.Request(url=self.start_urls[0]+next_link)
# print(authors)


process = CrawlerProcess()
process.crawl(AuthorsSpider)
process.start()