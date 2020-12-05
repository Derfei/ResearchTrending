# -*- coding: utf-8 -*-
import scrapy


class GetarchivesSpider(scrapy.Spider):
    name = 'GetArchives'
    allowed_domains = ['https://arxiv.org/']
    start_urls = ['https://arxiv.org//']

    def parse(self, response):
        # get all subject, css selector is #search-category > option::text
        subjectOptions = {}
        optionsSelectors = response.css('#search-category > option')
        for tmpOption in optionsSelectors:
            tmpSubjectName = tmpOption.css('::text').get()
            # clear \n and space 
            tmpSubjectName = tmpSubjectName.strip().replace('\n', '')

            tmpSubjectLink = tmpOption.css('::attr(data-url)').get()
            subjectOptions[tmpSubjectName] = tmpSubjectLink