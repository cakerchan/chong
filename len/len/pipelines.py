# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors

from scrapy.crawler import Settings as settings

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url,meta={'item':item,'index':item['image_urls'].index(image_url)})

    def file_path(self, request, response=None, info=None):
        item=request.meta['item'] #通过上面的meta传递过来item
        index=request.meta['index'] #通过上面的index传递过来列表中当前下载图片的下标
        image_guid = request.url.split('/')[-1]
        image_guids = request.url.split('/')[-2]
        filename = u'{0}{1}'.format(image_guids,image_guid)
        return filename


    #def item_completed(self, results, item, info):
    #    image_paths = [x['path'] for ok, x in results if ok]
    #    if not image_paths:
    #        raise DropItem("Item contains no images")
    #    return item

class LenPipeline(object):

    def __init__(self):

        dbargs = dict(
            host = 'localhost' ,
            db = '1213content',
            user = 'root', #replace with you user name
            passwd = 'root', # replace with you password
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
            )
        self.dbpool = adbapi.ConnectionPool('MySQLdb',**dbargs)


    def process_item(self, item, spider):
        res = self.dbpool.runInteraction(self.insert_into_table,item)
        return item

    def insert_into_table(self,conn,item):       
        conn.execute('insert into cc(title,article,img,des,datime,category) values(%s,%s,%s,%s,%s,%s)', (item['title'],item['article'],item['img'],item['des'],item['datime'],item['category']))
