'''
Created on Dec 29, 2014

@author: sen
'''
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VfxinfoAnalyzeDispatch import VfxinfoAnalyzeDispatch
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VfxinfoObject(VfxinfoAnalyzeDispatch):
    '''
    classdocs
    '''
    def analuze(self,obj,dates,parent_id):
        if obj.name=='object' and obj.find('embed')!=None:
            dates.append(("INSERT INTO page_embed(id,parent_id,embed_html,embed_url,page_index) VALUES(%s,%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(obj),str(obj.find('embed')['src']),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
        elif obj.name=='img':
            if obj.get('data-original')==None and obj.get('src')==None:
                return True
            elif obj.get('data-original')==None:
                image_url=str(obj['src'])
            else:
                image_url=str(obj['data-original'])
            imageblob=self.downLoadPicture(image_url)
            dates.append(("INSERT INTO page_image(id,parent_id,image_blob,image_url,page_index) VALUES(%s,%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,imageblob,image_url,VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
        elif obj.name=='embed':
            dates.append(("INSERT INTO page_embed(id,parent_id,embed_html,embed_url,page_index) VALUES(%s,%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(obj),str(obj['src']),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True