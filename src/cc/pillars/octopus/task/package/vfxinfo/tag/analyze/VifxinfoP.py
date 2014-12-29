'''
Created on Dec 29, 2014

@author: sen
'''
from bs4.element import Tag, NavigableString

from cc.pillars.octopus.task.package.BaseScratch import BaseScratch
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VifxinfoP(BaseScratch):
    '''
    VifxinfoP
    '''
    def analyze(self,p,dates,parent_id):
        img=p.find('img')
        embed=p.find('embed')
        if img!=None:
            for images in p.findAll('img'):
                if images.get('data-original')==None and images.get('src')==None:
                    return True
                if images.get('data-original')==None:
                    image_url=str(images['src'])
                else:
                    image_url=str(images['data-original'])
                imageblob=self.downLoadPicture(image_url)
                dates.append(("INSERT INTO page_image(id,parent_id,image_blob,image_url,page_index) VALUES(%s,%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,imageblob,image_url,VfxinfoCounter.index)))
                VfxinfoCounter.index+=1
            return True
        if embed!=None:
            dates.append(("INSERT INTO page_embed(id,parent_id,embed_html,embed_url,page_index) VALUES(%s,%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(embed),str(embed['src']),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
        if p.string==None:
            if len(p.findAll('b'))!=0:
                strP=""
                for i in p.findAll('b'):
                    strP+=str(i.string)
                dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,strP,VfxinfoCounter.index)))
                VfxinfoCounter.index+=1
                return True
            if len(p.contents)==0:
                return True
        #如果其中是duo个span 且有链接a  把他当做链接
        if len(p.findAll('span'))!=0:
            if p.find('a')!=None:
                dates.append(("INSERT INTO page_href(id,parent_id,page_href_html,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(p),VfxinfoCounter.index)))
                VfxinfoCounter.index+=1
                return True
            #其他样式一律当段落 且不进行分割
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(p),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
        if len(p.contents)==2 and type(p.contents[0])==Tag and p.contents[0].name=='strong' and type(p.contents[1])==NavigableString:
            strStrong=str(p.contents[0].string)+str(p.contents[1])
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,strStrong,VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
        if p.find('a')!=None:
            dates.append(("INSERT INTO page_href(id,parent_id,page_href_html,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(p),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
        if p.string==None:
            return True
        if p.string.strip()=='':
            return True
        if p.string.strip()=='.':
            return True
            
        dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(p.string),VfxinfoCounter.index)))
        VfxinfoCounter.index+=1  