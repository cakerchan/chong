# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from the.items import TheItem
import re


class Lacspider(scrapy.Spider):
    name = 't'
    all_domain = ['https://www.the-scientist.com']
    start_urls = ['https://www.the-scientist.com/?articles.list/tagNo/14/tags/techniques/pageNo/{}/'.format(i) for i in range(1, 40)]
    #r1 = ['https://newtelegraphonline.com/category/saturday-magazine/page/{}'.format(i) for i in range(1, 101)]
    #r2 = ['https://newtelegraphonline.com/category/sunday-magazine/page/{}'.format(i) for i in range(1, 227)]
    #start_urls = r1 + r2
    def parse(self, response):
        sel = Selector(response)
        try:
            link = sel.xpath('//h4/a/@href').extract()
            for url in link:
                urls = 'https://www.the-scientist.com'+url
                print urls
                yield Request(urls, callback=self.parse_content)
        except Exception as e:
            print '错误原因：', e

    def parse_content(self, response):
        item = TheItem()
        sel2 = Selector(response)
        try:
            title = sel2.xpath('//h1[@itemprop="name"]/text()').extract()
            if not title:
                item['title'] = ['']
            else:
                item['title'] = title
            des = sel2.xpath('//p[@itemprop="description"]').extract()
            if not des:
                item['des'] = ['']
            else:
                item['des'] = des
            img =sel2.xpath('//span[@class="imageBlock"]/img/@src').extract()
            if not img:
                item['image_urls'] = ['']
            else:
                listurl1 = sorted(set(img))
                ilist = []
                for ims in listurl1:
                    imgurl = 'https://www.the-scientist.com' + ims
                    ilist.append(imgurl)
                item['image_urls'] = ilist
            article = sel2.xpath('//div[@itemprop="articleBody"]').extract()
            if not article:
                item['article'] = ['']
            else:
                dalist = []
                for ar in article:
                    tj = 'href="'
                    tj2 = '<img'
                    if tj2 in ar:
                        yyurl = 'http://www.actualites-les.com/static/images/the'
                        data1 = re.sub('(?<=src=").*?(?=/[^/]*")', yyurl, ar)
                    else:
                        data1 = ar
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
            now = datetime.datetime.now()
            bb = now.strftime('%Y-%m-%d')
            cc = str(bb)
            listd = []
            listd.append(cc)
            item['datime'] = listd
            item['img'] = ['']
            item['category'] = ['tech']
            yield item


        except Exception as e:
            print '内容解析错误原因：', e