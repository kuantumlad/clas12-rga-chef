#!/bin/bash

list="/w/hallb-scifs17exp/clas12/rg-a/software/clara_data/coatjava-5bp7p8/config/files_clas12-2_special.txt"

special_dir="/work/clas12/rg-a/data/decoded/special/"

while read F  ;
do
    run=$F
    echo $run
    A="$(echo ${run} | cut -d'.' -f1 | cut -d'_' -f2)"
    echo $A
    echo " moving /work/clas12/rg-a/data/decoded/r00${A}/$F to $special_dir " 
    mv /work/clas12/rg-a/data/decoded/r${A}/$F $special_dir
    
done <${list}
