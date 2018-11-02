#! /bin/sh
while getopts "j:sc:p:" o; do
  case "${o}" in
    j)
      jobName=${OPTARG}
      ;;
    s)
      source /software/sb17498/FCCSW/init.sh
      git clone https://github.com/simonecid/heppy -b jetMETStudies
      cd heppy
      source ./init.sh
      ;;
    c) 
      clusterId=_${OPTARG}
      ;;
    p)
      processId=.${OPTARG}
    esac
done

case $jobName in
############## AK4 #################
  0)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU200_PF_PUSubtraction \
      --option minimumPtToReachBarrel=3 \
      --option minimumPtToReachEndcap=1000000 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_PF_PUSubtraction \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfCandidates_QCD_PU200_PF_PUSubtraction 
    
    cd jetMETStudies/PU200_PF_PUSubtraction
    tar czvf MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU200_PF_PUSubtraction
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  1)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU200_PF_PUSubtraction \
      --option minimumPtToReachBarrel=1000000 \
      --option minimumPtToReachEndcap=3 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_PF_PUSubtraction \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfCandidates_QCD_PU200_PF_PUSubtraction 
    
    cd jetMETStudies/PU200_PF_PUSubtraction
    tar czvf MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU200_PF_PUSubtraction
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  2)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU200_PF_PUSubtraction \
      --option minimumPtToReachBarrel=3 \
      --option minimumPtToReachEndcap=1000000 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_PF_PUSubtraction \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfClusters_QCD_PU200_PF_PUSubtraction 
    
    cd jetMETStudies/PU200_PF_PUSubtraction
    tar czvf MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU200_PF_PUSubtraction
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  3)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU200_PF_PUSubtraction \
      --option minimumPtToReachBarrel=1000000 \
      --option minimumPtToReachEndcap=3 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_PF_PUSubtraction \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfClusters_QCD_PU200_PF_PUSubtraction 
    
    cd jetMETStudies/PU200_PF_PUSubtraction
    tar czvf MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU200_PF_PUSubtraction
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
############## Phase1 #################
  4)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU200_PF_PUSubtraction \
      --option minimumPtToReachBarrel=3 \
      --option minimumPtToReachEndcap=1000000 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_PF_PUSubtraction \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_QCD_PU200_PF_PUSubtraction 
    
    cd jetMETStudies/PU200_PF_PUSubtraction
    tar czvf MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU200_PF_PUSubtraction
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  5)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU200_PF_PUSubtraction \
      --option minimumPtToReachBarrel=1000000 \
      --option minimumPtToReachEndcap=3 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_PF_PUSubtraction \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_QCD_PU200_PF_PUSubtraction 
    
    cd jetMETStudies/PU200_PF_PUSubtraction
    tar czvf MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU200_PF_PUSubtraction
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  6)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU200_PF_PUSubtraction \
      --option minimumPtToReachBarrel=3 \
      --option minimumPtToReachEndcap=1000000 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_PF_PUSubtraction \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfClusters_QCD_PU200_PF_PUSubtraction 
    
    cd jetMETStudies/PU200_PF_PUSubtraction
    tar czvf MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU200_PF_PUSubtraction
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
  7)
    python myScripts/runYAMLWorkflow.py \
      --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
      --option saveFolder=jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU200_PF_PUSubtraction \
      --option minimumPtToReachBarrel=1000000 \
      --option minimumPtToReachEndcap=3 \
      --option minimumPtToReachForward=1000000 \
      --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_PF_PUSubtraction \
      --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfClusters_QCD_PU200_PF_PUSubtraction 
    
    cd jetMETStudies/PU200_PF_PUSubtraction
    tar czvf MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU200_PF_PUSubtraction
    /usr/bin/hdfs dfs -rm /user/sb17498/CMS_Phase_2/jetMETStudies/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz
    /usr/bin/hdfs dfs -moveFromLocal MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU200_PF_PUSubtraction${clusterId}${processId}.tar.gz /user/sb17498/CMS_Phase_2/jetMETStudies/      
    ;;
esac

while true
do
  sleep 1m
done