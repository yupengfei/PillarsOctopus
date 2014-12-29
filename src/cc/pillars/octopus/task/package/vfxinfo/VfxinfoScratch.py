'''
Created on Dec 9, 2014

@author: sen
'''
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag, Comment
import urllib.request

from cc.pillars.octopus.dao.BaseDao import BaseDao
from cc.pillars.octopus.task.package.BaseScratch import BaseScratch
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoCounter import VfxinfoCounter
from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VfxinfoDiv import VfxinfoDiv
from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VfxinfoLink import VfxinfoLink
from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VfxinfoNavigableString import VfxinfoNavigableString
from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VfxinfoObject import VfxinfoObject
from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VifxinfoP import VifxinfoP
from cc.pillars.octopus.util.DateUtil import DateUtil
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil
from cc.pillars.octopus.task.package.vfxinfo.tag.analyze.VfxinfoTitle import VfxinfoTitle


class VfxinfoScratch(BaseScratch):
    '''
    VfxinfoScratch
    '''
        
    def doScratch(self,task,taskPackage): 
        '''
        对页面进行抓取
        '''
        #self.page_index=0
        VfxinfoCounter.index=0
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
        #如果是NavigableString 类型
        elif type(child)==NavigableString:
            return VfxinfoNavigableString().analyze(child, dates, parent_id)
        #如果是注释
        elif type(child)==Comment:
            return True
        #如果是换行
        elif child.name=='br':
            return True
        #如果是个页面object
        elif child.name=='object':
            return VfxinfoObject().analuze(child, dates, parent_id)
        #如果是个超链接
        elif child.name=='a':
            return VfxinfoLink().analyze(child, dates, parent_id)
        #如果这个tag是个div
        elif child.name=='div':
            return VfxinfoDiv().analyze(child, dates, parent_id)        
        #如果是<P>
        elif child.name=='p':
            return VifxinfoP().analyze(child, dates, parent_id)
        elif child.name=='h3':
            return VfxinfoTitle().analyze(child, dates, parent_id)
        dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(UUIDUtil.getId(),parent_id,str(child.string),VfxinfoCounter.index)))
        VfxinfoCounter.index+=1