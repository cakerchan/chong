# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from lac.items import LacItem
import re


class Lacspider(scrapy.Spider):
    name = 'lac'
    all_domain = ['http://lactualite.com']
    l1 = ['http://lactualite.com/politique/page/{}'.format(i) for i in range(1, 410)]
    l2 = ['http://lactualite.com/societe/page/{}'.format(i) for i in range(1, 189)]
    l3 = ['http://lactualite.com/sujet/analyses-et-opinions/page/{}'.format(i) for i in range(1, 769)]
    l4 = ['http://lactualite.com/culture/page/{}'.format(i) for i in range(1, 253)]
    l5 = ['http://lactualite.com/lactualite-affaires/page/{}'.format(i) for i in range(1, 215)]
    l6 = ['http://lactualite.com/sante-et-science/page/{}'.format(i) for i in range(1, 245)]
    #l7 = ['http://lactualite.com/actualites/page/{}'.format(i) for i in range(1, 3113)]
    start_urls = ['http://lactualite.com/actualites/page/{}'.format(i) for i in range(1, 3)]
    def parse(self, response):
        sel = Selector(response)
        try:
            link = sel.xpath('//div[@class="grid-article-inner ellipsis"]/a/@href').extract()
            for url in link:
                yield Request(url, callback=self.parse_content)
        except Exception as e:
            print '错误原因：', e

    def parse_content(self, response):
        item = LacItem()
        sel2 = Selector(response)
        try:
            imgurls = sel2.xpath(r'//div[@class="entry-content-asset"]/img/@data-src').extract()
            if not imgurls:
                #item['image_urls'] = ['']
                list = ['']
            else:
                list = []
                for imgurl in imgurls:
                    picname1 = imgurl.split('/')[-1]
                    picname2 = picname1.split(';')[-2]
                    picname3 = picname1.split('.')[-1]
                    picname = picname2 + '.' + picname3
                    list.append(picname)
            category = sel2.xpath('//link[@rel="canonical"]/@href').extract()
            for ca in category:
                cat = ca.split('/')[3]
                if cat == 'politique':
                    ca1 = ['editorial']
                    #print '分类名称ca1', ca1
                    item['category'] = ['editorial']
                elif cat == 'societe':
                    #ca2 = ['societe']
                    #print '分类名称ca2', ca2
                    item['category'] = ['societe']
                elif cat == 'techno':
                    #ca3 = ['idees']
                    #print '分类名称ca3', ca3
                    item['category'] = ['idees']
                elif cat == 'culture':
                    #ca4 = ['culture']
                    #print '分类名称ca4', ca4
                    item['category'] = ['culture']
                elif cat == 'lactualite-affaires':
                    ca5 = ['economie']
                    print '分类名称ca5', ca5
                    #item['category'] = ['economie']
                elif cat == 'sante-et-science':
                    #ca6 = ['sante']
                    #print '分类名称ca6', ca6
                    item['category'] = ['sante']
                elif cat == 'actualites':
                    #ca7 = ['national']
                    #print '分类名称ca7', ca7
                    item['category'] = ['national']
            
            desf = sel2.xpath('//p[@class="lead"]').extract()
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
            #print '看看标题：',title
            item['title'] = title
            data = sel2.xpath('//div[@class="entry-body clearfix"]/p').extract()
            listae = []
            dalist = []
            urllist2 = []
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
                    dac1 =  re.findall('<img.*?width="(.*?)".*?height="(.*?)".*?data-src="(.*?)"',data1)
                    dac2 = re.findall('<img.*?data-src="(.*?)".*?width="(.*?)".*?height="(.*?)"',data1)
                    if not dac1:
                        dachaa = dac2
                    else:
                        dachaa = dac1
                    dacha = sorted(set(dachaa))
                    for img2 in dacha:
                        iac = '<>'.join(img2)
                        url2 = iac.split('<>')[-1]
                        urllist2.append(url2)
                        imgname2 = url2.split('/')[-1]
                        height = 'height=' + '"' + iac.split('<>')[-2] + '"'
                        width = 'width=' + '"' + iac.split('<>')[-3] + '"'
                        imgname22 = 'http://www.actualites-les.com/static/images/lac/' + imgname2
                        imgname3 = "<img.*?http.*?" + imgname2+'.*?>'
                        data2m = re.sub(imgname3, imgname22, data1)
                        tjlac = 'http://lactualite.com'
                        if tjlac in data2m:
                            data2 = re.sub('<img.*?http://lactualite.com.*?>', '', data2m)
                            #print '这个是文中有图片的dai：', data2
                        else:
                            data2 = data2m
                            #print '这个是文中有图片的mei：', data2
                else:
                    data2 = data1
                if tj3 in data2:
                    data3 = re.sub('<p><iframe.*?</p>','',data2)
                    #print 'ifram-----看看这个：',data3
                else:
                    data3 = data2
                if tj4 in data3:
                    data4 = re.sub('<p style=.*?</p>','',data3)
                    #print 'style---看这个去除没：',data4
                else:
                    data4 = data3
                if tj5 in data4:
                    data5 = re.sub('<script.*?</script>','',data4)
                    data11 = ''.join(data5)
                    dalist.append(data11)
                else:
                    data5 = data4
                    data11 = ''.join(data5)
                    dalist.append(data11)

            article = ''.join(dalist)
            listae.append(article)
            item['article'] = listae
            if not urllist2:
                item['image_urls'] = imgurls
            else:
                item['image_urls'] = imgurls + urllist2
            #print '看看文章解析：', listae
            if '' in list1:
                #desa = ['']
                item['des'] = ['']
            else:
                #desa = list1
                #print '描述看看：',desa
                item['des'] = list1
            if '' in list:
                #imag = ['']
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
                #print '图片链接地址：',imgl
            yield item


        except Exception as e:
            print '内容解析错误原因：', e
