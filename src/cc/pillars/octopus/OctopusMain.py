'''
Created on Dec 8, 2014

@author: pillars
'''
import os

from cc.pillars.octopus.config.DateBaseConfig import DateBaseConfig


configFilePath=os.getcwd()+'/config'

if __name__ == '__main__':
    #测试
    #siteConfig=SiteConfig(configFilePath)
    dateBaseConfig=DateBaseConfig(configFilePath);
    dateBaseConfig.createConnect();
    count=dateBaseConfig.execute('select count(*) from textinfo', [])
    print(count)
else:
    print('name is not __main__')