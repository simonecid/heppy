#!/usr/bin/env python

from heppy.framework.heppy_loop import * 
from heppy.genObjectToL1TObjectConvolutionCurves.computeEfficiencies import computeEfficiencies
from ROOT import TH1F
from ROOT import TFile
import os
from array import array
import ast
from heppy.myScripts.plotDistributionComparisonPlot import plotDistributionComparisonPlot
from math import isnan

saveFolder = "_jetTriggerRate_BarrelOnly"
binning = "[3, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 100, 125, 150, 175, 200, 250, 300]"
##binning = "[0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]"
qualityThreshold = 0
detectorEta = 1.1 #Focussing only on barrel
barrelEta = detectorEta #No cuts
binningArray = array("f", ast.literal_eval(binning))
magneticField = 3.8 # Tesla
#Used to normalise trigger rates in output from Delphes sim
#minimumPtToReachBarrel = barrelRadius * magneticField/6.6
minimumPtToReachBarrel = 3 # No cuts
minimumPtToReachEndcap = 3 # No cuts
sample_BinnedDistributions = "cmsMatching_QCD_15_3000_L1TJet_GenJet"
genObject="genJet"
triggerObject="l1tJet"

efficiencySourceFolder = "/hdfs/FCC-hh/l1tGenJetMatching_QCD_15_3000_NoPU_Phase1_L11Obj_To_GenJet_Match_ClosestDR"
efficiencyMatchTree = "MatchGenJetWithL1Objects/matchedL1TJetGenJetTree"
efficiencyGenTree = "MatchGenJetWithL1Objects/genJetTree"

sampleRateEstimation = "MinimumBias_14TeV_GenParticles_partial"
numberOfDelphesEvents = 3860000
averagePileUp = 140
bunchCrossingFrequency = 31.6e6 # 2808 bunches
#instantaneousLuminosity = 5e34 #cm^-2 s^-1
#minBiasCrossSection = 56.79 # mb, from Pythia
interactionFrequency = averagePileUp * bunchCrossingFrequency

###################################################################################################
#################################### DO NOT TOUCH FROM DOWN ON ####################################
###################################################################################################
#
#os.system("mkdir -p " + saveFolder)
#if os.listdir(saveFolder):
#  print "Save directory is not empty. It will be cleaned. Continue?"
#  if raw_input() == "y":
#    os.system("rm -r " + saveFolder + "/*")
#  else:
#    print "Stopping process."
#    exit()
#
# Common options
#
#print "--- COMPUTING CONVOLUTION CURVES ---"
#
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/binnedDistributionsCMS_cfg.py"]
#options.extraOptions.append("sample=" + sample_BinnedDistributions)
#options.extraOptions.append("binning=" + binning)
#options.extraOptions.append("quality=" + str(qualityThreshold))
#options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrel))
#options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcap))
#options.extraOptions.append("barrelEta=" + str(barrelEta))
#options.extraOptions.append("triggerObjectName=" + triggerObject)
#options.extraOptions.append("genObjectName=" + genObject)
#options.nevents=500000
#loop = main(options, folderAndScriptName, parser)
#os.system("mv " + saveFolder + "/" + sample_BinnedDistributions + " " + saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves")
#
#print "--- COMPUTING THE CONVERSION FACTORS/EFFICIENCIES ---"
#
#numberOfMatchedObjects, numberOfGenObjects = computeEfficiencies(
#                                                                  GenObjTree = efficiencyGenTree,
#                                                                  GenObjFileFolder = efficiencySourceFolder,
#                                                                  MatchTree = efficiencyMatchTree,
#                                                                  MatchFileFolder = efficiencySourceFolder,
#                                                                  binning = binning,
#                                                                  eta = detectorEta,
#                                                                  quality = qualityThreshold,
#                                                                  barrelEta = barrelEta,
#                                                                  minPtInBarrel = minimumPtToReachBarrel,
#                                                                  minPtInEndcap = minimumPtToReachEndcap,
#                                                                )
#
#numberOfMatchedObjects = numberOfMatchedObjects
#numberOfGenObjects = numberOfGenObjects
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
#efficiencyHistogram = TH1F("efficiencyHistogram", "Trigger efficiency", len(binningArray)-1, binningArray)
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
print "--- APPLYING CONVOLUTION TO EVENT SAMPLE TO COMPUTE RATES ---"

print "CREATING THE NON-NORMALISED PLOTS"

parser = create_parser()
(options,args) = parser.parse_args()
folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/l1tObjectTriggerRateMinBiasFromJets_cfg.py"]
convolutionFileName = saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves/histograms.root"
options.extraOptions.append("sample=" + sampleRateEstimation)
options.extraOptions.append("convolutionFileName=" + convolutionFileName)
options.extraOptions.append("binning=" + binning)
options.extraOptions.append("probabilityFile=" + "" + saveFolder + "/efficiencyFactors.root")
options.extraOptions.append("probabilityHistogram=" + "efficiencyHistogram")
options.extraOptions.append("detectorEta=" + str(detectorEta))
options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrel))
options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcap))
options.extraOptions.append("barrelEta=" + str(barrelEta))
options.extraOptions.append("triggerObjectName=" + str(triggerObject))
options.nevents=200000
loop = main(options, folderAndScriptName, parser)
os.system("mv " + saveFolder + "/" + sampleRateEstimation + "/ratePlots.root " + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_NotNormalised.root")

print "OBTAINING THE RATE IN THE LINEAR SCALING APPROXIMATION"

nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_NotNormalised.root")
totalRateHist = nonNormalisedRatePlotFile.Get("simL1TObjectTriggerRate")
barrelRateHist = nonNormalisedRatePlotFile.Get("barrelSimL1TObjectRate")
endcapRateHist = nonNormalisedRatePlotFile.Get("endcapSimL1TObjectRate")

totalRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
barrelRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
endcapRateHist.Scale(interactionFrequency/numberOfDelphesEvents)

totalRateHist.GetXaxis().SetTitle("p_{t}")
totalRateHist.GetXaxis().SetRangeUser(5, 200)
totalRateHist.GetYaxis().SetTitle("Rate [Hz]")
barrelRateHist.GetXaxis().SetTitle("p_{t}")
barrelRateHist.GetXaxis().SetRangeUser(5, 200)
barrelRateHist.GetYaxis().SetTitle("Rate [Hz]")
endcapRateHist.GetXaxis().SetTitle("p_{t}")
endcapRateHist.GetXaxis().SetRangeUser(5, 200)
endcapRateHist.GetYaxis().SetTitle("Rate [Hz]")

normalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_Normalised.root", "RECREATE")
normalisedRatePlotFile.cd()
totalRateHist.Write()
barrelRateHist.Write()
endcapRateHist.Write()
normalisedRatePlotFile.Close()
nonNormalisedRatePlotFile.Close()

print "NORMALISING THE RATE PLOT TO OBTAIN THE TRIGGER PASS PROBABILITY FOR MINBIAS AND PU140 EVENTS"

nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_NotNormalised.root")
passProbabilityFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_TriggerPassProbability.root", "RECREATE")
totalRateHist = nonNormalisedRatePlotFile.Get("simL1TObjectTriggerRate")
ppPassProbabilityHistogram = totalRateHist.Clone("ppPassProbabilityHistogram")
ppPassProbabilityHistogram.Scale(1./numberOfDelphesEvents)
passProbabilityFile.cd()
eventPassProbabilityHistogram = ppPassProbabilityHistogram.Clone("eventPassProbabilityHistogram")

for x in xrange(1, eventPassProbabilityHistogram.GetNbinsX()+1):
  ppPassProbability = ppPassProbabilityHistogram.GetBinContent(x)
  eventPassProbability = 1. - (1. - ppPassProbability)**averagePileUp
  eventPassProbabilityHistogram.SetBinContent(x, eventPassProbability)

probabilityRatioHistogram = eventPassProbabilityHistogram.Clone("probabilityRatioHistogram")
probabilityRatioHistogram.Divide(ppPassProbabilityHistogram)

probabilityRatioHistogram.Write()
ppPassProbabilityHistogram.Write()
eventPassProbabilityHistogram.Write()

nonNormalisedRatePlotFile.Close()
passProbabilityFile.Close()

print "COMPUTING THE TRIGGER PASS PROBABIITY IN LINEAR SCALING APPROXIMATION AND WITH FULL FORMULA"

passProbabilityFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_TriggerPassProbability.root")
ppPassProbabilityHistogram = passProbabilityFile.Get("ppPassProbabilityHistogram")
eventPassProbabilityHistogram = passProbabilityFile.Get("eventPassProbabilityHistogram")

linearPURatePlot = ppPassProbabilityHistogram.Clone("linearPURatePlot")
fullPURatePlot = eventPassProbabilityHistogram.Clone("fullPURatePlot")

linearPURatePlot.Scale(interactionFrequency)
fullPURatePlot.Scale(bunchCrossingFrequency)

pileupRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_PU" + str(averagePileUp) + "RatePlot.root", "RECREATE")
pileupRatePlotFile.cd()
linearPURatePlot.Write()
fullPURatePlot.Write()

pileupRatePlotFile.Close()
#
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
#options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrel))
#options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcap))
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
#options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrel))
#options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcap))
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