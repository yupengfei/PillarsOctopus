'''
Created on Dec 25, 2014

@author: sen
'''
from bs4 import BeautifulSoup
import urllib.request

from cc.pillars.octopus.dao.BaseDao import BaseDao
from cc.pillars.octopus.task.package.vfxinfo.entity.VfxinfoTask import VfxinfoTask
from cc.pillars.octopus.util.UUIDUtil import UUIDUtil


class VfxinfoTaskList:
    '''
    classdocs
    '''


    def createTaskList(self,site,taskPackage):
        '''
        创建任务列表
        '''
        #任务列表
        list=[]
        hashList=[]
        self.list=list
        self.hashList=hashList
        self.taskPackage=taskPackage
        #生成任务列表    
        for href in site.hrefList:
            self.analyzePage(href)
        #保存任务列表
        self.saveTaskList()
    def analyzePage(self,href):
        '''
        解析页面
        '''
        fp = urllib.request.urlopen(href.href)
        mybytes = fp.read()
        htmlString = mybytes.decode("utf8")
        fp.close()
        
        while True:
            soup=BeautifulSoup(htmlString)
            #过滤html 
            #页面中间
            postList=soup.find('div',class_='post-list group')
            #分页Div
            pageNav=postList.find('div',class_='page-nav')
            #获得所有的链接DIV
            posts=postList.find_all('div',class_='post-inner post-hover')
            #遍历所有链接并验证是否已经被添加到任务列表
            dao=BaseDao()
            hasTask=True
            for a in posts:
                h3=a.find('h3',class_='post-title')
                a=h3.find('a')
                aHref=a['href']
                dao.createConnect()
                pageTask=dao.doSelect("SELECT * FROM task_list WHERE href='"+aHref+"'")
                if len(pageTask)!=0:
                    hasTask=False
                    break
                if self.hashList.count(str(aHref))==0:
                    self.hashList.append(str(aHref))
                    self.list.append((str(aHref),href.classify))
                
            if hasTask==False:
                break
            #判断是否有下一页
            if self.hasNext(pageNav):
                #读取下一页的内容
                span=pageNav.find('span',class_='current')
                next=span.next_sibling
                fp=urllib.request.urlopen(next['href'])
                mybytes = fp.read()
                htmlString = mybytes.decode("utf8")
                fp.close()
            else:
                #如果没有下一页跳出循环
                break
    def hasNext(self,pageNav):
        '''
        判断是否有下一页
        '''
        if pageNav==None:
            return False
        span=pageNav.find('span',class_='current')
        next=span.next_sibling
        nextStr=next.string
        nextStr=nextStr.strip()
        if nextStr=='':
            return False
        return True
    def saveTaskList(self):
        '''
        保存任务列表
        '''
        data=[]
        taskList=[]
        if len(self.list)!=0:
            for task,classify in self.list:
                taskId=UUIDUtil.getId()
                taskList.append(VfxinfoTask(taskId,task,classify))
                data.append(("INSERT INTO task_list(id,href,site_id,classify) VALUES(%s,%s,%s,%s)",(taskId,task,self.taskPackage.siteId,classify)))
            self.taskList=taskList 
            dao=BaseDao()
            dao.createConnect()
            dao.beachInsert(data)