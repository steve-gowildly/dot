# Tell the server who we are just in case something bad happens
USER_AGENT = 'dotbot (dotbot@gowildly.com)'
# Put in a 5 second delay to give the server time to respond
DOWNLOAD_DELAY = 1.0
# Let the server tell us how it's doing on performance
AUTOTHROTTLE_ENABLED = True
# Set the global pipelines for ingesting content
ITEM_PIPELINES = {
    'pipelines.validation.PageValidationPipeline': 0,
    'pipelines.datastore.MongoPipeline': 100,
}

# Set for development only
HTTPCACHE_ENABLED = True