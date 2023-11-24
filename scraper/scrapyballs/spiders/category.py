import scrapy
import json
import os

class CategorySpider(scrapy.Spider):

    custom_settings = {
        'LOG_LEVEL': 'ERROR',
    }

    name = "category"
    allowed_domains = ["bombkarnia.pl"]
    start_urls = ['https://bombkarnia.pl/sklep/']

    def parse(self, response):
        categories = {}
        all_links = []

        categories_menu = response.css('ul.product-categories')
        for category in categories_menu.xpath('./li'):
            category_name = category.css('a::text').get()
            categories[category_name] = {}

            subcategories = []
            for subcategory in category.xpath('./ul/li'):
                subcategory_name = subcategory.css('a::text').get()
                subcategories.append(subcategory_name)
                
                subsubcategories = []
                for subsubcategory in subcategory.xpath('./ul/li'):
                    subsubcategory_name = subsubcategory.css('a::text').get()
                    subsubcategories.append(subsubcategory_name)
            
                categories[category_name].update({
                    subcategory_name: subsubcategories
                })

        # Write to file
        if not os.path.exists('../results'):
            os.makedirs('../results')

        with open('../results/categories.json', 'w', encoding='utf-8') as f:
            json.dump(categories, f, indent=4, ensure_ascii=False)
