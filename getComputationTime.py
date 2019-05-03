###############
##
## Script to determine run time for reconstruction
## Brandon Clary
## 4/18/2019
##
###############


# string and file 
import mmap
import re
import os
import glob

# plotting libraries
import matplotlib.pyplot as plt


dirIn="/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-5bp7p8/log/"


monitor_time=[]
avg_event_time=[]

test_counter = 0
for root, dirs, files in os.walk('/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-5bp7p8/log/'):
   for file in files:
      if 'dataUT' in file:
         if 'orch.log' in file:

            print file
      
            f = open(dirIn+file)

            if 'Total orchestrator time  =' in open(dirIn+file).read():
               #print "true"
               s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
               while True:
                  line=s.readline()
               
                  if line.find('Processed  500 events in  ') != -1:
                     newstr = ''.join((ch if ch in '0123456789.' else ' ') for ch in line[10:])
                     listOfNumbers = [float(i) for i in newstr.split()]
                     avg_event_time.append(listOfNumbers[5:][0])
                     
                  if line.find('Total orchestrator time  =') != -1:
                     #print line.rstrip()
                     newstr = ''.join((ch if ch in '0123456789.' else ' ') for ch in line[10:])
                     listOfNumbers = [float(i) for i in newstr.split()]
                     #print(listOfNumbers[-1:][0])      
                     monitor_time.append(listOfNumbers[-1:][0])
                     break
            test_counter=test_counter+1

      #if test_counter == 200:
      #   print test_counter
      #   break



print ' making histogram '
fig1, ax1 = plt.subplots()
ax1.set_title('CLARA Orchestrator Time for Full Jobs')
ax1.hist(monitor_time,bins=100)
ax1.set_xlabel('Orchestrator Time (sec)')
fig1.savefig('time_to_complete_full_recon.png')

fig2, ax2 = plt.subplots()
ax2.set_title('CLARA Avg Time per Event for Full Jobs')
ax2.hist(avg_event_time,bins=500)
ax2.set_xlabel('Avg. Event Time (ms)')
fig2.savefig('avg_event_time_full_recon.png')

print 'done'
