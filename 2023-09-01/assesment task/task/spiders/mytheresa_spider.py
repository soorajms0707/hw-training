import scrapy
import json
import csv
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import dropbox
from dropbox.exceptions import ApiError, AuthError
import pymongo



DROPBOX_ACCESS_TOKEN = "sl.Bj4LaoqU-tCq1GsOxKcWLQs9xEJ3JpWXdp_3NGQiDQQ25Vl-kUNs-2fMDB6iPfY4Hxw5XUuxiek29o8LKIXPKgH8AIGZaCACH3P3wxBiD1kjqxc3sbRfXfgjz_-ug9SETF2idGy13mMExko"
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mytheresa_db"]
collection = db["products"]

class MyTheresaSpider(scrapy.Spider):
    name = "mytheresa"
    start_urls = ["https://www.mytheresa.com/int/en/men/shoes?rdr_src=mag"]
    counter = 0 
    url_data_mapping = {}  # To map URL to its extracted data

    def parse(self, response):
        product_urls_type1 = response.css(
            'div.list__container div.item.item--sale a.item__link::attr(href)').getall()
        product_urls_type2 = response.css(
            'div.list__container div.item.item a.item__link::attr(href)').getall()
        product_urls = product_urls_type1 + product_urls_type2

        # if self.counter == 0:
        #     header = [
        #         "Breadcrumb", "Image URL", "Brand", "Product Name", "Listing Price", "Offer Price",
        #         "Discount", "Product ID", "Sizes", "Description", "Other Images"
        #     ]
        #     self.save_to_csv(header)

        for index, url in enumerate(product_urls):
            yield response.follow(url, self.parse_product, priority=index)

        # Check if the counter has reached the limit
        if self.counter < 1000:
            next_page_url = response.css(
                'div.list__pagination div.pagination__item[data-label="nextPage"]::attr(data-index)').get()
            if next_page_url:
                next_page_url = response.urljoin(f'?page={next_page_url}')
                yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_product(self, response):
        def clean_data(value):
            if value:
                value = value.strip()
                value = value.replace("Item number: ", "")
                value = value.replace("<span class=\"pricing__prices__price\"> <!-- -->\u20ac", "€")
                value = value.replace("</span>", "")
            return value

        data = {
            "breadcrumb": [breadcrumb.strip() for breadcrumb in response.xpath('//div[@class="breadcrumb"]//a/text()').getall()],
            "image_url": response.xpath('//img[@class="product__gallery__carousel__image"]/@src').get(),
            "brand": clean_data(response.xpath('//a[contains(@class,"product__area__branding__designer__link")]/text()').get()),
            "product_name": clean_data(response.xpath('//div[@class="product__area__branding__name"]/text()').get()),
            "listing_price": clean_data(response.xpath('//span[@class="pricing__prices__original"]/span[@class="pricing__prices__price"]').get()),
            "offer_price": clean_data(response.xpath('//span[@class="pricing__prices__discount"]/span[@class="pricing__prices__price"]').get()),
            "discount": clean_data(response.xpath('//span[@class="pricing__info__percentage"]/text()').get()),
            "product_id_text": clean_data(response.xpath('//div[@class="accordion__body__content"]//li[last()]/text()').get()),
            "sizes": [size.strip() for size in response.xpath('//span[contains(@class, "sizeitem__label")]/text()').getall()],
            "description": clean_data(response.xpath('//div[@class="accordion__body__content"]//p/text()').get()),
            "other_images": response.xpath('//div[@class="item__images"]//img/@src').getall(),
        }

        if self.counter < 1000:
            yield data


            self.save_to_mongodb(data)
            self.save_to_json(data)
            self.save_to_csv(data)
            self.save_to_xml(data)
            self.upload_to_dropbox("output.json")
            self.upload_to_dropbox("output.csv")
            self.upload_to_dropbox("output.xml")

            with open("product_links.txt", "a") as file:
                file.write(response.url + "\n")

            self.counter += 1
            if self.counter >= 1000:
                self.log("Reached the response limit of 2. Stopping the spider")

    def save_to_json(self,data):
        filename = "output.json"
        # print(type(data))
        with open(filename, "a") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.write("\n")



    def save_to_csv(self, data):
        filename = "output.csv"
        if not os.path.exists(filename):
            header = [
                "Breadcrumb", "Image URL", "Brand", "Product Name", "Listing Price", "Offer Price",
                "Discount", "Product ID", "Sizes", "Description", "Other Images"
            ]
        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(data.values())

    def save_to_xml(self, data):
        root = ET.Element("products")
        product_element = ET.SubElement(root, "product")
        for key, value in data.items():
            sub_element = ET.SubElement(product_element, key.replace(" ", "_").lower())
            sub_element.text = str(value)

        xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
        filename = "output.xml"
        with open(filename, "ab") as file:
            file.write(xml_str.encode("utf-8"))

    def save_to_mongodb(self, data):
        response=collection.insert_one(dict(data))
        print(response)


    def upload_to_dropbox(self, filename):
        try:
            with open(filename, "rb") as file:
                dbx.files_upload(file.read(), f"/{filename}", mode=dropbox.files.WriteMode("overwrite"))
        except ApiError as e:
            print("Error uploading file to Dropbox:", e)