'''
Created on Dec 29, 2014

@author: sen
'''

from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VfxinfoAnalyzeDispatch import VfxinfoAnalyzeDispatch


class VifxinfoP(VfxinfoAnalyzeDispatch):
    '''
    VifxinfoP
    '''
    def analyze(self,p,dates,parent_id):
        
        p_childs=p.contents
        if len(p_childs)==0:
            return
        
        #dispatch=VfxinfoAnalyzeDispatch()
        for p_child in p_childs:
            self.dispatch(dates, p_child, parent_id)
        return True
                
        
            
