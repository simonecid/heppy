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
#    s)
#      sampleName=${OPTARG}
#      ;;
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

OUTPUT_FOLDER="${jobName}_allSamples_${clusterId}.${processId}"

mkdir ${OUTPUT_FOLDER}

source /software/sb17498/FCCSW/init.sh
cp -r /software/sb17498/heppy .
cd heppy
source init.sh

samples=(MinBiasDistribution_100TeV_DelphesFCC_CMSJets HardQCD_100TeV_PtBinned_10_30_GeV HardQCD_100TeV_PtBinned_30_300_GeV HardQCD_100TeV_PtBinned_300_500_GeV HardQCD_100TeV_PtBinned_500_700_GeV HardQCD_100TeV_PtBinned_700_900_GeV HardQCD_100TeV_PtBinned_900_1000_GeV HardQCD_100TeV_PtBinned_900_1400_GeV HardQCD_100TeV_PtBinned_1400_2000_GeV)

for sampleName in ${samples[*]}; do
  heppy ${HOME_FOLDER}/${OUTPUT_FOLDER} ${inputFile} -f --option=sample=${sampleName} -j ${numThreads} 
  #echo ${sampleName}
done

# Zip file
cd ${HOME_FOLDER}
tar -czvf ${jobName}_allSamples_${clusterId}.${processId}.tar.gz ${OUTPUT_FOLDER}

set +o xtrace