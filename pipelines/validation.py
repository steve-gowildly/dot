from scrapy.exceptions import DropItem


class PageValidationPipeline(object):

    def process_item(self, item, spider):
        # Check to make sure the page has content before saving. We don't save transition/index pages
        #if item['author']:
            return item
        #else:
        #    raise DropItem("Page does not contain content: %s" % item)