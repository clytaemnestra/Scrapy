import scrapy


class AlzaSpider(scrapy.Spider):
    name = "alza"
    start_urls = ['https://www.alza.cz/herni-notebooky/18848814.htm']

    def parse(self, response):
        for products in response.css('div.box.browsingitem.js-box.canBuy.inStockAvailability'):
            try:
                yield {
                    'name': response.css('a.pc.browsinglink').attrib['data-impression-name'],
                    'description': products.css('div.Description::text').get().replace('\r', '').replace('\n', '').replace('\t', '').replace('"', ''),
                    'price': products.css('span.c2::text').get().replace('\xa0', '').replace(',-', '')
                }
            except:
                yield {
                    'name': response.css('a.pc.browsinglink').attrib['data-impression-name'],
                    'description': 'not available',
                    'price': 'not available'
                }

        next_page = response.css('a.next.fa.fa-chevron-right').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)