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
from heppy.framework.config import split

###################################################################################################
#################################### DO NOT TOUCH FROM DOWN ON ####################################
###################################################################################################

#if os.listdir(saveFolder):
#  print "Save directory is not empty. It will be cleaned. Continue?"
#  if raw_input() == "y":
#    os.system("rm -r " + saveFolder + "/*")
#  else:
#    print "Stopping process."
#    exit()
#
# 

def computeConvolutionCurves(yamlConf):

  print "--- COMPUTING CONVOLUTION CURVES ---"

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]

  moduleNameConvolutionCurves = yamlConf["moduleNameConvolutionCurves"]
  componentNameConvolutionCurves = yamlConf["componentNameConvolutionCurves"]

  componentConvolutionCurves = [getattr(import_module(
      moduleNameConvolutionCurves), componentNameConvolutionCurves, None)]
  
  if componentConvolutionCurves[0] is None:
    print "Error:  component does not exist"
    raise ValueError('Component ' + componentNameConvolutionCurves +
                     " has not been declared in module " + moduleNameConvolutionCurves)

  parser = create_parser()
  (options,args) = parser.parse_args()
  folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/binnedDistributionsCMS_cfg.py"]
  options.components = split(componentConvolutionCurves)
  for component in options.components:
    component.splitFactor = 1

  #options.extraOptions.append("sample=" + yamlConf["sampleBinnedDistributions"])
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("quality=" + str(yamlConf["qualityThreshold"]))
  options.extraOptions.append("minimumPtInBarrel=" + str(yamlConf["minimumPtToReachBarrel"]))
  options.extraOptions.append("minimumPtInEndcap=" + str(yamlConf["minimumPtToReachEndcap"]))
  options.extraOptions.append("minimumPtInForward=" + str(yamlConf["minimumPtToReachForward"]))
  options.extraOptions.append("barrelEta=" + str(yamlConf["barrelEta"]))
  options.extraOptions.append("endcapEta=" + str(yamlConf["endcapEta"]))
  options.extraOptions.append("detectorEta=" + str(yamlConf["detectorEta"]))
  options.extraOptions.append("triggerObjectName=" + yamlConf["triggerObject"])
  options.extraOptions.append("genObjectName=" + yamlConf["genObject"])
  options.extraOptions.append("deltaR2Matching=" + str(yamlConf["deltaR2Matching"]))
  if "numberOfEventsConvolutionCurves" in yamlConf:
    options.nevents = yamlConf["numberOfEventsConvolutionCurves"]
  options.force = True
  loop = main(options, folderAndScriptName, parser)
  os.system("rm -r " + saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves")
  if componentConvolutionCurves[0].splitFactor > 1:
    os.system("mkdir " + saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves")
    os.system("hadd " + saveFolder + "/" + genObject + "_" + triggerObject + "_" + "convolutionCurves/histograms.root " +
              saveFolder + "/" + componentNameConvolutionCurves + "_Chunk*/histograms.root")
  else:
    os.system("mv " + saveFolder + "/" + componentNameConvolutionCurves + " " +
    saveFolder + "/" + genObject + "_" + triggerObject + "_" + "convolutionCurves")


def obtainEfficiencies(yamlConf):

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]
  binningArray = array("f", ast.literal_eval(yamlConf["binning"]))
  print "--- COMPUTING THE CONVERSION FACTORS/EFFICIENCIES ---"

  numberOfMatchedObjects, numberOfGenObjects = computeEfficiencies(
                                                                    GenObjTree = yamlConf["efficiencyGenTree"],
                                                                    GenObjFileFolder = yamlConf["efficiencySourceFolder"],
                                                                    MatchTree = yamlConf["efficiencyMatchTree"],
                                                                    MatchFileFolder = yamlConf["efficiencySourceFolder"],
                                                                    binning = yamlConf["binning"],
                                                                    eta = yamlConf["detectorEta"],
                                                                    quality = yamlConf["qualityThreshold"],
                                                                    barrelEta = yamlConf["barrelEta"],
                                                                    endcapEta = yamlConf["endcapEta"],
                                                                    minPtInBarrel = yamlConf["minimumPtToReachBarrel"],
                                                                    minPtInEndcap = yamlConf["minimumPtToReachEndcap"],
                                                                    minPtInForward = yamlConf["minimumPtToReachForward"],
                                                                    deltaR2Matching = yamlConf["deltaR2Matching"],
                                                                    numberOfFiles = yamlConf["numberOfEfficiencyFiles"]
                                                                  )

  numberOfMatchedObjects = numberOfMatchedObjects
  numberOfGenObjects = numberOfGenObjects

  efficiencyFactors = numberOfMatchedObjects/numberOfGenObjects
  for binIdx in xrange(0, len(efficiencyFactors)): 
    efficiencyFactors[binIdx] = 0 if isnan(efficiencyFactors[binIdx]) else efficiencyFactors[binIdx]
    if efficiencyFactors[binIdx] > 1:
      efficiencyFactors[binIdx] = 1
  print efficiencyFactors

  efficiencyFactorsFile = TFile("" + saveFolder + "/efficiencyFactors.root", "RECREATE")
  efficiencyFactorsFile.cd()
  efficiencyHistogram = TH1F("efficiencyHistogram", "Trigger efficiency", len(binningArray)-1, binningArray)
  numberOfMatchedObjectsHistogram = TH1F("numberOfMatchedObjectsHistogram", "numberOfMatchedObjectsHistogram", len(binningArray)-1, binningArray)
  numberOfGenObjectsHistogram = TH1F("numberOfGenObjectsHistogram", "numberOfGenObjectsHistogram", len(binningArray)-1, binningArray)

  for x in xrange(0, len(efficiencyFactors)): 
    #Excluding overflow bin
    if x != len(efficiencyFactors) - 1:
      efficiencyHistogram.SetBinContent(x + 1, efficiencyFactors[x])
      numberOfMatchedObjectsHistogram.SetBinContent(x + 1, numberOfMatchedObjects[x])
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
  (options,args) = parser.parse_args()
  folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/l1tObjectTriggerRateMinBiasFromJets_cfg.py"]
  convolutionFileName = saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves/histograms.root"
  options.components = split(componentRatePlots)
  for component in options.components:
    component.splitFactor = 1

  # Getting the job index from the heppy extra options
  if "job" in yamlConf:
    job = int(yamlConf["job"])
  else:
    job = None

  if job is not None: 
    options.components = [options.components[job]]

  #options.extraOptions.append("sample=" + yamlConf["sampleRateEstimation"])
  options.extraOptions.append("convolutionFileName=" + convolutionFileName)
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("probabilityFile=" + "" + yamlConf["saveFolder"] + "/efficiencyFactors.root")
  options.extraOptions.append("probabilityHistogram=efficiencyHistogram")
  options.extraOptions.append("minimumPtInBarrel=" + str(yamlConf["minimumPtToReachBarrel"]))
  options.extraOptions.append("minimumPtInEndcap=" + str(yamlConf["minimumPtToReachEndcap"]))
  options.extraOptions.append("minimumPtInForward=" + str(yamlConf["minimumPtToReachForward"]))
  options.extraOptions.append("barrelEta=" + str(yamlConf["barrelEta"]))
  options.extraOptions.append("endcapEta=" + str(yamlConf["endcapEta"]))
  options.extraOptions.append("detectorEta=" + str(yamlConf["detectorEta"]))
  options.extraOptions.append("triggerObjectName=" + str(yamlConf["triggerObject"]))
  options.extraOptions.append(
      "genJetCollection=" + str(yamlConf["genJetCollection"]))
  if "momentumShift" in yamlConf:
    options.extraOptions.append(
        "momentumShift=" + str(yamlConf["momentumShift"]))
  else:
    options.extraOptions.append(
        "momentumShift=0")
  if "usePtTransformer" in yamlConf:
    options.extraOptions.append(
        "usePtTransformer=" + str(yamlConf["usePtTransformer"]))
  else:
    options.extraOptions.append(
        "usePtTransformer=False")
  
  if "useOnlyLeadingGenJet" in yamlConf:
    options.extraOptions.append(
        "useOnlyLeadingGenJet=" + str(yamlConf["useOnlyLeadingGenJet"]))
  else:
    options.extraOptions.append(
        "useOnlyLeadingGenJet=False")
  options.force = True

  if "numberOfDelphesEvents" in yamlConf:
    options.nevents = yamlConf["numberOfDelphesEvents"]

  loop = main(options, folderAndScriptName, parser)

def mergeNonNormalisedRatePlots(yamlConf):

  print "MERGING LOCAL HEPPY CHUNKS"
  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]

  moduleNameRatePlots = yamlConf["moduleNameRatePlots"]
  componentNameRatePlots = yamlConf["componentNameRatePlots"]

  #Merging the histograms and trees
  filesToMerge = glob(saveFolder + "/" + componentNameRatePlots + "*/ratePlots.root")
  
  nonNormalisedRatePlotFile = TFile(filesToMerge[0])
  totalRateHist = nonNormalisedRatePlotFile.Get("simL1TObjectTriggerRate")
  barrelRateHist = nonNormalisedRatePlotFile.Get("barrelSimL1TObjectRate")
  endcapRateHist = nonNormalisedRatePlotFile.Get("endcapSimL1TObjectRate")
  forwardRateHist = nonNormalisedRatePlotFile.Get("forwardSimL1TObjectRate")
  mergedTotalRateHist = totalRateHist.Clone("mergedTotalSimL1TObjectTriggerRate")
  mergedBarrelRateHist = barrelRateHist.Clone("mergedBarrelSimL1TObjectRate")
  mergedEndcapRateHist = endcapRateHist.Clone("mergedEndcapSimL1TObjectRate")
  mergedForwardRateHist = forwardRateHist.Clone("mergedForwardSimL1TObjectRate")
  mergedTotalRateHist.SetDirectory(0)
  mergedBarrelRateHist.SetDirectory(0)
  mergedEndcapRateHist.SetDirectory(0)
  mergedForwardRateHist.SetDirectory(0)
  
  
  treeChain = TChain("genJetSimL1TObjectTree")
  treeChain.Add(filesToMerge[0])
  nonNormalisedRatePlotFile.Close()
  # First file has been handled, so it is removed from the list
  filesToMerge.pop(0)
  #Merging the others
  for fileName in filesToMerge:
    nonNormalisedRatePlotFile = TFile(fileName)
    totalRateHist = nonNormalisedRatePlotFile.Get("simL1TObjectTriggerRate")
    barrelRateHist = nonNormalisedRatePlotFile.Get("barrelSimL1TObjectRate")
    endcapRateHist = nonNormalisedRatePlotFile.Get("endcapSimL1TObjectRate")
    forwardRateHist = nonNormalisedRatePlotFile.Get("forwardSimL1TObjectRate")
    treeChain.Add(fileName)
    mergedTotalRateHist.Add(totalRateHist)
    mergedBarrelRateHist.Add(barrelRateHist)
    mergedEndcapRateHist.Add(endcapRateHist)
    mergedForwardRateHist.Add(forwardRateHist)
    nonNormalisedRatePlotFile.Close()
  
  treeChain.Merge(saveFolder + "/" + genObject + "_" + triggerObject + "_" + componentNameRatePlots + "_" + genObject + "_Sim" + triggerObject + "_Tree.root")
  
  #Saving everything
  mergedHistogramsFile = TFile(saveFolder + "/" + genObject + "_" + triggerObject + "_" + componentNameRatePlots + "_RatePlots_NotNormalised.root", "RECREATE")
  mergedHistogramsFile.cd()
  mergedTotalRateHist.SetDirectory(mergedHistogramsFile)
  mergedBarrelRateHist.SetDirectory(mergedHistogramsFile)
  mergedEndcapRateHist.SetDirectory(mergedHistogramsFile)
  mergedForwardRateHist.SetDirectory(mergedHistogramsFile)
  mergedTotalRateHist.Write()
  mergedBarrelRateHist.Write()
  mergedEndcapRateHist.Write()
  mergedForwardRateHist.Write()
  mergedHistogramsFile.Close()


def normaliseRatePlots(yamlConf):
  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]

  moduleNameRatePlots = yamlConf["moduleNameRatePlots"]
  componentNameRatePlots = yamlConf["componentNameRatePlots"]

  componentRatePlots = [getattr(import_module(
      moduleNameRatePlots), componentNameRatePlots, None)]

  if componentRatePlots[0] is None:
    print "Error:  component does not exist"
    raise ValueError('Component ' + componentNameRatePlots +
                     " has not been declared in module " + moduleNameRatePlots)

  print "OBTAINING THE RATE IN THE LINEAR SCALING APPROXIMATION"

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]
  moduleNameRatePlots = yamlConf["moduleNameRatePlots"]
  componentNameRatePlots = yamlConf["componentNameRatePlots"]
  averagePileUp = yamlConf["averagePileUp"]
  bunchCrossingFrequency = yamlConf["bunchCrossingFrequency"]
  interactionFrequency = averagePileUp * bunchCrossingFrequency
  
  if "numberOfDelphesEvents" in yamlConf:
    numberOfDelphesEvents = yamlConf["numberOfDelphesEvents"]
  else:
    componentRatePlots = [getattr(import_module(
      moduleNameRatePlots), componentNameRatePlots, None)]
    numberOfDelphesEvents = componentRatePlots[0].nGenEvents
  
  
  nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + componentNameRatePlots + "_RatePlots_NotNormalised.root")
  totalRateHist = nonNormalisedRatePlotFile.Get("mergedTotalSimL1TObjectTriggerRate")
  barrelRateHist = nonNormalisedRatePlotFile.Get("mergedBarrelSimL1TObjectRate")
  endcapRateHist = nonNormalisedRatePlotFile.Get("mergedEndcapSimL1TObjectRate")
  forwardRateHist = nonNormalisedRatePlotFile.Get("mergedForwardSimL1TObjectRate")
  
  totalRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
  barrelRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
  endcapRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
  forwardRateHist.Scale(interactionFrequency/numberOfDelphesEvents)
  
  totalRateHist.GetXaxis().SetTitle("p_{t}")
  totalRateHist.GetXaxis().SetRangeUser(5, 200)
  totalRateHist.GetYaxis().SetTitle("Rate [Hz]")
  barrelRateHist.GetXaxis().SetTitle("p_{t}")
  barrelRateHist.GetXaxis().SetRangeUser(5, 200)
  barrelRateHist.GetYaxis().SetTitle("Rate [Hz]")
  endcapRateHist.GetXaxis().SetTitle("p_{t}")
  endcapRateHist.GetXaxis().SetRangeUser(5, 200)
  endcapRateHist.GetYaxis().SetTitle("Rate [Hz]")
  forwardRateHist.GetXaxis().SetTitle("p_{t}")
  forwardRateHist.GetXaxis().SetRangeUser(5, 200)
  forwardRateHist.GetYaxis().SetTitle("Rate [Hz]")
  
  normalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + componentNameRatePlots + "_RatePlots_Normalised.root", "RECREATE")
  normalisedRatePlotFile.cd()
  totalRateHist.Write()
  barrelRateHist.Write()
  endcapRateHist.Write()
  forwardRateHist.Write()
  normalisedRatePlotFile.Close()
  nonNormalisedRatePlotFile.Close()
  
  print "NORMALISING THE RATE PLOT TO OBTAIN THE TRIGGER PASS PROBABILITY FOR MINBIAS AND PU140 EVENTS"
  
  nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + componentNameRatePlots + "_RatePlots_NotNormalised.root")
  passProbabilityFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + componentNameRatePlots + "_RatePlots_TriggerPassProbability.root", "RECREATE")
  totalRateHist = nonNormalisedRatePlotFile.Get("mergedTotalSimL1TObjectTriggerRate")
  barrelRateHist = nonNormalisedRatePlotFile.Get("mergedBarrelSimL1TObjectRate")
  endcapRateHist = nonNormalisedRatePlotFile.Get("mergedEndcapSimL1TObjectRate")
  forwardRateHist = nonNormalisedRatePlotFile.Get("mergedForwardSimL1TObjectRate")
  ppPassProbabilityHistogram = totalRateHist.Clone("ppPassProbabilityHistogram")
  ppPassProbabilityHistogramInBarrel = totalRateHist.Clone("ppPassProbabilityHistogramInBarrel")
  ppPassProbabilityHistogramInEndcap = totalRateHist.Clone("ppPassProbabilityHistogramInEndcap")
  ppPassProbabilityHistogramInForward = totalRateHist.Clone("ppPassProbabilityHistogramInForward")
  ppPassProbabilityHistogram.Scale(1./numberOfDelphesEvents)
  ppPassProbabilityHistogramInBarrel.Scale(1./numberOfDelphesEvents)
  ppPassProbabilityHistogramInEndcap.Scale(1./numberOfDelphesEvents)
  ppPassProbabilityHistogramInForward.Scale(1./numberOfDelphesEvents)
  passProbabilityFile.cd()
  eventPassProbabilityHistogram = ppPassProbabilityHistogram.Clone("eventPassProbabilityHistogram")
  eventPassProbabilityHistogramInBarrel = ppPassProbabilityHistogramInBarrel.Clone("eventPassProbabilityHistogramInBarrel")
  eventPassProbabilityHistogramInEndcap = ppPassProbabilityHistogramInEndcap.Clone("eventPassProbabilityHistogramInEndcap")
  eventPassProbabilityHistogramInForward = ppPassProbabilityHistogramInForward.Clone("eventPassProbabilityHistogramInForward")
  
  for x in xrange(1, eventPassProbabilityHistogram.GetNbinsX()+1):
    ppPassProbability = ppPassProbabilityHistogram.GetBinContent(x)
    ppPassProbabilityInBarrel = ppPassProbabilityHistogramInBarrel.GetBinContent(x)
    ppPassProbabilityInEndcap = ppPassProbabilityHistogramInEndcap.GetBinContent(x)
    ppPassProbabilityInForward = ppPassProbabilityHistogramInForward.GetBinContent(x)
    eventPassProbability = 1. - (1. - ppPassProbability)**averagePileUp
    eventPassProbabilityInBarrel = 1. - (1. - ppPassProbabilityInBarrel)**averagePileUp
    eventPassProbabilityInEndcap = 1. - (1. - ppPassProbabilityInEndcap)**averagePileUp
    eventPassProbabilityInForward = 1. - (1. - ppPassProbabilityInForward)**averagePileUp
    eventPassProbabilityHistogram.SetBinContent(x, eventPassProbability)
    eventPassProbabilityHistogramInBarrel.SetBinContent(x, eventPassProbabilityInBarrel)
    eventPassProbabilityHistogramInEndcap.SetBinContent(x, eventPassProbabilityInEndcap)
    eventPassProbabilityHistogramInForward.SetBinContent(x, eventPassProbabilityInForward)
  
  probabilityRatioHistogram = eventPassProbabilityHistogram.Clone("probabilityRatioHistogram")
  probabilityRatioHistogram.Divide(ppPassProbabilityHistogram)
  probabilityRatioHistogramInBarrel = eventPassProbabilityHistogramInBarrel.Clone("probabilityRatioHistogramInBarrel")
  probabilityRatioHistogramInBarrel.Divide(ppPassProbabilityHistogramInBarrel)
  probabilityRatioHistogramInEndcap = eventPassProbabilityHistogramInEndcap.Clone("probabilityRatioHistogramInEndcap")
  probabilityRatioHistogramInEndcap.Divide(ppPassProbabilityHistogramInEndcap)
  probabilityRatioHistogramInForward = eventPassProbabilityHistogramInForward.Clone("probabilityRatioHistogramInForward")
  probabilityRatioHistogramInForward.Divide(ppPassProbabilityHistogramInForward)
  
  probabilityRatioHistogram.Write()
  probabilityRatioHistogramInBarrel.Write()
  probabilityRatioHistogramInEndcap.Write()
  probabilityRatioHistogramInForward.Write()
  ppPassProbabilityHistogram.Write()
  ppPassProbabilityHistogramInBarrel.Write()
  ppPassProbabilityHistogramInEndcap.Write()
  ppPassProbabilityHistogramInForward.Write()
  eventPassProbabilityHistogram.Write()
  eventPassProbabilityHistogramInBarrel.Write()
  eventPassProbabilityHistogramInEndcap.Write()
  eventPassProbabilityHistogramInForward.Write()
  
  nonNormalisedRatePlotFile.Close()
  passProbabilityFile.Close()
  
  print "COMPUTING THE TRIGGER PASS PROBABILITY IN LINEAR SCALING APPROXIMATION AND WITH FULL FORMULA"
  
  passProbabilityFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + componentNameRatePlots + "_RatePlots_TriggerPassProbability.root")
  ppPassProbabilityHistogram = passProbabilityFile.Get("ppPassProbabilityHistogram")
  ppPassProbabilityHistogramInBarrel = passProbabilityFile.Get("ppPassProbabilityHistogramInBarrel")
  ppPassProbabilityHistogramInEndcap = passProbabilityFile.Get("ppPassProbabilityHistogramInEndcap")
  ppPassProbabilityHistogramInForward = passProbabilityFile.Get("ppPassProbabilityHistogramInForward")
  eventPassProbabilityHistogram = passProbabilityFile.Get("eventPassProbabilityHistogram")
  eventPassProbabilityHistogramInBarrel = passProbabilityFile.Get("eventPassProbabilityHistogramInBarrel")
  eventPassProbabilityHistogramInEndcap = passProbabilityFile.Get("eventPassProbabilityHistogramInEndcap")
  eventPassProbabilityHistogramInForward = passProbabilityFile.Get("eventPassProbabilityHistogramInForward")
  
  linearPURatePlot = ppPassProbabilityHistogram.Clone("linearPURatePlot")
  linearPURatePlotInBarrel = ppPassProbabilityHistogramInBarrel.Clone("linearPURatePlotInBarrel")
  linearPURatePlotInEndcap = ppPassProbabilityHistogramInEndcap.Clone("linearPURatePlotInEndcap")
  linearPURatePlotInForward = ppPassProbabilityHistogramInForward.Clone("linearPURatePlotInForward")
  fullPURatePlot = eventPassProbabilityHistogram.Clone("fullPURatePlot")
  fullPURatePlotInBarrel = eventPassProbabilityHistogramInBarrel.Clone("fullPURatePlotInBarrel")
  fullPURatePlotInEndcap = eventPassProbabilityHistogramInEndcap.Clone("fullPURatePlotInEndcap")
  fullPURatePlotInForward = eventPassProbabilityHistogramInForward.Clone("fullPURatePlotInForward")
  
  linearPURatePlot.Scale(interactionFrequency)
  linearPURatePlotInBarrel.Scale(interactionFrequency)
  linearPURatePlotInEndcap.Scale(interactionFrequency)
  linearPURatePlotInForward.Scale(interactionFrequency)
  fullPURatePlot.Scale(bunchCrossingFrequency)
  fullPURatePlotInBarrel.Scale(bunchCrossingFrequency)
  fullPURatePlotInEndcap.Scale(bunchCrossingFrequency)
  fullPURatePlotInForward.Scale(bunchCrossingFrequency)
  
  pileupRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + componentNameRatePlots + "_RatePlots_PU" + str(averagePileUp) + "RatePlot.root", "RECREATE")
  pileupRatePlotFile.cd()
  
  linearPURatePlot.Write()
  linearPURatePlotInBarrel.Write()
  linearPURatePlotInEndcap.Write()
  linearPURatePlotInForward.Write()
  fullPURatePlot.Write()
  fullPURatePlotInBarrel.Write()
  fullPURatePlotInEndcap.Write()
  fullPURatePlotInForward.Write()
  
  pileupRatePlotFile.Close()


def runClosureTest1(yamlConf):

  print "CREATING THE MOMENTUM DISTRIBUTION PLOTS FOR MATCHED CMS GEN JET TO SIML1TOBJECT"
  #Taking the matched gen muons
  #Applying the quality selection on the corresponding l1tmu to get only the gen mu matched to a quality l1tmu
  #Applying the smearing without any probabilistic exclusion to see if resolution curve are accurate enough

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]
  
  moduleNameClosureTest1 = yamlConf["moduleNameClosureTest1"]
  componentNameClosureTest1 = yamlConf["componentNameClosureTest1"]

  componentClosureTest1 = [getattr(import_module(
      moduleNameClosureTest1), componentNameClosureTest1, None)]

  if componentClosureTest1[0] is None:
    print "Error: component does not exist"
    raise ValueError('Component ' + componentNameClosureTest1 +
                     " has not been declared in module " + moduleNameClosureTest1)

  parser = create_parser()
  (options,args) = parser.parse_args()
  folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/plotTransverseMomentumDistributionForClosureTest_cfg.py"]
  convolutionFileName = saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves/histograms.root"
  #options.extraOptions.append("sample=" + yamlConf["sampleClosureTest1"])
  options.components = split(componentClosureTest1)
  for component in options.components:
    component.splitFactor = 1

  options.extraOptions.append("convolutionFileName=" + convolutionFileName)
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("quality=" + str(yamlConf["qualityThreshold"]))
  options.extraOptions.append("minimumPtInBarrel=" + str(yamlConf["minimumPtToReachBarrel"]))
  options.extraOptions.append("minimumPtInEndcap=" + str(yamlConf["minimumPtToReachEndcap"]))
  options.extraOptions.append("minimumPtInForward=" + str(yamlConf["minimumPtToReachForward"]))
  options.extraOptions.append("detectorEta=" + str(yamlConf["detectorEta"]))
  options.extraOptions.append("barrelEta=" + str(yamlConf["barrelEta"]))
  options.extraOptions.append("endcapEta=" + str(yamlConf["endcapEta"]))
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
    [saveFolder + "/" + componentNameClosureTest1 + "_ClosureTestPlots_QualityCutOnGenObject/histograms.root", "coarseBinnedSmearedPt" + genObject + "Distribution", "Sim " + triggerObject + " from matched " + genObject]
  #  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtSimL1TMuonDistribution", "SimL1TMuon"],
  #  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtL1TMuonDistribution", "Original L1TMuon"],
  ]
  cfg.saveFileName = "" + saveFolder + "/closureTest1.root"
  
  plotDistributionComparisonPlot(cfg)
  
def runClosureTest2(yamlConf):

  print "CREATING THE MOMENTUM DISTRIBUTION PLOTS FOR CMS GEN JET TO SIML1TOBJECT (EVERY GEN JET IS CONSIDERED)"

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]

  moduleNameClosureTest1 = yamlConf["moduleNameClosureTest1"]
  moduleNameClosureTest2 = yamlConf["moduleNameClosureTest2"]
  componentNameClosureTest1 = yamlConf["componentNameClosureTest1"]
  componentNameClosureTest2 = yamlConf["componentNameClosureTest2"]

  componentClosureTest2 = [getattr(import_module(
      moduleNameClosureTest2), componentNameClosureTest2, None)]

  if componentClosureTest2[0] is None:
    print "Error: component does not exist"
    raise ValueError('Component ' + componentNameClosureTest2 +
                     " has not been declared in module " + moduleNameClosureTest2)

  #We take every gen mu.
  #We check if they fall into the detector
  #If they do, we apply the probabilistic selection and the smearing

  parser = create_parser()
  (options,args) = parser.parse_args()
  folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/plotTransverseMomentumDistributionForClosureTest_cfg.py"]
  convolutionFileName = saveFolder + "/" + genObject + "_" +  triggerObject + "_" + "convolutionCurves/histograms.root"
  #options.extraOptions.append("sample=" + sampleClosureTest2)
  options.components = split(componentClosureTest2)
  for component in options.components:
    component.splitFactor = 1

  options.extraOptions.append("convolutionFileName=" + convolutionFileName)
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("minimumPtInBarrel=" + str(yamlConf["minimumPtToReachBarrel"]))
  options.extraOptions.append("minimumPtInEndcap=" + str(yamlConf["minimumPtToReachEndcap"]))
  options.extraOptions.append("minimumPtInForward=" + str(yamlConf["minimumPtToReachForward"]))
  options.extraOptions.append("detectorEta=" + str(yamlConf["detectorEta"]))
  options.extraOptions.append("barrelEta=" + str(yamlConf["barrelEta"]))
  options.extraOptions.append("endcapEta=" + str(yamlConf["endcapEta"]))
  options.extraOptions.append("probabilityFile=" + "" + yamlConf["saveFolder"] + "/efficiencyFactors.root")
  options.extraOptions.append("probabilityHistogram=" + "efficiencyHistogram")
  options.extraOptions.append("quality=" + str(yamlConf["qualityThreshold"]))
  options.extraOptions.append("triggerObjectName=" + yamlConf["triggerObject"])
  options.extraOptions.append("genObjectName=" + yamlConf["genObject"])
  options.extraOptions.append("deltaR2Matching=" + str(yamlConf["deltaR2Matching"]))
  #options.nevents=300000
  options.force = True
  loop = main(options, folderAndScriptName, parser)
  os.system("mv " + saveFolder + "/" + componentNameClosureTest2 + " " +
            saveFolder + "/" + componentNameClosureTest2 + "_ClosureTestPlots_AllGenObjects")

  print "CREATING THE COMPARISON PLOTS"

  #
  cfg = lambda x: 1
  cfg.plots = [
  #  #Files here
      [saveFolder + "/" + componentNameClosureTest1 + "_ClosureTestPlots_QualityCutOnGenObject/histograms.root",
       "coarseBinnedPt" + triggerObject + "Distribution", "CMS " + triggerObject],
    [saveFolder + "/" + componentNameClosureTest2 + "_ClosureTestPlots_AllGenObjects/histograms.root",
     "coarseBinnedSmearedPt" + genObject + "Distribution", "Sim " + triggerObject + " from every " + genObject]
  #  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtSimL1TMuonDistribution", "SimL1TMuon"],
  #  ["_closureTest/l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtL1TMuonDistribution", "Original L1TMuon"],
  ]
  cfg.saveFileName = "" + saveFolder + "/closureTest2.root"

  plotDistributionComparisonPlot(cfg)
  

def runRateClosureTest(yamlConf):
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
  folderAndScriptName = [saveFolder, "genObjectToL1TObjectConvolutionCurves/computeTriggerRatesFromCMS_cfg.py"]
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
    ["" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + componentNameRatePlots + \
     "_RatePlots_PU" + str(averagePileUp) + "RatePlot.root", "fullPURatePlot", "Sim " + triggerObject]
  ]
  cfg.saveFileName = "" + saveFolder + "/rateClosureTest.root"
  plotDistributionComparisonPlot(cfg)


def buildRateComparisonPlotFromHDFS(yamlConf):
  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]
  averagePileUp = yamlConf["averagePileUp"]
  bunchCrossingFrequency = yamlConf["bunchCrossingFrequency"]
  moduleNameRateClosureTest = yamlConf["moduleNameRateClosureTest"]
  componentNameRateClosureTest = yamlConf["componentNameRateClosureTest"]
  componentNameRatePlots = yamlConf["componentNameRatePlots"]

  print "CREATING RATIO PLOT FOR CMS VS DELPHES RATE"

  def cfg(x): return 1
  cfg.plots = [
      #  #Files here
      ["/hdfs/FCC-hh/" + componentNameRateClosureTest + \
       "_CMSTriggerRate/ratePlots.root",
       "triggerRate", "CMS " + triggerObject],
      ["" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + componentNameRatePlots + \
          "_RatePlots_PU" + str(averagePileUp) + "RatePlot.root", "fullPURatePlot", "Sim " + triggerObject]
  ]
  cfg.saveFileName = "" + saveFolder + "/rateClosureTest.root"
  plotDistributionComparisonPlot(cfg)
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
