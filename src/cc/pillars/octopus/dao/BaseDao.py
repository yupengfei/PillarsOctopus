'''
Created on Dec 18, 2014

@author: sen
'''
import mysql.connector

from cc.pillars.octopus.util.ConfigParserUtil import ConfigParserUtil


class BaseDao:
    '''
    mysql数据库访问
    '''

    databaseConfig=None

    def getParameter(self,key):
        '''
        加载配置
        '''
        if BaseDao.databaseConfig==None:
            configParser=ConfigParserUtil()
            BaseDao.databaseConfig=configParser.getDictionary('database')
        return BaseDao.databaseConfig[key]
    def createConnect(self):
        '''
        获得数据库链接
        '''
        #如果是mysql数据库
        if self.getParameter('type')=='mysql':
            con=mysql.connector.connect(user=self.getParameter('user'), password=self.getParameter('password'), host=self.getParameter('host'), database=self.getParameter('db'),charset=self.getParameter('charset'))
            cursor = con.cursor()
            self.con=con
            self.cursor=cursor
            #如果是oracle数据库 其他数据库未填写如有需要再补充
        elif self.getParameter('type')=='oracle':
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
        if self.getParameter('type')=='mysql':
            self.cursor.close()
            self.con.close()
        else:
            print('不支持数据库')       