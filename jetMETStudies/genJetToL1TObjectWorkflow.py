#!/usr/bin/env python

from heppy.framework.heppy_loop import * 
from heppy.genObjectToL1TObjectConvolutionCurves.computeEfficiencies import computeEfficiencies
from ROOT import TH1F
from ROOT import TFile
from ROOT import TGraphErrors
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
from math import sqrt

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
  folderAndScriptName = [saveFolder, "jetMETStudies/binnedDistributionsCMS_cfg.py"]
  options.components = split(componentConvolutionCurves)
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
  if "minimumPtToReachForwardConvolutionCurve" in yamlConf:
    minimumPtToReachForward = yamlConf["minimumPtToReachForwardConvolutionCurve"]
  else:
    minimumPtToReachForward = yamlConf["minimumPtToReachForward"]
  if "barrelEtaConvolutionCurve" in yamlConf:
    barrelEta = yamlConf["barrelEtaConvolutionCurve"]
  else:
    barrelEta = yamlConf["barrelEta"]
  if "endcapEtaConvolutionCurve" in yamlConf:
    endcapEta = yamlConf["endcapEtaConvolutionCurve"]
  else:
    endcapEta = yamlConf["endcapEta"]
  if "detectorEtaConvolutionCurve" in yamlConf:
    detectorEta = yamlConf["detectorEtaConvolutionCurve"]
  else:
    detectorEta = yamlConf["detectorEta"]

  #options.extraOptions.append("sample=" + yamlConf["sampleBinnedDistributions"])
  options.extraOptions.append("binning=" + yamlConf["binning"])
  options.extraOptions.append("quality=" + str(yamlConf["qualityThreshold"]))
  options.extraOptions.append("minimumPtInBarrel=" + str(minimumPtToReachBarrel))
  options.extraOptions.append("minimumPtInEndcap=" + str(minimumPtToReachEndcap))
  options.extraOptions.append("minimumPtInForward=" + str(minimumPtToReachForward))
  options.extraOptions.append("barrelEta=" + str(barrelEta))
  options.extraOptions.append("endcapEta=" + str(endcapEta))
  options.extraOptions.append("detectorEta=" + str(detectorEta))
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

  if "minimumPtToReachBarrelConvolutionCurve" in yamlConf:
    minimumPtToReachBarrel = yamlConf["minimumPtToReachBarrelConvolutionCurve"]
  else:
    minimumPtToReachBarrel = yamlConf["minimumPtToReachBarrel"]
  if "minimumPtToReachEndcapConvolutionCurve" in yamlConf:
    minimumPtToReachEndcap = yamlConf["minimumPtToReachEndcapConvolutionCurve"]
  else:
    minimumPtToReachEndcap = yamlConf["minimumPtToReachEndcap"]
  if "minimumPtToReachForwardConvolutionCurve" in yamlConf:
    minimumPtToReachForward = yamlConf["minimumPtToReachForwardConvolutionCurve"]
  else:
    minimumPtToReachForward = yamlConf["minimumPtToReachForward"]
  if "barrelEtaConvolutionCurve" in yamlConf:
    barrelEta = yamlConf["barrelEtaConvolutionCurve"]
  else:
    barrelEta = yamlConf["barrelEta"]
  if "endcapEtaConvolutionCurve" in yamlConf:
    endcapEta = yamlConf["endcapEtaConvolutionCurve"]
  else:
    endcapEta = yamlConf["endcapEta"]
  if "detectorEtaConvolutionCurve" in yamlConf:
    detectorEta = yamlConf["detectorEtaConvolutionCurve"]
  else:
    detectorEta = yamlConf["detectorEta"]

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
                                                                    eta = detectorEta,
                                                                    quality = yamlConf["qualityThreshold"],
                                                                    barrelEta = barrelEta,
                                                                    endcapEta = endcapEta,
                                                                    minPtInBarrel = minimumPtToReachBarrel,
                                                                    minPtInEndcap = minimumPtToReachEndcap,
                                                                    minPtInForward = minimumPtToReachForward,
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
  numberOfMatchedObjectsHistogram = TH1F("numberOfMatchedObjectsHistogram", "numberOfMatchedObjectsHistogram", len(binningArray)-1, binningArray)
  numberOfGenObjectsHistogram = TH1F("numberOfGenObjectsHistogram", "numberOfGenObjectsHistogram", len(binningArray)-1, binningArray)

  for x in xrange(0, len(efficiencyFactors)): 
    #Excluding overflow bin
    if x != len(efficiencyFactors) - 1:
      numberOfMatchedObjectsHistogram.SetBinContent(x + 1, numberOfMatchedObjects[x])
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


