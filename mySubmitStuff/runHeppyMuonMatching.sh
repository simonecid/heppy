#! /bin/bash

while getopts "j:c:p:s;" o; do
  case "${o}" in
    j)
      jobName=${OPTARG}
      ;;
    c)
      clusterId=${OPTARG}
      ;;
    p)
      processId=${OPTARG}
      ;;
    s)
      sampleName=${OPTARG}
      ;;
    esac
done

echo "Dumping sysinfo"

lsb_release -a

python /cvmfs/fcc.cern.ch/sw/0.8.1/tools/hsf_get_platform.py --get=os 

echo "Running heppy job"

HOME_FOLDER="$(pwd)"
SAVE_DESTINATION="muonMatching_${sampleName}"


mkdir ${SAVE_DESTINATION}

source /software/sb17498/FCCSW/init.sh
cp -r /software/sb17498/heppy .
cd heppy
source init.sh

heppy ${HOME_FOLDER}/${SAVE_DESTINATION} test/matchJetMuons_cfg.py --option=sample=${sampleName}

# Zip file
cd ${HOME_FOLDER}
tar -czvf muonMatching_${sampleName}_${jobName}_${clusterId}.${processId}.tar.gz ${SAVE_DESTINATION}
