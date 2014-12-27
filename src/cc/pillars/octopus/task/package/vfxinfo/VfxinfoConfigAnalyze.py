'''
Created on Dec 25, 2014

@author: sen
'''
from cc.pillars.octopus.task.package.ConfigAnalyze import ConfigAnalyze
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoHref import VfxinfoHref
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoSite  import  VfxinfoSite


class VfxinfoConfigAnalyze(ConfigAnalyze):
    '''
    classdocs
    '''


    def __init__(self, configPath):
        self.configPath=configPath
    
    def analyze(self):
        '''
        解析配置
        '''
        soup=self.read()
        site=soup.find('site')
        name=site['name']
        address=site['address']
        scratch=site.find('scratch').string
        hrefList=site.findAll('href')
        list=[]
        #解析所有的href
        for i in hrefList:
            classify=i['classify']
            href=i.string
            list.append(VfxinfoHref(str(classify),str(href)))
        return VfxinfoSite(str(name),str(address),list,str(scratch))
        