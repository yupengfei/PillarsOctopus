'''
Created on Dec 9, 2014

@author: pillars
'''
from bs4 import BeautifulSoup

from cc.pillars.octopus.entity.Href import Href
from cc.pillars.octopus.entity.Site import Site


class EasyScratch:
    '''
    解析xml 将其转化成对象
    网站配置类型EasyScratch
    '''
    def getSite(self,site):
        name=site['name']
        address=site['address']
        scratch=site.find('scratch').string
        hrefList=site.findAll('href')
        list=[]
        #name[len(name):]从末尾添加
        #解析所有的href
        for i in hrefList:
            classify=i['classify']
            href=i.string
            list.append(Href(classify,href))
        siteObj=Site(name,address,list,scratch)
        return siteObj