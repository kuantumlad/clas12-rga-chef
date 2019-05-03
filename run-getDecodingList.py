import os
import glob

rga_fall18_runs =open("runListFall2018Check.txt","r")
rga_fall18_files = open("runListFall2018Decoded.txt","r")

rga_fall18_to_decode = open("runListFall2018toDecode.txt","w");


file_list = []
for f in rga_fall18_files:
#    print f[:-1]
    file_list.append(f[:-1])


run_list = []
for r in rga_fall18_runs:
 #   print r[:-1]
    run_list.append(r[:-1])


files_per_run=[]
for r in run_list:    
    temp_list=[f for f in file_list if 'clas_00'+r in f]
    temp_list_size=len(temp_list)
    if temp_list_size < 10 :
        n_files_to_decode = 10 - temp_list_size
        print "%s %d" % (r, n_files_to_decode)
        rga_fall18_to_decode.write(r + " " +str(n_files_to_decode) +"\n")
   # files_per_run.append(temp_list)
    


rga_fall18_runs.close()
rga_fall18_files.close()
rga_fall18_to_decode.close()
