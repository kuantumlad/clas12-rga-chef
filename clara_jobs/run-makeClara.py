import glob
import os
import sys, getopt
import argparse
from RunFileUtil import RunFileGroups
from SwifJob import SwifJob
from SwifWorkflow import SwifWorkflow

'''
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
'''

parse = argparse.ArgumentParser(description="Script to create clara submission files for reconstruction")
parse.add_argument('--pass', action="store", help='production pass', dest='prod_pass',type=str,default='pass0') #remove default later
parse.add_argument('--version', action="store", help='version pass', dest='prod_version',type=str,default='v0')
parse.add_argument('-l', action="store", help='run list in txt file', dest='run_list',type=str)
parse.add_argument('-t', action="store", help='jobType data/calibration/monitor', dest='job_type',type=str)
parse.add_argument('-s', action="store", help='time stamp MMDDYYYY',dest='time_stamp',type=str)
parse.add_argument('--resubmit', action="store", help='create updated resubmission file', default=False,dest='resubmit',type=bool)
parse.add_argument('-v', action="store", help='coatjava version', dest='clara_version',type=str)
parse.add_argument('--outDir', action="store", help='dir for clara submission files',dest='out_dir',type=str,default='/w/hallb-scifs17exp/clas12/rg-a/software/clara_jobs/')
parse.add_argument('--reconOutDir', action="store", help='dir for cooked files mon/unfiltered ',dest='recon_out_dir',type=str)
parse.add_argument('--decodedInDir',action='store', help='parent dir with decoded files',dest='decoded_in_dir',type=str)
parse.add_argument('--jobSize', action="store", help='small/medium/big use exclusive for big jobs',dest='job_size',type=str)
parse.add_argument('--farmTime',action="store",help='farm.time value',dest='farm_time',type=str,default="900")
parse.add_argument('--runPeriod',action="store",help='run period Spring2018/Fall2018/etc.',dest='run_period',type=str)

print parse.parse_args()

results=parse.parse_args()

input_runList = results.run_list
input_recon_bank_format=results.job_type
input_resub=results.resubmit
input_timestamp=results.time_stamp
input_version=results.clara_version
input_outDir=results.out_dir
input_recon_outdir = results.recon_out_dir
input_decoded_in_dir = results.decoded_in_dir
input_prod_pass=results.prod_pass
resub=False #results.resubmit

print 'Input pass is : ', results.prod_pass
print 'Input version is : ', results.prod_version
print 'Input file is :', input_runList
print 'Input job type:"', input_recon_bank_format
print 'Input Resubmit :', input_resub
print 'Input timestamp :', input_timestamp
print 'Input version :', input_version
print 'Input outDir :', input_outDir
print 'Input reconOutDir :' , input_recon_outdir
print 'Input input_decoded_in_dir : ', input_decoded_in_dir 
print 'Input input_recon_bank_format : ', input_recon_bank_format 


recon_out_dir=''
clara_recon_bank_format=input_recon_bank_format
if clara_recon_bank_format=='monitor':
    recon_out_dir='mon'
elif clara_recon_bank_format=='data':
    recon_out_dir='unfiltered'
elif  clara_recon_bank_format =='calibration':
    recon_out_dir='unfiltered'
# set user inputs to variables used in code 


if results.job_type =='calibration':
    input_prod_pass='calib'

 
clara_version="clara-"+input_version
clara_recon_bank_format=input_recon_bank_format #'data' #'monitor' #'calibration'
#clara_service_file='/w/hallb-scifs17exp/clas12/rg-a/software/'+clara_version+'/plugins/clas12/config/'+clara_recon_bank_format+'_'+input_timestamp+'.yaml'
clara_service_file='/w/hallb-scifs17exp/clas12/rg-a/software/'+clara_version+'/plugins/clas12/config/'+clara_recon_bank_format+'.yaml'
clara_command_dir='/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-'+clara_version+'/config/farm_clas12'


#path locations
clara_config_dir='/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-'+input_version+'/config/'
clara_job_dir = results.out_dir #'/w/hallb-scifs17exp/clas12/rg-a/software/clara_jobs/'
runList = open("/w/hallb-scifs17exp/clas12/rg-a/software/"+input_runList,"r")
inputDir = input_decoded_in_dir #"/work/clas12/rg-a/data/decoded/"
output_dir="/work/clas12/rg-a/production/recon/"+input_prod_pass+'/'+results.prod_version+'/'+recon_out_dir+'/'


#set farm variables
farm_time=results.farm_time
farm_job_size=results.job_size


'''output_dir=""
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
'''


print ' output dir: ' + output_dir
#get unixtime for timestamp
import time
unix_timestamp = int(time.time()) 
print "RECON TIME STAMP: " + str(unix_timestamp)

#grab runs in run list file
runs=[]
for r in runList:
    #this will be used to check if directory for this run exists with 10 or more files in it.     
    runs.append(r[:-1])
    

#create txt file with files to reconstruct for a given run
 

run_counter=0
farm_cpu=""
farm_mem=""
farm_node=""
farm_node_options=["qcd12s","farm18","farm16"]
farm_mem_options=["31","92","62","0"]
farm_cpu_options=["32","80","72","0"]
farm_scaling="20"

farm_big_jobs=False
if farm_job_size == 'big':
    farm_scaling="50"
    farm_big_jobs=True
elif farm_job_size == 'small':
    farm_scaling="20"


job_number=0
workflow = SwifWorkflow("swf_clas12_RGA_"+input_recon_bank_format)

for r in runs:

    # name list with files for clara
    r_file_list='files_clas12-2_00'+str(r)+'.txt'

    # break the jobs across mutliple clara nodes 
    # dont use qcd nodes - continually face issues where JAVA is not installed on node
    if run_counter < len(runs)/2 :
        farm_node=farm_node_options[1]
    #elif run_counter >= len(runs)/3 and run_counter < len(runs)*2.0/3.0 :
    #    farm_node=farm_node_options[1]
    else:
        farm_node=farm_node_options[2]
    print ' sending jobs to farm node %s ' % (farm_node)


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
        farm_mem=farm_mem_options[3]
        farm_cpu=farm_cpu_options[3]

    print ' requesting cpu %s and mem %s ' % (farm_cpu,farm_mem)


    # check if directory with decoded files exists and has at least one file before creating jobs
    if os.path.exists(inputDir+"00"+str(r)+'/'): ######## r here
        path, dirs, files = next(os.walk(inputDir+"00"+str(r))) # add r here for calib
        file_count = len(files)
        print ' Found %d files' % (file_count)

        #group_file_list=[]
        file_list=[]
        if file_count >= 10 :
            print ' here '
            print resub
            if resub == False:

                clara_file_list = open(clara_config_dir+r_file_list,"w")
                temp_file_list = glob.glob(os.path.join(inputDir+"00"+r,"*.hipo")) # add r here for calib
                temp_file_list.sort(key=lambda f: int(filter(str.isdigit, os.path.basename(f))))
                #print "file list "
                #print temp_file_list
                file_counter=0

                file_limit=10
                if clara_recon_bank_format  == 'monitor':
                    file_limit=10
                if clara_recon_bank_format == 'calib' or clara_recon_bank_format == 'data':
                    file_limit=len(temp_file_list)

                print ' File Limit for Jobs is: %d ' % (file_limit)

                for f in temp_file_list:
                    #if file_counter < 10:  # or file_counter > (len(file_list)-10): #####################
                    if file_counter < file_limit:
                        print " adding file " + os.path.basename(f) + " to " + r_file_list
                        if resub == False:
                            #clara_file_list.write(os.path.basename(f)+'\n')
                            file_list.append(os.path.basename(f))
                            print 'here'
                            file_counter=file_counter+1

                clara_file_list.close()

            #create output directory for recon files to go if it doesnt exist already
            if not os.path.exists(output_dir+"00"+r) :
                print output_dir+"00"+r + " doesnt exist -> Creating directory"
                #os.mkdir(output_dir+"00"+r)

            #####################
            ## use SwifJob to help write job to json for swif
            swif_job=SwifJob("clas12-rga-"+input_recon_bank_format)
            swif_job.setNumber(run_counter)
            swif_job.setPhase(1)
            swif_job.setTime('1440s')
            swif_job.setDisk('5GB')
            swif_job.setCores(int(farm_cpu))
            swif_job.setRam(farm_mem)
            swif_job.setCmd(clara_command_dir+'clas122'+'R00'+r+'_'+clara_recon_bank_format + "UT" + str(unix_timestamp) + 'PASS0V0R00'+r+'.sh')
            workflow.addJob(swif_job)
            print swif_job.getJson()

            '''clara_job=open(clara_job_dir+clara_recon_bank_format+'_r00'+r+'_ConfigSlurm.txt',"w")
            clara_job.write('set servicesFile '+clara_service_file +'\n')
            clara_job.write('set fileList '+clara_config_dir+r_file_list+'\n')
            clara_job.write('set inputDir ' + inputDir +'r00'+r+'\n'); ################## add r here
            clara_job.write('set outputDir ' + output_dir +'00'+r+'\n');
            clara_job.write('set outputFilePrefix ' + clara_recon_bank_format+'_'+'\n');
            if not os.path.exists('/work/clas12/rg-a/software/clara_data/coatjava-'+input_version+'/log/'+clara_version+'/'+clara_recon_bank_format+'/'):
                os.mkdir('/work/clas12/rg-a/software/clara_data/coatjava-'+input_version+'/log/'+clara_version+'/'+clara_recon_bank_format+'/')
            clara_job.write('set logDir /work/clas12/rg-a/software/clara_data/coatjava-'+input_version+'/log/'+clara_version+'/'+clara_recon_bank_format+'/' + '\n');
            clara_job.write('set session clas122'+'R00'+r+' \n')
            clara_job.write('set description ' + clara_recon_bank_format + "UT" + str(unix_timestamp) + 'PASS0V0R00'+r +' \n') ## will needs to change later
            clara_job.write('set farm.cpu '+ farm_cpu +' \n')
            clara_job.write('set farm.memory ' + farm_mem + ' \n')
            clara_job.write('set farm.disk 5 \n')
            clara_job.write('set farm.time ' + farm_time + ' \n')
            clara_job.write('set farm.os centos7 \n')
            clara_job.write('set farm.node ' + farm_node + ' \n')
            if results.job_size == 'big':
                clara_job.write('set farm.exclusive \n')
            clara_job.write('set farm.stage /scratch/clara/clas12-2 \n')
            clara_job.write('set farm.track reconstruction \n')
            clara_job.write('set farm.scaling '+farm_scaling+' \n')
            clara_job.write('set farm.system jlab \n')
            clara_job.write('run farm \n')
            
            clara_job.close()
            '''
            print (file_count)
   
            if file_count > 20:

                farm_scaling_int=int(farm_scaling)
                print " scaling value %d " % (farm_scaling_int)
                n_jobs_scaled = (int)(file_count)/farm_scaling_int
                print ' n jobs scaled %d ' %(n_jobs_scaled)
                ff_counter = 0
                print file_list
                group_file_list= [file_list[i * farm_scaling_int:(i + 1) * farm_scaling_int] for i in range((len(file_list) + farm_scaling_int - 1) // farm_scaling_int )]  
                print (group_file_list)

                for jj in range(0,len(group_file_list)):
                    print " job %d " % (jj)
                                
                    
                    clara_bash=open("/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-"+results.clara_version+"/config/clas12_rga_"+str(r)+"_"+str(jj)+".sh","w")
                    if not os.path.exists("/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-"+results.clara_version+"/config/.clas122R00"+str(r)+"_"+input_recon_bank_format+"UT"+str(unix_timestamp)+"R00"+str(r)+"/"):
                        os.mkdir("/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-"+results.clara_version+"/config/.clas122R00"+str(r)+"_"+input_recon_bank_format+"UT"+str(unix_timestamp)+"R00"+str(r)+"/")

                    clara_file_list=open("/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-"+results.clara_version+"/config/.clas122R00"+str(r)+"_"+input_recon_bank_format+"UT"+str(unix_timestamp)+"R00"+str(r)+"/"+input_recon_bank_format+"UT"+str(unix_timestamp)+"R00"+str(r)+"_"+str(jj),"w")
                    clara_bash.write("#!/bin/bash \n")
                    clara_bash.write("export MALLOC_ARENA_MAX=2 \n")
                    clara_bash.write("export MALLOC_MMAP_THRESHOLD_=131072 \n")
                    clara_bash.write("export MALLOC_TRIM_THRESHOLD_=131072 \n")
                    clara_bash.write("export MALLOC_TOP_PAD_=131072 \n")
                    clara_bash.write("export MALLOC_MMAP_MAX_=65536 \n")            
                    clara_bash.write("export MALLOC_MMAP_MAX_=65536 \n")
                    clara_bash.write('export JAVA_OPTS="-XX:+UseNUMA -XX:+UseBiasedLocking" \n')
                    
                    clara_bash.write('export CLARA_HOME="/w/hallb-scifs17exp/clas12/rg-a/software/clara-'+results.clara_version+'" \n')
                    clara_bash.write('export CLARA_MONITOR_FE="clara1601%9000_java" \n')
                    clara_bash.write('export CLAS12DIR="/w/hallb-scifs17exp/clas12/rg-a/software/clara-'+results.clara_version+'/plugins/clas12" \n')
                    clara_bash.write('export CLARA_USER_DATA="/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-'+results.clara_version+'/" \n')
                    
                    clara_bash.write('"$CLARA_HOME/bin/kill-dpes" \n')
                    
                    clara_bash.write("sleep $[ ( $RANDOM % 20 )  + 1 ]s \n")
                    
                    clara_bash.write("/w/hallb-scifs17exp/clas12/rg-a/software/clara-"+results.clara_version+"/lib/clara/run-clara \\ \n")
                    clara_bash.write("-i /lustre/expphy/volatile/clas12/rg-a/production/decoded/"+results.prod_pass+"/"+results.prod_version+"/00"+str(r)+" \\ \n")
                    clara_bash.write("-o /work/clas12/rg-a/production/recon/"+results.prod_pass+"/"+results.prod_version+"/"+recon_out_dir+"/00"+str(r) +" \\ \n")
                    clara_bash.write("-z "+input_recon_bank_format+"_"+" \\ \n")
                    clara_bash.write("-l /scratch/clara/clas12-2 \\ \n")
                    clara_bash.write("-t 8 \\ \n")
                    clara_bash.write("-s clas122R00"+str(r)+"_"+input_recon_bank_format+"UT"+str(unix_timestamp)+"R00"+str(r)+"_"+str(jj)+" \\ \n")
                    clara_bash.write(clara_service_file + " \\ \n")
                    clara_bash.write("/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-"+results.clara_version+"/config/.clas122R00"+str(r)+"_"+input_recon_bank_format+"UT"+str(unix_timestamp)+"R00"+str(r)+"/"+input_recon_bank_format+"UT"+str(unix_timestamp)+"R00"+str(r)+"_"+str(jj)+" \n")
                    for ff in group_file_list[jj]:
                        clara_file_list.write(ff +" \n")
                    
                    clara_bash.close()
                    clara_file_list.close()

            

    else:
        print ' output directory exists. exiting reconstruction submission '
    run_counter=run_counter+1
                

print workflow.getJson()

    
    



print 'complete'
