'''
Created on Dec 12, 2014

@author: pillars
'''
from apscheduler.schedulers.background import BackgroundScheduler
import sched
import time

from cc.pillars.octopus.scratch.BaseScratch import BaseScratch
from cc.pillars.octopus.scratch.VfxinfoScratch import VfxinfoScratch
from cc.pillars.octopus.task.TimingTask import TimingTask
from cc.pillars.octopus.util.ConfigParserUtil import ConfigParserUtil


if __name__ == '__main__':
    #v=VfxinfoScratch()
    #v.doScratch('http://vfxinfo.net/2014/03/30/maya-vray-nuke-deep/')
    
    #ConfigParserUtil.filePath='/home/pillars/Public/workspace/octopus/src/cc/pillars/octopus/config/config.ini'
    #task=TimingTask()
    #task.run()
    inportModule=__import__('ConfigParserUtil', globals=None, locals=None, fromlist=['cc.pillars.octopus.util'])
    print(inportModule)
    #a=getattr(inportModule,'__init__')
