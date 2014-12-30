'''
Created on Dec 29, 2014

@author: sen
'''
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VfxinfoAnalyzeDispatch import VfxinfoAnalyzeDispatch
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VfxinfoTitle(VfxinfoAnalyzeDispatch):
    '''
    VfxinfoTitle
    '''
    def analyze(self,title,dates,parent_id):
        if len(title.contents)==0:
            return True
        elif title.find('img')!=None:
            #dispatch=VfxinfoAnalyzeDispatch()
            for child_ in title.contents:
                self.dispatch(dates, child_, parent_id)
            return True
        elif title.find('strong')!=None or title.find('span')!=None:
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(title),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
        elif title.string==None:
            return True
        elif title.string.strip()=='.':
            return True