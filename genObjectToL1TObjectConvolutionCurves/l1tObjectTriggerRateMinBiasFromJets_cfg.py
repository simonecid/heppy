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



#logging.shutdown()
#reload(logging)
#logging.basicConfig(level=logging.WARNING)

# Retrieving the sample to analyse

sampleName = "NeutrinoGun_NoTau_13TeV_DelphesCMS_JetPTMin_5"
convolutionFileName = "_binnedDistributions/distributionWithQuality8/histograms.root"
minimumPtInBarrel = float(_heppyGlobalOptions["minimumPtInBarrel"])
minimumPtInEndcap = float(_heppyGlobalOptions["minimumPtInEndcap"])
barrelEta = float(_heppyGlobalOptions["barrelEta"])
detectorEta = float(_heppyGlobalOptions["detectorEta"])
triggerObjectName = _heppyGlobalOptions["triggerObjectName"]

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

if sample is None:
  raise Exception("ERROR: You have selected a non-declared sample, exiting script.")

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

  gen_jets = 'genJets',

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
  elif (abs(ptc.eta()) < float(_heppyGlobalOptions["detectorEta"])):
  #Otherwise, check if is in endcap
    return (ptc.pt() > minimumPtInEndcap)
  

lowPtMuonSelector = cfg.Analyzer(
  Selector,
  'lowPtMuonSelector',
  output = 'good_jets',
  input_objects = 'gen_jets',
  filter_func = jetInDetector 
)

smearJetToTriggerObject = cfg.Analyzer(
  Smearer,
  'smearJetToTriggerObject',
  input_collection = 'good_jets',
  output_collection = triggerObjectName,
  convolution_file = convolutionFileName,
  convolution_histogram_prefix = "deltaPtDistributionBinnedInMatchedObject",
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
  input_objects = triggerObjectName,
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
  histo_title = 'Muon leading transverse momentum distribution',
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

def barrelCut(ptc):
  return abs(ptc.eta()) < barrelEta

def endcapCut(ptc):
  return (abs(ptc.eta()) > barrelEta and abs(ptc.eta()) < detectorEta)

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
  output = 'leading_' + triggerObjectName + 'endcap',
  input_objects = 'leading_' + triggerObjectName,
  filter_func = endcapCut
)

def isSmeared(ptc):
  return ptc.match is not None

smearedSelector = cfg.Analyzer(
  Selector,
  'smearedSelector',
  output = 'smeared_good_jets',
  input_objects = 'good_jets',
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
  plot_title = '1.1 < abs(#eta) < 2.4 trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'leading_' + triggerObjectName + '_barrel',
  bins = steps,
  pileup = 140,
  yscale = mySettings.yScale,
  normalise = False
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  lowPtMuonSelector,
  smearJetToTriggerObject,
  smearedSelector,
  leadingPtSimL1TObjectFinder,
  barrelSelector,
  endcapSelector,
  simL1TObjectLeadingPtDistribution,
  genJetSimL1TObjectTree,
  simL1TObjectRate,
  genJetRate,
  barrelSimL1TObjectRate,
  endcapSimL1TObjectRate,
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

