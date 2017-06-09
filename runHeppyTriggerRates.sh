#! /bin/bash

echo "Dumping sysinfo"

lsb_release -a

python /cvmfs/fcc.cern.ch/sw/0.8.1/tools/hsf_get_platform.py --get=os 

echo "Running heppy job"

SAVE_DEST="$(pwd)"

mkdir output

source /software/sb17498/FCCSW/init.sh
cp -r /software/sb17498/heppy .
cd heppy
source init.sh

heppy ${SAVE_DEST}/output test/triggerRates_cfg.py

# Zip file
cd ${SAVE_DEST}
tar -czvf output.tar.gz output