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
                itemName = tmpli.css("a:nth-child(1)::text").get()
                itemLinks = [tmpli.css(r"a:nth-child({0})::attr(href)".format(j)).get() for j in range(3, 6)]

                # add the item to the tree
                if topSubject not in subjectTree:
                    subjectTree[topSubject] = []
                subjectTree[topSubject].append(itemName)
                subjectLinks[itemName] = response.urljoin(itemLinks[1])

                # if the item include something
                tmpTextList = tmpli.css("::text").getall()
                tmpStr = "".join(tmpTextList)
                if tmpStr.find("includes") != -1:
                    aList = tmpli.css("a")
                    for j in range(5, len(aList)):
                        subitemName = aList[j-1].css("::text").get()
                        subitemLink = aList[j-1].css("::attr(href)").get()

                        # add the subitems to the tree
                        if itemName not in subjectTree:
                            subjectTree[itemName] = []
                        subjectTree[itemName].append(subitemName)
                        subjectLinks[subitemName] = response.urljoin(subitemLink)

                        # 爬取数据
                        yield scrapy.http.Request(response.urljoin(subitemLink), callback=self.parse_pages)

    def parse_pages(self, response):
        # 看一下一共有多少页 selector=#dlpage > small:nth-child(4) /html/body/div[5]/div/small[1]  
        entnumText = response.css(r'#dlpage > small:nth-child(4)::text').get()
        entNum = int(entnumText.split(" ")[3], base=10)

        # 直接一页展示
        onepageUrl = r"pastweek?skip={0}&show={1}".format(0, entNum)
        onepageUrl = "{0}{1}".format(response.url.replace("recent", ""), onepageUrl)

        yield scrapy.http.Request(onepageUrl, callback=self.parse_entries)


    def parse_entries(self, response):
        # 获取上周所有论文的人abs链接地址 selector=#dlpage > dl > dt
        entriesList = response.css(r'#dlpage > dl > dt')

        # 获取论文链接地址 并爬取摘要信息 #dlpage > dl:nth-child(9) > dt:nth-child(1) > span > a:nth-child(1)
        for tmpentry in entriesList:
            entUrl = tmpentry.css(r"span > a:nth-child(1)::attr(href)").get()

            # 根据链接，爬取论文摘要信息
            yield scrapy.Request(response.urljoin(entUrl), callback=parse_abs)

    def parse_abs(self, response):

        # 爬取论文的数据信息
        absUrl = response.url
        pdfUrl = response.css(r"#abs-outer > div.extra-services > div.full-text > ul > li:nth-child(1) > a ::attr(href)").get()
        title = response.css(r"#abs > h1 ::text").getall()[1]
        authors = response.css(r"#abs > div.authors > a ::text").getall()
        absText = response.css(r"#abs > blockquote ::text").getall()[2].replace('\n', '').strip()
        comments = response.css(r"#abs > div.metatable > table  > tr:nth-child(1) > td.tablecell.comments.mathjax ::text").get()
        subjects = response.css(r"#abs > div.metatable > table > tbody > tr:nth-child(2) > td.tablecell.subjects ::text").getall()
        submitDate = response.css(r"#abs-outer > div.leftcolumn > div.submission-history ::text").getall()[6]
        updateDate = response.css(r"#abs-outer > div.leftcolumn > div.submission-history ::text").getall()[-1]

        # 简单清洗数据，去除所有的换行
        title = title.replace('\n', '')
        authors = [tmp.replace('\n', '') for tmp in authors]
        comments = comments.replace('\n', '')
        subjects = [tmp.replace('\n', '') for tmp in subjects]


        # 返回数据
        return {'absUrl': absUrl, 'pdfUrl': pdfUrl, 'title': title, 'authors': authors, 'absText': absText, 
        'comments': comments, 'subjects': subjects, 'submitDate': submitDate, 'updateDate': updateDate}
