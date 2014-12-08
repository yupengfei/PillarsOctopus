'''
Created on 2014年12月5日

@author: sen
'''
from bs4 import BeautifulSoup
class SiteConfig:
    '''
    该类用来解析octopuslaw.xml
    '''
    #配置文件名称
    fileName='octopusClaw.xml'

    def __init__(self,path):
        '''
        读取并解析
        '''
        #读取文件
        file = open(path+'/'+SiteConfig.fileName)
        try:
            xmlStr=file.read()
        except IOError as e:
            print(e)
        finally:
            file.close()
        #解析配置文件
        soup=BeautifulSoup(xmlStr)
        siteList=soup.findAll('site')
        print(siteList)
