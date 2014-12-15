'''
Created on 2014年12月7日

@author: sen
'''

import logging
import os


class LogUtil:
    '''
    日志配置
    '''
    #任务日志文件路径
    runtimeLogFile=os.getcwd()+'/config/runtimeLog.log'
    #错误日志文件路径
    errorLogFile=os.getcwd()+'/config/errorLog'

    @staticmethod
    def info(message):
        '''
        记录任务日志
        '''
        print(message)
        logging.basicConfig(level=logging.INFO,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename=LogUtil.runtimeLogFile)
        logging.info(message)
    @staticmethod
    def error(message):
        '''
        记录错误日志
        '''
        logging.basicConfig(level=logging.ERROR,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename=LogUtil.errorLogFile)
        logging.ERROR(message)