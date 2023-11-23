from concurrent.futures.thread import ThreadPoolExecutor
import scrapy
import json
import os

all_products = []

class BallsSpider(scrapy.Spider):

    custom_settings = {
        'LOG_LEVEL': 'ERROR',
    }

    name = "balls"
    allowed_domains = ["bombkarnia.pl"]
    start_urls = ['https://bombkarnia.pl/sklep/']

    def parse(self, response):
        pages_amount = int(response.css('div.container nav.woocommerce-pagination ul.page-numbers li a::text').extract()[-1])

        products = response.css('div.products')
        for p in products.xpath('./div'):
            product_link = p.css('.box-text .title-wrapper .name a::attr(href)').get()
            yield scrapy.Request(product_link, callback=self.parse_product)


        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            # Write to file
            if not os.path.exists('../results'):
                os.makedirs('../results')

            with open('../results/products.json', 'w', encoding='utf-8') as f:
                json.dump(all_products, f, indent=4, ensure_ascii=False, separators=(',', ': '))

    def parse_product(self, response):
        product_link = response.request.url
        product_name = response.css('h1.product-title::text').get()
        product_price = response.css('p.price .amount bdi::text').get()
        product_sku = response.css('span.sku_wrapper .sku::text').get()
        product_categories = response.css('span.posted_in a::text').getall()
        product_tags = response.css('span.tagged_as a::text').getall()
        product_short_description = response.css('div.product-short-description p::text').get()
        product_description = response.css('div.woocommerce-Tabs-panel--description p::text').getall()
        
        product_images_html = response.css('div.woocommerce-product-gallery__image a')
        product_images = []
        for image_html in product_images_html.xpath('./img'):
            product_images.append(image_html.css('::attr(data-src)').get())

        product = {
            'link': product_link,
            'name': product_name.replace('–', '-').replace('\n','').replace('\t', ''),
            'price': product_price.replace(' ', ''),
            'sku': product_sku.replace('SKU:', '').replace(' ', ''),
            'categories': product_categories,
            'tags': product_tags,
            'short_description': product_short_description,
            'description': '\n\n'.join(product_description),
            'images': product_images
        }

        all_products.append(product)

