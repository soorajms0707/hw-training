import csv
import requests
from parsel import Selector
import os
import re  # Import the re module for regular expressions

class OLXScraper:
    def __init__(self):
        self.base_url = "https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723"
        self.page = 1
        self.counter = 0
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        self.max_listings = float('inf')  # Define the maximum number of listings to scrape
        self.unique_property_ids = set()  # Set to store unique property IDs

    def start(self):
        while self.counter < self.max_listings:
            url = f"{self.base_url}?page={self.page}"
            headers = {'User-Agent': self.user_agent}

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                selector = Selector(text=response.text)

                if self.parse_page(selector):
                    self.page += 1
                else:
                    print("No more data available.")
                    break

            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
                self.page += 1

    def parse_page(self, selector):
        listing_urls = selector.xpath('//li[contains(@class, "_1DNjI")]/a/@href').getall()

        if not listing_urls:
            return False  # No more listings on the page

        for relative_url in listing_urls:
            print(relative_url)
            absolute_url = 'https://www.olx.in' + relative_url
            headers = {'User-Agent': self.user_agent}

            try:
                response = requests.get(absolute_url, headers=headers)
                response.raise_for_status()
                property_selector = Selector(text=response.text)
                
                # Extract the property ID from the URL
                property_id = self.get_property_id_from_url(absolute_url)

                if property_id:
                    # Check if the property ID is already in the set
                    if property_id not in self.unique_property_ids:
                        self.unique_property_ids.add(property_id)
                        self.counter += 1
                    else:
                        # Skip this property as it's a duplicate
                        continue

                if self.counter >= self.max_listings:
                    break

                self.parse_property(property_selector, absolute_url, property_id)  # Pass property_id

            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")

        return True

    def parse_property(self, selector, absolute_url, property_id):
        price_amount = selector.xpath('//span[contains(@class, "T8y-z")]/text()').re_first(r'\d+')
        price_currency = '₹'
        data = {
            "property_name": selector.xpath('//h1[contains(@class, "_1hJph")]/text()').get(),
            "property_id": property_id,  # Use the extracted property_id
            "breadcrumbs": selector.xpath('//ol[contains(@class, "rui-2Pidb")]//li/a/text()').getall(),
            "price": {
                "amount": price_amount,
                "currency": price_currency,
            },
            "image_url": selector.xpath('//div[@class="_23Jeb"]/figure/img/@src').get(),
            "description": selector.xpath('//div[@data-aut-id="itemDescriptionContent"]/p/text()').get(),
            "seller_name": selector.xpath('//div[contains(@class, "eHFQs")]/text()').get(),
            "location": selector.xpath('//span[contains(@class, "_1RkZP")]/text()').get(),
            "property_type": selector.xpath('//span[contains(@class, "B6X7c")]/text()').get(),
            "bathrooms": selector.xpath('//span[@data-aut-id="value_bathrooms"]/text()').get(),
            "bedrooms": selector.xpath('//span[@data-aut-id="value_rooms"]/text()').get(),
            "property_url": absolute_url
        }

        self.save_to_csv(data)

    def get_property_id_from_url(self, url):
        # Use regular expression to extract the property ID (the "iid" portion) from the URL
        match = re.search(r'iid-(\d+)', url)
        if match:
            return match.group(1)
        return None

    def save_to_csv(self, data):
        filename = "output.csv"

        header = [
            "Property Name", "Property Id", "Breadcrumbs", "Price", "Image URL", "Description",
            "Seller Name", "Location", "Property Type", "Bathrooms", "Bedrooms", "Property URL"
        ]

        if not os.path.exists(filename):
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(header)

        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(data.values())
        print(filename)

if __name__ == '__main__':
    scraper = OLXScraper()
    scraper.start()