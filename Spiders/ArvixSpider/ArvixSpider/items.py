# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArvixspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 论文名字
    title = scrapy.Field()
    # 作者列表
    authors = scrapy.Field()
    # 文章摘要
    abstract = scrapy.Field()
    # 上传日期
    uploadDate = scrapy.Field()
    # 最后更新日期
    updateDate = scrapy.Field()
    # 评论
    comments = scrapy.Field()
    # 领域
    subjects = scrapy.Field()
    # 摘要链接
    absLink = scrapy.Field()
    # pdf下载链接
    pdfLink = scrapy.Field()
    
