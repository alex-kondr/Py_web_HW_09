import json

import requests
from bs4 import BeautifulSoup


url = "https://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

quotes = soup.find_all("span", class_="text")
authors = soup.find_all(class_="author")
tags = soup.find_all(class_="tags")

quotes_for_json = []

for i, quote in enumerate(quotes):
    tags_for_quote = tags[i].find_all(class_="tag")
    
    tags_ = []
    
    for tag_for_quote in tags_for_quote:
        tags_.append(tag_for_quote.text)
    
    
    quotes_for_json.append({
        "tags": tags_,
        "author": authors[i].text,
        "quote": quote.text
    })
    
with open("quotes.json", "w", encoding="utf-8") as file:
    json.dump(quotes_for_json, file) 
