'''
Created on Dec 9, 2014

@author: sen
'''
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import urllib.request

from cc.pillars.octopus.dao.BaseDao import BaseDao
from cc.pillars.octopus.task.package.BaseScratch import BaseScratch
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil
from cc.pillars.octopus.util.DateUtil import DateUtil


class VfxinfoScratch(BaseScratch):
    '''
    VfxinfoScratch
    '''
        
    def doScratch(self,task,taskPackage): 
        '''
        对页面进行抓取
        '''
        self.page_index=0
        dao=BaseDao()
        
        fp = urllib.request.urlopen(task.href)
        mybytes = fp.read()
        htmlString = mybytes.decode("utf8")
        fp.close()
        
        soup=BeautifulSoup(htmlString)
        #过滤只留中间部分
        post=soup.find('div',id='post')
        #获得头部信息
        header=post.find('header',class_='entry-header')
        #标题
        titleSoup=header.find('h1',class_='post-title')
        title=str(titleSoup.string)
        
        postMeta=header.find('p',class_='post-meta')
        #发布者
        #span=postMeta.contents[0]
        if postMeta.contents[0]=='\n':
            span=postMeta.contents[1]
        else:
            span=postMeta.contents[0]
        promulgatorSoup=span.find('a')
        promulgator=str(promulgatorSoup.string)
        #发布时间
        time=postMeta.find('span',class_='time')
        time.i.decompose()
        issuesTime=str(time.string)
        
        #此处之前该方法一测试
        #div entry-inner 内容 遍历所有子节点
        #div bdsharebuttonbox post-share 当看到这个div时不在便利
        
        #获得内容信息        
        entryInner=post.find('div',class_='entry-inner')
        parent_id=UUIDUtil.getId()
        dates=[]
        dates.append(("INSERT INTO page_info(id,url,belongs_site,title,promulgator,issues_time,scratch_time,task_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(parent_id,task.href,taskPackage.siteId,title,promulgator,issuesTime,DateUtil.getTime_Long(),task.taskId)))
        dates.append(("UPDATE task_list SET state=%s WHERE id=%s",('0',task.taskId)))
        #遍历所有子节点并区分类型        
        for child in entryInner.contents:
            state=self.doDistinguish(dates,child,parent_id)
            if state==False:
                break
        dao.createConnect()
        dao.beachInsert(dates)
        return True
    def doDistinguish(self,dates,child,parent_id):
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
        #如果这个tag是个div
        if type(child)==NavigableString:
            if str(child).strip()=='' or  str(child).strip()=='.':
                return True
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(child),self.page_index)))
            self.page_index+=1
            return True
        if child.name=='div':
            if 'class' in child.attrs:
                classs=child['class']
                #判断是否是最后一个DIV标记
                if len(classs)==2 and classs[0]=='bdsharebuttonbox' and classs[1]=='post-share':
                    return False
                if len(classs)==1 and classs[0]=='clear':
                    return True
            dates.append(("INSERT INTO page_href(id,parent_id,page_href_html,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(child),self.page_index)))
            self.page_index+=1
        #如果是ul
        if child.name=='ul':
            strLi=''
            for li in child.findAll('li'):
                strLi+=str(li.string)
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,strLi,self.page_index)))
            self.page_index+=1
            return True
        #如果是<P>
        if child.name=='p':
            img=child.find('img')
            embed=child.find('embed')
            if img!=None:
                for images in child.findAll('img'):
                    if images.get('data-original')==None:
                        image_url=str(images['src'])
                    else:
                        image_url=str(images['data-original'])
                    imageblob=self.downLoadPicture(image_url)
                    dates.append(("INSERT INTO page_image(id,parent_id,image_blob,image_url,page_index) VALUES(%s,%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,imageblob,image_url,self.page_index)))
                    self.page_index+=1
                return True
            if embed!=None:
                dates.append(("INSERT INTO page_embed(id,parent_id,embed_html,embed_url,page_index) VALUES(%s,%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(embed),str(embed['src']),self.page_index)))
                self.page_index+=1
                return True
            if child.string==None:
                if len(child.findAll('b'))!=0:
                    strP=""
                    for i in child.findAll('b'):
                        strP+=str(i.string)
                    dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,strP,self.page_index)))
                    self.page_index+=1
                    return True
                if len(child.contents)==0:
                    return True
            #如果其中是duo个span 且有链接a  把他当做链接
            if len(child.findAll('span'))!=0:
                if child.find('a')!=None:
                    dates.append(("INSERT INTO page_href(id,parent_id,page_href_html,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(child),self.page_index)))
                    self.page_index+=1
                    return True
                #其他样式一律当段落 且不进行分割
                dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(child),self.page_index)))
                self.page_index+=1
                return True
            if len(child.contents)==2 and type(child.contents[0])==Tag and child.contents[0].name=='strong' and type(child.contents[1])==NavigableString:
                strStrong=str(child.contents[0].string)+str(child.contents[1])
                dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,strStrong,self.page_index)))
                self.page_index+=1
                return True
            if child.string.strip()=='':
                return True
            if child.string.strip()=='.':
                return True
            
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(child.string),self.page_index)))
            self.page_index+=1
        if child.name=='h3':
            if child.string.strip()=='.':
                return True
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(child.string),self.page_index)))
            self.page_index+=1