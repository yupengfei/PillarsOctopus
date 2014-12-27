'''
Created on Dec 25, 2014

@author: sen
'''
from bs4 import BeautifulSoup


class ConfigAnalyze:


    def __init__(self, params):
        '''
        读取配置文件
        '''
    def read(self):
        file = open(self.configPath)
        try:
            xmlStr=file.read()
        except IOError as e:
            print(e)
        finally:
            file.close()
        #解析配置文件
        return BeautifulSoup(xmlStr)