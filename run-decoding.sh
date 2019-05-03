#!/bin/bash

#./scripts/gen-decoding.py --workflow v0 --runGroup rga --inputs /mss/clas12/rg-a/data/ --runFile ../runList.txt --coatjava /work/clas12/rg-a/software/clara-5bp7p8/plugins/clas12/ --outDir /volatile/clas12/rg-a/production/decoded/coatV5bp7p8/ --fileReg '.*clas[_A-Za-z]*_(\d+)\.evio\.(0004\d+)' --model 2 --multiRun

job_number=`swif list | grep '[0-9][0-9][0-9][0-9][0-9]' | sort -rn | head -n 1`
echo $job_number

echo `swif list | grep -A 1 '${job_number}' | grep -v "${job_number}" | grep -e "rga-"`


#swif import -slurm -file clas12-workflow/jobs/

