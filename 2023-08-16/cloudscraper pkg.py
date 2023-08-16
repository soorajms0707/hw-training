import cloudscraper

url="https://wordpress.com/"
scraper=cloudscraper.create_scraper()

response=scraper.get(url)
content=response.content

print(content)