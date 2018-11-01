#!/bin/

while getopts "j:s:" o; do
  case "${o}" in
    j)
      jobName=${OPTARG}
      ;;
    s)
      source /cvmfs/sft.cern.ch/lcg/releases/ROOT/6.08.06-c8fb4/x86_64-slc6-gcc49-opt/bin/thisroot.sh
      git clone https://github.com/simonecid/heppy -b jetMETStudies
      ;;
    esac
done

case $jobName in
############## AK4 #################
  0)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU0_PF/MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU0_PF \
      --option minimumPtToReachBarrel=3 \
      --option minimumPtToReachEndcap=1000000 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU0_PF \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfCandidates_QCD_PU0_PF

    cd jetMETStudies/PU0_PF
    tar czvf MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU0_PF.tar.gz MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU0_PF
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU0_PF.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU0_PF.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  1)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU0_PF/MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU0_PF \
      --option minimumPtToReachBarrel=1000000 \
      --option minimumPtToReachEndcap=3 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU0_PF \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfCandidates_QCD_PU0_PF

    cd jetMETStudies/PU0_PF
    tar czvf MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU0_PF.tar.gz MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU0_PF
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU0_PF.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU0_PF.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  2)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU0_PF/MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU0_PF \
      --option minimumPtToReachBarrel=3 \
      --option minimumPtToReachEndcap=1000000 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU0_PF \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfClusters_QCD_PU0_PF

    cd jetMETStudies/PU0_PF
    tar czvf MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU0_PF.tar.gz MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU0_PF
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU0_PF.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU0_PF.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  3)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU0_PF/MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU0_PF \
      --option minimumPtToReachBarrel=1000000 \
      --option minimumPtToReachEndcap=3 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU0_PF \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfClusters_QCD_PU0_PF

    cd jetMETStudies/PU0_PF
    tar czvf MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU0_PF.tar.gz MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU0_PF
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU0_PF.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU0_PF.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
############## Phase1 #################
  4)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU0_PF/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU0_PF \
      --option minimumPtToReachBarrel=3 \
      --option minimumPtToReachEndcap=1000000 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU0_PF \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_QCD_PU0_PF

    cd jetMETStudies/PU0_PF
    tar czvf MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU0_PF.tar.gz MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU0_PF
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU0_PF.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU0_PF.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  5)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU0_PF/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU0_PF \
      --option minimumPtToReachBarrel=1000000 \
      --option minimumPtToReachEndcap=3 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU0_PF \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_QCD_PU0_PF

    cd jetMETStudies/PU0_PF
    tar czvf MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU0_PF.tar.gz MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU0_PF
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU0_PF.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU0_PF.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  6)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU0_PF/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU0_PF \
      --option minimumPtToReachBarrel=3 \
      --option minimumPtToReachEndcap=1000000 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU0_PF \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfClusters_QCD_PU0_PF

    cd jetMETStudies/PU0_PF
    tar czvf MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU0_PF.tar.gz MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU0_PF
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU0_PF.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU0_PF.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  7)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU0_PF/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU0_PF \
      --option minimumPtToReachBarrel=1000000 \
      --option minimumPtToReachEndcap=3 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU0_PF \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfClusters_QCD_PU0_PF

    cd jetMETStudies/PU0_PF
    tar czvf MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU0_PF.tar.gz MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU0_PF
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU0_PF.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU0_PF.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
esac

while true
do
  sleep 1m
done

