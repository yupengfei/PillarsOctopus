'''
Created on 2014年12月5日

@author: root
'''
from bs4 import BeautifulSoup
import mysql.connector
import os


class DateBaseConfig:
    '''
    数据库配置文件解析类
    ps:mysqldbl 不支持python3
    这里使用 MySQL Connector/Python
    '''
    #配置文件名称
    fileName='datebaseConfig.xml'
    #数据库类型 默认为mysql
    dateBaseType='mysql'


    def __init__(self):
        '''
        构造函数，解析配置文件
        '''
        file = open(os.getcwd()+'/config/'+DateBaseConfig.fileName)
        try:
            xmlStr=file.read()
        except IOError as e:
            print(e)
        finally:
            file.close()
        #解析配置文件
        soup=BeautifulSoup(xmlStr)
        dateBase=soup.find('datebase')
        #获得数据库类型
        DateBaseConfig.dateBaseType=dateBase['type']
        #数据库地址
        self.host=soup.find('host').string
        #用户名
        self.user=soup.find('user').string
        #密码
        self.password=soup.find('password').string
        #数据库
        self.db=soup.find('db').string
        #端口
        self.port=soup.find('port').string
        #字符集
        self.charset=soup.find('charset').string
        #如果需要可继续添加或修改
    def createConnect(self):
        '''
        获得数据库链接
        '''
        #如果是mysql数据库
        if DateBaseConfig.dateBaseType=='mysql':
            con=mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.db,charset=self.charset)
            cursor = con.cursor()
            self.con=con
            self.cursor=cursor
            #如果是oracle数据库 其他数据库未填写如有需要再补充
        elif DateBaseConfig.dateBaseType=='oracle':
            pass
        else:
            #如果以上都不符合说明不支持该数据库
            print('不支持该数据库')
    def beachInsert(self,dates):
        '''
        批量执行插入操作
        '''
        cursor=self.cursor
        con=self.con
        for sql,date in dates:
            cursor.execute(sql,date)
        con.commit()
        self.close()
    def doSelect(self,sql):
        '''
        执行查询语句
        '''
        cursor=self.cursor
        cursor.execute(sql)
        fetchall=cursor.fetchall()
        self.close()
        return fetchall
    def close(self):
        '''
        关闭链接
        '''
        if DateBaseConfig.dateBaseType=='mysql':
            self.cursor.close()
            self.con.close()
        else:
            print('不支持数据库')        