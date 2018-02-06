# -*- coding: utf-8 -*-

import urllib2
import re
urltj3 = 'https://www.challenges.fr/economie/le-ceta-entre-en-vigueur-les-ong-sont-sur-le-pied-de-guerre_501001'
#url = 'https://www.challenges.fr/economie/ces-seismes-ouragans-et-tempetes-qui-font-peur-comme-harvey-et-irma_497925'
a497207 = 'https://www.challenges.fr/economie/social/le-sort-que-reserve-le-gouvernement-au-regime-social-des-independants-rsi-se-precise_497207'
request =  urllib2.urlopen(a497207)
response = request.read()
#allurl =  re.findall('<img alt=.*?src="(.*?)".*?>',response)
data888 = re.findall('<div class="article-diaporama diapo-micro".*?</div></div></div>',response)
print '看看：',data888
#list = []
#for al in allurl:
#    picname = al.split('/')[-1]
#    url = 'http://www.actualites-les.com/static/images/ch' + picname
#    list.append(url)
