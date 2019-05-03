#!/usr/bin/bash

inDir='/w/hallb-scifs17exp/clas12/rg-a/data/decoded/'
run_list=/w/hallb-scifs17exp/clas12/rg-a/software/$1

echo $run_list

filename=$run_list
while read -r line; do
    name="$line"
    echo " creating directory for run - $name "
    echo " mkdir  ${inDir}r00${name}/ "
    mkdir  ${inDir}r00${name}/
    echo " moving files for ${name} into ${inDir}r00${name}/ "
    echo " mv ${inDir}clas_00${name}.*.hipo  ${inDir}r00${name}/ "
    mv ${inDir}clas_00${name}.*.hipo  ${inDir}r00${name}/
done < "$filename"

