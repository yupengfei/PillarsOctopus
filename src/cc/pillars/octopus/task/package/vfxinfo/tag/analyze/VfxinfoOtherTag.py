'''
Created on Dec 29, 2014

@author: sen
'''
from cc.pillars.octopus.task.package.BaseScratch import BaseScratch
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VfxinfoOtherTag(BaseScratch):
    '''
    其他类型标签
    '''
    def analyze(self,other,dates,parent_id):
        if other.name=='ul':
            strLi=''
            for li in other.findAll('li'):
                strLi+=str(li.string)
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,strLi,VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True