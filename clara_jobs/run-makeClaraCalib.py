import glob
import os


# user inputs
#clara version
clara_version='clara-5bp7p8'
clara_recon_bank_format='calibration'
clara_service_file='/w/hallb-scifs17exp/clas12/rg-a/software/'+clara_version+'/plugins/clas12/config/'+clara_recon_bank_format+'.yaml'

#path locations
clara_config_dir='/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-5bp7p8/config/'
clara_job_dir='/w/hallb-scifs17exp/clas12/rg-a/software/clara_jobs/'
runList = open("/w/hallb-scifs17exp/clas12/rg-a/software/runListCalibPart2.txt","r") ######################### CHANGE THIS 

######################################
#####   CHANGE THIS!!!!!!!!
#####
inputDir="/volatile/clas12/clas12/data/calib/decoded/" #"/volatile/clas12/rg-a/production/decoded/coatV5bp7p8/"
#inputDir="/lustre/expphy/volatile/clas12/rg-a/production/decoded/coatV5bp7p8/"# "/volatile/clas12/rg-a/production/decoded/coatV5bp7p8/"


output_dir=""
if clara_recon_bank_format == 'monitor':
    output_dir="/volatile/clas12/rg-a/production/recon/pass0/v0/mon/"
elif clara_recon_bank_format == 'calibration':
    output_dir="/w/hallb-scifs17exp/clas12/rg-a/production/recon/calib/v0/unfiltered/"

print ' output dir: ' + output_dir
#get unixtime for timestamp
import time
unix_timestamp = int(time.time()) 
print "RECON TIME STAMP: " + str(unix_timestamp)

#grab runs in run list file
runs=[]
for r in runList:
    #check if directory for this run exists with 10 or more files in it.     
    runs.append(r[:-1])
    

#create txt file with files to reconstruct for a given run

for r in runs:
    r_file_list='files_clas12-2_00'+str(r)+'.txt'

    # check if directory with decoded files exists and has at least one file before creating jobs
    # add another condition that it will only run reconstruction if the recon run output directory does not exist
    if os.path.exists(inputDir+"r00"+str(r)+'/'): ######## r here
        path, dirs, files = next(os.walk(inputDir+"r00"+str(r))) # add r here for calib
        file_count = len(files)
        print 'here '
        if file_count >= 10 :
            clara_file_list = open(clara_config_dir+r_file_list,"w")
            file_list = glob.glob(os.path.join(inputDir+"r00"+r,"*.hipo")) # add r here for calib
            file_counter=0

            file_list.sort(key=lambda f: int(filter(str.isdigit, os.path.basename(f))))

            for f in file_list:
                #if file_counter < 10:  # or file_counter > (len(file_list)-10): #####################
                print " adding file " + os.path.basename(f) + " to " + r_file_list
                clara_file_list.write(os.path.basename(f)+'\n')
                file_counter=file_counter+1

            clara_file_list.close()

            #create output directory for recon files to go if it doesnt exist already
            if not os.path.exists(output_dir+"00"+r) :
                print output_dir+"00"+r + " doesnt exist -> Creating directory"
                os.mkdir(output_dir+"00"+r)

            clara_job=open(clara_job_dir+clara_recon_bank_format+'_r00'+r+'_ConfigSlurm.txt',"w")
            clara_job.write('set servicesFile '+clara_service_file +'\n')
            clara_job.write('set fileList '+clara_config_dir+r_file_list+'\n')
            clara_job.write('set inputDir ' + inputDir +'r00'+r+'\n'); ################## add r here
            clara_job.write('set outputDir ' + output_dir +'00'+r+'\n');
            clara_job.write('set outputFilePrefix ' + clara_recon_bank_format+'\n');
            if not os.path.exists('/work/clas12/rg-a/software/clara_data/coatjava-5bp7p8/log/'+clara_version+'/'+clara_recon_bank_format+'/'):
                os.mkdir('/work/clas12/rg-a/software/clara_data/coatjava-5bp7p8/log/'+clara_version+'/'+clara_recon_bank_format+'/')
            clara_job.write('set logDir /work/clas12/rg-a/software/clara_data/coatjava-5bp7p8/log/'+clara_version+'/'+clara_recon_bank_format+'/' + '\n');
            clara_job.write('set session clas122'+'R00'+r+' \n')
            clara_job.write('set description ' + clara_recon_bank_format + "UT" + str(unix_timestamp) + 'R00'+r +' \n')
            clara_job.write('set farm.cpu 8 \n')
            clara_job.write('set farm.memory 30 \n')
            clara_job.write('set farm.disk 5 \n')
            clara_job.write('set farm.time 800 \n')
            clara_job.write('set farm.os centos7 \n')
            clara_job.write('set farm.node qcd12s \n')
            clara_job.write('set farm.exclusive \n')
            clara_job.write('set farm.stage /scratch/clara/clas12-2 \n')
            clara_job.write('set farm.track reconstruction \n')
            clara_job.write('set farm.scaling 12 \n')
            clara_job.write('set farm.system jlab \n')
            clara_job.write('run farm \n')
            clara_job.close()
    else:
        print ' output directory exists. exiting reconstruction submission '

                

    
    



print 'complete'
