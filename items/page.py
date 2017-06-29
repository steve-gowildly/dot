import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


"""
Adds carriage returns to each paragraph so we retain formatting for markup.
"""
def add_carriage_returns(doc):
    return doc + '\r\r'

"""
Keeps the link tags as those may help better understand the context.
"""
def remove_unimportant_tags(doc):
    return remove_tags(doc, keep=('a',))

"""
The class used to store all pages.
"""
class Page(scrapy.Item):
    _id = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        output_processor=TakeFirst()
    )
    publish_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        output_processor=TakeFirst()
    )
    language = scrapy.Field(
        output_processor=TakeFirst()
    )
    authors = scrapy.Field()
    links = scrapy.Field()
    videos = scrapy.Field()
    cleaned_text = scrapy.Field(
        output_processor=TakeFirst()
    )
    raw_html = scrapy.Field(
        output_processor=TakeFirst()
    )

