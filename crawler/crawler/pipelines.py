# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import json
class CrawlerPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    
    DATA_FILENAME = "data.json"
    
    def __init__(self):
        self.seen_id = set()
        self.data = []
    
    def open_spider(self, spider):
        #init task here
        pass
        
    def close_spider(self, spider):
        #destroy task here
        with open(self.DATA_FILENAME, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.data, ensure_ascii=False))

    def process_item(self, item, spider):
        #loc duplicate
        adapter = ItemAdapter(item)
        if adapter['created_time'] in self.seen_id:
            #DROP
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.seen_id.add(adapter['created_time'])
            self.data.append(item)
            return item