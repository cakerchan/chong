# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from challengs.items import ChallengsItem
import urllib2
import re


class Lenspider(scrapy.Spider):
    name = 'ceshi'
    all_domain = ['https://www.challenges.fr']
    # start_urls = ['https://www.challenges.fr/economie/page-{}'.format(i) for i in range(1, 301)]
    start_urls = ['https://www.challenges.fr/economie/page-{}'.format(i) for i in range(7, 9)]

    def parse(self, response):
        sel = Selector(response)
        try:
            link = sel.xpath('//div[@class="item"]/a/@href').extract()
            for url in link:
                # urls = 'http://www.lematindz.net/' + url
                yield Request(url, callback=self.parse_content)
        except Exception as e:
            print '错误原因：', e

    def parse_content(self, response):
        item = ChallengsItem()
        sel2 = Selector(response)
        try:
            data = sel2.xpath('//div[@itemprop="articlebody"]').extract()
            for da in data:
                body =da
                tj = '<a href="'
                tj2 = '</iframe>'
                tj3 = 'data-uri='
                tj4 = '<div class="right">'
                tj5 = '<li class="item"'
                tj6 = '<script async src='
                tj7 = '<img alt='
                tj8 = '</ul></div></div></div>'
                datas1 = re.sub('<a.*?">', '', da)
                datas2 = re.sub('</a>', '', datas1)
                if tj in body:
                    data1 = datas2
                    #print '有链接',data1
                else:
                    data1 = body
                    #print '无链接', data1
                if tj2 in data1:
                    data2 = re.sub(r'<iframe.*?</iframe>','',data1)
                    #print '有tj2------------data2', data2

                else:
                    data2 = data1
                    #print '无TJ2-----------', data1
                if tj3 in data2:
                    tj3a = re.findall('<div class="article-diaporama diapo-micro".*?</div>', data2)
                    tj8a = re.sub('<div class="article-diaporama diapo-micro".*?</ul></div></div></div>', '', data2)
                    if not tj8a:
                        data3 = tj3a
                        print '有tj3第一个------------data3',data3
                    else:
                        data3 = tj8a
                        print '有tj3第22222个------------data3',data3
                else:
                    data3 = data2
                if tj4 in data3:
                    data4 = re.sub('<div class="right">.*?</div>','',data3)
                    #print '有tj4------------data4',data4
                else:
                    data4 = data3
                if tj5 in data4:
                    data5 = re.sub('<ul><li class="item".*?</div>','',data4)
                    #print '有tj5------------data5', data5
                else:
                    data5 = data4
                    #print '这个是data5,看看显示什么',data5
                if tj6 in data5:
                    data6 = re.sub('<script.*?</script>','',data4)
                    #print '有tj6------------data6', data6
                else:
                    data6 = data5
                    #print '这个是data6,看看显示什么', data6
                if tj7 in data6:
                    #namepic = '<img alt="' + title '"'+ 'src="'+ url '">'
                    imgurl = re.findall('<img alt=.*?src="(.*?)".*?>',data6)

                    #print '有tj7------------data7', imgurl
                else:
                    data7 = data6
                    #print '这个是data6,看看显示什么', data7
            yield item

        except Exception as e:
            print '内容解析错误原因：', e



