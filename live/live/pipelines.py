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
            if not image_url:
                None
            else:
                yield Request(image_url,meta={'item':item,'index':item['image_urls'].index(image_url)})

    def file_path(self, request, response=None, info=None):
        item=request.meta['item'] #通过上面的meta传递过来item
        index=request.meta['index'] #通过上面的index传递过来列表中当前下载图片的下标
        image_guid = request.url.split('/')[-1]
        filename = u'{0}'.format(image_guid)
        return filename

class LivePipeline(object):

    def __init__(self):

        dbargs = dict(
            host = 'localhost' ,
            db = 'news',
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
        conn.execute('insert into ne(title,article,des,img,datime,category) values(%s,%s,%s,%s,%s,%s)', (item['title'],item['article'],item['des'],item['img'],item['datime'],item['category']))
