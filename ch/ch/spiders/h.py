# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from ch.items import ChItem
import re


class Lacspider(scrapy.Spider):
    name = 'c'
    allowed_domain = ['http://www.getit01.com']
    start_urls = ['https://www.getit01.com/p2018012429498548/']
    def parse(self, response):
        item = ChItem()
        sel = Selector(response)
        try:
            title = sel.xpath('//h1/text()').extract()
            if not title:
                print 'meiyou title'
                #item['title'] = ['']
            else:
                print 'biati title:',title
                #item['title'] = title
            '''    
            now = datetime.datetime.now()
            bb = now.strftime('%Y-%m-%d')
            cc = str(bb)
            listd = []
            listd.append(cc)
            '''
            #item['datime'] = listd
            #item['des'] = ['']
            #item['img'] = ['']
            #item['category'] = ['news']
            link = sel.xpath('//*[@id="post_content"]/p[1]/a/@href').extract()
            if not link:
                print 'no link'
            else:
                for url in link:
                    urls = 'https://www.getit01.com' + url
                    print urls
                    yield Request(urls, callback=self.parse)
            data = sel.xpath('//div[@id="fc"]').extract()
            imgurls = sel.xpath(r'//img/@src').extract()
            if not imgurls:
                print 'meiyoutupian'
                #item['image_urls'] = ['']
            else:
                listurl1 = sorted(set(imgurls))
                print 'tupian:', listurl1
                #item['image_urls'] = listurl1
            if not data:
                print 'zmkeneng meiyou wenzhang neirong'
                #item['article'] = ['']
            else:
                dalist = []
                for da in data:
                    tj = 'href="'
                    tj2 = '<img'
                    if tj2 in da:
                        yyurl = 'http://www.actualites-les.com/static/images/ch'
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
                #item['article'] = dalist
                        print '文章内容：',data2
                #print '文章数量：',x
            yield item


        except Exception as e:
            print '内容解析错误原因：', e
