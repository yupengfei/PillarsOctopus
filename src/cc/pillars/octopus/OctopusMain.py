'''
Created on Dec 8, 2014

@author: sen
'''
from cc.pillars.octopus import scratch
'''
章鱼的main方法  也是控制器
'''
#配置文件存放路径

import os
import threading

from cc.pillars.octopus.config.DateBaseConfig import DateBaseConfig
from cc.pillars.octopus.config.SiteConfig import SiteConfig
from cc.pillars.octopus.scratch.VfxinfoScratch import VfxinfoScratch


configFilePath=os.getcwd()+'/config'


def doScratch(site):
    '''
    启动线程调用该方法
    对各个站点进行抓取
    '''
    #所有类反射
    allClass=globals()
    scratch=allClass[site.scratch]()
    scratch.doWork(site)
    
if __name__ == '__main__':
    #解析配置文件
    siteConfig=SiteConfig(configFilePath)
    #站点对象列表
    siteObjList=siteConfig.getSiteObjList()
    for site in siteObjList:
        thread = threading.Thread(target=doScratch,args=(site,))
        #thread.setDaemon(True)
        thread.start()
    #dateBaseConfig=DateBaseConfig(configFilePath);
    #dateBaseConfig.createConnect();
    #count=dateBaseConfig.execute('select count(*) from textinfo', [])
    #print(count)
else:
    print('name is not __main__')

    
