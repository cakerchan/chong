# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from phy.items import PhyItem
import re


class Lacspider(scrapy.Spider):
    name = 'ph'
    all_domain = ['']
    #start_urls = ['http://physicsworld.com/cws/channel/news/news/{}'.format(i) for i in range(827, 829)]
    start_urls = ['http://physicsworld.com/cws/channel/news/news/{}'.format(i) for i in range(1, 5326)]
    #r1 = ['https://newtelegraphonline.com/category/saturday-magazine/page/{}'.format(i) for i in range(1, 101)]
    #r2 = ['https://newtelegraphonline.com/category/sunday-magazine/page/{}'.format(i) for i in range(1, 227)]
    #start_urls = r1 + r2
    def parse(self, response):
        sel = Selector(response)
        try:
            link = sel.xpath('//h3[@class="withStrapline"]/a/@href').extract()
            for url in link:
                urls = 'http://physicsworld.com'+url
                print urls
                yield Request(urls, callback=self.parse_content)
        except Exception as e:
            print '错误原因：', e

    def parse_content(self, response):
        item = PhyItem()
        sel2 = Selector(response)
        try:
            title = sel2.xpath('//h1[@class="articleHeadline"]/text()').extract()
            if not title:
                item['title'] = ['']
            else:
                item['title'] = title
            now = datetime.datetime.now()
            bb = now.strftime('%Y-%m-%d')
            cc = str(bb)
            listd = []
            listd.append(cc)
            item['datime'] = listd
            item['des'] = ['']
            item['img'] = ['']
            item['category'] = ['news']
            data = sel2.xpath('//div[@class="articleBody"]').extract()
            imgurls = sel2.xpath(r'//a[@class="thickbox"]/@href').extract()
            if not imgurls:
                item['image_urls'] = ['']
            else:
                listurl1 = sorted(set(imgurls))
                item['image_urls'] = listurl1
            if not data:
                item['article'] = ['']
            else:
                dalist = []
                for da in data:
                    tj = 'href="'
                    tj2 = '<img'
                    if tj2 in da:
                        yyurl = 'http://www.actualites-les.com/static/images/phy'
                        th = re.sub('((?<=src=")(.*?)(?=/[^/]*"))',yyurl,da)
                        th2 = re.sub('<div class="articleThumbnailCentre">.*?<img', '<img', th)
                        data1 = re.sub('</a>.*?</div>', '</div>', th2)
                    else:
                        data1 = da
                    if tj in data1:
                        datas1 = re.sub('<a[\s\S]*?>', '', data1)
                        data2 = re.sub('</a>', '', datas1)
                        data11 = ''.join(data2)
                        dalist.append(data11)
                    else:
                        data2 = data1
                        data11 = ''.join(data2)
                        dalist.append(data11)
                item['article'] = dalist
            yield item


        except Exception as e:
            print '内容解析错误原因：', e
