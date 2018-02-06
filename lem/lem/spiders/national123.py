# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from lem.items import LemItem
import urllib2
import re


class Lenspider(scrapy.Spider):
    name = 'interall'
    all_domain = ['http://www.lematindz.net']
    a1 = ['http://www.lematindz.net/algerie/index.{}.html'.format(i) for i in range(1, 95)]
    a2 = ['http://www.lematindz.net/algerie-france/index.{}.html'.format(i) for i in range(1, 60)]
    a3 = ['http://www.lematindz.net/debats-idees/index.{}.html'.format(i) for i in range(1, 109)]
    start_urls = a1 + a2 + a3


    def parse(self, response):
        sel = Selector(response)
        try:
            link = sel.xpath('//article[@class="linkbox"]/a/@href').extract()
            for url in link:
                urls = 'http://www.lematindz.net/' + url
                yield Request(urls, callback=self.parse_content)
        except Exception as e:
            print '错误原因：', e

    def parse_content(self, response):
        item = LemItem()
        sel2 = Selector(response)
        try:
            imgurls = sel2.xpath(r'//div[@class="head-image thumb-wrap relative"]/img/@src').extract()
            if not imgurls:
                item['image_urls'] = ['']
                list = ['']
            else:
                item['image_urls'] = imgurls
                list = []
                for imgurl in imgurls:
                    picname = imgurl.split('/')[-1]
                    list.append(picname)
            item['category'] = ['national']
            desf = sel2.xpath('//div[@class="col-sm-9"]/p').extract()
            if not desf:
                list1 = ['']
            else:
                for dea in desf:
                    tj = '<a href="'
                    if tj in dea:
                        dess1 = re.sub('<a.*?">', '', tj)
                        des = re.sub('</a>', '', dess1)
                    else:
                        des = desf
                a1 = ''.join(des)
                list1 = []
                list1.append(a1)
            now = datetime.datetime.now()
            bb = now.strftime('%Y-%m-%d')
            cc = str(bb)
            listd = []
            listd.append(cc)
            item['datime'] = listd
            title = sel2.xpath('//header/h1/text()').extract()
            item['title'] = ''.join(title)
            data = sel2.xpath('//*[@id="article_in"]').extract()
            for da in data:
                tiaojian = '<a href="'
                if tiaojian in da:
                    datas1 = re.sub('<a.*?">', '', da)
                    data1 = re.sub('</a>', '', datas1)
                else:
                    data1 = data
            article = data1
            item['article'] = ''.join(article)
            if '' in list1:
                item['des'] = ['']
            else:
                item['des'] = list1
            if '' in list:
                item['img'] = ['']

            else:
                imgl = []
                for tit in title:
                    tita = tit
                for imga in list:
                    imgadress = 'http://www.actualites-les.com/static/images/national/' + imga
                    img = '<img src="' + imgadress + '" width="600" height="350" alt="' + tita + '">'
                    a = ''.join(img)
                    imgl.append(a)
                item['img'] = imgl
            yield item


        except Exception as e:
            print '内容解析错误原因：', e
