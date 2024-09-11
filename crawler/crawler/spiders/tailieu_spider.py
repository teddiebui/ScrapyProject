import scrapy
import urllib.parse
import re
from pathlib import Path

class TaiLieuSpider(scrapy.Spider):
    BASE_URL = "https://tailieu.vn/tim-kiem"
    
    name= "tailieu"
    allowed_domain = ["tailieu.vn"]
    start_urls = []
    
    def __init__(self, keyword=None, *args, **kwargs):
        super(TaiLieuSpider, self).__init__(*args, **kwargs)
        if keyword:
            encoded_keyword = urllib.parse.quote(keyword)
            self.start_urls.append(f"{self.BASE_URL}/{encoded_keyword}.html")
        else:
            raise Exception("thieu keyword")
    
    #mimic lai real user
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.3,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        # Add proxy neu can
        # 'HTTPPROXY_ENABLED': True,
        # 'HTTPPROXY_PROXY': 'http://yourproxy:port',
    }
    
    def parse(self, response):
        
        self.log(f"HEHE: {self.start_urls[0]}")
        search_result = response.css('#loaddoc li a.titga::attr(href)').getall() 
        if search_result:
            for url in search_result:
                yield response.follow(url, callback=self.extract_document_link)
    
    def extract_document_link(self, response):
        #trich xuat link file PDF
        body = response.body.decode()
        search_result = re.search(r"iframe.*?id=[\'\"]loaddocdetail2[\'\"].*?src=\"https.*?(https.*?.\w+)\"", body, re.S|re.I)
        if search_result:
            tailieu_source = search_result.group(1)
            if tailieu_source:
                yield response.follow(tailieu_source, callback=self.save_document)
    
    def save_document(self, response):
        
        #tai noi dung PDF va luu ve local computer
        
        filename = response.url.split('/')[-1].split('?')[0]  #trich xuat ten file
        path = Path("document") / filename 
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            f.write(response.body)
            
        self.log(f'Saved file {path}')
        
        