import os
import copy
import heppy.framework.config as cfg
from heppy.framework.heppy_loop import _heppyGlobalOptions
import logging
# next 2 lines necessary to deal with reimports from ipython
from heppy.analyzers.fcc.Reader import Reader
from ROOT import gSystem
from EventStore import EventStore as Events
from heppy.framework.services.tfile import TFileService
from heppy.analyzers.triggerrates.RatePlotProducer import RatePlotProducer
from heppy.analyzers.triggerrates.MatchedParticlesTreeProducer import MatchedParticlesTreeProducer
import sys
from heppy.framework.looper import Looper
from heppy.analyzers.triggerrates.Transformer import Transformer  
from heppy.analyzers.Selector import Selector
from heppy.analyzers.triggerrates.Smearer import Smearer
from importlib import import_module
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
from heppy.analyzers.triggerrates.LeadingQuantityHistogrammer import LeadingQuantityHistogrammer
from heppy.analyzers.triggerrates.LeadingObjectFinder import LeadingObjectFinder  
from heppy.analyzers.triggerrates.MomentumShifter import MomentumShifter



#logging.shutdown()
#reload(logging)
#logging.basicConfig(level=logging.WARNING)

# Retrieving the sample to analyse

sampleName = "NeutrinoGun_NoTau_13TeV_DelphesCMS_JetPTMin_5"
convolutionFileName = "_binnedDistributions/distributionWithQuality8/histograms.root"
minimumPtInBarrel = float(_heppyGlobalOptions["minimumPtInBarrel"])
minimumPtInEndcap = float(_heppyGlobalOptions["minimumPtInEndcap"])
minimumPtInForward = float(_heppyGlobalOptions["minimumPtInForward"])
barrelEta = float(_heppyGlobalOptions["barrelEta"])
endcapEta = float(_heppyGlobalOptions["endcapEta"])
detectorEta = float(_heppyGlobalOptions["detectorEta"])
momentumShift = float(_heppyGlobalOptions["momentumShift"])
triggerObjectName = _heppyGlobalOptions["triggerObjectName"]

if "usePtTransformer" in _heppyGlobalOptions:
  usePtTransformer = True if _heppyGlobalOptions["usePtTransformer"].lower() == "true" else False
if "useOnlyLeadingGenJet" in _heppyGlobalOptions:
  useOnlyLeadingGenJet = True if _heppyGlobalOptions["useOnlyLeadingGenJet"].lower() == "true" else False
if "genJetCollection" in _heppyGlobalOptions:
  genJetCollection = _heppyGlobalOptions["genJetCollection"]
else:
  genJetCollection = "genJets"

ptBins = [0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]

if "binning" in _heppyGlobalOptions:
  import ast
  ptBins = ast.literal_eval(_heppyGlobalOptions["binning"])

#if specified in sample, a specific set will be used, otherwise the full set will be employed
if "sample" in _heppyGlobalOptions:
  sampleName = _heppyGlobalOptions["sample"]
if "convolutionFileName" in _heppyGlobalOptions:
  convolutionFileName = _heppyGlobalOptions["convolutionFileName"]

if "probabilityFile" in _heppyGlobalOptions:
  probabilityFile = _heppyGlobalOptions["probabilityFile"]
  probabilityHistogram = _heppyGlobalOptions["probabilityHistogram"]
else: 
  probabilityFile = ""
  probabilityHistogram = ""

sample = getattr(import_module("heppy.samples.sample_MinimumBias_NoTau_14TeV_GenParticles"), sampleName, None)
if sample is None:
  sample = getattr(import_module("heppy.samples.mySamples"), sampleName, None)

selectedComponents = [
  sample
]

mySettings = lambda a: None
mySettings.yScale = 1e6
'''Instantaneous lumi in cm^-2 s^-1'''
mySettings.bunchCrossingFrequency = 31.6e6 # 2808 bunches

source = cfg.Analyzer(
  Reader,

  #gen_particles = 'skimmedGenParticles',
  #gen_vertices = 'genVertices',

  gen_jets = genJetCollection,

  #jets = 'jets',
  #bTags = 'bTags',
  #cTags = 'cTags',
  #tauTags = 'tauTags',

  #electrons = 'electrons',
  #electronITags = 'electronITags',

  #muons = 'muons',
  #muonITags = 'muonITags',

  #photons = 'photons',
  #met = 'met',
)

gSystem.Load("libdatamodelDict")


#ptBins = [0, 1.5, 3, 5, 10, 20, 30, 40, 50, 70, 100, 140, 200] # set 3
# ptBins = [0, 5, 10, 20, 30, 40, 50, 60] # set 1
#ptBins = [0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200] #set 4


def jetInDetector(ptc):
  if (abs(ptc.eta()) < barrelEta):
    #It is OK if the momentum is high enough to not start spiralling
    return (ptc.pt() > minimumPtInBarrel)
  #Otherwise, check if is in endcap
  elif (abs(ptc.eta()) < endcapEta):
    return (ptc.pt() > minimumPtInEndcap)
  #then, is it in the forward?
  elif (abs(ptc.eta()) < detectorEta):
    return (ptc.pt() > minimumPtInForward)
  

goodJetSelector = cfg.Analyzer(
  Selector,
  'goodJetSelector',
  output = 'good_jets',
  input_objects = 'gen_jets',
  filter_func = jetInDetector 
)

shiftJetMomentum = cfg.Analyzer(
  MomentumShifter,
  'shiftJetMomentum',
  input_collection = 'good_jets',
  output_collection = "shifted_good_jets",
  shift = momentumShift
)

smearJetToTriggerObject = cfg.Analyzer(
  Smearer,
  'smearJetToTriggerObject',
  input_collection='shifted_good_jets',
  output_collection = triggerObjectName,
  convolution_file = convolutionFileName,
  convolution_histogram_prefix = "deltaPtDistributionBinnedInMatchedObject",
  bins = ptBins,
  object_x_range = (-300, 300),
  probability_file = probabilityFile,
  probability_histogram = probabilityHistogram
)

if usePtTransformer:
  smearJetToTriggerObject = cfg.Analyzer(
    Transformer,
    'transformJetToTriggerObject',
    input_collection='shifted_good_jets',
    output_collection = triggerObjectName,
    convolution_file = convolutionFileName,
    convolution_histogram_prefix = "objectPtDistributionBinnedInMatchedObject",
    bins = ptBins,
    object_x_range = (-300, 300),
    probability_file = probabilityFile,
    probability_histogram = probabilityHistogram
  )

steps = []

x = 0
while x <= 500:
  steps.append(x)
  x += 0.5

# File in which all the rate plots will be stored 

tfile_service_1 = cfg.Service(
  TFileService,
  'ratePlotFile',
  fname='ratePlots.root',
  option='recreate'
)

simL1TObjectRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'simL1TObjectRate',
  file_label = 'ratePlotFile',
  plot_name = 'simL1TObjectTriggerRate',
  plot_title = 'Sim-' + triggerObjectName + ' trigger rate',
  input_objects = 'leading_' + triggerObjectName,
  bins = steps,
  pileup = 140,
  yscale = mySettings.yScale,
  normalise = False
)

genJetRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'genJetRate',
  file_label = 'ratePlotFile',
  plot_name = 'genJetTriggerRate',
  plot_title = 'Gen jet trigger rate',
  input_objects = 'good_jets',
  bins = steps,
  pileup = 140,
  yscale = mySettings.yScale,
  normalise = False
)

def pt (ptc):
  return ptc.pt()


simL1TObjectLeadingPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  instance_label = 'simL1TObjectLeadingPtDistribution',
  file_label = 'ratePlotFile',
  histo_name = 'simL1TObjectLeadingPtDistribution',
  histo_title = triggerObjectName + ' leading transverse momentum distribution',
  min = 0,
  max = 50,
  nbins = 100,
  input_objects = triggerObjectName,
  key_func = pt,
  value_func = pt,
  x_label = "pt [GeV]",
  y_label = "\# events"
)

genJetSimL1TObjectTree = cfg.Analyzer(
  MatchedParticlesTreeProducer,
  'genJetSimL1TObjectTree',
  file_label = "ratePlotFile",
  tree_name = 'genJetSimL1TObjectTree',
  tree_title = 'Tree containing info about matched gen and Sim' + triggerObjectName,
  particle_collection = 'smeared_good_jets',
  matched_particle_name = "Sim" + triggerObjectName,
  particle_name = "genJet"
)

leadingPtSimL1TObjectFinder = cfg.Analyzer(
  LeadingObjectFinder ,
  "leadingPtSimL1TObjectFinder",
  input_collection = triggerObjectName,
  output_collection = 'leading_' + triggerObjectName,
  key_func = pt
)

leadingPtGenJetFinder = cfg.Analyzer(
  LeadingObjectFinder,
  "leadingPtGenJetFinder",
  input_collection = "good_jets",
  output_collection = "good_jets",
  key_func = pt
)

def barrelCut(ptc):
  return abs(ptc.eta()) < barrelEta

def endcapCut(ptc):
  return (abs(ptc.eta()) >= barrelEta and abs(ptc.eta()) < endcapEta)

def forwardCut(ptc):
  return (abs(ptc.eta()) >= endcapEta and abs(ptc.eta()) < detectorEta)

barrelSelector = cfg.Analyzer(
  Selector,
  'barrelSelector',
  output = 'leading_' + triggerObjectName + '_barrel',
  input_objects = 'leading_' + triggerObjectName,
  filter_func = barrelCut 
)

endcapSelector = cfg.Analyzer(
  Selector,
  'endcapSelector',
  output = 'leading_' + triggerObjectName + '_endcap',
  input_objects = 'leading_' + triggerObjectName,
  filter_func = endcapCut
)

forwardSelector = cfg.Analyzer(
  Selector,
  'forwardSelector',
  output = 'leading_' + triggerObjectName + '_forward',
  input_objects = 'leading_' + triggerObjectName,
  filter_func = forwardCut
)

def isSmeared(ptc):
  return ptc.match is not None

smearedSelector = cfg.Analyzer(
  Selector,
  'smearedSelector',
  output = 'smeared_good_jets',
  input_objects = 'shifted_good_jets',
  filter_func = isSmeared
)

barrelSimL1TObjectRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'barrelSimL1TObjectRate',
  file_label = 'ratePlotFile',
  plot_name = 'barrelSimL1TObjectRate',
  plot_title = 'abs(#eta) < ' + str(barrelEta) + ' trigger rate',
  input_objects = 'leading_' + triggerObjectName + '_barrel',
  bins = steps,
  pileup = 140,
  yscale = mySettings.yScale,
  normalise = False
)

endcapSimL1TObjectRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'endcapSimL1TObjectRate',
  file_label = 'ratePlotFile',
  plot_name = 'endcapSimL1TObjectRate',
  plot_title = '' + str(barrelEta) + ' < abs(#eta) < ' + str(endcapEta) + ' trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'leading_' + triggerObjectName + '_endcap',
  bins = steps,
  pileup = 140,
  yscale = mySettings.yScale,
  normalise = False
)

forwardSimL1TObjectRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'forwardSimL1TObjectRate',
  file_label = 'ratePlotFile',
  plot_name = 'forwardSimL1TObjectRate',
  plot_title = '' + str(endcapEta) + ' < abs(#eta) < ' + str(detectorEta) + ' trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'leading_' + triggerObjectName + '_forward',
  bins = steps,
  pileup = 140,
  yscale = mySettings.yScale,
  normalise = False
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order

if useOnlyLeadingGenJet:
  sequence = cfg.Sequence( [
    source,
    goodJetSelector,
    leadingPtGenJetFinder,
    shiftJetMomentum,
    smearJetToTriggerObject,
    smearedSelector,
    leadingPtSimL1TObjectFinder,
    barrelSelector,
    endcapSelector,
    forwardSelector,
    simL1TObjectLeadingPtDistribution,
    genJetSimL1TObjectTree,
    simL1TObjectRate,
    genJetRate,
    barrelSimL1TObjectRate,
    endcapSimL1TObjectRate,
    forwardSimL1TObjectRate,
  ] )
else:
  sequence = cfg.Sequence( [
    source,
    goodJetSelector,
    shiftJetMomentum,
    smearJetToTriggerObject,
    smearedSelector,
    leadingPtSimL1TObjectFinder,
    barrelSelector,
    endcapSelector,
    forwardSelector,
    simL1TObjectLeadingPtDistribution,
    genJetSimL1TObjectTree,
    simL1TObjectRate,
    genJetRate,
    barrelSimL1TObjectRate,
    endcapSimL1TObjectRate,
    forwardSimL1TObjectRate,
  ] )


config = cfg.Config(
  components = selectedComponents,
  sequence = sequence,
  services = [tfile_service_1],
  events_class = Events
)

if __name__ == '__main__':



  def next():
      loop.process(loop.iEvent+1)

  loop = Looper( 'looper', config,
                 nEvents=100,
                 nPrint=0,
                 timeReport=True)
  loop.process(6)
  print loop.event

