# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from challengs.items import ChallengsItem
import urllib2
import re


class Lenspider(scrapy.Spider):
    name = 'eco'
    all_domain = ['https://www.challenges.fr']
    c1 = ['https://www.challenges.fr/economie/page-{}'.format(i) for i in range(1, 301)]
    c2 = ['https://www.challenges.fr/luxe/page-{}'.format(i) for i in range(1, 15)]
    c3 = ['https://www.challenges.fr/patrimoine/page-{}'.format(i) for i in range(1, 23)]
    c4 = ['https://www.challenges.fr/emploi/page-{}'.format(i) for i in range(1, 34)]
    c5 = ['https://www.challenges.fr/automobile/page-{}'.format(i) for i in range(1, 347)]
    c6 = ['https://www.challenges.fr/high-tech/page-{}'.format(i) for i in range(1, 130)]
    c7 = ['https://www.challenges.fr/media/page-{}'.format(i) for i in range(1, 61)]
    c8 = ['https://www.challenges.fr/monde/page-{}'.format(i) for i in range(1, 220)]
    c9 = ['https://www.challenges.fr/politique/page-{}'.format(i) for i in range(1, 98)]
    c10 = ['https://www.challenges.fr/entreprise/page-{}'.format(i) for i in range(1, 727)]
    start_urls =c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9
    #start_urls = ['https://www.challenges.fr/economie/page-{}'.format(i) for i in range(7, 9)]

    def parse(self, response):
        sel = Selector(response)
        try:
            link = sel.xpath('//div[@class="item"]/a/@href').extract()
            for url in link:
                #urls = 'http://www.lematindz.net/' + url
                yield Request(url, callback=self.parse_content)
        except Exception as e:
            print '错误原因：', e

    def parse_content(self, response):
        item = ChallengsItem()
        sel2 = Selector(response)

        try:

            imgurls = sel2.xpath(r'//div[@class="in"]/img/@data-src').extract()
            if not imgurls:
                image_urls_a  = ['']
                list = ['']

            else:
                image_urls_a = imgurls
                listimg = []
                list = []
                for imgurl in imgurls:
                    picname = imgurl.split('/')[-1]
                    list.append(picname)
            item['category'] = ['economie']
            desf = sel2.xpath('//div[@class="article-start"]/p[2]').extract()
            print desf
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
            title = sel2.xpath('//h1[@itemprop="headline"]/text()').extract()
            for tit in title:
                tita = tit
            item['title'] = title
            #item_title = ''.join(title)
            data = sel2.xpath('//div[@itemprop="articlebody"]').extract()

            if '' in list1:
                item['des'] = ['']
                #item_des = ['']

            else:
                item['des'] = list1
                #item_des = list1

                

            if '' in list:
                item['img'] = ['']
                 #item_img = ['']

            
            else:
              imgl = []
              for imga in list:
                  imgadress = 'http://www.actualites-les.com/static/images/ch/' + imga
                  img = '<img src="' + imgadress + '" alt="' + tita + '">'
                  a = ''.join(img)
                  imgl.append(a)
              item['img'] = imgl
              #item_img = imgl
            ilist = []
            for da in data:
                body = da
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
                else:
                    data1 = body
                if tj2 in data1:
                    data2 = re.sub(r'<iframe.*?</iframe>', '', data1)
                else:
                    data2 = data1

                if tj3 in data2:
                    tj3a = re.sub('<div class="article-diaporama diapo-micro".*?</div>', '', data2)
                    tj8a = re.sub('<div class="article-diaporama diapo-micro".*?</ul></div></div></div>','',data2)
                    if not tj8a:
                        data3 = tj3a
                    else:
                        data3 = tj8a
                else:
                    data3 = data2
                if tj4 in data3:
                    data4 = re.sub('<div class="right">.*?</div>', '', data3)
                else:
                    data4 = data3
                if tj5 in data4:
                    data5 = re.sub('<ul><li class="item".*?</div>', '', data4)
                else:
                    data5 = data4
                if tj6 in data5:
                    data6 = re.sub('<script.*?</script>', '', data4)
                else:
                    data6 = data5
                if tj7 in data6:
                    imgurl = re.findall('<img alt=.*?src="(.*?)".*?>', data6)
                    image_urls2 = imgurl
                    #item['image_urls'] = ['']
                    if not image_urls2:
                        ilist=['']
                    else:
                        ilist=image_urls2

                    list2img = []
                    for img2 in imgurl:
                        picname2 = img2.split('/')[-1]
                        listar = []
                        picurl2 = 'http://www.actualites-les.com/static/images/ch' + picname2
                        namepic = '<img alt="' + tita + '"' + 'src="' + picurl2 + '">'
                        data7 = re.sub('<img alt=.*?">', namepic, data6)
                        article = ''.join(data7)
                        listar.append(article)
                        item['article'] = listar
                        # print '------这个是有条件7的------', item['article']
                else:
                    data7 = data6
                    listar = []
                    article = ''.join(data7)
                    listar.append(article)
                    item['article'] = listar
                    # print '这个是没有条件7的',item['article']
            item['image_urls'] = image_urls_a + ilist
            yield item

        except Exception as e:
            print '内容解析错误原因：', e



