import scrapy


class CompanyItem(scrapy.Item):
    # 公司信息
    id = scrapy.Field()
    name = scrapy.Field()
    industry = scrapy.Field()
    website = scrapy.Field()
    description = scrapy.Field()
    logo = scrapy.Field()


class PersonItem(scrapy.Item):
    # 人员信息
    id = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    companyId = scrapy.Field()
    parentId = scrapy.Field()


class NewsItem(scrapy.Item):
    # 新闻信息
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    source = scrapy.Field()
    personId = scrapy.Field()
