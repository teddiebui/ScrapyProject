import scrapy
import urllib.parse
import re
from pathlib import Path
from ..items import MediaItem

class TaiLieuSpider(scrapy.Spider):
    BASE_URL = "https://tailieu.vn/tim-kiem"
    
    name= "tailieu"
    allowed_domain = ["tailieu.vn"]
    start_urls = []
    
    def __init__(self, keywords=None, *args, **kwargs):
        super(TaiLieuSpider, self).__init__(*args, **kwargs)
        if keywords:
            keyword_list = [kw.strip() for kw in keywords.split(",")]
            self.log(f"KEYWORDS {keyword_list}" )
            for keyword in keyword_list:
                encoded_keyword = urllib.parse.quote(keyword)
                self.start_urls.append(f"{self.BASE_URL}/{encoded_keyword}.html")
        else:
            raise Exception("thieu keyword")
    
    #mimic lai real user
    # custom_settings = {
    #     Add proxy neu can
    #     'HTTPPROXY_ENABLED': True,
    #     'HTTPPROXY_PROXY': 'http://yourproxy:port',
    # }
    
    def parse(self, response):
        
        search_result = response.css('#loaddoc li a.titga::attr(href)').getall() 
        
        #khoi tao item
        item = MediaItem()
        
        if search_result:
            for url in search_result:
                yield response.follow(url, callback=self.extract_document_link, meta={"item": item})
    
    def extract_document_link(self, response):
        #trich xuat link file PDF
        
        #trich xuat item tu meta truoc
        item = response.meta["item"]
        item['created_time'] = re.findall(r"jQuery\(\'#idngay\'\)\.html\(\'(.*?)\'\)\;", response.text, re.S|re.I)[0]
        
        body = response.body.decode()
        search_result = re.search(r"iframe.*?id=[\'\"]loaddocdetail2[\'\"].*?src=\"https.*?(https.*?.\w+)\"", body, re.S|re.I)
        if search_result:
            tailieu_source = search_result.group(1)
            if tailieu_source:
                yield response.follow(tailieu_source, callback=self.save_document, meta={'item': item})
    
    def save_document(self, response):
        
        #tai noi dung PDF va luu ve local computer
        filename = response.url.split('/')[-1].split('?')[0]  #trich xuat ten file
        
        #trich xuat item tu meta truoc
        item = response.meta['item']
        
        #luu file local
        path = Path("document") / filename 
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            f.write(response.body)
        
        self.log(f'Saved file {path}')
        
        media_id = re.findall(r"(\d+)\.\w+$", filename)[0]
        media_name = filename.split(media_id)[0]
        
        content_type = response.headers.get('Content-Type').decode()
        mime_type = content_type.split(';')[0]
        
        item['updated_time'] = item['created_time'] #web khong hien thi ngay update
        item['media_name'] = media_name
        item['media_size'] = len(response.body)
        item['media_type'] = 'document'
        item['media_mime_type'] = mime_type
        
        item['media_url'] = response.url
        item['media_path'] = str(path)

        self.log(f'Item {item}')
        
        yield item
        
        
        