#! /bin/bash

set -o xtrace

while getopts "j:c:p:s:i:t:" o; do
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
    i)
      inputFile=${OPTARG}
      ;;
    t)
      numThreads=${OPTARG}
      ;;
    esac
done

echo "Dumping sysinfo"

echo "> lsb_release -a"
lsb_release -a

echo "> Platform name"
python /cvmfs/fcc.cern.ch/sw/0.8.1/tools/hsf_get_platform.py --get=os 

echo "I am running on" $HOSTNAME

echo "Running heppy job"

HOME_FOLDER="$(pwd)"
SAVE_DESTINATION="${jobName}_${sampleName}"

mkdir ${SAVE_DESTINATION}

source /software/sb17498/FCCSW/init.sh
cp -r /software/sb17498/heppy .
cd heppy
source init.sh

heppy ${HOME_FOLDER}/${SAVE_DESTINATION} ${inputFile} --option=sample=${sampleName} -j ${numThreads}

# Zip file
cd ${HOME_FOLDER}
tar -czvf ${jobName}_${sampleName}_${clusterId}.${processId}.tar.gz ${SAVE_DESTINATION}