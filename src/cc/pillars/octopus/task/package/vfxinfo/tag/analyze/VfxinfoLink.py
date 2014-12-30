'''
Created on Dec 29, 2014

@author: sen
'''
from cc.pillars.octopus.task.package.BaseScratch import BaseScratch
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VfxinfoAnalyzeDispatch import VfxinfoAnalyzeDispatch
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VfxinfoLink(VfxinfoAnalyzeDispatch):
    '''
    超链接解析
    '''


    def analyze(self,link,dates,parent_id):
        if link.name=="a":
            dates.append(("INSERT INTO page_href(id,parent_id,page_href_html,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(link),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True