'''
Created on Dec 12, 2014

@author: pillars
'''
from cc.pillars.octopus.scratch.VfxinfoScratch import VfxinfoScratch
from cc.pillars.octopus.scratch.BaseScratch import BaseScratch


if __name__ == '__main__':
    #v=VfxinfoScratch()
    #v.doScratch('http://vfxinfo.net/2014/10/16/thinkingparticles-v6-is-released-with-new-pricing/')
    basse=BaseScratch()
    print(len(basse.downLoadPicture("http://pic.yupoo.com/wkkw/EhDrU1tO/4p7aS.jpg")))