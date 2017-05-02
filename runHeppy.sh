#! /bin/bash

SAVE_DEST="$(pwd)"

mkdir output

cd /software/sb17498/FCCSW
source /software/sb17498/FCCSW/init.sh
cd /software/sb17498/heppy
source /software/sb17498/heppy/init.sh

heppy ${SAVE_DEST}/output test/triggerRates_cfg.py

# Zip file
cd ${SAVE_DEST}
tar -czvf output.tar.gz output