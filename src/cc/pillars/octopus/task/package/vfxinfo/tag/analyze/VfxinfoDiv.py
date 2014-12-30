'''
Created on Dec 29, 2014

@author: sen
'''
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VfxinfoAnalyzeDispatch import VfxinfoAnalyzeDispatch
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VfxinfoDiv(VfxinfoAnalyzeDispatch):
    '''
    div 解析
    '''
    def analyze(self,div,dates,parent_id):
        class_=None
        if div.get('class')!=None:
            class_=div['class']
        #判断是否是最后一个DIV标记
        if  class_!=None and len(class_)==2 and class_[0]=='bdsharebuttonbox' and class_[1]=='post-share':
            return False
        #验证是否是空div
        elif class_!=None and len(class_)==1 and class_[0]=='clear':
            return True
                #if len(classs)==2 and classs[0]=='et-box' and classs[1]=='et-bio':
                    #etBoxContent=child.find('div',class_='et-box-content')
                    #if etBoxContent==None:
                        #return True
        dates.append(("INSERT INTO page_href(id,parent_id,page_href_html,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(div),VfxinfoCounter.index)))
        VfxinfoCounter.index+=1
        return True    