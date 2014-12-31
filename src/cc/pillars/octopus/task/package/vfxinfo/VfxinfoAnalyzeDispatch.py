'''
Created on Dec 30, 2014

@author: sen
'''
from bs4.element import NavigableString, Comment, Tag

from cc.pillars.octopus.task.package.BaseScratch import BaseScratch
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VfxinfoAnalyzeDispatch(BaseScratch):
    '''
    解析调度类
    '''


    def dispatch(self,dates,child,parent_id):
        '''
        对页面内容进行分割
        去除没用的tag
        段落标题 div中的链接 段落内容 存一张表 带tag标签存 不 影响展示
        视频存一张表  存链接
        图片存一张表 图片以2进制的方式保存
        '''
        if child=='\n':
            return True
        elif child=='':
            return True
        elif child==' ':
            return True
        #如果是NavigableString 类型
        elif type(child)==NavigableString:
            if str(child).strip()=='\xa0' or str(child).strip()=='' or str(child).strip()=='\n' or str(child).strip()=='.':
                return True
            return self.vfxinfoNavigableString(child,dates,parent_id)
        #如果是注释
        elif type(child)==Comment:
            return True
        elif child.name=='wbr' and len(child.contents)==0:
            return True
        elif child.name=='noscript':
            return True
        #如果是换行
        elif child.name=='br':
            return True
        #如果是个页面object
        elif child.name=='object':
            return self.vfxinfoObject(child,dates,parent_id)
        #如果是个超链接
        elif child.name=='a':
            return self.vfxinfoLink(child,dates,parent_id)
        #如果这个tag是个div
        elif child.name=='div':
            return self.vfxinfoDiv(child,dates,parent_id)        
        #如果是<P>
        elif child.name=='p':
            return self.vifxinfoP(child,dates,parent_id)
        elif child.name=='h3' or child.name=='h2' or child.name=='h1' or child.name=='h4' or child.name=='h5' or child.name=='h6':
            return self.vfxinfoTitle(child,dates,parent_id)
        elif child.name=='img':
            return self.vfxinfoObject(child,dates,parent_id)
        elif child.name=='embed':
            return self.vfxinfoObject(child,dates,parent_id)
        else:
            return self.vfxinfoOtherTag(child,dates,parent_id)
        
    def vfxinfoNavigableString(self,str_,dates,parent_id):
        '''
        如果是字符串
        '''
        if str(str_).strip()=='' or  str(str_).strip()=='.':
            return True
        dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(str_),VfxinfoCounter.index)))
        VfxinfoCounter.index+=1
        return True
    def vfxinfoObject(self,obj,dates,parent_id):
        '''
        如果是字符图片视频等对象
        '''
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
            if obj.get('src')==None:
                return True
            dates.append(("INSERT INTO page_embed(id,parent_id,embed_html,embed_url,page_index) VALUES(%s,%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(obj),str(obj['src']),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
    def vfxinfoLink(self,link,dates,parent_id):
        '''
        如果是链接
        '''
        if link.name=="a":
            if link.find('img')!=None or link.find('embed')!=None or link.find('object')!=None:
                a_childs=link.contents
                for child in a_childs:
                    self.dispatch(dates, child, parent_id)
                return True
            dates.append(("INSERT INTO page_href(id,parent_id,page_href_html,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(link),VfxinfoCounter.index)))
            VfxinfoCounter.index+=1
            return True
    def vfxinfoDiv(self,div,dates,parent_id):
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
        if div.get('class')==None and len(div.contents)!=0:
            for child in div.contents:
                self.dispatch(dates, child, parent_id)
            return True
        elif div.get('class')!=None and div.find('img')!=None or div.find('embed')!=None or div.find('object')!=None:
            for child in div.contents:
                self.dispatch(dates, child, parent_id)
            return True
        dates.append(("INSERT INTO page_href(id,parent_id,page_href_html,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(div),VfxinfoCounter.index)))
        VfxinfoCounter.index+=1
        return True
    def vifxinfoP(self,p,dates,parent_id):
        '''
        如果是段落
        '''
        p_childs=p.contents
        if len(p_childs)==0:
            return
        
        #dispatch=VfxinfoAnalyzeDispatch()
        for p_child in p_childs:
            self.dispatch(dates, p_child, parent_id)
        return True
    def vfxinfoTitle(self,title,dates,parent_id):
        '''
        如果是标题
        '''
        if len(title.contents)==0:
            return True
        elif title.find('img')!=None or title.find('embed')!=None or title.find('object')!=None:
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
        dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(title),VfxinfoCounter.index)))
        VfxinfoCounter.index+=1
        return True
    def vfxinfoOtherTag(self,other,dates,parent_id):
        '''
        其他标签
        '''
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
        elif type(other)==Tag and other.name=='span' or other.name=='strong' or other.name=='blockquote':
            if len(other.contents)==0:
                return True
            #dispatch=VfxinfoAnalyzeDispatch()
            for child in other.contents:
                self.dispatch(dates, child, parent_id)
            return True
        dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(other),VfxinfoCounter.index)))
        VfxinfoCounter.index+=1
        return True