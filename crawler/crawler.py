import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from db import db

crawler_col = db['crawler']

class MySpider(CrawlSpider):
    name = 'uva.nl'
    allowed_domains = ['uva.nl']
    start_urls = ['http://www.uva.nl/onderwijs/bachelor/bacheloropleidingen/bacheloropleidingen.html']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        filename = response.url.split("/")[-2] + '.html'
        print(response.body)
        d = {
            "url": response.url,
            "title": response.xpath('//title/text()').extract()[0],
            #"keywords": response.xpath("//meta[@name='keywords']/@content")[0].extract(),
            "raw": str(response.body)
        }
        x = crawler_col.insert_one(d)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(MySpider)
process.start() # the script will block here until the crawling is finished
