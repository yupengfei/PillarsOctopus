'''
Created on Dec 10, 2014

@author: sen
'''
import time
import urllib.request
import uuid


class BaseScratch:
    '''
    基础类 其他Scratch继承该类 使用该类的方法
    '''


    def downLoadPicture(self,src):
        '''
        获得一网站上的图片并读取返回二进制流
        '''
        conn = urllib.request.urlopen(src)
        str=conn.read()
        conn.close()
        return str
        #print(conn.read())        

    def getId(self):
        '''
        生成以个36位随机数
        当做ID
        '''
        return uuid.uuid1().__str__()
    def getTime_Long(self):
        return time.time()