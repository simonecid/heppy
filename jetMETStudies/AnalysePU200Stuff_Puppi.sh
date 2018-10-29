  ############## AK4 #################

python myScripts/runYAMLWorkflow.py \
  --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
  --option saveFolder=jetMETStudies/PU200_Puppi/MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU200_Puppi \
  --option minimumPtToReachBarrel=3 \
  --option minimumPtToReachEndcap=1000000 \
  --option minimumPtToReachForward=1000000 \
  --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_Puppi \
  --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfCandidates_QCD_PU200_Puppi &

python myScripts/runYAMLWorkflow.py \
  --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
  --option saveFolder=jetMETStudies/PU200_Puppi/MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU200_Puppi \
  --option minimumPtToReachBarrel=1000000 \
  --option minimumPtToReachEndcap=3 \
  --option minimumPtToReachForward=1000000 \
  --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_Puppi \
  --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfCandidates_QCD_PU200_Puppi &

  python myScripts/runYAMLWorkflow.py \
  --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
  --option saveFolder=jetMETStudies/PU200_Puppi/MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU200_Puppi \
  --option minimumPtToReachBarrel=3 \
  --option minimumPtToReachEndcap=1000000 \
  --option minimumPtToReachForward=1000000 \
  --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_Puppi \
  --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfClusters_QCD_PU200_Puppi &

python myScripts/runYAMLWorkflow.py \
  --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
  --option saveFolder=jetMETStudies/PU200_Puppi/MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU200_Puppi \
  --option minimumPtToReachBarrel=1000000 \
  --option minimumPtToReachEndcap=3 \
  --option minimumPtToReachForward=1000000 \
  --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_Puppi \
  --option componentNameConvolutionCurves=MatchAK4GenJetWithAK4JetFromPfClusters_QCD_PU200_Puppi &

  ############## Phase1 #################

python myScripts/runYAMLWorkflow.py \
  --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
  --option saveFolder=jetMETStudies/PU200_Puppi/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU200_Puppi \
  --option minimumPtToReachBarrel=3 \
  --option minimumPtToReachEndcap=1000000 \
  --option minimumPtToReachForward=1000000 \
  --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_Puppi \
  --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_QCD_PU200_Puppi &

python myScripts/runYAMLWorkflow.py \
  --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
  --option saveFolder=jetMETStudies/PU200_Puppi/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU200_Puppi \
  --option minimumPtToReachBarrel=1000000 \
  --option minimumPtToReachEndcap=3 \
  --option minimumPtToReachForward=1000000 \
  --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_Puppi \
  --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_QCD_PU200_Puppi &

  python myScripts/runYAMLWorkflow.py \
  --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
  --option saveFolder=jetMETStudies/PU200_Puppi/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU200_Puppi \
  --option minimumPtToReachBarrel=3 \
  --option minimumPtToReachEndcap=1000000 \
  --option minimumPtToReachForward=1000000 \
  --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_Puppi \
  --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfClusters_QCD_PU200_Puppi &

python myScripts/runYAMLWorkflow.py \
  --option ConfigFile=jetMETStudies/ComputeResolutions_Base.yaml \
  --option saveFolder=jetMETStudies/PU200_Puppi/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU200_Puppi \
  --option minimumPtToReachBarrel=1000000 \
  --option minimumPtToReachEndcap=3 \
  --option minimumPtToReachForward=1000000 \
  --option moduleNameConvolutionCurves=heppy.jetMETStudies.ComputePhase1AndAK4L1TJetsFromPfClustersAndCandidates_QCD_PU200_Puppi \
  --option componentNameConvolutionCurves=MatchAK4GenJetWithPhase1L1TJetFromPfClusters_QCD_PU200_Puppi &