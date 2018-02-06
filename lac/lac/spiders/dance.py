# -*- coding: utf-8 -*-
import urllib2
import re
from lxml import etree

url = ' http://lactualite.com/lactualite-affaires/2017/12/08/la-deuxieme-vie-des-cadeaux-mal-aimes/'
#url = 'http://lactualite.com/societe/2017/12/08/le-grand-recit-de-la-crise-du-verglas/'
html = urllib2.urlopen(url)
body = html.read()
#print body
tree = etree.HTML(body)

cc = tree.xpath('//div[@class="entry-body clearfix"]')


list = []
for ccc in cc:
    content = etree.tostring(ccc,pretty_print=True,method='html')
    oo = ''.join(content)
    list.append(oo)
    #print content
    p1 = re.sub('<p><iframe.*?</p>','',content)
    p3 = re.sub('<p style=.*?</p>','',p1)
    p2= ''.join(p3).strip()
    list.append(p2)
lista = ''.join(list)
listb = []
listb.append(lista)
for listpp in listb:
    lpp = listpp
    datas1 = re.sub('<a.*?">', '', lpp)
    data1 = re.sub('</a>', '', datas1)
    ppm =  re.findall('<img.*?width="(.*?)".*?height="(.*?)".*?data-src="(.*?)"',lpp)
    #ppm = re.findall('<img.*?>',lpp)
    ppp = sorted(set(ppm))
    #print 'shangmiange',ppm
    for img2 in ppp:
        iac = '<>'.join(img2)
        url = iac.split('<>')[-1]
        imgname2 = url.split('/')[-1]
        height = 'height=' + '"'+iac.split('<>')[-2]+'"'
        width = 'width=' + '"'+iac.split('<>')[-3]+'"'
        imgname3 = "<img.*?http.*?" + imgname2+'.*?>'
        imgname22 = 'http://www.actualites-les.com/static/images/lac/' + imgname2
        data2 = '<img src="' + imgname22 + '" '+width +' '+ height + '>'
        scc = re.sub(imgname3, data2, data1)
        jcc = re.sub('<img.*?http://lactualite.com.*?>','',scc)
        jc = re.findall('<img.*?>',jcc)
        jca = sorted(set(jc))
        print '二层：',jca
        #图片下载地址
        ##imgurl2 = img2
        '''
        imgname2 = img2.split('/')[-1]
        #imgname2 = ''.join(imgnamee)
        io = re.findall('width=".*?".*?height=".*?"', data1)
        imgname3 = "http.*?" + imgname2
        imgname22 = 'http://www.actualites-les.com/static/images/lac/' + imgname2
        img = '<img src="' + imgname22 + '" width="600" height="350" alt="' + tita + '">'
        data2 = re.sub(imgname3, imgname22, data1)

        ioo = sorted(set(io))

        #print imgname2
        '''
#print listb




#print '全文解析：',body
    #print '正则解析：',c
