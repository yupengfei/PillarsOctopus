'''
Created on Dec 9, 2014

@author: sen
'''
from bs4 import BeautifulSoup
import os
import urllib
import urllib.request

from cc.pillars.octopus.config.DateBaseConfig import DateBaseConfig
from cc.pillars.octopus.scratch.BaseScratch import BaseScratch


class VfxinfoScratch(BaseScratch):
    '''
    VfxinfoScratch
    '''

    
    def doWork(self,site):
        self.site=site
        list=site.hrefList
        for href in list:
            self.doAnalyze(href)
            
    def doAnalyze(self,href):
        '''
            对页面进行解析
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
            bo=True
            for a in posts:
                h3=a.find('h3',class_='post-title')
                a=h3.find('a')
                aHref=a['href']
                bo=self.doScratch(aHref)
                if bo==False:
                    break
            if bo==False:
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
        #<span class="current">6</span>        </div>
        #<span class="current">3</span><a 
        #sibling_soup.b.next_sibling
        span=pageNav.find('span',class_='current')
        next=span.next_sibling
        nextStr=next.string
        nextStr=nextStr.strip()
        if nextStr=='':
            return False
        return True
    
    def doScratch(self,href): 
        '''
        对页面进行抓取
        '''
        self.page_index=0
        dao=DateBaseConfig()
        dao.createConnect()
        fetchall=dao.doSelect("SELECT id FROM page_info WHERE url='"+href+"'")
        if len(fetchall)!=0:
            return False
        fp = urllib.request.urlopen(href)
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
        parent_id=self.getId()
        dates=[]
        #sqls.append("INSERT INTO page_info(id,url,belongs_site,title,promulgator,issues_time,scratch_time) VALUES(%s,%s,%s,%s,%s,%s,%s)")
        #date.append((self.getId(),href,self.site.address,title,promulgator,issuesTime,self.getTime_Long()))
        dates.append(("INSERT INTO page_info(id,url,belongs_site,title,promulgator,issues_time,scratch_time) VALUES(%s,%s,%s,%s,%s,%s,%s)",(parent_id,href,self.site.address,title,promulgator,issuesTime,self.getTime_Long())))
        #dates.append(("INSERT INTO page_info(id,url,belongs_site,title,promulgator,issues_time,scratch_time) VALUES(%s,%s,%s,%s,%s,%s,%s)",(parent_id,href,'aaa',title,promulgator,issuesTime,self.getTime_Long())))
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
        if child.name=='div':
            if 'class' in child.attrs:
                classs=child['class']
                #判断是否是最后一个DIV标记
                if len(classs)==2 and classs[0]=='bdsharebuttonbox' and classs[1]=='post-share':
                    return False
                if len(classs)==1 and classs[0]=='clear':
                    return True
            dates.append(("INSERT INTO page_href(id,parent_id,page_href_html,page_index) VALUES(%s,%s,%s,%s)",(self.getId(),parent_id,str(child),self.page_index)))
            self.page_index+=1
        #如果是<P>
        if child.name=='p':
            img=child.find('img')
            embed=child.find('embed')
            if img!=None:
                image_url=str(img['data-original'])
                imageblob=self.downLoadPicture(image_url)
                dates.append(("INSERT INTO page_image(id,parent_id,image_blob,image_url,page_index) VALUES(%s,%s,%s,%s,%s)",(self.getId(),parent_id,imageblob,image_url,self.page_index)))
                self.page_index+=1
                return True
            if embed!=None:
                dates.append(("INSERT INTO page_embed(id,parent_id,embed_html,embed_url,page_index) VALUES(%s,%s,%s,%s,%s)",(self.getId(),parent_id,str(embed),str(embed['src']),self.page_index)))
                self.page_index+=1
                return True
            if child.string==None:
                if len(child.findAll('b'))!=0:
                    strP=""
                    for i in child.findAll('b'):
                        strP+=str(i.string)
                    dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(self.getId(),parent_id,strP,self.page_index)))
                    self.page_index+=1
                    return True
            if child.string.strip()=='':
                return True
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(self.getId(),parent_id,str(child.string),self.page_index)))
            self.page_index+=1
        if child.name=='h3':
            dates.append(("INSERT INTO page_paragraph(id,parent_id,paragraph,page_index) VALUES(%s,%s,%s,%s)",(self.getId(),parent_id,str(child.string),self.page_index)))
            self.page_index+=1