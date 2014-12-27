'''
Created on Dec 19, 2014

@author: sen
'''
from bs4 import BeautifulSoup
import threading

from cc.pillars.octopus.dao.BaseDao import BaseDao
from cc.pillars.octopus.entity.TaskPackage import TaskPackage
from cc.pillars.octopus.task.package.vfxinfo.VfxinfoTaskManager import VfxinfoTaskManager
from cc.pillars.octopus.util.ConfigParserUtil import ConfigParserUtil


class TimingTask:
    '''
    定时任务 
    '''
    def doTask(self,taskPackage):
        '''
        启动所有任务包
        '''
        obj=globals()[taskPackage.module](taskPackage)
        obj.run()
        
    def run(self):
        '''
        运行任务
        '''
        self.getTask()
        for taskPackage in self.packageList:
            #如果站点状态为不可用 不启动该任务包
            validate=self.validateSite(taskPackage)
            if validate:
                thread = threading.Thread(target=self.doTask,args=(taskPackage,))
                thread.start()
        
    def getTask(self):
        '''
        获得所有任务包
        '''
        configPath=ConfigParserUtil.getValue('configFilePath', 'TaskPackageConfig')
        file = open(configPath)
        try:
            xmlStr=file.read()
        except IOError as e:
            print(e)
        finally:
            file.close()
        #解析配置文件
        soup=BeautifulSoup(xmlStr)
        packageList=[]
        for package in soup.findAll('task-package'):
            packageList.append(TaskPackage(str(package['id']),str(package['name']),str(package['config_path']),str(package['module']),str(package['id'])))
        self.packageList=packageList
        
    def validateSite(self,taskPackage):
        '''
        验证是否有该站点
        '''
        dao=BaseDao()
        dao.createConnect()
        siteList=dao.doSelect("SELECT * FROM site_info WHERE id='"+taskPackage.siteId+"' and name='"+taskPackage.siteName+"'")
        if len(siteList)==0:
            dao.createConnect()
            dao.beachInsert([("INSERT INTO site_info(id,name,remarks) VALUES(%s,%s,%s)",(taskPackage.siteId,taskPackage.siteName,taskPackage.remarks))])
        elif siteList[0][3]=='0':
            return True
        
        return False  
        
    


