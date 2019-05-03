import glob
import os
import sys, getopt

input_runList = ''
input_recon_bank_format=''
input_resub=False
outputfile = ''
input_timestamp=''

argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv,"hl:t:r:s:",["runList=","jobType=","resub=","timestamp="])
except getopt.GetoptError:
    print 'run-makeClara.py -l <runList> -t <jobType> -r <resub default =false>, -s <timestamp monthdayyear>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print 'run-makeClara.py -l <runList> -t <jobType data/calibration/monitor> -r <resub default=False> -s <timestamp monthdayyear>'
        sys.exit()
    elif opt in ("-l", "--runList"):
        input_runList = arg
    elif opt in ("-t", "--jobType"):
        input_recon_bank_format = arg
    elif opt in ("-r", "--resub"):
        input_resub = arg
    elif opt in ("-s","--timestamp"):
        input_timestamp=arg

print 'Input file is :', input_runList
print 'Input job type:"', input_recon_bank_format
print 'Input Resubmit :', input_resub
print 'Input timestamp :', input_timestamp





# user inputs
#clara version
clara_version='clara-5bp7p8'
clara_recon_bank_format=input_recon_bank_format #'data' #'monitor' #'calibration'

resub=False
if input_resub == 'True':
    resub=True


clara_service_file='/w/hallb-scifs17exp/clas12/rg-a/software/'+clara_version+'/plugins/clas12/config/'+clara_recon_bank_format+'_'+input_timestamp+'.yaml'

#path locations
clara_config_dir='/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-5bp7p8/config/'
clara_job_dir='/w/hallb-scifs17exp/clas12/rg-a/software/clara_jobs/'
runList = open("/w/hallb-scifs17exp/clas12/rg-a/software/"+input_runList,"r") ######################### CHANGE THIS 

######################################
#####   CHANGE THIS!!!!!!!!
#####
#inputDir="/volatile/clas12/clas12/data/calib/decoded/" #"/volatile/clas12/rg-a/production/decoded/coatV5bp7p8/"
#inputDir="/lustre/expphy/volatile/clas12/rg-a/production/decoded/coatV5bp7p8/"# "/volatile/clas12/rg-a/production/decoded/coatV5bp7p8/"
inputDir="/work/clas12/rg-a/data/decoded/"

output_dir=""
farm_time=''
if clara_recon_bank_format == 'monitor':
    farm_time='900'
     #/volatile/clas12/rg-a/production/recon/pass0/v0/mon/" is the old file location, but still could be used in various cases
    output_dir="/work/clas12/rg-a/production/recon/pass0/v0/mon/"
elif clara_recon_bank_format == 'data':
    farm_time='800'
    output_dir="/work/clas12/rg-a/production/recon/pass0/v0/unfiltered/" #/volatile/clas12/rg-a/production/recon/pass0/v0/mon/"
elif clara_recon_bank_format == 'calibration':
    farm_time='700'
    output_dir="/w/hallb-scifs17exp/clas12/rg-a/production/recon/calib/v0/filtered/"

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
 

run_counter=0
farm_cpu=""
farm_mem=""
farm_node=""
farm_node_options=["qcd12s","farm18","farm16"]
farm_mem_options=["31","92","62"]
farm_cpu_options=["32","80","72"]
farm_scaling=""

farm_big_jobs=False
if farm_big_jobs:
    farm_scaling="200"
else:
    farm_scaling="20"

for r in runs:
    r_file_list='files_clas12-2_00'+str(r)+'.txt'

    # check if directory with decoded files exists and has at least one file before creating jobs
    # add another condition that it will only run reconstruction if the recon run output directory does not exist
    if run_counter < len(runs)/2 :
        farm_node=farm_node_options[1]
    #elif run_counter >= len(runs)/3 and run_counter < len(runs)*2.0/3.0 :
    #    farm_node=farm_node_options[1]
    else:
        farm_node=farm_node_options[2]
    print ' sending jobs to farm node %s ' % (farm_node)

    
    #farm_node="farm16"

    if farm_big_jobs==True:
        if farm_node == farm_node_options[0]:
            farm_mem=farm_mem_options[0]
            farm_cpu=farm_cpu_options[0]
        elif farm_node == farm_node_options[1]:
            farm_mem=farm_mem_options[1]
            farm_cpu=farm_cpu_options[1]
        elif farm_node == farm_node_options[2]:
            farm_mem=farm_mem_options[2]
            farm_cpu=farm_cpu_options[2]
    else:
        farm_mem="40"
        farm_cpu="10"

    print ' requesting cpu %s and mem %s ' % (farm_cpu,farm_mem)

    if os.path.exists(inputDir+"r00"+str(r)+'/'): ######## r here
        path, dirs, files = next(os.walk(inputDir+"r00"+str(r))) # add r here for calib
        file_count = len(files)
        print ' Found %d files' % (file_count)
        if file_count >= 10 :
            if resub == False:

                clara_file_list = open(clara_config_dir+r_file_list,"w")
                file_list = glob.glob(os.path.join(inputDir+"r00"+r,"*.hipo")) # add r here for calib
                file_counter=0
                file_list.sort(key=lambda f: int(filter(str.isdigit, os.path.basename(f))))

                file_limit=10
                if clara_recon_bank_format  == 'monitor':
                    file_limit=10
                if clara_recon_bank_format == 'calib' or clara_recon_bank_format == 'data':
                    file_limit=len(file_list)

                print ' File Limit for Jobs is: %d ' % (file_limit)

                for f in file_list:
                    #if file_counter < 10:  # or file_counter > (len(file_list)-10): #####################
                    if file_counter < file_limit:
                        print " adding file " + os.path.basename(f) + " to " + r_file_list
                        if resub == False:
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
            clara_job.write('set outputFilePrefix ' + clara_recon_bank_format+'_'+'\n');
            if not os.path.exists('/work/clas12/rg-a/software/clara_data/coatjava-5bp7p8/log/'+clara_version+'/'+clara_recon_bank_format+'/'):
                os.mkdir('/work/clas12/rg-a/software/clara_data/coatjava-5bp7p8/log/'+clara_version+'/'+clara_recon_bank_format+'/')
            clara_job.write('set logDir /work/clas12/rg-a/software/clara_data/coatjava-5bp7p8/log/'+clara_version+'/'+clara_recon_bank_format+'/' + '\n');
            clara_job.write('set session clas122'+'R00'+r+' \n')
            clara_job.write('set description ' + clara_recon_bank_format + "UT" + str(unix_timestamp) + 'PASS0V0R00'+r +' \n')
            clara_job.write('set farm.cpu '+ farm_cpu +' \n')
            clara_job.write('set farm.memory ' + farm_mem + ' \n')
            clara_job.write('set farm.disk 5 \n')
            clara_job.write('set farm.time ' + farm_time + ' \n')
            clara_job.write('set farm.os centos7 \n')
            clara_job.write('set farm.node ' + farm_node + ' \n')
            #clara_job.write('set farm.exclusive \n')
            clara_job.write('set farm.stage /scratch/clara/clas12-2 \n')
            clara_job.write('set farm.track reconstruction \n')
            clara_job.write('set farm.scaling '+farm_scaling+' \n')
            clara_job.write('set farm.system jlab \n')
            clara_job.write('run farm \n')
            clara_job.close()
    else:
        print ' output directory exists. exiting reconstruction submission '
    run_counter=run_counter+1
                

    
    



print 'complete'
