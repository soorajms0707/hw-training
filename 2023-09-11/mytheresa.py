import requests
from parsel import Selector
import csv


class MyTheresaScraper:
    def __init__(self):
        self.start_url = "https://www.mytheresa.com/int/en/men/shoes?rdr_src=mag"
        self.counter = 0
        self.duplicate_urls = set()
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        
    def start(self):
        headers = {'User-Agent': self.user_agent}
        response = requests.get(self.start_url, headers=headers)
        print(response.status_code)
        print(response.reason)
        if response.status_code == 200:
            selector = Selector(text=response.text)
            self.parse(selector)
            
    def parse(self, selector):
        product_urls_type1 = selector.css(
            'div.list__container div.item.item--sale a.item__link::attr(href)').getall()
        product_urls_type2 = selector.css(
            'div.list__container div.item.item a.item__link::attr(href)').getall()
        product_urls = product_urls_type1 + product_urls_type2

        for url in product_urls:
            headers = {'User-Agent': self.user_agent}
            full_url = "https://www.mytheresa.com"+url
            if full_url not in self.duplicate_urls:
                self.duplicate_urls.add(full_url)
                print(full_url)
                
                response = requests.get(full_url,headers=headers)
                if response.status_code == 200:
                    product_selector = Selector(text=response.text)
                    self.parse_product(product_selector,response)
            else:
                with open("mytheresa_duplicate_urls.txt", "a") as file:
                    file.write(full_url + "\n")



        next_page_url = selector.css(
            'div.list__pagination div.pagination__item[data-label="nextPage"]::attr(data-index)').get()
        if next_page_url:
            next_page_url = f'https://www.mytheresa.com/int/en/men/shoes?page={next_page_url}'
            print(next_page_url)
            headers = {'User-Agent': self.user_agent}
            response = requests.get(next_page_url, headers=headers)
            if response.status_code == 200:
                selector = Selector(text=response.text)
                self.parse(selector)

    def parse_product(self, selector, response):
        def clean_data(value):
            if value:
                value = value.strip()
                value = value.replace("Item number: ", "")
                value = value.replace("<span class=\"pricing__prices__price\"> <!-- -->â¬", "€")
                value = value.replace("â¬", "€")
                value = value.replace("</span>", "")
            return value

        data = {
            "product_url":response.url,
            "breadcrumb": [breadcrumb.strip() for breadcrumb in selector.xpath('//div[@class="breadcrumb"]//a/text()').getall()],
            "image_url": selector.xpath('//img[@class="product__gallery__carousel__image"]/@src').get(),
            "brand": clean_data(selector.xpath('//a[contains(@class,"product__area__branding__designer__link")]/text()').get()),
            "product_name": clean_data(selector.xpath('//div[@class="product__area__branding__name"]/text()').get()),
            "listing_price": clean_data(selector.xpath('//span[@class="pricing__prices__original"]/span[@class="pricing__prices__price"]').get()),
            "offer_price": None,
            "discount": clean_data(selector.xpath('//div[@class="productinfo__extradiscount"]/text()').get()),
            "product_id_text": clean_data(selector.xpath('//div[@class="accordion__body__content"]//li[last()]/text()').get()),
            "sizes": [size.strip() for size in selector.xpath('//span[contains(@class, "sizeitem__label")]/text()').getall()],
            "description": clean_data(selector.xpath('//div[@class="accordion__body__content"]//p/text()').get()),
            "other_images": selector.xpath('//div[@class="item__images"]//img/@src').getall(),
        }
        
        

      
        self.save_to_csv(data)
        self.counter += 1



    def save_to_csv(self, data):
        filename = "output_mytheresa.csv"
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if self.counter == 0:
                writer.writeheader()
            writer.writerow(data)
        print(filename)


if __name__ == "__main__":
    scraper = MyTheresaScraper()
    scraper.start()