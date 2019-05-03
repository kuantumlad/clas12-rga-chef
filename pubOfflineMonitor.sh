#!/bin/bash

#/site/ace/certified/apps/bin/logentry -l TLOG -t "test plots" -c "electron overview" -a /work/clas12/rg-a/software/clas12_monitoring/plots6619/e_rec_mon.png

run=$1
runPeriod=$2
monDir=/work/clas12/rg-a/software/clas12_monitoring/plots${run}

/site/ace/certified/apps/bin/logentry -l TLOG -t "Offline Analysis 100 files: $* set i" \
                                      -g "$rga_{runPeriod}_${run}" \
                                      -b "${monDir}/r${run}Config.txt" \
                                      -c "electron overview" -a plots/e_rec_mon.png \
                                      -c "electron trigger per sector" -a plots/trig_sect.png \
                                      -c "RF Histograms" -a plots/RF.png \
                                      -c "electron per sector" -a plots/e_sects.png \
                                      -c "electron detector acceptance" -a plots/e_ratio_sects.png \
                                      -c "photon pairs in ECAL" -a plots/gg.png \
                                      -c "DC tracks overview" -a plots/dc_rec_mon.png \
                                      -c "TOF calibration" -a plots/TOF_cal.png \
                                      -c "DST FTOF 1A Mass Distributions" -a plots/dst_FTOF1A_mass.png \
                                      -c "DST FTOF 1B Mass distributions" -a plots/dst_FTOF1B_mass.png \
                                      -c "BST occupancies" -a plots/bst_occ.png \
                                      -c "BMT occupancies" -a plots/bmt_occ.png \
                                      -c "overview of CVT tracks" -a plots/cvt.png \
                                      -c "Forward Tagger" -a plots/FT.png \
                                      -c "CTOF timing with SVT matching" -a plots/central.png \
                                      -c "CND timing with SVT matching" -a plots/cnd.png \
                                      -c "BAND Overview" -a plots/BAND.png\

