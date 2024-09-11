# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MediaItem(scrapy.Item):
    created_time = scrapy.Field()
    updated_time = scrapy.Field()
    media_name = scrapy.Field()
    media_size = scrapy.Field()
    media_type = scrapy.Field()
    media_mime_type = scrapy.Field()
    media_id = scrapy.Field()
    media_url = scrapy.Field()
    media_path = scrapy.Field()