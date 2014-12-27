'''
Created on Dec 24, 2014

@author: pillars
'''

class TaskPackage:
    '''
    entity TaskPackage
    '''


    def __init__(self,siteId,siteName,configPath,module,remarks):
        self.siteId=siteId
        self.siteName=siteName
        self.configPath=configPath
        self.module=module
        self.remarks=remarks