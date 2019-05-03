#!/bin/tcsh

# CLARA submission script to SLURM
# By: Brandon Clary
# 4/3/2019
# Inputs: RunList which governs the entire chain from decoding to reconstruction
# Settings: Be sure clara version and coatjava versions are  the desired ones.


set CLARA_VERSION=clara-5bp7p8
set COATJAVA=coatjava-5bp7p8



setenv CLARA_HOME /w/hallb-scifs17exp/clas12/rg-a/software/${CLARA_VERSION}
setenv CLARA_USER_DATA /w/hallb-scifs17exp/clas12/rg-a/software/clara_data/${COATJAVA}/

# set slurm path to submit jobs to slurm nodes
setenv PATH /site/scicomp/auger-slurm/bin:$PATH

#set v=`cat /w/hallb-scifs17exp/clas12/rg-a/software/runList${TYPE}.txt`
set RUN_LIST=$1
set JOB_TYPE=$2

echo "CREATING JOBS FOR RUNS FROM ${RUN_LIST}"
set v=`cat /w/hallb-scifs17exp/clas12/rg-a/software/${RUN_LIST}` #runList100.txt`
set i=1


while ( $i < = $#v )
    echo "Submitting jobs for run " $v[$i]
    echo " CLARA source script: " ${JOB_TYPE}_r00${v[$i]}_ConfigSlurm.txt
    $CLARA_HOME/bin/clara-shell ${JOB_TYPE}_r00${v[$i]}_ConfigSlurm.txt
    @ i = $i + 1
end



