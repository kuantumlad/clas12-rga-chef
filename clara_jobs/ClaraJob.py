import sys
import collections
import json

class ClaraJob:


    def __init__(self,workflow):
        self.project='clas12'
        self.track='reconstruction'
        self.cores=1
        self.time='2h'
        self.disk='3GB'
        self.ram='3500MB'
        self.shell='/bin/tcsh'
        self.tags=collections.OrderedDict()
        self.inputs=[]
        self.outputs=[]
        self.logDir=None
        self.cmd=''
