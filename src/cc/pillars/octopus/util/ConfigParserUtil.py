'''
Created on Dec 18, 2014

@author: sen
'''
import configparser


class ConfigParserUtil:
    '''
    读取.ini配置文件工具类
    '''
    #配置文件存放目录
    filePath=None
    
    @staticmethod
    def getValue(section,option):
        '''
        取得section中option的值
        '''
        config = configparser.ConfigParser()
        config.read(ConfigParserUtil.filePath)
        return config.get(section, option)
    @staticmethod
    def getDictionary(section=None):
        '''
        以字典的形式返回配置文件的参数
        如果section==None 返回所有{section，{k:v,k:v}}格式
        如果如果section！=None 返回{k:v,k:v}格式
        '''
        config = configparser.ConfigParser()
        config.read(ConfigParserUtil.filePath)
        dictionarys={}
        for i in config.sections():
            params = config.items(i)
            dictionary={}
            for (k,v) in params:
                dictionary[k]=v
            dictionarys[i]=dictionary
            if section!=None and  section==i:
                return dictionary
        return dictionarys
                