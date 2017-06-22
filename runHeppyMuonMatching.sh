#! /bin/bash

echo "Dumping sysinfo"

lsb_release -a

python /cvmfs/fcc.cern.ch/sw/0.8.1/tools/hsf_get_platform.py --get=os 

echo "Running heppy job"

HOME_FOLDER="$(pwd)"
SAVE_DESTINATION = "muonMatching"

mkdir ${SAVE_DESTINATION}

source /software/sb17498/FCCSW/init.sh
cp -r /software/sb17498/heppy .
cd heppy
source init.sh

heppy ${HOME_FOLDER}/${SAVE_DESTINATION} test/matchJetMuons_cfg.py

# Zip file
cd ${HOME_FOLDER}
tar -czvf muonMatching_output.tar.gz ${SAVE_DESTINATION}
