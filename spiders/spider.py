import scrapy
from goose import Goose
from pages.items.page import Page
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

class DoTBot(CrawlSpider):
    name = 'dotbot'
    allowed_domains = [
        'www.cnn.com',
        'www.usatoday.com',
        'www.nytimes.com'
    ]
    start_urls = [
        'http://www.cnn.com/politics',
        'https://www.usatoday.com/washington',
        'https://www.nytimes.com/pages/politics'
    ]

    # We only want to parse stuff on the index pages, but allow everything in politics
    rules = (
        Rule(LinkExtractor(allow=('/politics/', )), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.logger.info('Parsing Page: %s', response.url)

        extractor = Goose()
        article = extractor.extract(raw_html=response.body)

        itemLoader = ItemLoader(item=Page(), response=response)
        itemLoader.add_value('_id', response.url)
        itemLoader.add_value('url', response.url)
        itemLoader.add_value('title', article.title)
        itemLoader.add_value('publish_date', article.publish_date)
        itemLoader.add_value('description', article.meta_description)
        itemLoader.add_value('language', article.meta_lang)
        itemLoader.add_value('authors', article.authors)
        itemLoader.add_value('links', article.links)
        itemLoader.add_value('videos', article.movies)
        itemLoader.add_value('cleaned_text', article.cleaned_text)
        itemLoader.add_value('raw_html', article.raw_html)

        yield itemLoader.load_item()
        yield scrapy.Request(response.url, callback=self.parse_item)
