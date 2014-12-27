'''
Created on Dec 8, 2014

@author: sen
'''
'''
章鱼的启动器
'''
#配置文件存放路径

from cc.pillars.octopus.task.TaskManager import TaskManager
from cc.pillars.octopus.util.ConfigParserUtil import ConfigParserUtil

#配置文件的路径
configPath='/home/pillars/Public/workspace/octopus/src/cc/pillars/octopus/config/config.ini'

if __name__ == '__main__':
    #启动任务管理器
    #初始化配置
    ConfigParserUtil.filePath=configPath
    taskManager=TaskManager()
    taskManager.start()


