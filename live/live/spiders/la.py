# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from live.items import LiveItem
import re


class Lacspider(scrapy.Spider):
    name = 'live'
    all_domain = ['https://newtelegraphonline.com']
    #start_urls = ['https://newtelegraphonline.com/category/news/page/{}'.format(i) for i in range(1, 1757)]
    r1 = ['https://newtelegraphonline.com/category/saturday-magazine/page/{}'.format(i) for i in range(1, 101)]
    r2 = ['https://newtelegraphonline.com/category/sunday-magazine/page/{}'.format(i) for i in range(1, 227)]
    start_urls = r1 + r2
    def parse(self, response):
        sel = Selector(response)
        try:
            link = sel.xpath('//h2[@class="entry-title"]/a/@href').extract()
            for url in link:
                yield Request(url, callback=self.parse_content)
        except Exception as e:
            print '错误原因：', e

    def parse_content(self, response):
        item = LiveItem()
        sel2 = Selector(response)
        try:
            imgurls = sel2.xpath(r'//figure[@class="single-thumb single-thumb-full"]/img/@src').extract()
            if not imgurls:
                list = ['']
                item['image_urls'] = list
            else:
                listurl1 = []
                list = []
                for imgurl in imgurls:
                    picname1 = imgurl.split('?')[-2]
                    picurl = ''.join(picname1)
                    listurl1.append(picurl)
                    picname2 = picname1.split('/')[-1]
                    list.append(picname2)
                item['image_urls'] = listurl1
            desf = sel2.xpath('//div[@class="entry-content"]/ul').extract()
            list1 = []
            if not desf:
                list1 = ['']
            else:
                for dea in desf:
                    tj = '<a href="'
                    if tj in dea:
                        dess1 = re.sub('<a.*?">', '', dea)
                        des = re.sub('</a>', '', dess1)
                        a1 = ''.join(des)
                        list1.append(a1)
                    else:
                        des = dea
                        a1 = ''.join(des)
                        list1.append(a1)
            now = datetime.datetime.now()
            bb = now.strftime('%Y-%m-%d')
            cc = str(bb)
            listd = []
            listd.append(cc)
            item['datime'] = listd
            title = sel2.xpath('//h1[@class="entry-title"]/text()').extract()
            item['title'] = title
            item['category'] = ['news']
            data = sel2.xpath('//div[@class="entry-content"]/p').extract()
            listae = []
            dalist = []
            for da in data:
                tj = '<a href="'
                tj2 = '<img'
                tj3 = '<p><iframe'
                tj4 = '<p style='
                tj5 = '<script'
                if tj in da:
                    datas1 = re.sub('<a.*?">', '', da)
                    data1 = re.sub('</a>', '', datas1)
                else:
                    data1 = da
                if tj2 in data1:
                    data2 = re.sub('<img.*?>','', data1)
                else:
                    data2 = data1
                if tj3 in data2:
                    data3 = re.sub('<p><iframe.*?</p>', '', data2)
                else:
                    data3 = data2
                if tj4 in data3:
                    data4 = re.sub('<p style=.*?</p>', '', data3)
                else:
                    data4 = data3
                if tj5 in data4:
                    data5 = re.sub('<script.*?</script>', '', data4)
                    data11 = ''.join(data5)
                    dalist.append(data11)
                else:
                    data5 = data4
                    data11 = ''.join(data5)
                    dalist.append(data11)
            article = ''.join(dalist)
            listae.append(article)
            item['article'] = listae
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
                    imgadress = 'http://www.actualites-les.com/static/images/lac/' + imga
                    img = '<img src="' + imgadress + '" width="600" height="350" alt="' + tita + '">'
                    a = ''.join(img)
                    imgl.append(a)
                item['img'] = imgl
            yield item


        except Exception as e:
            print '内容解析错误原因：', e
