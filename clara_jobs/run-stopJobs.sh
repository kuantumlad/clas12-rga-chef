#!/bin/bash



setenv PATH /site/scicomp/auger-slurm/bin:$PATH

jobId=$1

while [ ${jobId} -le $2 ]
do
    echo ' killing job ' $jobId
    jkill ${jobId}
    jobId=$(($jobId + 1))
done
