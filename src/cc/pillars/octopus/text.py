'''
Created on Dec 12, 2014

@author: pillars
'''

from cc.pillars.octopus.entity.TaskPackage import TaskPackage
from cc.pillars.octopus.task.package.vfxinfo.VfxinfoScratch import VfxinfoScratch
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoTask import VfxinfoTask
from cc.pillars.octopus.util.ConfigParserUtil import ConfigParserUtil
from cc.pillars.octopus.dao.BaseDao import BaseDao


if __name__ == '__main__':
    configPath='/home/pillars/Public/workspace/octopus/src/cc/pillars/octopus/config/config.ini'
    ConfigParserUtil.filePath=configPath
    
    #task=VfxinfoTask('b91b9dba-8d73-11e4-bbc9-6431503bb136','http://vfxinfo.net/2014/12/23/hdr-technology-explanation-denoise/')
    package=TaskPackage('1','1','1','1','1')
    
    scratch=VfxinfoScratch()
    #scratch.doScratch(task,package)
    
    dao=BaseDao();
    dao.createConnect()
    taskList=dao.doSelect("SELECT * FROM task_list WHERE state='1'")
    for i in taskList:
        task=VfxinfoTask(i[0],i[1])
        scratch.doScratch(task, package)
