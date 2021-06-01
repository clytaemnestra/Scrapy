import scrapy


class AlzaSpider(scrapy.Spider):
    name = "czc"
    start_urls = ['https://www.czc.cz/notebooky/produkty']

    def parse(self, response):
        for products in response.css('div.new-tile'):
            try:
                yield {
                    'name': response.xpath('//*[@id="tiles"]/div[1]/div[2]/div[1]/h5/a/text()').get().replace('\n', ''),
                    'description': response.css('div.desc::text').get(),
                    'price': products.css('span.price-vatin::text').get().replace('\xa0', '').replace('Kč', '')
                }
            except:
                yield {
                    'name': response.xpath('//*[@id="tiles"]/div[1]/div[2]/div[1]/h5/a/text()').get().replace('\n', ''),
                    'description': 'not available',
                    'price': 'not available'
                }

        next_page = response.css('a.page-next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)