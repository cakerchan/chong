# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from len.items import LenItem


class Lenspider(scrapy.Spider):
    name = 'societe'
    all_domain = ['http://lenouvelliste.com']
    a = 'http://lenouvelliste.com/societe'
    b = '?'
    c = 'page='
    start_urls = [a + b + c + '{}'.format(i) for i in range(1, 218)]

    def parse(self, response):
        sel = Selector(response)
        try:
            link = sel.xpath('//div[@class="content_widget"]/h2/a/@href').extract()
            for url in link:
                yield Request(url, callback=self.parse_content)
        except Exception as e:
            print '错误原因：', e

    def parse_content(self, response):
        item = LenItem()
        sel2 = Selector(response)
        item['image_urls'] = sel2.xpath(r'//div[@class="content_banner"]/*/img/@src').extract()
        item['category'] = ['societe']
        img = sel2.xpath(r'//div[@class="content_banner"]/*/img').extract()
        a = ''.join(img)
        list = []
        list.append(a)

        des = sel2.xpath('//div[@class="detail_content_area"]/i/text()').extract()
        a = ''.join(des)
        list1 = []
        list1.append(a)

        try:
            now = datetime.datetime.now()
            bb = now.strftime('%Y-%m-%d')
            cc = str(bb)
            listd = []
            listd.append(cc)
            item['datime'] = listd
            item['title'] = sel2.xpath('//div[@class="detail_content_area"]/h2/text()').extract()
            item['article'] = sel2.xpath('//div[@class="detail_content_area"]/article').extract()
            if '' in list1:
                item['des'] = ['']
            else:
                item['des'] = list1
            if '' in list:
                item['img'] = ['']
            else:
                item['img'] = list
            yield item


        except Exception as e:
            print '内容解析错误原因：', e



