#! /bin/bash

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