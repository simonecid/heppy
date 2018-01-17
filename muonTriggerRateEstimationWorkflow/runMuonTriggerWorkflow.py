#!/usr/bin/env python

from heppy.framework.heppy_loop import * 
from heppy.muonTriggerRateEstimationWorkflow.computeEfficiencies import computeEfficiencies
from ROOT import TH1F
from ROOT import TFile
from ROOT import TChain
import os
from array import array
import ast
from heppy.myScripts.plotDistributionComparisonPlot import plotDistributionComparisonPlot
from math import isnan
import yaml
from importlib import import_module
from glob import glob

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
## Common options


def computeConvolutionCurvesHighPtMuons(yamlConf):

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]

  moduleNameConvolutionCurvesHighPt = yamlConf["moduleNameConvolutionCurvesHighPt"]
  componentNameConvolutionCurvesHighPt = yamlConf["componentNameConvolutionCurvesHighPt"]

  componentConvolutionCurvesHighPt = [getattr(import_module(
      moduleNameConvolutionCurvesHighPt), componentNameConvolutionCurvesHighPt, None)]

  if componentConvolutionCurvesHighPt[0] is None:
    print "Error:  component does not exist"
    raise ValueError('Component ' + componentNameConvolutionCurvesHighPt +
                     " has not been declared in module " + moduleNameConvolutionCurvesHighPt)

  parser = create_parser()
  (options, args) = parser.parse_args()
  folderAndScriptName = [
      saveFolder, "muonTriggerRateEstimationWorkflow/binnedDistributionsCMS_L1TMuon_cfg.py"]
  options.components = split(componentConvolutionCurvesHighPt)
  for component in options.components:
    component.splitFactor = 1

  #options.extraOptions.append("sample=" + yamlConf["sampleBinnedDistributions"])
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("quality=" + str(yamlConf["qualityThreshold"]))
  options.extraOptions.append(
      "minimumPtInBarrel=" + str(yamlConf["minimumPtToReachBarrel"]))
  options.extraOptions.append(
      "minimumPtInEndcap=" + str(yamlConf["minimumPtToReachEndcap"]))
  options.extraOptions.append("barrelEta=" + str(yamlConf["barrelEta"]))
  options.extraOptions.append("detectorEta=" + str(yamlConf["detectorEta"]))
  options.extraOptions.append("triggerObjectName=" + yamlConf["triggerObject"])
  options.extraOptions.append("genObjectName=" + yamlConf["genObject"])
  options.extraOptions.append(
      "deltaR2Matching=" + str(yamlConf["deltaR2Matching"]))
  #options.nevents=300000
  options.force = True
  loop = main(options, folderAndScriptName, parser)
  os.system("rm -r " + saveFolder + "/" + genObject +
            "_" + triggerObject + "_" + "convolutionCurves_highPt")
  os.system("mkdir " + saveFolder + "/" + genObject +
            "_" + triggerObject + "_" + "convolutionCurves_highPt")
  if componentConvolutionCurvesHighPt[0].splitFactor > 1:
    os.system("hadd " + saveFolder + "/" + genObject + "_" + triggerObject + "_" + "convolutionCurves_highPt/histograms.root " +
              saveFolder + "/" + componentNameConvolutionCurvesHighPt + "_Chunk*/histograms.root")
  else:
    os.system("mv " + saveFolder + "/" + componentNameConvolutionCurvesHighPt + "/histograms.root " +
              saveFolder + "/" + genObject + "_" + triggerObject + "_" + "convolutionCurves_highPt/histograms.root")

def computeConvolutionCurvesLowPtMuons(yamlConf):

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]

  moduleNameConvolutionCurvesLowPt = yamlConf["moduleNameConvolutionCurvesLowPt"]
  componentNameConvolutionCurvesLowPt = yamlConf["componentNameConvolutionCurvesLowPt"]

  componentConvolutionCurvesLowPt = [getattr(import_module(
      moduleNameConvolutionCurvesLowPt), componentNameConvolutionCurvesLowPt, None)]

  if componentConvolutionCurvesLowPt[0] is None:
    print "Error:  component does not exist"
    raise ValueError('Component ' + componentNameConvolutionCurvesLowPt +
                     " has not been declared in module " + moduleNameConvolutionCurvesLowPt)

  parser = create_parser()
  (options, args) = parser.parse_args()
  folderAndScriptName = [
      saveFolder, "muonTriggerRateEstimationWorkflow/binnedDistributionsCMS_L1TMuon_cfg.py"]
  options.components = split(componentConvolutionCurvesLowPt)
  for component in options.components:
    component.splitFactor = 1

  #options.extraOptions.append("sample=" + yamlConf["sampleBinnedDistributions"])
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("quality=" + str(yamlConf["qualityThreshold"]))
  options.extraOptions.append(
      "minimumPtInBarrel=" + str(yamlConf["minimumPtToReachBarrel"]))
  options.extraOptions.append(
      "minimumPtInEndcap=" + str(yamlConf["minimumPtToReachEndcap"]))
  options.extraOptions.append("barrelEta=" + str(yamlConf["barrelEta"]))
  options.extraOptions.append("detectorEta=" + str(yamlConf["detectorEta"]))
  options.extraOptions.append("triggerObjectName=" + yamlConf["triggerObject"])
  options.extraOptions.append("genObjectName=" + yamlConf["genObject"])
  options.extraOptions.append(
      "deltaR2Matching=" + str(yamlConf["deltaR2Matching"]))
  #options.nevents=300000
  options.force = True
  loop = main(options, folderAndScriptName, parser)
  os.system("rm -r " + saveFolder + "/" + genObject +
            "_" + triggerObject + "_" + "convolutionCurves_lowPt")
  os.system("mkdir " + saveFolder + "/" + genObject +
            "_" + triggerObject + "_" + "convolutionCurves_lowPt")
  if componentConvolutionCurvesLowPt[0].splitFactor > 1:
    os.system("hadd " + saveFolder + "/" + genObject + "_" + triggerObject + "_" + "convolutionCurves_lowPt/histograms.root " +
              saveFolder + "/" + componentNameConvolutionCurvesLowPt + "_Chunk*/histograms.root")
  else:
    os.system("mv " + saveFolder + "/" + componentNameConvolutionCurvesLowPt + "/histograms.root " +
              saveFolder + "/" + genObject + "_" + triggerObject + "_" + "convolutionCurves_lowPt/histograms.root")


def mergeConvolutionCurves(yamlConf):
  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]

  print "MERGING RESULTS"
  os.system("hadd " + saveFolder + "/binnedDistributions.root " +
  saveFolder + "/" + genObject + "_" + triggerObject + "_" + "convolutionCurves_lowPt/histograms.root " +
  saveFolder + "/" + genObject + "_" + triggerObject + "_" + "convolutionCurves_highPt/histograms.root")


def obtainEfficiencies(yamlConf):

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]
  binningArray = array("f", ast.literal_eval(yamlConf["binning"]))
  print "--- COMPUTING THE CONVERSION FACTORS/EFFICIENCIES ---"
  print "PROCESSING FROM LOW MOMENTUM MUONS"
  numberOfMatchedObjects_lowPt, numberOfGenObjects_lowPt = computeEfficiencies(
      GenObjTree=yamlConf["efficiencyLowPtGenTree"],
      GenObjFileFolder=yamlConf["efficiencyLowPtSourceFolder"],
      MatchTree=yamlConf["efficiencyLowPtMatchTree"],
      MatchFileFolder=yamlConf["efficiencyLowPtSourceFolder"],
      binning=yamlConf["binning"],
      eta=yamlConf["detectorEta"],
      quality=yamlConf["qualityThreshold"],
      barrelEta=yamlConf["barrelEta"],
      minPtInBarrel=yamlConf["minimumPtToReachBarrel"],
      minPtInEndcap=yamlConf["minimumPtToReachEndcap"],
  )
  print "PROCESSING FROM HIGH MOMENTUM MUONS"
  numberOfMatchedObjects_highPt, numberOfGenObjects_highPt = computeEfficiencies(
      GenObjTree=yamlConf["efficiencyHighPtGenTree"],
      GenObjFileFolder=yamlConf["efficiencyHighPtSourceFolder"],
      MatchTree=yamlConf["efficiencyHighPtMatchTree"],
      MatchFileFolder=yamlConf["efficiencyHighPtSourceFolder"],
      binning=yamlConf["binning"],
      eta=yamlConf["detectorEta"],
      quality=yamlConf["qualityThreshold"],
      barrelEta=yamlConf["barrelEta"],
      minPtInBarrel=yamlConf["minimumPtToReachBarrel"],
      minPtInEndcap=yamlConf["minimumPtToReachEndcap"],
  )

  numberOfMatchedObjects = numberOfMatchedObjects_lowPt + numberOfMatchedObjects_highPt
  numberOfGenObjects = numberOfGenObjects_lowPt + numberOfGenObjects_highPt

  efficiencyFactors = numberOfMatchedObjects / numberOfGenObjects
  for binIdx in xrange(0, len(efficiencyFactors)):
    efficiencyFactors[binIdx] = 0 if isnan(
        efficiencyFactors[binIdx]) else efficiencyFactors[binIdx]
    if efficiencyFactors[binIdx] > 1:
      efficiencyFactors[binIdx] = 1
  print efficiencyFactors

  efficiencyFactorsFile = TFile(
      "" + saveFolder + "/efficiencyFactors.root", "RECREATE")
  efficiencyFactorsFile.cd()
  efficiencyHistogram = TH1F("efficiencyHistogram", "Trigger efficiency", len(
      binningArray) - 1, binningArray)
  numberOfMatchedObjectsHistogram = TH1F(
      "numberOfMatchedObjectsHistogram", "numberOfMatchedObjectsHistogram", len(binningArray) - 1, binningArray)
  numberOfGenObjectsHistogram = TH1F(
      "numberOfGenObjectsHistogram", "numberOfGenObjectsHistogram", len(binningArray) - 1, binningArray)

  for x in xrange(0, len(efficiencyFactors)):
    #Excluding overflow bin
    if x != len(efficiencyFactors) - 1:
      efficiencyHistogram.SetBinContent(x + 1, efficiencyFactors[x])
      numberOfMatchedObjectsHistogram.SetBinContent(
          x + 1, numberOfMatchedObjects[x])
      numberOfGenObjectsHistogram.SetBinContent(x + 1, numberOfGenObjects[x])

  efficiencyHistogram.Write()
  numberOfMatchedObjectsHistogram.Write()
  numberOfGenObjectsHistogram.Write()
  efficiencyFactorsFile.Close()
  

def computeNonNormalisedRatePlots(yamlConf):

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]
  print "CREATING THE NON-NORMALISED PLOTS"

  moduleNameRatePlots = yamlConf["moduleNameRatePlots"]
  componentNameRatePlots = yamlConf["componentNameRatePlots"]

  componentRatePlots = [getattr(import_module(
      moduleNameRatePlots), componentNameRatePlots, None)]

  if componentRatePlots[0] is None:
    print "Error:  component does not exist"
    raise ValueError('Component ' + componentNameRatePlots +
                     " has not been declared in module " + moduleNameRatePlots)

  parser = create_parser()
  (options, args) = parser.parse_args()
  folderAndScriptName = [
      saveFolder, "muonTriggerRateEstimationWorkflow/muonFCCTriggerRates_cfg.py"]
  convolutionFileName = saveFolder + "/binnedDistributions.root"
  options.components = split(componentRatePlots)
  for component in options.components:
    component.splitFactor = 1

  #options.extraOptions.append("sample=" + yamlConf["componentNameRatePlots"])
  options.extraOptions.append("convolutionFileName=" + convolutionFileName)
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append(
      "probabilityFile=" + "" + yamlConf["saveFolder"] + "/efficiencyFactors.root")
  options.extraOptions.append("probabilityHistogram=efficiencyHistogram")
  options.extraOptions.append(
      "minimumPtInBarrel=" + str(yamlConf["minimumPtToReachBarrel"]))
  options.extraOptions.append(
      "minimumPtInEndcap=" + str(yamlConf["minimumPtToReachEndcap"]))
  options.extraOptions.append("barrelEta=" + str(yamlConf["barrelEta"]))
  options.extraOptions.append("detectorEta=" + str(yamlConf["detectorEta"]))
  options.extraOptions.append(
      "triggerObjectName=" + str(yamlConf["triggerObject"]))
  options.force = True
  if "numberOfDelphesEvents" in yamlConf:
    options.nevents = numberOfDelphesEvents
  #loop = main(options, folderAndScriptName, parser)

  print "MERGING LOCAL HEPPY CHUNKS"

  #Merging the histograms and treesR 
  filesToMerge = glob(
      saveFolder + "/" + componentNameRatePlots + "*/ratePlots.root")

  nonNormalisedRatePlotFile = TFile(filesToMerge[0])
  totalRateHist = nonNormalisedRatePlotFile.Get("simL1TMuonRate")
  barrelRateHist = nonNormalisedRatePlotFile.Get("barrelSimL1TMuonRate")
  endcapRateHist = nonNormalisedRatePlotFile.Get("endcapSimL1TMuonRate")
  mergedTotalRateHist = totalRateHist.Clone(
      "mergedTotalSimL1TMuonRate")
  mergedBarrelRateHist = barrelRateHist.Clone("mergedBarrelSimL1TMuonRate")
  mergedEndcapRateHist = endcapRateHist.Clone("mergedEndcapSimL1TMuonRate")

  mergedTotalRateHist.SetDirectory(0)
  mergedBarrelRateHist.SetDirectory(0)
  mergedEndcapRateHist.SetDirectory(0)

  treeChain = TChain("genMuonSimL1TMuonTree")
  treeChain.Add(filesToMerge[0])
  nonNormalisedRatePlotFile.Close()
  # First file has been handled, so it is removed from the list
  filesToMerge.pop(0)
  #Merging the others
  for fileName in filesToMerge:
    nonNormalisedRatePlotFile = TFile(fileName)
    totalRateHist = nonNormalisedRatePlotFile.Get("simL1TMuonRate")
    barrelRateHist = nonNormalisedRatePlotFile.Get("barrelSimL1TMuonRate")
    endcapRateHist = nonNormalisedRatePlotFile.Get("endcapSimL1TMuonRate")
    treeChain.Add(fileName)
    mergedTotalRateHist.Add(totalRateHist)
    mergedBarrelRateHist.Add(barrelRateHist)
    mergedEndcapRateHist.Add(endcapRateHist)
    nonNormalisedRatePlotFile.Close()

  treeChain.Merge(saveFolder + "/" + genObject + "_" + triggerObject + "_" +
                  componentNameRatePlots + "_" + genObject + "_Sim" + triggerObject + "_Tree.root")

  #Saving everything
  mergedHistogramsFile = TFile(saveFolder + "/" + genObject + "_" + triggerObject +
                               "_" + componentNameRatePlots + "_RatePlots_NotNormalised.root", "RECREATE")
  mergedHistogramsFile.cd()
  mergedTotalRateHist.SetDirectory(mergedHistogramsFile)
  mergedBarrelRateHist.SetDirectory(mergedHistogramsFile)
  mergedEndcapRateHist.SetDirectory(mergedHistogramsFile)
  mergedTotalRateHist.Write()
  mergedBarrelRateHist.Write()
  mergedEndcapRateHist.Write()
  mergedHistogramsFile.Close()

def normaliseMinimumBiasRate(yamlConf):

  saveFolder=yamlConf["saveFolder"]
  genObject=yamlConf["genObject"]
  triggerObject=yamlConf["triggerObject"]
  bunchCrossingFrequency = parameters["bunchCrossingFrequency"]
  componentNameRatePlots = parameters["componentNameRatePlots"]
  interactionFrequency = averagePileUp * bunchCrossingFrequency
  print "CREATING THE NON-NORMALISED PLOTS"

  moduleNameRatePlots=yamlConf["moduleNameRatePlots"]
  componentNameRatePlots=yamlConf["componentNameRatePlots"]

  componentRatePlots=[getattr(import_module(
      moduleNameRatePlots), componentNameRatePlots, None)]

  if componentRatePlots[0] is None:
    print "Error:  component does not exist"
    raise ValueError('Component ' + componentNameRatePlots +
                     " has not been declared in module " + moduleNameRatePlots)

  numberOfDelphesEvents = -1
  if "numberOfDelphesEvents" in yamlConf:
    numberOfDelphesEvents = yamlConf["numberOfDelphesEvents"] * componentRatePlots[0].splitFactor 

  if (numberOfDelphesEvents < 0) or (numberOfDelphesEvents > componentRatePlots[0].nGenEvents):
    numberOfDelphesEvents = componentRatePlots[0].nGenEvents

  print "OBTAINING THE RATE IN THE LINEAR SCALING APPROXIMATION"

  nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject +
                                    "_" + componentNameRatePlots + "_RatePlots_NotNormalised.root")
  totalRateHist = nonNormalisedRatePlotFile.Get(
      "mergedTotalSimL1TMuonRate")
  barrelRateHist = nonNormalisedRatePlotFile.Get("mergedBarrelSimL1TMuonRate")
  endcapRateHist = nonNormalisedRatePlotFile.Get("mergedEndcapSimL1TMuonRate")

  totalRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
  barrelRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
  endcapRateHist.Scale(interactionFrequency/numberOfDelphesEvents)

  totalRateHist.GetXaxis().SetTitle("p_{t}")
  totalRateHist.GetXaxis().SetRangeUser(5, 50)
  totalRateHist.GetYaxis().SetTitle("Rate [Hz]")
  barrelRateHist.GetXaxis().SetTitle("p_{t}")
  barrelRateHist.GetXaxis().SetRangeUser(5, 50)
  barrelRateHist.GetYaxis().SetTitle("Rate [Hz]")
  endcapRateHist.GetXaxis().SetTitle("p_{t}")
  endcapRateHist.GetXaxis().SetRangeUser(5, 50)
  endcapRateHist.GetYaxis().SetTitle("Rate [Hz]")

  normalisedRatePlotFile = TFile("" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_Normalised.root", "RECREATE")
  normalisedRatePlotFile.cd()
  totalRateHist.Write()
  barrelRateHist.Write()
  endcapRateHist.Write()
  normalisedRatePlotFile.Close()
  nonNormalisedRatePlotFile.Close()

  print "NORMALISING THE RATE PLOT TO OBTAIN THE TRIGGER PASS PROBABILITY FOR MINBIAS AND PU140 EVENTS"

  nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_NotNormalised.root")
  passProbabilityFile = TFile("" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_TriggerPassProbability.root", "RECREATE")
  totalRateHist = nonNormalisedRatePlotFile.Get(
      "mergedTotalSimL1TMuonRate")
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

  passProbabilityFile = TFile("" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_TriggerPassProbability.root")
  ppPassProbabilityHistogram = passProbabilityFile.Get("ppPassProbabilityHistogram")
  eventPassProbabilityHistogram = passProbabilityFile.Get("eventPassProbabilityHistogram")

  linearPURatePlot = ppPassProbabilityHistogram.Clone("linearPURatePlot")
  fullPURatePlot = ppPassProbabilityHistogram.Clone("fullPURatePlot")

  linearPURatePlot.Scale(interactionFrequency)
  fullPURatePlot.Scale(bunchCrossingFrequency)

  pileupRatePlotFile = TFile("" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_PU" + str(averagePileUp) + "RatePlot.root", "RECREATE")
  pileupRatePlotFile.cd()
  linearPURatePlot.Write()
  fullPURatePlot.Write()

  pileupRatePlotFile.Close()

def normalisePileUpRate(yamlConf):

  saveFolder=yamlConf["saveFolder"]
  genObject=yamlConf["genObject"]
  triggerObject=yamlConf["triggerObject"]
  print "CREATING THE NON-NORMALISED PLOTS"

  moduleNameRatePlots=yamlConf["moduleNameRatePlots"]
  componentNameRatePlots=yamlConf["componentNameRatePlots"]

  componentRatePlots=[getattr(import_module(
      moduleNameRatePlots), componentNameRatePlots, None)]

  if componentRatePlots[0] is None:
    print "Error:  component does not exist"
    raise ValueError('Component ' + componentNameRatePlots +
                     " has not been declared in module " + moduleNameRatePlots)

  numberOfDelphesEvents = -1
  if "numberOfDelphesEvents" in yamlConf:
    numberOfDelphesEvents = yamlConf["numberOfDelphesEvents"] * componentRatePlots[0].splitFactor 

  if (numberOfDelphesEvents < 0) or (numberOfDelphesEvents > componentRatePlots[0].nGenEvents):
    numberOfDelphesEvents = componentRatePlots[0].nGenEvents

  nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject +
                                    "_" + componentNameRatePlots + "_RatePlots_NotNormalised.root")
  totalRateHist = nonNormalisedRatePlotFile.Get(
      "mergedTotalSimL1TMuonRate")
  barrelRateHist = nonNormalisedRatePlotFile.Get("mergedBarrelSimL1TMuonRate")
  endcapRateHist = nonNormalisedRatePlotFile.Get(
      "mergedEndcapSimL1TMuonRate")

  totalRateHist.Scale(31.6e6/numberOfDelphesEvents)
  barrelRateHist.Scale(31.6e6/numberOfDelphesEvents)
  endcapRateHist.Scale(31.6e6/numberOfDelphesEvents)

  totalRateHist.GetXaxis().SetTitle("p_{t}")
  totalRateHist.GetXaxis().SetRangeUser(5, 50)
  totalRateHist.GetYaxis().SetTitle("Rate [Hz]")
  barrelRateHist.GetXaxis().SetTitle("p_{t}")
  barrelRateHist.GetXaxis().SetRangeUser(5, 50)
  barrelRateHist.GetYaxis().SetTitle("Rate [Hz]")
  endcapRateHist.GetXaxis().SetTitle("p_{t}")
  endcapRateHist.GetXaxis().SetRangeUser(5, 50)
  endcapRateHist.GetYaxis().SetTitle("Rate [Hz]")

  normalisedRatePlotFile = TFile("" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_Normalised.root", "RECREATE")
  normalisedRatePlotFile.cd()
  totalRateHist.Write()
  barrelRateHist.Write()
  endcapRateHist.Write()
  normalisedRatePlotFile.Close()
  nonNormalisedRatePlotFile.Close()



def runClosureTest1(yamlConf):

  #Taking the matched gen muons
  #Applying the quality selection on the corresponding l1tmu to get only the gen mu matched to a quality l1tmu
  #Applying the smearing without any probabilistic exclusion to see if resolution curve are accurate enough

  saveFolder=yamlConf["saveFolder"]
  genObject=yamlConf["genObject"]
  triggerObject=yamlConf["triggerObject"]

  moduleNameClosureTest1=yamlConf["moduleNameClosureTest1"]
  componentNameClosureTest1=yamlConf["componentNameClosureTest1"]

  componentClosureTest1=[getattr(import_module(
      moduleNameClosureTest1), componentNameClosureTest1, None)]

  if componentClosureTest1[0] is None:
    print "Error: component does not exist"
    raise ValueError('Component ' + componentNameClosureTest1 +
                     " has not been declared in module " + moduleNameClosureTest1)

  parser = create_parser()
  (options,args) = parser.parse_args()
  folderAndScriptName = [saveFolder, "muonTriggerRateEstimationWorkflow/plotTransverseMomentumDistributionForMuonClosureTest_FromMatchedPairs_cfg.py"]
  convolutionFileName = "" + saveFolder + "/binnedDistributions.root"
  options.components = split(componentClosureTest1)
  for component in options.components:
    component.splitFactor = 1

  options.extraOptions.append("convolutionFileName=" + convolutionFileName)
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("quality=" + str(yamlConf["qualityThreshold"]))
  options.extraOptions.append("minimumPtInBarrel=" + str(yamlConf["minimumPtToReachBarrel"]))
  options.extraOptions.append("minimumPtInEndcap=" + str(yamlConf["minimumPtToReachEndcap"]))
  options.extraOptions.append("detectorEta=" + str(yamlConf["detectorEta"]))
  options.extraOptions.append("barrelEta=" + str(yamlConf["barrelEta"]))
  options.extraOptions.append("triggerObjectName=" + yamlConf["triggerObject"])
  options.extraOptions.append("genObjectName=" + yamlConf["genObject"])
  options.extraOptions.append("deltaR2Matching=" + str(yamlConf["deltaR2Matching"]))
  #options.nevents=300000
  options.force = True
  loop = main(options, folderAndScriptName, parser)
  os.system("mv " + saveFolder + "/" + componentNameClosureTest1 + " " + saveFolder + "/" + componentNameClosureTest1 + "_ClosureTestPlots_QualityCutOnGenObject")
  cfg = lambda x: 1
  cfg.plots = [
  #  #Files here
    [saveFolder + "/" + componentNameClosureTest1 + "_ClosureTestPlots_QualityCutOnGenObject/histograms.root", "coarseBinnedPt" + triggerObject + "Distribution", "CMS " + triggerObject],
    [saveFolder + "/" + componentNameClosureTest1 + "_ClosureTestPlots_QualityCutOnGenObject/histograms.root", "coarseBinnedSmearedPt" + genObject + "Distribution", "Sim " + triggerObject + " from matched " + genObject],
  #  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtSimL1TMuonDistribution", "SimL1TMuon"],
  #  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtL1TMuonDistribution", "Original L1TMuon"],
  ]
  cfg.saveFileName = "" + saveFolder + "/closureTest1.root"
  
  plotDistributionComparisonPlot(cfg)


def runClosureTest2(yamlConf):

  ##We take every gen mu.
  ##We check if they fall into the detector
  ##If they do, we apply the probabilistic selection and the smearing

  saveFolder=yamlConf["saveFolder"]
  genObject=yamlConf["genObject"]
  triggerObject=yamlConf["triggerObject"]

  moduleNameClosureTest2=yamlConf["moduleNameClosureTest2"]
  moduleNameClosureTest1=yamlConf["moduleNameClosureTest1"]
  componentNameClosureTest2=yamlConf["componentNameClosureTest2"]
  componentNameClosureTest1=yamlConf["componentNameClosureTest1"]

  componentClosureTest2=[getattr(import_module(
      moduleNameClosureTest2), componentNameClosureTest2, None)]

  if componentClosureTest2[0] is None:
    print "Error: component does not exist"
    raise ValueError('Component ' + componentNameClosureTest2 +
                     " has not been declared in module " + moduleNameClosureTest2)

  parser = create_parser()
  (options,args) = parser.parse_args()
  folderAndScriptName = [saveFolder, "muonTriggerRateEstimationWorkflow/plotTransverseMomentumDistributionForMuonClosureTest_FromMatchedPairs_cfg.py"]
  convolutionFileName = "" + saveFolder + "/binnedDistributions.root"
  options.components = split(componentClosureTest2)
  for component in options.components:
    component.splitFactor = 1

  options.extraOptions.append("convolutionFileName=" + convolutionFileName)
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("quality=" + str(yamlConf["qualityThreshold"]))
  options.extraOptions.append("minimumPtInBarrel=" + str(yamlConf["minimumPtToReachBarrel"]))
  options.extraOptions.append("minimumPtInEndcap=" + str(yamlConf["minimumPtToReachEndcap"]))
  options.extraOptions.append("detectorEta=" + str(yamlConf["detectorEta"]))
  options.extraOptions.append("barrelEta=" + str(yamlConf["barrelEta"]))
  options.extraOptions.append("triggerObjectName=" + yamlConf["triggerObject"])
  options.extraOptions.append("genObjectName=" + yamlConf["genObject"])
  options.extraOptions.append("deltaR2Matching=" + str(yamlConf["deltaR2Matching"]))
  options.extraOptions.append("probabilityFile=" + "" + saveFolder + "/efficiencyFactors.root")
  options.extraOptions.append("probabilityHistogram=" + "efficiencyHistogram")
  #options.nevents=300000
  options.force = True
  loop = main(options, folderAndScriptName, parser)
  os.system("mv " + saveFolder + "/" + componentNameClosureTest2 + " " + saveFolder + "/" + componentNameClosureTest2 + "_ClosureTestPlots_AllGenMuons")
  
  cfg = lambda x: 1
  cfg.plots = [
  #  #Files here
    [saveFolder + "/" + componentNameClosureTest1 + "_ClosureTestPlots_QualityCutOnGenObject/histograms.root", "coarseBinnedPt" + triggerObject + "Distribution", "CMS " + triggerObject],
    [saveFolder + "/" + componentNameClosureTest2 + "_ClosureTestPlots_AllGenMuons/histograms.root",
     "coarseBinnedSmearedPt" + genObject + "Distribution", "Sim " + triggerObject + " from every " + genObject],
  #  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtSimL1TMuonDistribution", "SimL1TMuon"],
  #  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtL1TMuonDistribution", "Original L1TMuon"],
  ]
  cfg.saveFileName = "" + saveFolder + "/closureTest2.root"
  
  plotDistributionComparisonPlot(cfg)

def runCMSRateCalculation(yamlConf):
  print "CREATING THE ORIGINAL CMS RATE PLOT"

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]
  averagePileUp = yamlConf["averagePileUp"]
  bunchCrossingFrequency = yamlConf["bunchCrossingFrequency"]
  moduleNameRateClosureTest = yamlConf["moduleNameRateClosureTest"]
  componentNameRateClosureTest = yamlConf["componentNameRateClosureTest"]
  componentNameRatePlots = yamlConf["componentNameRatePlots"]

  componentRateClosureTest = [getattr(import_module(
      moduleNameRateClosureTest), componentNameRateClosureTest, None)]

  if componentRateClosureTest[0] is None:
    print "Error: component does not exist"
    raise ValueError('Component ' + componentNameRateClosureTest +
                     " has not been declared in module " + moduleNameRateClosureTest)
  
  parser = create_parser()
  (options,args) = parser.parse_args()
  folderAndScriptName = [saveFolder, "muonTriggerRateEstimationWorkflow/computeTriggerRatesCMSMuons_cfg.py"]
  #options.extraOptions.append("sample=" + sampleClosureTest3)
  options.components = split(componentRateClosureTest)
  for component in options.components:
    component.splitFactor = 1

  options.extraOptions.append("barrelEta=" + str(yamlConf["barrelEta"]))
  options.extraOptions.append("detectorEta=" + str(yamlConf["detectorEta"]))
  options.force = True

  #options.nevents=100
  loop = main(options, folderAndScriptName, parser)
  os.system("mv " + saveFolder + "/" + componentNameRateClosureTest +
            " " + saveFolder + "/" + componentNameRateClosureTest + "_CMSTriggerRate")
  
  cmsRatePlotFile = TFile("" + saveFolder + "/" + componentNameRateClosureTest +
                          "_CMSTriggerRate/ratePlots.root", "UPDATE")
  totalRateHist = cmsRatePlotFile.Get("triggerRate")
  barrelRateHist = cmsRatePlotFile.Get("barrelTriggerRate")
  endcapRateHist = cmsRatePlotFile.Get("endcapTriggerRate")
  totalRateHist.GetXaxis().SetTitle("p_{t}")
  totalRateHist.GetYaxis().SetTitle("Rate [Hz]")
  barrelRateHist.GetXaxis().SetTitle("p_{t}")
  barrelRateHist.GetYaxis().SetTitle("Rate [Hz]")
  endcapRateHist.GetXaxis().SetTitle("p_{t}")
  endcapRateHist.GetYaxis().SetTitle("Rate [Hz]")
  totalRateHist.Write()
  barrelRateHist.Write()
  endcapRateHist.Write()
  cmsRatePlotFile.Close()

def buildRateComparisonPlot(yamlConf):
  
  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]
  averagePileUp = yamlConf["averagePileUp"]
  bunchCrossingFrequency = yamlConf["bunchCrossingFrequency"]
  moduleNameRateClosureTest = yamlConf["moduleNameRateClosureTest"]
  componentNameRateClosureTest = yamlConf["componentNameRateClosureTest"]
  componentNameRatePlots = yamlConf["componentNameRatePlots"]

  print "CREATING RATIO PLOT FOR CMS VS DELPHES RATE"
  
  cfg = lambda x: 1
  cfg.plots = [
  #  #Files here
      ["" + saveFolder + "/" + componentNameRateClosureTest + \
       "_CMSTriggerRate/ratePlots.root", "triggerRate", "CMS " + triggerObject],
      ["" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_Normalised.root",
       "mergedTotalSimL1TMuonRate", "Sim " + triggerObject]
  ]
  cfg.saveFileName = "" + saveFolder + "/rateClosureTest.root"
  plotDistributionComparisonPlot(cfg)


#  ["" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_Normalised.root", "simL1TMuonTriggerRate", "Sim L1TMuon"]
#]
#cfg.saveFileName = "" + saveFolder + "/rateClosureTest.root"
#plotDistributionComparisonPlot(cfg)


if __name__ == "__main__":

  parser = create_parser()

  options, other = parser.parse_args()

  # Getting the config file from the hreppy extra options
  for opt in options.extraOptions:
        if "=" in opt:
            (key, val) = opt.split("=", 1)
            if key == "ConfigFile":
              configFile = val

  parameters = yaml.load(file(configFile, 'r'))
  saveFolder = parameters["saveFolder"]

  os.system("mkdir -p " + saveFolder)

  steps = parameters["steps"]
  for step in steps:
    moduleName = step["module"]
    functionName = step["function"]
    print ">>>>> Executing", functionName, "..."
    try:
      function = getattr(import_module(moduleName), functionName)
    except AttributeError:
      print ">>>>> Error: can not find function", functionName, "in module", moduleName
      exit()
    function(parameters)
