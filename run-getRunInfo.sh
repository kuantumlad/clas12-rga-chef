#!/bin/bash

run=$1

run_config_logbook="/w/hallb-scifs17exp/clas12/rg-a/software/clas12_monitoring/plots${run}/r${run}Config.txt"
echo $run '100 files'
more /farm_out/clas12-2/rec-clas12-2-monitor*R00${run}*_000*.out | grep 'Clara Framework  :    ' >> $run_config_logbook
more /farm_out/clas12-2/rec-clas12-2-monitor*R00${run}*_000*.out | grep 'CLAS12 plugin    :' >> $run_config_logbook 
more /farm_out/clas12-2/rec-clas12-2-monitor*R00${run}*_000*.out | grep '{"geomDBVariation":"thayward_test_00[0-9][0-9]","wireDistortionsFlag"' >> $run_config_logbook
