'''
Created on Dec 25, 2014

@author: sen
'''
import uuid


class UUIDUtil:
    '''
    UUIDUtil
    '''
    @staticmethod
    def getId():
        '''
        生成以个36位随机数
        当做ID
        '''
        return uuid.uuid1().__str__()