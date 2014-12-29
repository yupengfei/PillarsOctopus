'''
Created on Dec 29, 2014

@author: sen
'''
from cc.pillars.octopus.task.package.BaseScratch import BaseScratch
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VfxinfoNavigableString(BaseScratch):
    '''
    NavigableString 类型解析
    '''

    def analyze(self,str_,dates,parent_id):
        if str(str_).strip()=='' or  str(str_).strip()=='.':
                return True
        dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(str_),VfxinfoCounter.index)))
        VfxinfoCounter.index+=1
        return True
    
        