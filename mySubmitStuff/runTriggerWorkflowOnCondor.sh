#! /bin/bash

set -o xtrace

while getopts "j:c:p:i:" o; do
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
    i)
      inputFile=${OPTARG}
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


set +o xtrace
source /software/sb17498/FCCSW/init.sh
set -o xtrace

cd ${HOME_FOLDER}
git clone https://www.github.com/simonecid/heppy
cd heppy
set +o xtrace
source init.sh
set -o xtrace

if [ -z ${processId} ]
then 
  # if no process id then run in non-batch mode
  SAVE_DESTINATION="${jobName}_${clusterId}"
  mkdir ${SAVE_DESTINATION}
  python myScripts/runYAMLWorkflow.py --option ConfigFile=${inputFile} --option saveFolder=${SAVE_DESTINATION}
else
  # else go in batch mode.
  SAVE_DESTINATION="${jobName}_${clusterId}_${processId}"
  mkdir ${SAVE_DESTINATION}
  python myScripts/runYAMLWorkflow.py --option ConfigFile=${inputFile} --option job=${processId} --option saveFolder=${SAVE_DESTINATION}
fi

# Zip file
tar -czvf ${SAVE_DESTINATION}.tar.gz ${SAVE_DESTINATION}
mv ${SAVE_DESTINATION}.tar.gz ${HOME_FOLDER}
cd ${HOME_FOLDER}

set +o xtrace
