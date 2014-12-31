'''
Created on Dec 10, 2014

@author: sen
'''
import threading
import urllib.request
import urllib.parse


class BaseScratch:
    '''
    基础类 其他Scratch继承该类 使用该类的方法
    '''


    def downLoadPicture(self,src):
        '''
        获得一网站上的图片并读取返回二进制流
        '''
        mutex = threading.Lock()
        mutex.acquire()
        
        src=src.strip()
        conn = urllib.request.urlopen(urllib.parse.quote(src, '[:/?=]'))
        str=conn.read()
        conn.close()
        mutex.release()
        return str

