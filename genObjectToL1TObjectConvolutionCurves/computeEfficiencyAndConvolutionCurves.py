#!/usr/bin/env python

from heppy.framework.heppy_loop import * 
from heppy.muonTriggerRateEstimationWorkflow.computeEfficiencies import computeEfficiencies
from ROOT import TH1F
from ROOT import TFile
import os
from array import array
import ast
from heppy.myScripts.plotDistributionComparisonPlot import plotDistributionComparisonPlot
from math import isnan

saveFolder = "_muonTriggerRate_BarrelCut5.5_EndcapCut1.5_Iteration2"
binning = "[0, 1.5, 2.3, 3, 4, 5, 5.5, 6, 7, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]"
##binning = "[0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]"
qualityThreshold = 8
detectorEta = 2.44
barrelEta = 1.1
binningArray = array("f", ast.literal_eval(binning))
barrelMuonChamberRadius = 2.95 # Taking solenoid inner edge as approximation
magneticField = 3.8 # Tesla
#Used to normalise trigger rates in output from Delphes sim
#minimumPtToReachBarrelMuonChamber = barrelMuonChamberRadius * magneticField/6.6
minimumPtToReachBarrelMuonChamber = 5.5
minimumPtToReachEndcapMuonChamber = 1.5
sampleRateEstimation = "MinBiasDistribution_13TeV_DelphesCMS_CMSJets"
numberOfDelphesEvents = 3e6
#sampleRateEstimation = "NeutrinoGun_NoTau_13TeV_DelphesCMS_JetPTMin_5_test"
sample_BinnedDistributions_highPt = "l1tMuonGenMuonMatching_SingleMu_FlatPt_8to100_QualityCut_WQualityBranch"
sample_BinnedDistributions_lowPt = "l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch"
sample_ClosureTest1 = "l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch"
sample_ClosureTest2 = "l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_GenMuons"
sample_ClosureTest3 = "cmsMatching_SingleNeutrinoPU140_LeadingL1TMuon_QualityCut8"
averagePileUp = 140
bunchCrossingFrequency = 31.6e6 # 2808 bunches

#instantaneousLuminosity = 5e34 #cm^-2 s^-1
#minBiasCrossSection = 56.79 # mb, from Pythia
interactionFrequency = averagePileUp * bunchCrossingFrequency



###################################################################################################
#################################### DO NOT TOUCH FROM DOWN ON ####################################
###################################################################################################

#os.system("mkdir -p " + saveFolder)
#if os.listdir(saveFolder):
#  print "Save directory is not empty. It will be cleaned. Continue?"
#  if raw_input() == "y":
#    os.system("rm -r " + saveFolder + "/*")
#  else:
#    print "Stopping process."
#    exit()
#
## Common options
#
#print "--- COMPUTING CONVOLUTION CURVES ---"
#
#
#print "PROCESSING FROM HIGH MOMENTUM MUONS"
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "muonTriggerRateEstimationWorkflow/binnedDistributionsCMS_L1TMuon_cfg.py"]
#options.extraOptions.append("sample=" + sample_BinnedDistributions_highPt)
#options.extraOptions.append("binning=" + binning)
#options.extraOptions.append("quality=" + str(qualityThreshold))
#options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrelMuonChamber))
#options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcapMuonChamber))
#options.extraOptions.append("barrelEta=" + str(barrelEta))
##options.nevents=100
#loop = main(options, folderAndScriptName, parser)
#os.system("mv " + saveFolder + "/" + sample_BinnedDistributions_highPt + " " + saveFolder + "/highPt_ConvolutionCurves")
#
#print "PROCESSING FROM LOW MOMENTUM MUONS"
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "muonTriggerRateEstimationWorkflow/binnedDistributionsCMS_L1TMuon_cfg.py"]
#options.extraOptions.append("sample=" + sample_BinnedDistributions_lowPt)
#options.extraOptions.append("binning=" + binning)
#options.extraOptions.append("quality=" + str(qualityThreshold))
#options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrelMuonChamber))
#options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcapMuonChamber))
#options.extraOptions.append("barrelEta=" + str(barrelEta))
##options.nevents=100
#loop = main(options, folderAndScriptName, parser)
#os.system("mv " + saveFolder + "/" + sample_BinnedDistributions_lowPt + " " + saveFolder + "/lowPt_ConvolutionCurves")
#
#print "MERGING RESULTS"
#os.system("hadd " + saveFolder + "/binnedDistributions.root " + saveFolder + "/highPt_ConvolutionCurves/histograms.root " + saveFolder + "/lowPt_ConvolutionCurves/histograms.root")
#print "--- COMPUTING THE CONVERSION FACTORS/EFFICIENCIES ---"
#
#highPtFolder = "/hdfs/FCC-hh/l1tMuonGenMuonMatching_SingleMu_FlatPt_8to100_QualityCut_WQualityBranch"
#highPtMatchTree = "MatchL1TMuonWithGenLevelMuons/matchedL1TMuonGenParticleTree"
#highPtGenTree = "MatchL1TMuonWithGenLevelMuons/genParticleTree"
#
#lowPtFolder = "/hdfs/FCC-hh/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch"
#lowPtMatchTree = "MatchL1TMuonWithGenLevelMuons/matchedL1TMuonGenParticleTree"
#lowPtGenTree = "MatchL1TMuonWithGenLevelMuons/genParticleTree"
#
#
#print "PROCESSING FROM LOW MOMENTUM MUONS"
#numberOfMatchedObjects_lowPt, numberOfGenObjects_lowPt = computeEfficiencies(
#                                                           GenObjTree = lowPtGenTree,
#                                                           GenObjFileFolder = lowPtFolder,
#                                                           MatchTree = lowPtMatchTree,
#                                                           MatchFileFolder = lowPtFolder,
#                                                           binning = binning,
#                                                           eta = detectorEta,
#                                                           quality = qualityThreshold,
#                                                           barrelEta = barrelEta,
#                                                           minPtInBarrel = minimumPtToReachBarrelMuonChamber,
#                                                           minPtInEndcap = minimumPtToReachEndcapMuonChamber,
#                                                         )
#
#print "PROCESSING FROM HIGH MOMENTUM MUONS"
#numberOfMatchedObjects_highPt, numberOfGenObjects_highPt = computeEfficiencies(
#                                                           GenObjTree = highPtGenTree,
#                                                           GenObjFileFolder = highPtFolder,
#                                                           MatchTree = highPtMatchTree,
#                                                           MatchFileFolder = highPtFolder,
#                                                           binning = binning,
#                                                           eta = detectorEta,
#                                                           quality = qualityThreshold,
#                                                           barrelEta = barrelEta,
#                                                           minPtInBarrel = minimumPtToReachBarrelMuonChamber,
#                                                           minPtInEndcap = minimumPtToReachEndcapMuonChamber,
#                                                         )
#
#
#print "MERGING RESULTS"
#
#numberOfMatchedObjects = numberOfMatchedObjects_lowPt + numberOfMatchedObjects_highPt 
#numberOfGenObjects = numberOfGenObjects_lowPt + numberOfGenObjects_highPt 
#
#efficiencyFactors = numberOfMatchedObjects/numberOfGenObjects
#for binIdx in xrange(0, len(efficiencyFactors)): 
#  efficiencyFactors[binIdx] = 0 if isnan(efficiencyFactors[binIdx]) else efficiencyFactors[binIdx]
#  if efficiencyFactors[binIdx] > 1:
#    efficiencyFactors[binIdx] = 1
#print efficiencyFactors
#
#efficiencyFactorsFile = TFile("" + saveFolder + "/efficiencyFactors.root", "RECREATE")
#efficiencyFactorsFile.cd()
#efficiencyHistogram = TH1F("efficiencyHistogram", "Muon trigger efficiency", len(binningArray)-1, binningArray)
#
#for x in xrange(0, len(efficiencyFactors)): 
#  #Excluding overflow bin
#  if x != len(efficiencyFactors) - 1:
#    efficiencyHistogram.SetBinContent(x + 1, efficiencyFactors[x])
#  
#efficiencyHistogram.Write()
#
#efficiencyFactorsFile.Close()
#
#print "--- APPLYING CONVOLUTION TO EVENT SAMPLE TO COMPUTE RATES ---"
#
#print "CREATING THE NON-NORMALISED PLOTS"
#
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "muonTriggerRateEstimationWorkflow/muonTriggerRateMinBias_cfg.py"]
#convolutionFileName = "" + saveFolder + "/binnedDistributions.root"
#options.extraOptions.append("sample=" + sampleRateEstimation)
#options.extraOptions.append("convolutionFileName=" + convolutionFileName)
#options.extraOptions.append("binning=" + binning)
#options.extraOptions.append("probabilityFile=" + "" + saveFolder + "/efficiencyFactors.root")
#options.extraOptions.append("probabilityHistogram=" + "efficiencyHistogram")
#options.extraOptions.append("detectorEta=" + str(detectorEta))
#options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrelMuonChamber))
#options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcapMuonChamber))
#options.extraOptions.append("barrelEta=" + str(barrelEta))
##options.nevents=100
#loop = main(options, folderAndScriptName, parser)
##os.system("hadd -f " + saveFolder + "/" + sampleRateEstimation + "_RatePlots_NotNormalised.root " + saveFolder + "/" + sampleRateEstimation + "_Chunk*/ratePlots.root")
#os.system("mv " + saveFolder + "/" + sampleRateEstimation + "/ratePlots.root " + saveFolder + "/" + sampleRateEstimation + "_RatePlots_NotNormalised.root")
#
#print "OBTAINING THE RATE IN THE LINEAR SCALING APPROXIMATION"
#
#nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + sampleRateEstimation + "_RatePlots_NotNormalised.root")
#totalRateHist = nonNormalisedRatePlotFile.Get("simL1TMuonTriggerRate")
#barrelRateHist = nonNormalisedRatePlotFile.Get("barrelMuonRate")
#endcapRateHist = nonNormalisedRatePlotFile.Get("endcapMuonRate")
#
#totalRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
#barrelRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
#endcapRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
#
#totalRateHist.GetXaxis().SetTitle("p_{t}")
#totalRateHist.GetXaxis().SetRangeUser(5, 50)
#totalRateHist.GetYaxis().SetTitle("Rate [Hz]")
#barrelRateHist.GetXaxis().SetTitle("p_{t}")
#barrelRateHist.GetXaxis().SetRangeUser(5, 50)
#barrelRateHist.GetYaxis().SetTitle("Rate [Hz]")
#endcapRateHist.GetXaxis().SetTitle("p_{t}")
#endcapRateHist.GetXaxis().SetRangeUser(5, 50)
#endcapRateHist.GetYaxis().SetTitle("Rate [Hz]")
#
#normalisedRatePlotFile = TFile("" + saveFolder + "/" + sampleRateEstimation + "_RatePlots_Normalised.root", "RECREATE")
#normalisedRatePlotFile.cd()
#totalRateHist.Write()
#barrelRateHist.Write()
#endcapRateHist.Write()
#normalisedRatePlotFile.Close()
#nonNormalisedRatePlotFile.Close()

print "NORMALISING THE RATE PLOT TO OBTAIN THE TRIGGER PASS PROBABILITY FOR MINBIAS AND PU140 EVENTS"

nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + sampleRateEstimation + "_RatePlots_NotNormalised.root")
passProbabilityFile = TFile("" + saveFolder + "/" + sampleRateEstimation + "_RatePlots_TriggerPassProbability.root", "RECREATE")
totalRateHist = nonNormalisedRatePlotFile.Get("simL1TMuonTriggerRate")
ppPassProbabilityHistogram = totalRateHist.Clone("ppPassProbabilityHistogram")
ppPassProbabilityHistogram.Scale(1/numberOfDelphesEvents)
passProbabilityFile.cd()
eventPassProbabilityHistogram = ppPassProbabilityHistogram.Clone("eventPassProbabilityHistogram")

for x in xrange(1, eventPassProbabilityHistogram.GetNbinsX()+1):
  ppPassProbability = ppPassProbabilityHistogram.GetBinContent(x)
  eventPassProbability = 1 - (1 - ppPassProbability)**averagePileUp
  eventPassProbabilityHistogram.SetBinContent(x, eventPassProbability)

probabilityRatioHistogram = eventPassProbabilityHistogram.Clone("probabilityRatioHistogram")
probabilityRatioHistogram.Divide(ppPassProbabilityHistogram)

probabilityRatioHistogram.Write()
ppPassProbabilityHistogram.Write()
eventPassProbabilityHistogram.Write()

nonNormalisedRatePlotFile.Close()
passProbabilityFile.Close()

print "COMPUTING THE TRIGGER PASS PROBABIITY IN LINEAR SCALING APPROXIMATION AND WITH FULL FORMULA"

passProbabilityFile = TFile("" + saveFolder + "/" + sampleRateEstimation + "_RatePlots_TriggerPassProbability.root")
ppPassProbabilityHistogram = passProbabilityFile.Get("ppPassProbabilityHistogram")
eventPassProbabilityHistogram = passProbabilityFile.Get("eventPassProbabilityHistogram")

linearPURatePlot = ppPassProbabilityHistogram.Clone("linearPURatePlot")
fullPURatePlot = ppPassProbabilityHistogram.Clone("fullPURatePlot")

linearPURatePlot.Scale(interactionFrequency)
fullPURatePlot.Scale(bunchCrossingFrequency)

pileupRatePlotFile = TFile("" + saveFolder + "/" + sampleRateEstimation + "_RatePlots_PU" + str(averagePileUp) + "RatePlot.root", "RECREATE")
pileupRatePlotFile.cd()
linearPURatePlot.Write()
fullPURatePlot.Write()

pileupRatePlotFile.Close()

#print "--- RUNNING THE CLOSURE TESTS ---"
#
#print "CREATING THE MOMENTUM DISTRIBUTION PLOTS FOR CMS GEN MUON TO SIML1TMUON (QUALITY CUT ON MATCHED GEN MU)"
##Taking the matched gen muons
##Applying the quality selection on the corresponding l1tmu to get only the gen mu matched to a quality l1tmu
##Applying the smearing without any probabilistic exclusion to see if resolution curve are accurate enough
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "muonTriggerRateEstimationWorkflow/plotTransverseMomentumDistributionForMuonClosureTest_FromMatchedPairs_cfg.py"]
#convolutionFileName = "" + saveFolder + "/binnedDistributions.root"
#options.extraOptions.append("sample=" + sample_ClosureTest1)
#options.extraOptions.append("convolutionFileName=" + convolutionFileName)
#options.extraOptions.append("binning=" + binning)
#options.extraOptions.append("quality=" + str(qualityThreshold))
#options.extraOptions.append("detectorEta=" + str(detectorEta))
#options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrelMuonChamber))
#options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcapMuonChamber))
#options.extraOptions.append("barrelEta=" + str(barrelEta))
##options.nevents=100
#loop = main(options, folderAndScriptName, parser)
#os.system("mv " + saveFolder + "/" + sample_ClosureTest1 + " " + saveFolder + "/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_ClosureTestPlots_QualityCutOnGenMuon")
#
#print "CREATING THE MOMENTUM DISTRIBUTION PLOTS FOR CMS GEN MUON TO SIML1TMUON (EVERY GEN MU IS CONSIDERED)"
#
##We take every gen mu.
##We check if they fall into the detector
##If they do, we apply the probabilistic selection and the smearing
#
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "muonTriggerRateEstimationWorkflow/plotTransverseMomentumDistributionForMuonClosureTest_FromMatchedPairs_cfg.py"]
#convolutionFileName = "" + saveFolder + "/binnedDistributions.root"
#options.extraOptions.append("sample=" + sample_ClosureTest2)
#options.extraOptions.append("convolutionFileName=" + convolutionFileName)
#options.extraOptions.append("binning=" + binning)
#options.extraOptions.append("detectorEta=" + str(detectorEta))
#options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrelMuonChamber))
#options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcapMuonChamber))
#options.extraOptions.append("barrelEta=" + str(barrelEta))
#options.extraOptions.append("probabilityFile=" + "" + saveFolder + "/efficiencyFactors.root")
#options.extraOptions.append("probabilityHistogram=" + "efficiencyHistogram")
#options.extraOptions.append("quality=" + str(qualityThreshold))
##options.nevents=100
#loop = main(options, folderAndScriptName, parser)
#os.system("mv " + saveFolder + "/" + sample_ClosureTest2 + " " + saveFolder + "/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_ClosureTestPlots_AllGenMuons")
#
#print "CREATING THE COMPARISON PLOTS"
#
#cfg = lambda x: 1
#cfg.plots = [
##  #Files here
#  ["" + saveFolder + "/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_ClosureTestPlots_QualityCutOnGenMuon/histograms.root", "coarseBinnedPtl1tMuonDistribution", "CMS L1TMuon"],
#  ["" + saveFolder + "/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_ClosureTestPlots_QualityCutOnGenMuon/histograms.root", "coarseBinnedSmearedPtgenParticleDistribution", "Sim L1TMuon from matched gen #mu"]
##  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtSimL1TMuonDistribution", "SimL1TMuon"],
##  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtL1TMuonDistribution", "Original L1TMuon"],
#]
#cfg.saveFileName = "" + saveFolder + "/closureTest1.root"
#
#plotDistributionComparisonPlot(cfg)
#
#cfg = lambda x: 1
#cfg.plots = [
##  #Files here
#  ["" + saveFolder + "/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_ClosureTestPlots_QualityCutOnGenMuon/histograms.root", "coarseBinnedPtl1tMuonDistribution", "CMS L1TMuon"],
#  ["" + saveFolder + "/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_ClosureTestPlots_AllGenMuons/histograms.root", "coarseBinnedSmearedPtgenParticleDistribution", "Sim L1TMuon from every gen #mu"]
##  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtSimL1TMuonDistribution", "SimL1TMuon"],
##  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtL1TMuonDistribution", "Original L1TMuon"],
#]
#cfg.saveFileName = "" + saveFolder + "/closureTest2.root"
#
#plotDistributionComparisonPlot(cfg)
#
#
#print "CREATING THE ORIGINAL CMS RATE PLOT"
#
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "muonTriggerRateEstimationWorkflow/computeTriggerRatesCMSMuons_cfg.py"]
#options.extraOptions.append("sample=" + sample_ClosureTest3)
##options.nevents=100
#loop = main(options, folderAndScriptName, parser)
#os.system("mv " + saveFolder + "/" + sample_ClosureTest3 + " " + saveFolder + "/" + sample_ClosureTest3 + "_CMSTriggerRate")
#
#cmsRatePlotFile = TFile("" + saveFolder + "/" + sample_ClosureTest3 + "_CMSTriggerRate/ratePlots.root", "UPDATE")
#totalRateHist = cmsRatePlotFile.Get("triggerRate")
#barrelRateHist = cmsRatePlotFile.Get("barrelTriggerRate")
#endcapRateHist = cmsRatePlotFile.Get("endcapTriggerRate")
#totalRateHist.GetXaxis().SetTitle("p_{t}")
#totalRateHist.GetXaxis().SetRangeUser(5, 50)
#totalRateHist.GetYaxis().SetTitle("Rate [Hz]")
#barrelRateHist.GetXaxis().SetTitle("p_{t}")
#barrelRateHist.GetXaxis().SetRangeUser(5, 50)
#barrelRateHist.GetYaxis().SetTitle("Rate [Hz]")
#endcapRateHist.GetXaxis().SetTitle("p_{t}")
#endcapRateHist.GetXaxis().SetRangeUser(5, 50)
#endcapRateHist.GetYaxis().SetTitle("Rate [Hz]")
#totalRateHist.Write()
#barrelRateHist.Write()
#endcapRateHist.Write()
#cmsRatePlotFile.Close()
#
#print "CREATING RATIO PLOT FOR CMS VS DELPHES RATE"
#
#cfg = lambda x: 1
#cfg.plots = [
##  #Files here
#  ["" + saveFolder + "/" + sample_ClosureTest3 + "_CMSTriggerRate/ratePlots.root", "triggerRate", "CMS L1TMuon"],
#  ["" + saveFolder + "/" + sampleRateEstimation + "_RatePlots_Normalised.root", "simL1TMuonTriggerRate", "Sim L1TMuon"]
#]
#cfg.saveFileName = "" + saveFolder + "/rateClosureTestMinBias.root"
#plotDistributionComparisonPlot(cfg)