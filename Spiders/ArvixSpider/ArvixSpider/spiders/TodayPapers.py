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

        # build the subject Tree {phics: [High phic experiment, High phic thory], High phsic: []}
        subjectTree = {}
        # the link for each subject {phics: ['http://arxiv.org/phics/recent']}
        subjectLinks = {}

        # for each top subject css path is #content > ul:nth-child(3) #content > ul:nth-child(3) #content > ul:nth-child(5) #content > ul:nth-child(7) #content > ul:nth-child(17)
        for i, topSubject in enumerate(subjectNames):
            # the list of topsubjects
            itemList = response.css(r"#content > ul:nth-child({0})".format(3+i*2))

            # for each item, get the name of the item. If each item include some sub-items, add subitems to the tree
            liList = itemList.css("li")
            for tmpli in liList:
                # get the name of the item #main-astro-ph
                itemName = tmpli.css("a:nth-child(0)::text")
                itemLinks = [tmpli.css(r"a:nth-child({0})::attr(href)".format(j))for j in range(2, 5)]

                # add the item to the tree
                if topSubject not in subjectTree:
                    subjectTree[topSubject] = []
                subjectTree[topSubject].append(itemName)
                subjectLinks[itemName] = itemLinks

                # if the item include something
                if tmpli.css("::text").get().find("includes"):
                    aList = tmpli.css("a")
                    for j in range(5, len(aList)):
                        subitemName = aList[j-1].css("::text").get()
                        subitemLink = aList[j-1].css("::href").get()

                        # add the subitems to the tree
                        if itemName not in subjectTree:
                            subjectTree[itemName] = []
                        subjectTree[itemName].append(subitemName)
                        subjectLinks[subitemName] = subitemLink

        # tranverse the subjectTree and get the recent infomation of the paper list
        
        

    def parse_pages(self, reponse):
        pass
        
