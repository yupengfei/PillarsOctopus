'''
Created on 2014年12月5日

@author: sen
'''
from bs4 import BeautifulSoup

from cc.pillars.octopus.config.EasyScratch import EasyScratch


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
        #获得所有站点
        siteList=soup.findAll('site')
        #映射类集合
        allClass=globals()
        #站点对象列表
        siteObjList=[]
        for site in siteList:
            easyScratch = allClass[site['type']]()
            siteObj=easyScratch.getSite(site);
            siteObjList.append(siteObj)
        self.siteObjList=siteObjList
    
    def getSiteObjList(self):
        return self.siteObjList