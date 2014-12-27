'''
Created on Dec 25, 2014

@author: sen
'''
from cc.pillars.octopus.task.package.vfxinfo.VfxinfoConfigAnalyze import VfxinfoConfigAnalyze
from cc.pillars.octopus.task.package.vfxinfo.VfxinfoScratch import VfxinfoScratch
from cc.pillars.octopus.task.package.vfxinfo.VfxinfoTaskList import VfxinfoTaskList


class VfxinfoTaskManager:
    '''
    classdocs
    '''


    def __init__(self, taskPackage):
        self.taskPackage=taskPackage
        self.configPath=taskPackage.configPath
        
    def run(self):
        #解析配置
        analyze=VfxinfoConfigAnalyze(self.configPath)
        site=analyze.analyze()
        #创建任务列表
        taskList=VfxinfoTaskList()
        taskList.createTaskList(site,self.taskPackage)
        #进行抓取
        scratch=VfxinfoScratch()
        for task in taskList.taskList:
            try:
                scratch.doScratch(task,self.taskPackage)
            except Exception as e:
                print('出现异常')
                print(e)