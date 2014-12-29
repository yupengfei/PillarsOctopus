'''
Created on Dec 29, 2014

@author: pillars
'''
from cc.pillars.octopus.task.package.BaseScratch import BaseScratch
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VfxinfoTitle(BaseScratch):
    '''
    VfxinfoTitle
    '''
    def analyze(self,title,dates,parent_id):
        if title.find('strong')!=None and title.find('strong').find('span')!=None:
            if len(title.contents)==1 and title.string!=None:
                dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(title.string),VfxinfoCounter.index)))
                VfxinfoCounter.index+=1
                return True
            if title.contents[0].name=='strong':
                val2=title.strong.span.extract().string
                val1=title.string
                dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(val2)+str(val1),VfxinfoCounter.index)))
                VfxinfoCounter.index+=1
                return True
            val2=str(title.span.strong.span.extract().string)
            val1=title.string
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(val2)+str(val1),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
        if title.find('img')!=None:
            for images in title.findAll('img'):
                if images.get('data-original')==None:
                    image_url=str(images['src'])
                else:
                    image_url=str(images['data-original'])
                imageblob=self.downLoadPicture(image_url)
                dates.append(("INSERT INTO page_image(id,parent_id,image_blob,image_url,page_index) VALUES(%s,%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,imageblob,image_url,VfxinfoCounter.index)))
                VfxinfoCounter.index+=1
            return True
        if title.string==None:
            return True
        if title.string.strip()=='.':
            return True