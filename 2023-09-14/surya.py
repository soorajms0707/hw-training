import requests
from parsel import Selector
import csv

class Bayutscraper:
    def __init__(self,max_pages=2084):
        self.start_url = "https://www.bayut.com/to-rent/property/dubai/"
        self.duplicate_urls = set()
        self.counter = 0
        self.page_counter = 2
        self.max_pages = max_pages

    def start(self):
        
        response = requests.get(self.start_url)
        if response.status_code == 200:
            selector = Selector(text=response.text)
            self.parse(selector)

    def parse(self, selector):
        while self.page_counter <=self.max_pages:

    
            apartment = selector.css('article.ca2f5674')
            
            for apartments in apartment:
                relative_url = apartments.css('._4041eb80 a ::attr(href)').get()
                full_url = "https://www.bayut.com/" + relative_url
                if full_url not in self.duplicate_urls:
                    self.duplicate_urls.add(full_url)
                    
                    print(full_url)

                    response = requests.get(full_url)
                    if response.status_code == 200:
                        product_selector = Selector(text=response.text)
                        self.parse_property_page(product_selector, response)
                else:
                    print(full_url)
                    with open("bayutduplicatedata_urls2.txt", "a") as file:
                        file.write(full_url + "\n")

    
                         

            next_page_url = selector.css('[title="Next"] ::attr(href)').get()
            self.page_counter += 1
            if next_page_url:
                next_page_url = f'https://www.bayut.com/{next_page_url}'
                print(next_page_url)

            

                response = requests.get(next_page_url)
                
                if response.status_code == 200:
                    selector = Selector(text=response.text)
                else:
                    print(f"Error fetching {next_page_url}. Status code: {response.status_code}")

            else:
                print("Scraping finished. No next page found.")
                break
                    # self.parse(selector)


    def parse_property_page(self ,selector,response):
        data ={
        'property_link' : response.url,
        'property_id': selector.xpath("//*[contains(@class, '_033281ab')]//*[@aria-label='Reference']/text()").get(),
        'purpose': selector.xpath("//*[contains(@class, '_033281ab')]//*[@aria-label='Purpose']/text()").get(),
        'type': selector.xpath("//*[contains(@class, '_033281ab')]//*[@aria-label='Type']/text()").get(),
        'added_on': selector.xpath("//*[contains(@class, '_033281ab')]//*[@aria-label='Reactivated date']/text()").get(),
        'furnishing':  selector.xpath("//*[contains(@class, '_033281ab')]//*[@aria-label='Furnishing']/text()").get(),
        'price':  {
            'currency' : selector.xpath("//*[contains(@class, 'c4fc20ba')]//*[contains(@class, 'e63a6bfb')]/text()").get(),
            'amount' : selector.xpath("//*[contains(@class, 'c4fc20ba')]//*[contains(@class, '_105b8a67')]/text()").get(),
        },
        'location' :  selector.xpath("//*[contains(@class, '_1f0f1758')]/text()").get(),
        'bed_bath_size':  {
            'bedrooms' : selector.xpath("//*[@aria-label='Beds']//*[contains(@class, 'fc2d1086')]/text()").get(),
            'bathrooms' : selector.xpath("//*[@aria-label='Baths']//*[contains(@class, 'fc2d1086')]/text()").get(),
            'size' : selector.xpath("//*[contains(@class, 'fc2d1086')]//span/text()").get(),
        },
        'agent_name' :  selector.xpath("//*[contains(@class, '_63b62ff2')]//*[contains(@class, 'f730f8e6')]/text()").get(),
        'img_url' :  selector.xpath('//*[@aria-label="Property image"]//*[@class="bea951ad"]/@src').get(),
        'breadcrumbs': ' > '.join(selector.xpath('//*[@aria-label="Breadcrumb"]//*[contains(@class, "_327a3afc")]/text()').getall()),
        'amenities' : selector.xpath("//*[contains(@class, '_40544a2f')]//*[contains(@class, '_005a682a')]/text()").getall(),
        'description' : ', '.join([size.strip() for size in selector.xpath("//*[contains(@class, '_96aa05ec')]//*[contains(@class, '_2a806e1e')]/text()").getall()]),
        }

           
        self.save_to_csv(data)
        self.counter += 1
            


    def save_to_csv(self, data):
        filename = "bayut_fulldata2.csv"
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if self.counter == 0:
                writer.writeheader()  # Write the header only if it's the first time
            writer.writerow(data)
        # print(filename)


if __name__ == "__main__":
    scraper = Bayutscraper(max_pages=2084)
    scraper.start()