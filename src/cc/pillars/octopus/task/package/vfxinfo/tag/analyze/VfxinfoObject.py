'''
Created on Dec 29, 2014

@author: sen
'''
from cc.pillars.octopus.task.package.BaseScratch import BaseScratch
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VfxinfoObject(BaseScratch):
    '''
    classdocs
    '''
    def analuze(self,obj,dates,parent_id):
        if obj.name=='object' and obj.find('embed')!=None:
            dates.append(("INSERT INTO page_embed(id,parent_id,embed_html,embed_url,page_index) VALUES(%s,%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(obj),str(obj.find('embed')['src']),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True