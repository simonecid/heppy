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
from heppy.analyzers.triggerrates.RatePlotProducerPileUp import RatePlotProducerPileUp
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
muonMinimumPtInBarrel = float(_heppyGlobalOptions["minimumPtInBarrel"])
muonMinimumPtInEndcap = float(_heppyGlobalOptions["minimumPtInEndcap"])
barrelEta = float(_heppyGlobalOptions["barrelEta"])

muon_ptBins = [0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]

if "binning" in _heppyGlobalOptions:
  import ast
  muon_ptBins = ast.literal_eval(_heppyGlobalOptions["binning"])

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

sample = getattr(import_module("heppy.samples.sample_NeutrinoGun_NoTau_13TeV_DelphesCMS_JetPTMin_5"), sampleName)
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

  #gen_jets = 'genJets',

  #jets = 'jets',
  #bTags = 'bTags',
  #cTags = 'cTags',
  #tauTags = 'tauTags',

  #electrons = 'electrons',
  #electronITags = 'electronITags',

  muons = 'muons',
  #muonITags = 'muonITags',

  #photons = 'photons',
  #met = 'met',
)

gSystem.Load("libdatamodelDict")


#muon_ptBins = [0, 1.5, 3, 5, 10, 20, 30, 40, 50, 70, 100, 140, 200] # set 3
# muon_ptBins = [0, 5, 10, 20, 30, 40, 50, 60] # set 1
#muon_ptBins = [0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200] #set 4

def genMuonInDetector(ptc):
  #Check if muon
  if (
      (abs(ptc.pdgid()) == 13) and 
      (ptc.status() == 1) #Should be always 1 for muons (no hadronisation)
     ):
    #Check if in barrel
    if (abs(ptc.eta()) < barrelEta):
      #It is OK if the momentum is high enough to not start spiralling
      return (ptc.pt() > muonMinimumPtInBarrel)
    elif (abs(ptc.eta()) < float(_heppyGlobalOptions["detectorEta"])):
    #Otherwise, check if is in endcap
      return (ptc.pt() > muonMinimumPtInEndcap)


def muonInDetector(ptc):
  if (abs(ptc.eta()) < barrelEta):
    #It is OK if the momentum is high enough to not start spiralling
    return (ptc.pt() > muonMinimumPtInBarrel)
  elif (abs(ptc.eta()) < float(_heppyGlobalOptions["detectorEta"])):
  #Otherwise, check if is in endcap
    return (ptc.pt() > muonMinimumPtInEndcap)
  

lowPtMuonSelector = cfg.Analyzer(
  Selector,
  'lowPtMuonSelector',
  output = 'good_muons',
  input_objects = 'muons',
  filter_func = muonInDetector 
)

muonSmearer = cfg.Analyzer(
  Smearer,
  'muonSmearer',
  input_collection = 'good_muons',
  output_collection = 'l1tMuons',
  convolution_file = convolutionFileName,
  convolution_histogram_prefix = "deltaPtDistributionBinnedInMatchedObject",
  bins = muon_ptBins,
  object_x_range = (-100, 200),
  probability_file = probabilityFile,
  probability_histogram = probabilityHistogram
)

steps = []

x = 0
while x <= 100:
  steps.append(x)
  x += 0.5

# File in which all the rate plots will be stored 

tfile_service_1 = cfg.Service(
  TFileService,
  'ratePlotFile',
  fname='ratePlots.root',
  option='recreate'
)

l1tMuonRate = cfg.Analyzer(
  RatePlotProducerPileUp,
  instance_label = 'l1tMuonRate',
  file_label = 'ratePlotFile',
  plot_name = 'simL1TMuonTriggerRate',
  plot_title = 'Muon trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'l1tMuons',
  bins = steps,
  yscale = mySettings.yScale,
  normalise = False
)

muonRate = cfg.Analyzer(
  RatePlotProducerPileUp,
  instance_label = 'muonRate',
  file_label = 'ratePlotFile',
  plot_name = 'muonTriggerRate',
  plot_title = 'Muon trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'good_muons',
  bins = steps,
  yscale = mySettings.yScale,
  normalise = False
)

def pt (ptc):
  return ptc.pt()


muonLeadingPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  instance_label = 'muonLeadingPtDistribution',
  file_label = 'ratePlotFile',
  histo_name = 'muonLeadingPtDistribution',
  histo_title = 'Muon leading transverse momentum distribution',
  min = 0,
  max = 50,
  nbins = 100,
  input_objects = 'l1tMuons',
  key_func = pt,
  value_func = pt,
  x_label = "pt [GeV]",
  y_label = "\# events"
)

muonSimL1TMuonTree = cfg.Analyzer(
    MatchedParticlesTreeProducer,
    file_label = "ratePlotFile",
    tree_name = 'genMuonSimL1TMuonTree',
    tree_title = 'Tree containing info about matched gen and SimL1TMuons',
    particle_collection = 'smeared_good_muons',
    matched_particle_name = "SimL1TMuon",
    particle_name = "muon"
  )

leadingPtMuonFinder = cfg.Analyzer(
  LeadingObjectFinder ,
  "leadingPtMuonFinder",
  input_collection = 'l1tMuons',
  output_collection = 'leading_muon',
  key_func = pt
)

def barrelCut(ptc):
  return abs(ptc.eta()) < 1.1

def endcapCut(ptc):
  return (abs(ptc.eta()) > 1.1 and abs(ptc.eta()) < 2.4)

barrelSelector = cfg.Analyzer(
  Selector,
  'barrelSelector',
  output = 'leading_muon_barrel',
  input_objects = 'leading_muon',
  filter_func = barrelCut 
)

endcapSelector = cfg.Analyzer(
  Selector,
  'endcapSelector',
  output = 'leading_muon_endcap',
  input_objects = 'leading_muon',
  filter_func = endcapCut
)

def isSmeared(ptc):
  return ptc.match is not None

smearedSelector = cfg.Analyzer(
  Selector,
  'smearedSelector',
  output = 'smeared_good_muons',
  input_objects = 'good_muons',
  filter_func = isSmeared
)

barrelMuonRate = cfg.Analyzer(
  RatePlotProducerPileUp,
  instance_label = 'barrelMuonRate',
  file_label = 'ratePlotFile',
  plot_name = 'barrelMuonRate',
  plot_title = 'abs(#eta) < 1.1 trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'leading_muon_barrel',
  bins = steps,
  yscale = mySettings.yScale,
  normalise = False
)

endcapMuonRate = cfg.Analyzer(
  RatePlotProducerPileUp,
  instance_label = 'endcapMuonRate',
  file_label = 'ratePlotFile',
  plot_name = 'endcapMuonRate',
  plot_title = '1.1 < abs(#eta) < 2.4 trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'leading_muon_endcap',
  bins = steps,
  yscale = mySettings.yScale,
  normalise = False
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  lowPtMuonSelector,
  muonSmearer,
  smearedSelector,
  leadingPtMuonFinder,
  barrelSelector,
  endcapSelector,
  muonLeadingPtDistribution,
  muonSimL1TMuonTree,
  l1tMuonRate,
  muonRate,
  barrelMuonRate,
  endcapMuonRate,
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

