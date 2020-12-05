# -*- coding: utf-8 -*-
import scrapy


class TodaypapersSpider(scrapy.Spider):
    name = 'TodayPapers'
    allowed_domains = ['https://arxiv.org//']
    start_urls = ['https://arxiv.org//']

    def parse(self, response):
        # get all subject names
        subjectNames = response.css('#content > h2::text').getall()
        if 'About arXiv' in subjectNames:
            subjectNames.remove('About arXiv')

        # build the subject Tree 
        subjectTree = {}
        topicItems  = response.css('#content > ul > li')
        
        for tmpTopic in topicItems:
            topicName = tmpTopic.xpath('a').extract_first().text

            topicLink = tmpTopic.xpath('a').extract_first().attr('href')


            # get the topic name 
            

            # get the topic link 

        # get name and links of all subjects
        subjectOptions = {}
        optionsSelectors = response.css('#search-category > option')
        for tmpOption in optionsSelectors:
            tmpSubjectName = tmpOption.css('::text').get()
            # clear \n and space 
            tmpSubjectName = tmpSubjectName.strip().replace('\n', '')

            tmpSubjectLink = tmpOption.css('::attr(data-url)').get()
            subjectOptions[tmpSubjectName] = tmpSubjectLink

        # for each link, get data of the paper
        for tmpSubjectName, tmpSubjectLinks in subjectOptions:
            yield scrapy.Request(tmpSubjectLinks, callback=self.parse_pages)
        

    def parse_pages(self, reponse):
        pass
        
