'''
Created on Dec 18, 2014

@author: sen
'''
from bs4 import BeautifulSoup

from cc.pillars.octopus.entity.Task import Task
from cc.pillars.octopus.task.TimingTask import TimingTask
from cc.pillars.octopus.util.ConfigParserUtil import ConfigParserUtil


class TaskManager:
    '''
    任务管理器
    '''
    def start(self):
        '''
        启动任务管理器
        '''
        #获得所有任务
        tasks=self.getTasks()
        #启动所有任务
        for task in tasks:
            obj=obj=globals()[task.module]()
            obj.run()
    def getTasks(self):
        '''
        获得所有任务
        '''
        tasksConfigPath=ConfigParserUtil.getValue('configFilePath', 'tasksConfig');
        try:
            file = open(tasksConfigPath)
            xmlStr=file.read()
        except IOError as e:
            print(e)
        finally:
            file.close()
        #解析配置文件
        soup=BeautifulSoup(xmlStr)
        #获得所有任务
        tasks=[]
        for t in soup.findAll('task'):
            task=Task(str(t['module']),str(t.string))
            tasks.append(task)
        return tasks
