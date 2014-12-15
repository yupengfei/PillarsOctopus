'''
Created on Dec 9, 2014

@author: sen
'''
from cc.pillars.octopus.scratch.VfxinfoScratch import VfxinfoScratch

class Site:
    '''
    entity Site
    '''


    def __init__(self, name,address,hrefList,scratch):
        self.name=name
        self.address=address
        self.hrefList=hrefList
        self.scratch=scratch
