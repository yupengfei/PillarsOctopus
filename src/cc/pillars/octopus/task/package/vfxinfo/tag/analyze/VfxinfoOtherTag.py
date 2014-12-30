'''
Created on Dec 29, 2014

@author: sen
'''
from bs4.element import Tag

from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VfxinfoAnalyzeDispatch import VfxinfoAnalyzeDispatch
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VfxinfoOtherTag(VfxinfoAnalyzeDispatch):
    '''
    其他类型标签
    '''
    def analyze(self,other,dates,parent_id):
        if type(other)==Tag and other.name=='ul':
            strLi=''
            for li in other.findAll('li'):
                strLi+=str(li.string)
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,strLi,VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
        elif type(other)==Tag and other.name=='b' and other.string!=None:
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(other.string),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
        elif type(other)==Tag and other.name=='span' or other.name=='strong':
            if len(other.contents)==0:
                return True
            #dispatch=VfxinfoAnalyzeDispatch()
            for child in other.contents:
                self.dispatch(dates, child, parent_id)
            return True
        dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(other.string),VfxinfoCounter.index)))
        VfxinfoCounter.index+=1
        return True  