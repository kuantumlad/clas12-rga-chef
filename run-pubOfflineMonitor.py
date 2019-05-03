import os
import glob
import subprocess

input_file_list=open("/w/hallb-scifs17exp/clas12/rg-a/software/runList100.txt","r")

counter=1
for r in input_file_list:
    print 'Submitting clas12 offline monitoring plots for run ' + r[:-1]
    print subprocess.call('./run-getRunInfo.sh ' + r[:-1], shell=True)
    print subprocess.call('./pubOfflineMonitor.sh '+r[:-1], shell=True)
    






