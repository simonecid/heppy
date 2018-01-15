#!/usr/bin/env python

from heppy.framework.heppy_loop import * 
from heppy.genObjectToL1TObjectConvolutionCurves.computeEfficiencies import computeEfficiencies
from ROOT import TH1F
from ROOT import TFile
from ROOT import TChain
from ROOT import TTree
import os
from array import array
import ast
from heppy.myScripts.plotDistributionComparisonPlot import plotDistributionComparisonPlot
from math import isnan
from glob import glob
from importlib import import_module
import yaml
import argparse

saveFolder = "_jetTriggerRate_LeadingJet_full/"
binning = "[3, 4, 5, 7, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100, 110, 125, 150, 175, 200, 250, 300, 400, 500]"
##binning = "[0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]"
qualityThreshold = 0
barrelEta = 1.44 # 0-1.44 barrel
endcapEta = 3 #1.44 - 3 endcap
detectorEta = 5.05 # 3 - 1.44 forward
binningArray = array("f", ast.literal_eval(binning))
magneticField = 3.8 # Tesla
deltaR2Matching = 0.25
#Used to normalise trigger rates in output from Delphes sim
#minimumPtToReachBarrel = barrelRadius * magneticField/6.6
minimumPtToReachBarrel = 25 # Some cut
minimumPtToReachEndcap = 1000000 # disabling endcap with high pt threshold
minimumPtToReachForward = 1000000 # killing forward
sample_BinnedDistributions = "cmsMatching_QCD_15_3000_OnlyBarrelLeadingGenJet_GenJet_L1TJet"
genObject = "leadingGenJet"
triggerObject = "l1tJet"

efficiencySourceFolder = "/hdfs/FCC-hh/l1tGenJetMatching_QCD_15_3000_NoPU_Phase1_ClosestDRMatch_MuonVeto_BarrelLeadingL1TJetOnly_OnlyBarrelLeadingGenJet"
efficiencyMatchTree = "MatchLeadingGenJetWithL1Objects/matchedLeadingGenJetL1TJetTree"
efficiencyGenTree = "MatchLeadingGenJetWithL1Objects/leadingGenJetTree"
numberOfFiles = -1

sample_ClosureTest1 = "cmsMatching_QCD_15_3000_L1TJet_GenJet_Smaller"
sample_ClosureTest2 = "cmsMatching_QCD_15_3000_GenJet_Smaller"
sample_ClosureTest3 = "cmsMatching_SingleNeutrinoPU140_BarrelOnly_LeadingL1TJet"
#sample_ClosureTest4 = "cmsMatching_SingleNeutrinoPU140_BarrelOnly_L1TJet"

sampleModule = "sample_MinimumBias_NoTau_14TeV_GenParticles"
sampleRateEstimation = "MinimumBias_14TeV_GenParticles_full"
averagePileUp = 140
bunchCrossingFrequency = 31.6e6 # 2808 bunches
#instantaneousLuminosity = 5e34 #cm^-2 s^-1
#minBiasCrossSection = 56.79 # mb, from Pythia

###################################################################################################
#################################### DO NOT TOUCH FROM DOWN ON ####################################
###################################################################################################
interactionFrequency = averagePileUp * bunchCrossingFrequency
componentRateEstimation = getattr(import_module("heppy.samples." + sampleModule), sampleRateEstimation)
numberOfDelphesEvents = componentRateEstimation.nGenEvents
os.system("mkdir -p " + saveFolder)

#if os.listdir(saveFolder):
#  print "Save directory is not empty. It will be cleaned. Continue?"
#  if raw_input() == "y":
#    os.system("rm -r " + saveFolder + "/*")
#  else:
#    print "Stopping process."
#    exit()
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
#options.extraOptions.append("minimumPtInForward=" + str(minimumPtToReachForward))
#options.extraOptions.append("barrelEta=" + str(barrelEta))
#options.extraOptions.append("endcapEta=" + str(endcapEta))
#options.extraOptions.append("detectorEta=" + str(detectorEta))
#options.extraOptions.append("triggerObjectName=" + triggerObject)
#options.extraOptions.append("genObjectName=" + genObject)
#options.extraOptions.append("deltaR2Matching=" + str(deltaR2Matching))
##options.nevents=300000
#options.force = True
#loop = main(options, folderAndScriptName, parser)
#
#os.system("mkdir " + saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves")
#os.system("hadd " + saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves/histograms.root " + saveFolder + "/" + sample_BinnedDistributions + "_Chunk*/histograms.root")
#
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
#                                                                  endcapEta = endcapEta,
#                                                                  minPtInBarrel = minimumPtToReachBarrel,
#                                                                  minPtInEndcap = minimumPtToReachEndcap,
#                                                                  minPtInForward = minimumPtToReachForward,
#                                                                  deltaR2Matching = deltaR2Matching,
#                                                                  numberOfFiles = numberOfFiles
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
#numberOfMatchedObjectsHistogram = TH1F("numberOfMatchedObjectsHistogram", "numberOfMatchedObjectsHistogram", len(binningArray)-1, binningArray)
#numberOfGenObjectsHistogram = TH1F("numberOfGenObjectsHistogram", "numberOfGenObjectsHistogram", len(binningArray)-1, binningArray)
#
#for x in xrange(0, len(efficiencyFactors)): 
#  #Excluding overflow bin
#  if x != len(efficiencyFactors) - 1:
#    efficiencyHistogram.SetBinContent(x + 1, efficiencyFactors[x])
#    numberOfMatchedObjectsHistogram.SetBinContent(x + 1, numberOfMatchedObjects[x])
#    numberOfGenObjectsHistogram.SetBinContent(x + 1, numberOfGenObjects[x])
#  
#efficiencyHistogram.Write()
#numberOfMatchedObjectsHistogram.Write()
#numberOfGenObjectsHistogram.Write()
#efficiencyFactorsFile.Close()

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
options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrel))
options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcap))
options.extraOptions.append("minimumPtInForward=" + str(minimumPtToReachForward))
options.extraOptions.append("barrelEta=" + str(barrelEta))
options.extraOptions.append("endcapEta=" + str(endcapEta))
options.extraOptions.append("detectorEta=" + str(detectorEta))
options.extraOptions.append("triggerObjectName=" + str(triggerObject))
options.force = True
options.nevents = numberOfDelphesEvents
loop = main(options, folderAndScriptName, parser)
#
#print "MERGING HEPPY CHUNKS"
#
##Merging the histograms and trees
#filesToMerge = glob(saveFolder + "/" + sampleRateEstimation + "*/ratePlots.root")
#
#treeChain = TChain("genJetSimL1TObjectTree")
#nonNormalisedRatePlotFile = TFile(filesToMerge[0])
#totalRateHist = nonNormalisedRatePlotFile.Get("simL1TObjectTriggerRate")
#barrelRateHist = nonNormalisedRatePlotFile.Get("barrelSimL1TObjectRate")
#endcapRateHist = nonNormalisedRatePlotFile.Get("endcapSimL1TObjectRate")
#forwardRateHist = nonNormalisedRatePlotFile.Get("forwardSimL1TObjectRate")
#mergedTotalRateHist = totalRateHist.Clone("mergedTotalSimL1TObjectTriggerRate")
#mergedBarrelRateHist = barrelRateHist.Clone("mergedBarrelSimL1TObjectRate")
#mergedEndcapRateHist = endcapRateHist.Clone("mergedEndcapSimL1TObjectRate")
#mergedForwardRateHist = forwardRateHist.Clone("mergedForwardSimL1TObjectRate")
#mergedTotalRateHist.SetDirectory(0)
#mergedBarrelRateHist.SetDirectory(0)
#mergedEndcapRateHist.SetDirectory(0)
#mergedForwardRateHist.SetDirectory(0)
#treeChain.Add(filesToMerge[0])
#nonNormalisedRatePlotFile.Close()
## First file has been handled, so it is removed from the list
#filesToMerge.pop(0)
##Merging the others
#for fileName in filesToMerge:
#  nonNormalisedRatePlotFile = TFile(fileName)
#  totalRateHist = nonNormalisedRatePlotFile.Get("simL1TObjectTriggerRate")
#  barrelRateHist = nonNormalisedRatePlotFile.Get("barrelSimL1TObjectRate")
#  endcapRateHist = nonNormalisedRatePlotFile.Get("endcapSimL1TObjectRate")
#  forwardRateHist = nonNormalisedRatePlotFile.Get("forwardSimL1TObjectRate")
#  treeChain.Add(fileName)
#  mergedTotalRateHist.Add(totalRateHist)
#  mergedBarrelRateHist.Add(barrelRateHist)
#  mergedEndcapRateHist.Add(endcapRateHist)
#  mergedForwardRateHist.Add(forwardRateHist)
#  nonNormalisedRatePlotFile.Close()
#
#treeChain.Merge(saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_" + genObject + "_Sim" + triggerObject + "_Tree.root")
#
##Saving everything
#mergedHistogramsFile = TFile(saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_NotNormalised.root", "RECREATE")
#mergedHistogramsFile.cd()
#mergedTotalRateHist.SetDirectory(mergedHistogramsFile)
#mergedBarrelRateHist.SetDirectory(mergedHistogramsFile)
#mergedEndcapRateHist.SetDirectory(mergedHistogramsFile)
#mergedForwardRateHist.SetDirectory(mergedHistogramsFile)
#mergedTotalRateHist.Write()
#mergedBarrelRateHist.Write()
#mergedEndcapRateHist.Write()
#mergedForwardRateHist.Write()
#mergedHistogramsFile.Close()
#
#
#print "OBTAINING THE RATE IN THE LINEAR SCALING APPROXIMATION"
#
#nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_NotNormalised.root")
#totalRateHist = nonNormalisedRatePlotFile.Get("mergedTotalSimL1TObjectTriggerRate")
#barrelRateHist = nonNormalisedRatePlotFile.Get("mergedBarrelSimL1TObjectRate")
#endcapRateHist = nonNormalisedRatePlotFile.Get("mergedEndcapSimL1TObjectRate")
#forwardRateHist = nonNormalisedRatePlotFile.Get("mergedForwardSimL1TObjectRate")
#
#totalRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
#barrelRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
#endcapRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
#forwardRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
#
#totalRateHist.GetXaxis().SetTitle("p_{t}")
#totalRateHist.GetXaxis().SetRangeUser(5, 200)
#totalRateHist.GetYaxis().SetTitle("Rate [Hz]")
#barrelRateHist.GetXaxis().SetTitle("p_{t}")
#barrelRateHist.GetXaxis().SetRangeUser(5, 200)
#barrelRateHist.GetYaxis().SetTitle("Rate [Hz]")
#endcapRateHist.GetXaxis().SetTitle("p_{t}")
#endcapRateHist.GetXaxis().SetRangeUser(5, 200)
#endcapRateHist.GetYaxis().SetTitle("Rate [Hz]")
#forwardRateHist.GetXaxis().SetTitle("p_{t}")
#forwardRateHist.GetXaxis().SetRangeUser(5, 200)
#forwardRateHist.GetYaxis().SetTitle("Rate [Hz]")
#
#normalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_Normalised.root", "RECREATE")
#normalisedRatePlotFile.cd()
#totalRateHist.Write()
#barrelRateHist.Write()
#endcapRateHist.Write()
#forwardRateHist.Write()
#normalisedRatePlotFile.Close()
#nonNormalisedRatePlotFile.Close()
#
#print "NORMALISING THE RATE PLOT TO OBTAIN THE TRIGGER PASS PROBABILITY FOR MINBIAS AND PU140 EVENTS"
#
#nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_NotNormalised.root")
#passProbabilityFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_TriggerPassProbability.root", "RECREATE")
#totalRateHist = nonNormalisedRatePlotFile.Get("mergedTotalSimL1TObjectTriggerRate")
#barrelRateHist = nonNormalisedRatePlotFile.Get("mergedBarrelSimL1TObjectRate")
#endcapRateHist = nonNormalisedRatePlotFile.Get("mergedEndcapSimL1TObjectRate")
#forwardRateHist = nonNormalisedRatePlotFile.Get("mergedForwardSimL1TObjectRate")
#ppPassProbabilityHistogram = totalRateHist.Clone("ppPassProbabilityHistogram")
#ppPassProbabilityHistogramInBarrel = totalRateHist.Clone("ppPassProbabilityHistogramInBarrel")
#ppPassProbabilityHistogramInEndcap = totalRateHist.Clone("ppPassProbabilityHistogramInEndcap")
#ppPassProbabilityHistogramInForward = totalRateHist.Clone("ppPassProbabilityHistogramInForward")
#ppPassProbabilityHistogram.Scale(1./numberOfDelphesEvents)
#ppPassProbabilityHistogramInBarrel.Scale(1./numberOfDelphesEvents)
#ppPassProbabilityHistogramInEndcap.Scale(1./numberOfDelphesEvents)
#ppPassProbabilityHistogramInForward.Scale(1./numberOfDelphesEvents)
#passProbabilityFile.cd()
#eventPassProbabilityHistogram = ppPassProbabilityHistogram.Clone("eventPassProbabilityHistogram")
#eventPassProbabilityHistogramInBarrel = ppPassProbabilityHistogramInBarrel.Clone("eventPassProbabilityHistogramInBarrel")
#eventPassProbabilityHistogramInEndcap = ppPassProbabilityHistogramInEndcap.Clone("eventPassProbabilityHistogramInEndcap")
#eventPassProbabilityHistogramInForward = ppPassProbabilityHistogramInForward.Clone("eventPassProbabilityHistogramInForward")
#
#for x in xrange(1, eventPassProbabilityHistogram.GetNbinsX()+1):
#  ppPassProbability = ppPassProbabilityHistogram.GetBinContent(x)
#  ppPassProbabilityInBarrel = ppPassProbabilityHistogramInBarrel.GetBinContent(x)
#  ppPassProbabilityInEndcap = ppPassProbabilityHistogramInEndcap.GetBinContent(x)
#  ppPassProbabilityInForward = ppPassProbabilityHistogramInForward.GetBinContent(x)
#  eventPassProbability = 1. - (1. - ppPassProbability)**averagePileUp
#  eventPassProbabilityInBarrel = 1. - (1. - ppPassProbabilityInBarrel)**averagePileUp
#  eventPassProbabilityInEndcap = 1. - (1. - ppPassProbabilityInEndcap)**averagePileUp
#  eventPassProbabilityInForward = 1. - (1. - ppPassProbabilityInForward)**averagePileUp
#  eventPassProbabilityHistogram.SetBinContent(x, eventPassProbability)
#  eventPassProbabilityHistogramInBarrel.SetBinContent(x, eventPassProbabilityInBarrel)
#  eventPassProbabilityHistogramInEndcap.SetBinContent(x, eventPassProbabilityInEndcap)
#  eventPassProbabilityHistogramInForward.SetBinContent(x, eventPassProbabilityInForward)
#
#probabilityRatioHistogram = eventPassProbabilityHistogram.Clone("probabilityRatioHistogram")
#probabilityRatioHistogram.Divide(ppPassProbabilityHistogram)
#probabilityRatioHistogramInBarrel = eventPassProbabilityHistogramInBarrel.Clone("probabilityRatioHistogramInBarrel")
#probabilityRatioHistogramInBarrel.Divide(ppPassProbabilityHistogramInBarrel)
#probabilityRatioHistogramInEndcap = eventPassProbabilityHistogramInEndcap.Clone("probabilityRatioHistogramInEndcap")
#probabilityRatioHistogramInEndcap.Divide(ppPassProbabilityHistogramInEndcap)
#probabilityRatioHistogramInForward = eventPassProbabilityHistogramInForward.Clone("probabilityRatioHistogramInForward")
#probabilityRatioHistogramInForward.Divide(ppPassProbabilityHistogramInForward)
#
#probabilityRatioHistogram.Write()
#probabilityRatioHistogramInBarrel.Write()
#probabilityRatioHistogramInEndcap.Write()
#probabilityRatioHistogramInForward.Write()
#ppPassProbabilityHistogram.Write()
#ppPassProbabilityHistogramInBarrel.Write()
#ppPassProbabilityHistogramInEndcap.Write()
#ppPassProbabilityHistogramInForward.Write()
#eventPassProbabilityHistogram.Write()
#eventPassProbabilityHistogramInBarrel.Write()
#eventPassProbabilityHistogramInEndcap.Write()
#eventPassProbabilityHistogramInForward.Write()
#
#nonNormalisedRatePlotFile.Close()
#passProbabilityFile.Close()
#
#print "COMPUTING THE TRIGGER PASS PROBABILITY IN LINEAR SCALING APPROXIMATION AND WITH FULL FORMULA"
#
#passProbabilityFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_TriggerPassProbability.root")
#ppPassProbabilityHistogram = passProbabilityFile.Get("ppPassProbabilityHistogram")
#ppPassProbabilityHistogramInBarrel = passProbabilityFile.Get("ppPassProbabilityHistogramInBarrel")
#ppPassProbabilityHistogramInEndcap = passProbabilityFile.Get("ppPassProbabilityHistogramInEndcap")
#ppPassProbabilityHistogramInForward = passProbabilityFile.Get("ppPassProbabilityHistogramInForward")
#eventPassProbabilityHistogram = passProbabilityFile.Get("eventPassProbabilityHistogram")
#eventPassProbabilityHistogramInBarrel = passProbabilityFile.Get("eventPassProbabilityHistogramInBarrel")
#eventPassProbabilityHistogramInEndcap = passProbabilityFile.Get("eventPassProbabilityHistogramInEndcap")
#eventPassProbabilityHistogramInForward = passProbabilityFile.Get("eventPassProbabilityHistogramInForward")
#
#linearPURatePlot = ppPassProbabilityHistogram.Clone("linearPURatePlot")
#linearPURatePlotInBarrel = ppPassProbabilityHistogramInBarrel.Clone("linearPURatePlotInBarrel")
#linearPURatePlotInEndcap = ppPassProbabilityHistogramInEndcap.Clone("linearPURatePlotInEndcap")
#linearPURatePlotInForward = ppPassProbabilityHistogramInForward.Clone("linearPURatePlotInForward")
#fullPURatePlot = eventPassProbabilityHistogram.Clone("fullPURatePlot")
#fullPURatePlotInBarrel = eventPassProbabilityHistogramInBarrel.Clone("fullPURatePlotInBarrel")
#fullPURatePlotInEndcap = eventPassProbabilityHistogramInEndcap.Clone("fullPURatePlotInEndcap")
#fullPURatePlotInForward = eventPassProbabilityHistogramInForward.Clone("fullPURatePlotInForward")
#
#linearPURatePlot.Scale(interactionFrequency)
#linearPURatePlotInBarrel.Scale(interactionFrequency)
#linearPURatePlotInEndcap.Scale(interactionFrequency)
#linearPURatePlotInForward.Scale(interactionFrequency)
#fullPURatePlot.Scale(bunchCrossingFrequency)
#fullPURatePlotInBarrel.Scale(bunchCrossingFrequency)
#fullPURatePlotInEndcap.Scale(bunchCrossingFrequency)
#fullPURatePlotInForward.Scale(bunchCrossingFrequency)
#
#pileupRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_PU" + str(averagePileUp) + "RatePlot.root", "RECREATE")
#pileupRatePlotFile.cd()
#
#linearPURatePlot.Write()
#linearPURatePlotInBarrel.Write()
#linearPURatePlotInEndcap.Write()
#linearPURatePlotInForward.Write()
#fullPURatePlot.Write()
#fullPURatePlotInBarrel.Write()
#fullPURatePlotInEndcap.Write()
#fullPURatePlotInForward.Write()
#
#pileupRatePlotFile.Close()
#
#print "--- RUNNING THE CLOSURE TESTS ---"
#
#print "CREATING THE MOMENTUM DISTRIBUTION PLOTS FOR MATCHED CMS GEN JET TO SIML1TOBJECT"
##Taking the matched gen muons
##Applying the quality selection on the corresponding l1tmu to get only the gen mu matched to a quality l1tmu
##Applying the smearing without any probabilistic exclusion to see if resolution curve are accurate enough
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/plotTransverseMomentumDistributionForClosureTest_cfg.py"]
#convolutionFileName = saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves/histograms.root"
#options.extraOptions.append("sample=" + sample_ClosureTest1)
#options.extraOptions.append("convolutionFileName=" + convolutionFileName)
#options.extraOptions.append("binning=" + binning)
#options.extraOptions.append("quality=" + str(qualityThreshold))
#options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrel))
#options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcap))
#options.extraOptions.append("minimumPtInForward=" + str(minimumPtToReachForward))
#options.extraOptions.append("detectorEta=" + str(detectorEta))
#options.extraOptions.append("barrelEta=" + str(barrelEta))
#options.extraOptions.append("endcapEta=" + str(endcapEta))
#options.extraOptions.append("triggerObjectName=" + triggerObject)
#options.extraOptions.append("genObjectName=" + genObject)
#options.extraOptions.append("deltaR2Matching=" + str(deltaR2Matching))
#options.nevents=300000
#options.force = True
#loop = main(options, folderAndScriptName, parser)
#os.system("mv " + saveFolder + "/" + sample_ClosureTest1 + " " + saveFolder + "/" + sample_ClosureTest1 + "_ClosureTestPlots_QualityCutOnGenObject")
#
#print "CREATING THE MOMENTUM DISTRIBUTION PLOTS FOR CMS GEN JET TO SIML1TOBJECT (EVERY GEN JET IS CONSIDERED)"
#
##We take every gen mu.
##We check if they fall into the detector
##If they do, we apply the probabilistic selection and the smearing
#
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/plotTransverseMomentumDistributionForClosureTest_cfg.py"]
#convolutionFileName = saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves/histograms.root"
#options.extraOptions.append("sample=" + sample_ClosureTest2)
#options.extraOptions.append("convolutionFileName=" + convolutionFileName)
#options.extraOptions.append("binning=" + binning)
#options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrel))
#options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcap))
#options.extraOptions.append("minimumPtInForward=" + str(minimumPtToReachForward))
#options.extraOptions.append("detectorEta=" + str(detectorEta))
#options.extraOptions.append("barrelEta=" + str(barrelEta))
#options.extraOptions.append("endcapEta=" + str(endcapEta))
#options.extraOptions.append("probabilityFile=" + "" + saveFolder + "/efficiencyFactors.root")
#options.extraOptions.append("probabilityHistogram=" + "efficiencyHistogram")
#options.extraOptions.append("quality=" + str(qualityThreshold))
#options.extraOptions.append("triggerObjectName=" + triggerObject)
#options.extraOptions.append("genObjectName=" + genObject)
#options.extraOptions.append("deltaR2Matching=" + str(deltaR2Matching))
##options.nevents=300000
#options.force = True
#loop = main(options, folderAndScriptName, parser)
#os.system("mv " + saveFolder + "/" + sample_ClosureTest2 + " " + saveFolder + "/" + sample_ClosureTest2 + "_ClosureTestPlots_AllGenObjects")
#
#print "CREATING THE COMPARISON PLOTS"
#
#cfg = lambda x: 1
#cfg.plots = [
##  #Files here
#  [saveFolder + "/" + sample_ClosureTest1 + "_ClosureTestPlots_QualityCutOnGenObject/histograms.root", "coarseBinnedPt" + triggerObject + "Distribution", "CMS " + triggerObject],
#  [saveFolder + "/" + sample_ClosureTest1 + "_ClosureTestPlots_QualityCutOnGenObject/histograms.root", "coarseBinnedSmearedPt" + genObject + "Distribution", "Sim " + triggerObject + " from matched " + genObject]
##  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtSimL1TMuonDistribution", "SimL1TMuon"],
##  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtL1TMuonDistribution", "Original L1TMuon"],
#]
#cfg.saveFileName = "" + saveFolder + "/closureTest1.root"
#
#plotDistributionComparisonPlot(cfg)
##
#cfg = lambda x: 1
#cfg.plots = [
##  #Files here
#  [saveFolder + "/" + sample_ClosureTest1 + "_ClosureTestPlots_QualityCutOnGenObject/histograms.root", "coarseBinnedPt" + triggerObject + "Distribution", "CMS " + triggerObject],
#  [saveFolder + "/" + sample_ClosureTest2 + "_ClosureTestPlots_AllGenObjects/histograms.root", "coarseBinnedSmearedPt" + genObject + "Distribution", "Sim " + triggerObject + " from every " + genObject]
##  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtSimL1TMuonDistribution", "SimL1TMuon"],
##  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtL1TMuonDistribution", "Original L1TMuon"],
#]
#cfg.saveFileName = "" + saveFolder + "/closureTest2.root"
#
#plotDistributionComparisonPlot(cfg)
#
#print "CREATING THE ORIGINAL CMS RATE PLOT"
#
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/computeTriggerRatesFromCMS_cfg.py"]
#options.extraOptions.append("sample=" + sample_ClosureTest3)
#options.extraOptions.append("barrelEta=" + str(barrelEta))
#options.extraOptions.append("detectorEta=" + str(detectorEta))
##options.nevents=100
#loop = main(options, folderAndScriptName, parser)
#os.system("mv " + saveFolder + "/" + sample_ClosureTest3 + " " + saveFolder + "/" + sample_ClosureTest3 + "_CMSTriggerRate")
#
#cmsRatePlotFile = TFile("" + saveFolder + "/" + sample_ClosureTest3 + "_CMSTriggerRate/ratePlots.root", "UPDATE")
#totalRateHist = cmsRatePlotFile.Get("triggerRate")
#barrelRateHist = cmsRatePlotFile.Get("barrelTriggerRate")
#endcapRateHist = cmsRatePlotFile.Get("endcapTriggerRate")
#totalRateHist.GetXaxis().SetTitle("p_{t}")
#totalRateHist.GetYaxis().SetTitle("Rate [Hz]")
#barrelRateHist.GetXaxis().SetTitle("p_{t}")
#barrelRateHist.GetYaxis().SetTitle("Rate [Hz]")
#endcapRateHist.GetXaxis().SetTitle("p_{t}")
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
#  ["" + saveFolder + "/" + sample_ClosureTest3 + "_CMSTriggerRate/ratePlots.root", "triggerRate", "CMS " + triggerObject],
#  ["" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_RatePlots_PU" + str(averagePileUp) + "RatePlot.root", "fullPURatePlot", "Sim " + triggerObject]
#]
#cfg.saveFileName = "" + saveFolder + "/rateClosureTest.root"
#plotDistributionComparisonPlot(cfg)
#
#print "CREATING THE SIM-" + triggerObject + "PT DISTRIBUTION PLOT"
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/plotTransverseMomentumDistributionForClosureTest_cfg.py"]
#convolutionFileName = saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves/histograms.root"
#options.extraOptions.append("sample=delphesSample")
#options.extraOptions.append("sampleFileName=" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_" + genObject + "_Sim" + triggerObject + "_Tree.root")
#options.extraOptions.append("treeName=genJetSimL1TObjectTree")
#options.extraOptions.append("convolutionFileName=" + convolutionFileName)
#options.extraOptions.append("binning=" + binning)
#options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrel))
#options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcap))
#options.extraOptions.append("minimumPtInForward=" + str(minimumPtToReachForward))
#options.extraOptions.append("detectorEta=" + str(detectorEta))
#options.extraOptions.append("barrelEta=" + str(barrelEta))
#options.extraOptions.append("endcapEta=" + str(endcapEta))
#options.extraOptions.append("probabilityFile=" + "" + saveFolder + "/efficiencyFactors.root")
#options.extraOptions.append("probabilityHistogram=" + "efficiencyHistogram")
#options.extraOptions.append("quality=" + str(qualityThreshold))
#options.extraOptions.append("triggerObjectName=Sim" + triggerObject)
#options.extraOptions.append("genObjectName=" + genObject)
#options.force = True
#loop = main(options, folderAndScriptName, parser)
#os.system("mv " + saveFolder + "/delphesSample" + " " + saveFolder + "/genJetSimL1TObjectTree_ClosureTestPlots")
#
#print "CREATING THE " + triggerObject + " PT DISTRIBUTION PLOT FROM CMS"
#parser = create_parser()
#(options,args) = parser.parse_args()
#folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/plotTransverseMomentumDistribution_cfg.py"]
#options.extraOptions.append("sample=" + sample_ClosureTest4)
#options.nevents=5e5
#options.extraOptions.append("sampleFileName=" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + sampleRateEstimation + "_" + genObject + "_Sim" + triggerObject + "_Tree.root")
#
#loop = main(options, folderAndScriptName, parser)
#os.system("mv " + saveFolder + "/" + sample_ClosureTest4 + " " + saveFolder + "/" + sample_ClosureTest4+ "_TriggerObjectPtDistribution")


if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  parser.add_argument('--ConfigFile', type=str, required=True)
  arguments = parser.parse_args()

  configFile = parser.ConfigFile
  parameters = yaml.load(file(configFile, 'r'))

  