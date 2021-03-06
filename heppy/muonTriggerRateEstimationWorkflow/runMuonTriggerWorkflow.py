#!/usr/bin/env python

from heppy.framework.heppy_loop import * 
from heppy.muonTriggerRateEstimationWorkflow.computeEfficiencies import computeEfficiencies
from heppy.genObjectToL1TObjectConvolutionCurves.computeEfficiencies import computeEfficiencies as computeEfficienciesJetToMuon
from ROOT import TH1F
from ROOT import TFile
from ROOT import TChain
from ROOT import TGraphErrors
import os
from array import array
import ast
from heppy.myScripts.plotDistributionComparisonPlot import plotDistributionComparisonPlot
from math import isnan, sqrt
import yaml
from importlib import import_module
from glob import glob

############################fullPURatePlotErrorsfullPURatePlotErrors#######################################################################
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
      saveFolder, "heppy/muonTriggerRateEstimationWorkflow/binnedDistributionsCMS_L1TMuon_cfg.py"]
  options.components = split(componentConvolutionCurvesHighPt)
  for component in options.components:
    component.splitFactor = 1

  if "minimumPtToReachBarrelConvolutionCurve" in yamlConf:
    minimumPtToReachBarrel = yamlConf["minimumPtToReachBarrelConvolutionCurve"]
  else:
    minimumPtToReachBarrel = yamlConf["minimumPtToReachBarrel"]
  if "minimumPtToReachEndcapConvolutionCurve" in yamlConf:
    minimumPtToReachEndcap = yamlConf["minimumPtToReachEndcapConvolutionCurve"]
  else:
    minimumPtToReachEndcap = yamlConf["minimumPtToReachEndcap"]
  if "barrelEtaConvolutionCurve" in yamlConf:
    barrelEta = yamlConf["barrelEtaConvolutionCurve"]
  else:
    barrelEta = yamlConf["barrelEta"]
  if "detectorEtaConvolutionCurve" in yamlConf:
    detectorEta = yamlConf["detectorEtaConvolutionCurve"]
  else:
    detectorEta = yamlConf["detectorEta"]

  #options.extraOptions.append("sample=" + yamlConf["sampleBinnedDistributions"])
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("quality=" + str(yamlConf["qualityThreshold"]))
  options.extraOptions.append(
      "minimumPtInBarrel=" + str(minimumPtToReachBarrel))
  options.extraOptions.append(
      "minimumPtInEndcap=" + str(minimumPtToReachEndcap))
  options.extraOptions.append("barrelEta=" + str(barrelEta))
  options.extraOptions.append("detectorEta=" + str(detectorEta))
  options.extraOptions.append("triggerObjectName=" + yamlConf["triggerObject"])
  options.extraOptions.append("genObjectName=" + yamlConf["genObject"])
  options.extraOptions.append(
      "deltaR2Matching=" + str(yamlConf["deltaR2Matching"]))
  options.extraOptions.append(
      "deltaEtaMatching=" + str(yamlConf["deltaEtaMatching"]))
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
      saveFolder, "heppy/muonTriggerRateEstimationWorkflow/binnedDistributionsCMS_L1TMuon_cfg.py"]
  options.components = split(componentConvolutionCurvesLowPt)
  for component in options.components:
    component.splitFactor = 1


  if "minimumPtToReachBarrelConvolutionCurve" in yamlConf:
    minimumPtToReachBarrel = yamlConf["minimumPtToReachBarrelConvolutionCurve"]
  else:
    minimumPtToReachBarrel = yamlConf["minimumPtToReachBarrel"]
  if "minimumPtToReachEndcapConvolutionCurve" in yamlConf:
    minimumPtToReachEndcap = yamlConf["minimumPtToReachEndcapConvolutionCurve"]
  else:
    minimumPtToReachEndcap = yamlConf["minimumPtToReachEndcap"]
  if "barrelEtaConvolutionCurve" in yamlConf:
    barrelEta = yamlConf["barrelEtaConvolutionCurve"]
  else:
    barrelEta = yamlConf["barrelEta"]
  if "detectorEtaConvolutionCurve" in yamlConf:
    detectorEta = yamlConf["detectorEtaConvolutionCurve"]
  else:
    detectorEta = yamlConf["detectorEta"]

  #options.extraOptions.append("sample=" + yamlConf["sampleBinnedDistributions"])
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("quality=" + str(yamlConf["qualityThreshold"]))
  options.extraOptions.append(
      "minimumPtInBarrel=" + str(minimumPtToReachBarrel))
  options.extraOptions.append(
      "minimumPtInEndcap=" + str(minimumPtToReachEndcap))
  options.extraOptions.append("barrelEta=" + str(barrelEta))
  options.extraOptions.append("detectorEta=" + str(detectorEta))
  options.extraOptions.append("triggerObjectName=" + yamlConf["triggerObject"])
  options.extraOptions.append("genObjectName=" + yamlConf["genObject"])
  options.extraOptions.append(
      "deltaR2Matching=" + str(yamlConf["deltaR2Matching"]))
  options.extraOptions.append(
      "deltaEtaMatching=" + str(yamlConf["deltaEtaMatching"]))
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

def computeConvolutionCurvesJetToMuon(yamlConf):

  saveFolder = yamlConf["saveFolder"]
  genObject = "genJet"
  triggerObject = yamlConf["triggerObject"]

  moduleNameConvolutionCurvesJetToMuon = yamlConf["moduleNameConvolutionCurvesJetToMuon"]
  componentNameConvolutionCurvesJetToMuon = yamlConf["componentNameConvolutionCurvesJetToMuon"]

  componentConvolutionCurvesJetToMuon = [getattr(import_module(
      moduleNameConvolutionCurvesJetToMuon), componentNameConvolutionCurvesJetToMuon, None)]

  if componentConvolutionCurvesJetToMuon[0] is None:
    print "Error:  component does not exist"
    raise ValueError('Component ' + componentNameConvolutionCurvesJetToMuon +
                     " has not been declared in module " + moduleNameConvolutionCurvesJetToMuon)

  parser = create_parser()
  (options, args) = parser.parse_args()
  folderAndScriptName = [
      saveFolder, "heppy/muonTriggerRateEstimationWorkflow/binnedDistributionsCMS_L1TMuon_cfg.py"]
  options.components = split(componentConvolutionCurvesJetToMuon)
  for component in options.components:
    component.splitFactor = 1

  #options.extraOptions.append("sample=" + yamlConf["sampleBinnedDistributions"])
  if "binningJet" in yamlConf:
    binningArray = yamlConf["binningJet"]
  else:
    binningArray = yamlConf["binning"]

  options.extraOptions.append("binning=" + binningArray)
  options.extraOptions.append("quality=" + str(yamlConf["qualityThreshold"]))
  options.extraOptions.append(
      "minimumPtInBarrel=0")
  options.extraOptions.append(
      "minimumPtInEndcap=0")
  options.extraOptions.append("barrelEta=1000")
  options.extraOptions.append("detectorEta=1000")
  options.extraOptions.append("triggerObjectName=" + yamlConf["triggerObject"])
  options.extraOptions.append("genObjectName=genJet")
  options.extraOptions.append(
      "deltaR2Matching=" + str(yamlConf["deltaR2MatchingJetToMuon"]))
  options.extraOptions.append(
      "deltaEtaMatching=100")
  #options.nevents=300000
  options.force = True
  loop = main(options, folderAndScriptName, parser)
  os.system("rm -r " + saveFolder + "/" + genObject +
            "_" + triggerObject + "_" + "convolutionCurves_JetToMuon")
  os.system("mkdir " + saveFolder + "/" + genObject +
            "_" + triggerObject + "_" + "convolutionCurves_JetToMuon")
  if componentConvolutionCurvesJetToMuon[0].splitFactor > 1:
    os.system("hadd " + saveFolder + "/" + genObject + "_" + triggerObject + "_" + "convolutionCurves_JetToMuon/histograms.root " +
              saveFolder + "/" + componentNameConvolutionCurvesJetToMuon + "_Chunk*/histograms.root")
  else:
    os.system("mv " + saveFolder + "/" + componentNameConvolutionCurvesJetToMuon + "/histograms.root " +
              saveFolder + "/" + genObject + "_" + triggerObject + "_" + "convolutionCurves_JetToMuon/histograms.root")


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

  if "detectorEtaConvolutionCurve" in yamlConf:
    detectorEta = yamlConf["detectorEtaConvolutionCurve"]
  else:
    detectorEta = yamlConf["detectorEta"]
  if "barrelEtaConvolutionCurve" in yamlConf:
    barrelEta = yamlConf["barrelEtaConvolutionCurve"]
  else:
    barrelEta = yamlConf["barrelEta"]
  if "minimumPtToReachBarrelConvolutionCurve" in yamlConf:
    minimumPtToReachBarrel = yamlConf["minimumPtToReachBarrelConvolutionCurve"]
  else:
    minimumPtToReachBarrel = yamlConf["minimumPtToReachBarrel"]
  if "minimumPtToReachEndcapConvolutionCurve" in yamlConf:
    minimumPtToReachEndcap = yamlConf["minimumPtToReachEndcapConvolutionCurve"]
  else:
    minimumPtToReachEndcap = yamlConf["minimumPtToReachEndcap"]

  print "--- COMPUTING THE CONVERSION FACTORS/EFFICIENCIES ---"
  if "efficiencyLowPtSourceFolder" in yamlConf:
    print "PROCESSING FROM LOW MOMENTUM MUONS"
    numberOfMatchedObjects_lowPt, numberOfGenObjects_lowPt = computeEfficiencies(
      GenObjTree=yamlConf["efficiencyLowPtGenTree"],
      GenObjFileFolder=yamlConf["efficiencyLowPtSourceFolder"],
      MatchTree=yamlConf["efficiencyLowPtMatchTree"],
      MatchFileFolder=yamlConf["efficiencyLowPtSourceFolder"],
      binning=yamlConf["binning"],
      eta=detectorEta,
      quality=yamlConf["qualityThreshold"],
      barrelEta=barrelEta,
      minPtInBarrel=minimumPtToReachBarrel,
      minPtInEndcap=minimumPtToReachEndcap,
      deltaR2Matching=yamlConf["deltaR2Matching"],
      deltaEtaMatching=yamlConf["deltaEtaMatching"]
    )
    if 'numberOfMatchedObjects' in locals():
      numberOfMatchedObjects = numberOfMatchedObjects_lowPt + numberOfMatchedObjects_highPt
      numberOfGenObjects = numberOfGenObjects_lowPt + numberOfGenObjects_highPt
    else: 
      numberOfMatchedObjects = numberOfMatchedObjects_lowPt
      numberOfGenObjects = numberOfGenObjects_lowPt

  if "efficiencyHighPtSourceFolder" in yamlConf:
    print "PROCESSING FROM HIGH MOMENTUM MUONS"
    numberOfMatchedObjects_highPt, numberOfGenObjects_highPt = computeEfficiencies(
      GenObjTree=yamlConf["efficiencyHighPtGenTree"],
      GenObjFileFolder=yamlConf["efficiencyHighPtSourceFolder"],
      MatchTree=yamlConf["efficiencyHighPtMatchTree"],
      MatchFileFolder=yamlConf["efficiencyHighPtSourceFolder"],
      binning=yamlConf["binning"],
      eta=detectorEta,
      quality=yamlConf["qualityThreshold"],
      barrelEta=barrelEta,
      minPtInBarrel=minimumPtToReachBarrel,
      minPtInEndcap=minimumPtToReachEndcap,
      deltaR2Matching=yamlConf["deltaR2Matching"],
      deltaEtaMatching=yamlConf["deltaEtaMatching"]
    )
    if 'numberOfMatchedObjects' in locals():
      numberOfMatchedObjects = numberOfMatchedObjects_lowPt + numberOfMatchedObjects_highPt
      numberOfGenObjects = numberOfGenObjects_lowPt + numberOfGenObjects_highPt
    else: 
      numberOfMatchedObjects = numberOfMatchedObjects_highPt
      numberOfGenObjects = numberOfGenObjects_highPt

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
  numberOfMatchedObjectsHistogram = TH1F(
      "numberOfMatchedObjectsHistogram", "numberOfMatchedObjectsHistogram", len(binningArray) - 1, binningArray)
  numberOfGenObjectsHistogram = TH1F(
      "numberOfGenObjectsHistogram", "numberOfGenObjectsHistogram", len(binningArray) - 1, binningArray)

  for x in xrange(0, len(numberOfMatchedObjects)):
    #Excluding overflow bin
    if x != len(numberOfMatchedObjects) - 1:
      numberOfMatchedObjectsHistogram.SetBinContent(
          x + 1, numberOfMatchedObjects[x])
      numberOfGenObjectsHistogram.SetBinContent(x + 1, numberOfGenObjects[x])

  numberOfGenObjectsHistogram.Sumw2()
  numberOfMatchedObjectsHistogram.Sumw2()

  efficiencyHistogram = numberOfMatchedObjectsHistogram.Clone("efficiencyHistogram")
  efficiencyHistogram.Divide(numberOfGenObjectsHistogram)

  for x in xrange(0, len(numberOfMatchedObjects)):
    if efficiencyHistogram.GetBinContent(x + 1) > 1:
      efficiencyHistogram.SetBinContent(x + 1, 1)

  efficiencyHistogram.Write()
  numberOfMatchedObjectsHistogram.Write()
  numberOfGenObjectsHistogram.Write()
  efficiencyFactorsFile.Close()

def obtainEfficienciesJetToMuon(yamlConf):

  saveFolder = yamlConf["saveFolder"]
  genObject = "genJet"
  triggerObject = "l1tMuon"

  if "binningJetEfficiency" in yamlConf:
    binningArray = array("f", ast.literal_eval(yamlConf["binningJetEfficiency"]))
    binningStr = yamlConf["binningJetEfficiency"]
  elif "binningJet":
    binningArray = array("f", ast.literal_eval(yamlConf["binningJet"]))
    binningStr = yamlConf["binningJet"]
  else:
    binningArray = array("f", ast.literal_eval(yamlConf["binning"]))
    binningStr = yamlConf["binning"]

  print "--- COMPUTING THE CONVERSION FACTORS/EFFICIENCIES ---"
  numberOfMatchedObjects_jetToMuon, numberOfGenObjects_jetToMuon = computeEfficienciesJetToMuon(
    GenObjTree=yamlConf["efficiencyGenTreeJetToMuon"],
    GenObjFileFolder=yamlConf["efficiencySourceFolderJetToMuon"],
    MatchTree=yamlConf["efficiencyMatchTreeJetToMuon"],
    MatchFileFolder=yamlConf["efficiencySourceFolderJetToMuon"],
    binning=binningStr,
    eta=1400,
    quality=yamlConf["qualityThreshold"],
    barrelEta=1000,
    endcapEta=1200,
    minPtInBarrel=0,
    minPtInEndcap=0,
    minPtInForward=0,
    deltaR2Matching=yamlConf["deltaR2MatchingJetToMuon"],
  )
  numberOfMatchedObjects = numberOfMatchedObjects_jetToMuon
  numberOfGenObjects = numberOfGenObjects_jetToMuon

  efficiencyFactors = numberOfMatchedObjects / numberOfGenObjects
  for binIdx in xrange(0, len(efficiencyFactors)):
    efficiencyFactors[binIdx] = 0 if isnan(
        efficiencyFactors[binIdx]) else efficiencyFactors[binIdx]
    if efficiencyFactors[binIdx] > 1:
      efficiencyFactors[binIdx] = 1
  print efficiencyFactors

  efficiencyFactorsFile = TFile(
      "" + saveFolder + "/efficiencyFactors_JetToMuon.root", "RECREATE")
  efficiencyFactorsFile.cd()
  numberOfMatchedObjectsHistogram = TH1F(
      "numberOfMatchedObjectsHistogram", "numberOfMatchedObjectsHistogram", len(binningArray) - 1, binningArray)
  numberOfGenObjectsHistogram = TH1F(
      "numberOfGenObjectsHistogram", "numberOfGenObjectsHistogram", len(binningArray) - 1, binningArray)

  for x in xrange(0, len(efficiencyFactors)):
    #Excluding overflow bin
    if x != len(efficiencyFactors) - 1:
      numberOfMatchedObjectsHistogram.SetBinContent(
          x + 1, numberOfMatchedObjects[x])
      numberOfGenObjectsHistogram.SetBinContent(x + 1, numberOfGenObjects[x])

  numberOfGenObjectsHistogram.Sumw2()
  numberOfMatchedObjectsHistogram.Sumw2()

  efficiencyHistogram = numberOfMatchedObjectsHistogram.Clone(
      "efficiencyHistogram")
  efficiencyHistogram.Divide(numberOfGenObjectsHistogram)
  
  if "jetToMuonEfficiencyScaleFactor" in yamlConf:
    efficiencyHistogram.Scale(yamlConf["jetToMuonEfficiencyScaleFactor"])

  for x in xrange(0, len(numberOfMatchedObjects)):
    if efficiencyHistogram.GetBinContent(x + 1) > 1:
      efficiencyHistogram.SetBinContent(x + 1, 1)

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

  # Getting the job index from the heppy extra options
  if "job" in yamlConf:
    job = int(yamlConf["job"])
  else:
    job = None
  

  componentChunksArray = split(componentRatePlots)
  for component in componentChunksArray:
    component.splitFactor = 1
  
  if job is not None:
    componentChunksArray = [componentChunksArray[job]]

  if ("copyToLocal" in yamlConf) and (yamlConf["copyToLocal"] is True):
    os.mkdir(saveFolder + "/__localSourceFiles")
    for comp in componentChunksArray:

      hdfsCompliantFileList = [filePath.replace("/hdfs", "") for filePath in comp.files]
      
      print "COPYING FILES LOCALLY"
      for filePath in hdfsCompliantFileList:
        os.system("/usr/bin/hdfs dfs -copyToLocal " + filePath +
                  "  " + saveFolder + "/__localSourceFiles/")
      
      heppyLocalFileList = os.listdir(saveFolder + "/__localSourceFiles/")
      heppyLocalFileList = [saveFolder + "/__localSourceFiles/" + filePath for filePath in heppyLocalFileList]
      comp.files = heppyLocalFileList  

  parser = create_parser()
  (options, args) = parser.parse_args()
  folderAndScriptName = [
      saveFolder, "heppy/muonTriggerRateEstimationWorkflow/muonFCCTriggerRates_cfg.py"]
  convolutionFileName = saveFolder + "/binnedDistributions.root"
  options.components = componentChunksArray
  

  #options.extraOptions.append("sample=" + yamlConf["componentNameRatePlots"])
  options.extraOptions.append("convolutionFileName=" + convolutionFileName)
  options.extraOptions.append("convolutionFileNameJetToMuon=" + saveFolder + "/genJet_" + triggerObject + "_" + "convolutionCurves_JetToMuon/histograms.root")
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("binningJet=" + yamlConf["binningJet"])
  options.extraOptions.append(
      "probabilityFile=" + "" + yamlConf["saveFolder"] + "/efficiencyFactors.root")
  options.extraOptions.append("probabilityHistogram=efficiencyHistogram")
  options.extraOptions.append(
      "jetToMuonProbabilityFile=" + "" + yamlConf["saveFolder"] + "/efficiencyFactors_JetToMuon.root")
  options.extraOptions.append("jetToMuonProbabilityHistogram=efficiencyHistogram")
  options.extraOptions.append(
      "minimumPtInBarrel=" + str(yamlConf["minimumPtToReachBarrel"]))
  options.extraOptions.append(
      "minimumPtInEndcap=" + str(yamlConf["minimumPtToReachEndcap"]))
  options.extraOptions.append("barrelEta=" + str(yamlConf["barrelEta"]))
  options.extraOptions.append("detectorEta=" + str(yamlConf["detectorEta"]))
  options.extraOptions.append("genJetCollection=" + str(yamlConf["genJetCollection"]))
  
  options.extraOptions.append(
      "triggerObjectName=" + str(yamlConf["triggerObject"]))
  options.force = True

  if "numberOfDelphesEvents" in yamlConf:
    options.nevents = numberOfDelphesEvents
  loop = main(options, folderAndScriptName, parser)

  if ("copyToLocal" in yamlConf) and (yamlConf["copyToLocal"] is True):
    os.system("rm -r " + saveFolder + "/__localSourceFiles/")


def mergeNonNormalisedRatePlots(yamlConf):

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]
  print "CREATING THE NON-NORMALISED PLOTS"

  moduleNameRatePlots = yamlConf["moduleNameRatePlots"]
  componentNameRatePlots = yamlConf["componentNameRatePlots"]

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
  bunchCrossingFrequency = yamlConf["bunchCrossingFrequency"]
  componentNameRatePlots = yamlConf["componentNameRatePlots"]
  averagePileUp = yamlConf["averagePileUp"]
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
  totalRateHist.GetYaxis().SetTitle("Rate [Hz]")
  barrelRateHist.GetXaxis().SetTitle("p_{t}")
  barrelRateHist.GetYaxis().SetTitle("Rate [Hz]")
  endcapRateHist.GetXaxis().SetTitle("p_{t}")
  endcapRateHist.GetYaxis().SetTitle("Rate [Hz]")

  normalisedRatePlotFile = TFile("" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_Normalised.root", "RECREATE")
  normalisedRatePlotFile.cd()
  totalRateHist.Write()
  barrelRateHist.Write()
  endcapRateHist.Write()
  normalisedRatePlotFile.Close()
  nonNormalisedRatePlotFile.Close()

  print "NORMALISING THE RATE PLOT TO OBTAIN THE TRIGGER PASS PROBABILITY FOR MINBIAS AND PU140 EVENTS"

  nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject +
                                    "_" + componentNameRatePlots + "_RatePlots_NotNormalised.root")
  passProbabilityFile = TFile("" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_TriggerPassProbability.root", "RECREATE")
  totalRateHist = nonNormalisedRatePlotFile.Get(
      "mergedTotalSimL1TMuonRate")
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

  passProbabilityFile = TFile("" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_TriggerPassProbability.root")
  ppPassProbabilityHistogram = passProbabilityFile.Get("ppPassProbabilityHistogram")
  eventPassProbabilityHistogram = passProbabilityFile.Get("eventPassProbabilityHistogram")

  linearPURatePlot = ppPassProbabilityHistogram.Clone("linearPURatePlot")
  fullPURatePlot = eventPassProbabilityHistogram.Clone("fullPURatePlot")
  linearPURatePlot.Scale(interactionFrequency)
  fullPURatePlot.Scale(bunchCrossingFrequency)

  fullPURatePlotErrors = TGraphErrors(fullPURatePlot)
  fullPURatePlotErrors.SetName("fullPURatePlotErrors")

  #Estimating the error. The idea is to compute the base rate unit and use it to get the stat error.

  baseRate = (1. * interactionFrequency) / (1. * numberOfDelphesEvents)

  nonNormalisedRatePlotFile = TFile("" + saveFolder + "/" + genObject + "_" + triggerObject + "_" + componentNameRatePlots + "_RatePlots_NotNormalised.root")
  numberOfEventInDetector = nonNormalisedRatePlotFile.Get("mergedTotalSimL1TMuonRate")

  for index in xrange(0, fullPURatePlotErrors.GetN()):
    # Getting the number of pu 0
    numberOfEventsInBin = numberOfEventInDetector.GetBinContent(index + 1)
    # Computing the fractional error
    if numberOfEventsInBin > 0:
      relativeError = sqrt(1. * numberOfEventsInBin) / \
          (1. * numberOfEventsInBin)
    else:
      relativeError = 0

    # Reapplying the same fractional error to my rate plot
    error = relativeError * fullPURatePlotErrors.GetY()[index]
    # Trasferring the error to the plot
    fullPURatePlotErrors.GetEY()[index] = error

  pileupRatePlotFile = TFile("" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_PU" + str(averagePileUp) + "RatePlot.root", "RECREATE")
  pileupRatePlotFile.cd()
  linearPURatePlot.Write()
  fullPURatePlot.Write()
  fullPURatePlotErrors.Write()
  pileupRatePlotFile.Close()
  nonNormalisedRatePlotFile.Close()

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


def applyFinalScaling(yamlConf):

  saveFolder = yamlConf["saveFolder"]
  genObject = yamlConf["genObject"]
  triggerObject = yamlConf["triggerObject"]
  moduleNameRatePlots = yamlConf["moduleNameRatePlots"]
  componentNameRatePlots = yamlConf["componentNameRatePlots"]
  averagePileUp = yamlConf["averagePileUp"]
  bunchCrossingFrequency = yamlConf["bunchCrossingFrequency"]
  scalingFactorsFileName = yamlConf["scalingFactorsFileName"]
  scalingFactorsPlotName = yamlConf["scalingFactorsPlotName"]

  pileupRatePlotFile = TFile("" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_PU" + str(averagePileUp) + "RatePlot.root")

  pileupRatePlotFile.cd()

  fullPURatePlotErrors = pileupRatePlotFile.Get("fullPURatePlotErrors")

  scalingFactorsFile = TFile(scalingFactorsFileName)
  scalingFactorsPlot = scalingFactorsFile.Get(scalingFactorsPlotName)


  simplifiedRatioPlotXRangeBinning = array(
      "f", ast.literal_eval(yamlConf["simplifiedRatioPlotXRangeBinning"]))

  simplifiedFullPURatePlotErrors = TGraphErrors(len(simplifiedRatioPlotXRangeBinning))  # +1 for the initial/final point
  
  simplifiedFullPURatePlotErrors.SetName("simplifiedFullPURatePlotErrors")
  fullPURatePlotErrorsIdx = 0
  scalingFactorsPlotIdx = 0

  maxFractionalEY = 0

  for scalingFactorsPlotIdx in xrange(0, scalingFactorsPlot.GetN()):
    xPoint = fullPURatePlotErrors.GetX()[fullPURatePlotErrorsIdx]
    eXPoint = fullPURatePlotErrors.GetEX()[fullPURatePlotErrorsIdx]
    yPoint = fullPURatePlotErrors.GetY()[fullPURatePlotErrorsIdx]
    eYPoint = fullPURatePlotErrors.GetEY()[fullPURatePlotErrorsIdx]

    while (xPoint < scalingFactorsPlot.GetX()[scalingFactorsPlotIdx] - scalingFactorsPlot.GetEX()[scalingFactorsPlotIdx]):
      fullPURatePlotErrorsIdx += 1
      xPoint = fullPURatePlotErrors.GetX()[fullPURatePlotErrorsIdx]
      eXPoint = fullPURatePlotErrors.GetEX()[fullPURatePlotErrorsIdx]
      yPoint = fullPURatePlotErrors.GetY()[fullPURatePlotErrorsIdx]
      eYPoint = fullPURatePlotErrors.GetEY()[fullPURatePlotErrorsIdx]
    while ((fullPURatePlotErrorsIdx < fullPURatePlotErrors.GetN()) and (xPoint < scalingFactorsPlot.GetX()[scalingFactorsPlotIdx] + scalingFactorsPlot.GetEX()[scalingFactorsPlotIdx]) and (xPoint > scalingFactorsPlot.GetX()[scalingFactorsPlotIdx] - scalingFactorsPlot.GetEX()[scalingFactorsPlotIdx])):
      fullPURatePlotErrors.GetY()[fullPURatePlotErrorsIdx] *= scalingFactorsPlot.GetY()[scalingFactorsPlotIdx]
      fullPURatePlotErrors.GetEY()[fullPURatePlotErrorsIdx] = sqrt((eYPoint * scalingFactorsPlot.GetY()[scalingFactorsPlotIdx])**2 + (yPoint * scalingFactorsPlot.GetEY()[scalingFactorsPlotIdx])**2)
      if maxFractionalEY < fullPURatePlotErrors.GetEY()[fullPURatePlotErrorsIdx] / fullPURatePlotErrors.GetY()[fullPURatePlotErrorsIdx]:
        maxIdx = fullPURatePlotErrorsIdx
        maxFractionalEY = fullPURatePlotErrors.GetEY(
        )[fullPURatePlotErrorsIdx] / fullPURatePlotErrors.GetY()[fullPURatePlotErrorsIdx]
      fullPURatePlotErrorsIdx += 1
      if (fullPURatePlotErrorsIdx < fullPURatePlotErrors.GetN()):
        xPoint = fullPURatePlotErrors.GetX()[fullPURatePlotErrorsIdx]
        eXPoint = fullPURatePlotErrors.GetEX()[fullPURatePlotErrorsIdx]
        yPoint = fullPURatePlotErrors.GetY()[fullPURatePlotErrorsIdx]
        eYPoint = fullPURatePlotErrors.GetEY()[fullPURatePlotErrorsIdx]

  simplifiedFullPURatePlotErrorsIdx = 0
  for fullPURatePlotErrorsIdx in xrange(0, fullPURatePlotErrors.GetN()):
    xPoint = fullPURatePlotErrors.GetX()[fullPURatePlotErrorsIdx]
    eXPoint = fullPURatePlotErrors.GetEX()[fullPURatePlotErrorsIdx]
    yPoint = fullPURatePlotErrors.GetY()[fullPURatePlotErrorsIdx]
    eYPoint = fullPURatePlotErrors.GetEY()[fullPURatePlotErrorsIdx]
    if (xPoint > simplifiedRatioPlotXRangeBinning[simplifiedFullPURatePlotErrorsIdx]):
        if simplifiedFullPURatePlotErrorsIdx < len(simplifiedRatioPlotXRangeBinning) - 1:
          simplifiedFullPURatePlotErrors.GetX(
          )[simplifiedFullPURatePlotErrorsIdx] = xPoint
          simplifiedFullPURatePlotErrors.GetEX(
          )[simplifiedFullPURatePlotErrorsIdx] = eXPoint
          simplifiedFullPURatePlotErrors.GetY(
          )[simplifiedFullPURatePlotErrorsIdx] = yPoint
          simplifiedFullPURatePlotErrors.GetEY(
          )[simplifiedFullPURatePlotErrorsIdx] = eYPoint
          simplifiedFullPURatePlotErrorsIdx += 1
        else:
          # for the last point we want the previous one, not the next, as it is out-of-range
          xPoint = fullPURatePlotErrors.GetX()[fullPURatePlotErrorsIdx - 2]
          eXPoint = fullPURatePlotErrors.GetEX()[fullPURatePlotErrorsIdx - 2]
          yPoint = fullPURatePlotErrors.GetY()[fullPURatePlotErrorsIdx - 2]
          eYPoint = fullPURatePlotErrors.GetEY()[fullPURatePlotErrorsIdx - 2]
          simplifiedFullPURatePlotErrors.GetX(
          )[simplifiedFullPURatePlotErrorsIdx] = xPoint
          simplifiedFullPURatePlotErrors.GetEX(
          )[simplifiedFullPURatePlotErrorsIdx] = eXPoint
          simplifiedFullPURatePlotErrors.GetY(
          )[simplifiedFullPURatePlotErrorsIdx] = yPoint
          simplifiedFullPURatePlotErrors.GetEY(
          )[simplifiedFullPURatePlotErrorsIdx] = eYPoint
          #ending the loop
          break

  # UNCOMMENT ME TO HAVE THE MAXIMUM FRACTIONAL ERROR APPLIED ALL OVER THE RANGE
  #for idx in xrange(0, fullPURatePlotErrors.GetN()):
  #  fullPURatePlotErrors.GetEY()[idx] = maxFractionalEY * fullPURatePlotErrors.GetY()[idx]

  scaledPileupRatePlotFile = TFile("" + saveFolder + "/" +
                                   componentNameRatePlots + "_RatePlots_PU" + str(averagePileUp) + "RatePlot_Scaled.root", "RECREATE")

  scaledPileupRatePlotFile.cd()
  fullPURatePlotErrors.Write()
  simplifiedFullPURatePlotErrors.Write()
  scaledPileupRatePlotFile.Close()

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
  folderAndScriptName = [saveFolder, "heppy/muonTriggerRateEstimationWorkflow/plotTransverseMomentumDistributionForMuonClosureTest_FromMatchedPairs_cfg.py"]
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
  #loop = main(options, folderAndScriptName, parser)
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
  folderAndScriptName = [saveFolder, "heppy/muonTriggerRateEstimationWorkflow/plotTransverseMomentumDistributionForMuonClosureTest_FromMatchedPairs_cfg.py"]
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
  folderAndScriptName = [saveFolder, "heppy/muonTriggerRateEstimationWorkflow/computeTriggerRatesCMSMuons_cfg.py"]
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
  if "simplifiedRatioPlotXRangeBinning" in yamlConf:
    simplifiedRatioPlotXRangeBinning = array("f", ast.literal_eval(yamlConf["simplifiedRatioPlotXRangeBinning"]))

  ratePlotFilePath = saveFolder + "/" + componentNameRatePlots + \
      "_RatePlots_PU" + str(averagePileUp) + "RatePlot.root"
  if "scalingFactorsPlotName" in yamlConf:
    ratePlotFilePath = saveFolder + "/" + componentNameRatePlots + \
        "_RatePlots_PU" + str(averagePileUp) + "RatePlot_Scaled.root"

  print "CREATING RATIO PLOT FOR CMS VS DELPHES RATE"
  
  cfg = lambda x: 1
  cfg.plots = [
  #  #Files here
      ["" + saveFolder + "/" + componentNameRateClosureTest + \
       "_CMSTriggerRate/ratePlots.root", "triggerRate", "CMS " + triggerObject],
      [ratePlotFilePath, "fullPURatePlotErrors", "Sim " + triggerObject]
  ]
  cfg.saveFileName = "" + saveFolder + "/rateClosureTest.root"
  cfg.xRange = (0, 200)
  cfg.xAxisLabel = "p_{t} [GeV]"
  cfg.yAxisLabel = "Rate [Hz]"
  cfg.yRange = (1e2, 4e7)
  cfg.yRangeRatio = (0, 3)
  cfg.logY = True
  if "simplifiedRatioPlotXRangeBinning" in yamlConf and "scalingFactorsPlotName" not in yamlConf:
    cfg.simplifiedRatioPlotXRangeBinning = simplifiedRatioPlotXRangeBinning
  plotDistributionComparisonPlot(cfg)

#  ["" + saveFolder + "/" + componentNameRatePlots + "_RatePlots_Normalised.root", "simL1TMuonTriggerRate", "Sim L1TMuon"]
#]
#cfg.saveFileName = "" + saveFolder + "/rateClosureTest.root"
#plotDistributionComparisonPlot(cfg)
