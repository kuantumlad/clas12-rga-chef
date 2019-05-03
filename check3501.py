import os
import glob

dir_path1= "/work/clas12/rg-a/production/recon/calib/v0/filtered/003501/"
dir_path2= "/volatile/clas12/clas12/data/calib/decoded/"

file_list1=open("completed3501.txt","w")
file_list2=open("full3501.txt","w")

for filename in os.listdir(dir_path1):
    if filename.endswith(".hipo"):
         # print(os.path.join(directory, filename))
        file_list1.write(filename[11:]+"\n")
        continue
    else:
        continue


print glob.glob(dir_path2+'clas_003501*.')

#for filename in os.listdir(dir_path2):
    
 #   if filename.endswith(".hipo"):
         # print(os.path.join(directory, filename))
       # print filename[6:-14]
      #/#  #file_list2.write(filename)
  #      continue
   # else:
    #    continue
