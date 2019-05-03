#!/bin/bash

#/site/ace/certified/apps/bin/logentry -l TLOG -t "test plots" -c "electron overview" -a /work/clas12/rg-a/software/clas12_monitoring/plots6619/e_rec_mon.png

run=$1
runPeriod=$2
monDir=/work/clas12/rg-a/software/clas12_monitoring/plots${run}

/site/ace/certified/apps/bin/logentry -l TLOG -t "Offline Analysis 100 files: $* set i" \
                                      -g "$rga_{runPeriod}_${run}" \
                                      -b "${monDir}/r${run}Config.txt" \
                                      -c "electron overview" -a ${monDir}/e_rec_mon.png \
				      -c "physics kinematical coverage" -a ${monDir}/e_phys.png \
				      -c "electron trigger per sector" -a ${monDir}/trig_sect.png \
				      -c "electron per sector" -a ${monDir}/e_sects.png \
				      -c "electron phi distributions in theta bins per sector" -a ${monDir}/e_phi_sects.png \
				      -c "electron per sector projections" -a ${monDir}/e_sects_proj.png \
				      -c "electron detector positions" -a ${monDir}/e_pos_sects.png \
				      -c "electron detector acceptance" -a ${monDir}/e_ratio_sects.png \
				      -c "photon pairs in ECAL" -a ${monDir}/gg.png \
				      -c "DC tracks overview" -a ${monDir}/dc_rec_mon.png \
				      -c "DC positive tracks" -a ${monDir}/dc_p_vz_phi.png \
				      -c "DC negative tracks" -a ${monDir}/dc_m_vz_phi.png \
				      -c "DC residuals vs DOCA" -a ${monDir}/DC_resd_trkDoca.png \
				      -c "DC residuals" -a ${monDir}/DC_resd.png \
				      -c "DC Time" -a ${monDir}/DC_time.png \

/site/ace/certified/apps/bin/logentry -l TLOG -t "Offline Analysis 100 files: $* set ii" \
                                      -g "$rga_{runPeriod}_${run}" \
                                      -b "${monDir}/r${run}Config.txt" \
				      -c "TOF vertex times per charge per sector" -a ${monDir}/TOF.png \
				      -c "TOF calibration" -a ${monDir}/TOF_cal.png \
				      -c "DST FTOF 1A Mass Distributions" -a ${monDir}/dst_FTOF1A_mass.png \
				      -c "DST FTOF 1B Mass distributions" -a ${monDir}/dst_FTOF1B_mass.png \
				      -c "HTCC electron selection" -a ${monDir}/HTCC_e.png \
				      -c "HTCC electron nphe" -a ${monDir}/HTCC_nphe.png \
				      -c "HTCC electron ADC spectra" -a ${monDir}/HTCC_adc.png \
				      -c "overview of CVT tracks" -a ${monDir}/cvt.png \
				      -c "Forward Tagger" -a ${monDir}/FT.png \
				      -c "CTOF timing with SVT matching" -a ${monDir}/central.png \
				      -c "CND timing with SVT matching" -a ${monDir}/cnd.png \
				      -c "BST occupancies" -a ${monDir}/bst_occ.png \
				      -c "BMT occupancies" -a ${monDir}/bmt_occ.png \
				      -c "Barrel crosses" -a ${monDir}/barrel_crosses.png \
				      -c "e pip coincidence" -a ${monDir}/e_pip.png \
				      -c "e pip pim coincidence" -a ${monDir}/two_pions.png \
