import scrapy
from company_crawler.items import CompanyItem, PersonItem, NewsItem
import json
import re

class CompanySpider(scrapy.Spider):
    name = 'company'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com/companies']
    
    # 模拟数据，实际项目中会从真实网站抓取
    def parse(self, response):
        # 模拟公司数据
        companies = [
            {
                "id": "1",
                "name": "宝洁公司",
                "industry": "日化",
                "website": "https://www.pg.com",
                "description": "全球最大的日用消费品公司之一",
                "logo": "https://example.com/pg_logo.png"
            },
            {
                "id": "2",
                "name": "联合利华",
                "industry": "日化",
                "website": "https://www.unilever.com",
                "description": "全球领先的日用消费品公司",
                "logo": "https://example.com/unilever_logo.png"
            },
            {
                "id": "3",
                "name": "欧莱雅",
                "industry": "美妆",
                "website": "https://www.loreal.com",
                "description": "全球最大的化妆品公司",
                "logo": "https://example.com/loreal_logo.png"
            },
            {
                "id": "4",
                "name": "苹果公司",
                "industry": "数码",
                "website": "https://www.apple.com",
                "description": "全球领先的科技公司",
                "logo": "https://example.com/apple_logo.png"
            },
            {
                "id": "5",
                "name": "可口可乐",
                "industry": "快消",
                "website": "https://www.coca-cola.com",
                "description": "全球最大的饮料公司",
                "logo": "https://example.com/coca_cola_logo.png"
            }
        ]
        
        # 生成公司Item
        for company in companies:
            company_item = CompanyItem()
            company_item['id'] = company['id']
            company_item['name'] = company['name']
            company_item['industry'] = company['industry']
            company_item['website'] = company['website']
            company_item['description'] = company['description']
            company_item['logo'] = company['logo']
            yield company_item
            
            # 模拟抓取公司人员信息
            yield scrapy.Request(
                f"https://example.com/company/{company['id']}/employees",
                callback=self.parse_employees,
                meta={'company_id': company['id']}
            )
    
    def parse_employees(self, response):
        company_id = response.meta['company_id']
        
        # 模拟人员数据
        employees = {
            "1": [
                {
                    "id": "111",
                    "name": "David Taylor",
                    "position": "CEO",
                    "phone": "123-456-7890",
                    "email": "david.taylor@pg.com",
                    "parentId": ""
                },
                {
                    "id": "121",
                    "name": "John Smith",
                    "position": "市场总监",
                    "phone": "123-456-7891",
                    "email": "john.smith@pg.com",
                    "parentId": "111"
                }
            ],
            "2": [
                {
                    "id": "211",
                    "name": "Alan Jope",
                    "position": "CEO",
                    "phone": "234-567-8901",
                    "email": "alan.jope@unilever.com",
                    "parentId": ""
                }
            ]
        }
        
        # 生成人员Item
        for employee in employees.get(company_id, []):
            person_item = PersonItem()
            person_item['id'] = employee['id']
            person_item['name'] = employee['name']
            person_item['position'] = employee['position']
            person_item['phone'] = employee['phone']
            person_item['email'] = employee['email']
            person_item['companyId'] = company_id
            person_item['parentId'] = employee['parentId']
            yield person_item
            
            # 模拟抓取人员新闻信息
            yield scrapy.Request(
                f"https://example.com/person/{employee['id']}/news",
                callback=self.parse_news,
                meta={'person_id': employee['id']}
            )
    
    def parse_news(self, response):
        person_id = response.meta['person_id']
        
        # 模拟新闻数据
        news = {
            "111": [
                {
                    "title": "宝洁公司CEO David Taylor宣布退休",
                    "url": "https://example.com/news1",
                    "date": "2023-05-15",
                    "source": "财经日报"
                }
            ],
            "121": [
                {
                    "title": "宝洁市场总监John Smith分享品牌策略",
                    "url": "https://example.com/news2",
                    "date": "2023-06-20",
                    "source": "营销杂志"
                }
            ],
            "211": [
                {
                    "title": "联合利华CEO Alan Jope推动可持续发展战略",
                    "url": "https://example.com/news3",
                    "date": "2023-07-10",
                    "source": "环保时报"
                }
            ]
        }
        
        # 生成新闻Item
        for item in news.get(person_id, []):
            news_item = NewsItem()
            news_item['title'] = item['title']
            news_item['url'] = item['url']
            news_item['date'] = item['date']
            news_item['source'] = item['source']
            news_item['personId'] = person_id
            yield news_item
