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
detectorEta = float(_heppyGlobalOptions["detectorEta"])
barrelEta = float(_heppyGlobalOptions["barrelEta"])

#if specified in sample, a specific set will be used, otherwise the full set will be employed
if "sample" in _heppyGlobalOptions:
  sampleName = _heppyGlobalOptions["sample"]

sample = getattr(import_module("heppy.samples.mySamples"), sampleName, None)
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

  gen_particles = 'skimmedGenParticles',
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

def genObjectInDetector(ptc):
  #Check if muon
  if (
      (ptc.status() == 1) #Should be always 1 for muons (no hadronisation)
     ):
    #Check if in detector
    if (abs(ptc.eta()) < detectorEta):
      #It is OK if the momentum is high enough to not start spiralling
      return True

  return False  

def isGenJetInDetector(ptc):
  #Check if in detector
  if (abs(ptc.eta()) < detectorEta):
    #It is OK if the momentum is high enough to not start spiralling
    return True

  return False  

def isMuon(ptc):
  #Check if muon
  return abs(ptc.pdgid()) == 13

def isElectron(ptc):
  #Check if electron
  return abs(ptc.pdgid()) == 11

def isPhoton(ptc):
  #Check if photon
  return abs(ptc.pdgid()) == 22

def isEGamma(ptc):
  #Check if electron or photon
  return ((abs(ptc.pdgid()) == 11) or (abs(ptc.pdgid()) == 22))

genObjectInDetectorSelector = cfg.Analyzer(
  Selector,
  'genObjectInDetectorSelector',
  output = 'good_gen_particles',
  input_objects = 'gen_particles',
  filter_func = genObjectInDetector 
)

muonSelector = cfg.Analyzer(
  Selector,
  'muonSelector',
  output = 'good_gen_muons',
  input_objects = 'good_gen_particles',
  filter_func = isMuon 
)

electronSelector = cfg.Analyzer(
  Selector,
  'electronSelector',
  output = 'good_gen_electrons',
  input_objects = 'good_gen_particles',
  filter_func = isElectron 
)

photonSelector = cfg.Analyzer(
  Selector,
  'photonSelector',
  output = 'good_gen_photons',
  input_objects = 'good_gen_particles',
  filter_func = isPhoton 
)

egammaSelector = cfg.Analyzer(
  Selector,
  'egammaSelector',
  output = 'good_gen_egammas',
  input_objects = 'good_gen_particles',
  filter_func = isEGamma 
)

genJetInDetectorSelector = cfg.Analyzer(
  Selector,
  'genJetInDetectorSelector',
  output = 'good_gen_jets',
  input_objects = 'gen_jets',
  filter_func = isGenJetInDetector 
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

genMuonRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'genMuonRate',
  file_label = 'ratePlotFile',
  plot_name = 'genMuonTriggerRate',
  plot_title = 'Gen muon trigger rate',
  input_objects = 'good_gen_muons',
  bins = steps,
  pileup = 140,
  yscale = mySettings.yScale,
  normalise = False
)

genElectronRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'genElectronRate',
  file_label = 'ratePlotFile',
  plot_name = 'genElectronTriggerRate',
  plot_title = 'Gen electron trigger rate',
  input_objects = 'good_gen_electrons',
  bins = steps,
  pileup = 140,
  yscale = mySettings.yScale,
  normalise = False
)

genPhotonRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'genPhotonRate',
  file_label = 'ratePlotFile',
  plot_name = 'genPhotonTriggerRate',
  plot_title = 'Gen photon trigger rate',
  input_objects = 'good_gen_photons',
  bins = steps,
  pileup = 140,
  yscale = mySettings.yScale,
  normalise = False
)

genEGammaRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'genEGammaRate',
  file_label = 'ratePlotFile',
  plot_name = 'genEGammaTriggerRate',
  plot_title = 'Gen egamma trigger rate',
  input_objects = 'good_gen_egammas',
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
  input_objects = 'good_gen_jets',
  bins = steps,
  pileup = 140,
  yscale = mySettings.yScale,
  normalise = False
)

def pt (ptc):
  return ptc.pt()

leadingPtMuonFinder = cfg.Analyzer(
  LeadingObjectFinder ,
  "leadingPtMuonFinder",
  input_collection = 'good_gen_muons',
  output_collection = 'leading_gen_muon',
  key_func = pt
)

leadingPtElectronFinder = cfg.Analyzer(
  LeadingObjectFinder ,
  "leadingPtElectronFinder",
  input_collection = 'good_gen_electrons',
  output_collection = 'leading_gen_electron',
  key_func = pt
)

leadingPtPhotonFinder = cfg.Analyzer(
  LeadingObjectFinder ,
  "leadingPtPhotonFinder",
  input_collection = 'good_gen_photons',
  output_collection = 'leading_gen_photon',
  key_func = pt
)

leadingPtEGammaFinder = cfg.Analyzer(
  LeadingObjectFinder ,
  "leadingPtEGammaFinder",
  input_collection = 'good_gen_egammas',
  output_collection = 'leading_gen_egamma',
  key_func = pt
)

leadingPtJetFinder = cfg.Analyzer(
  LeadingObjectFinder ,
  "leadingPtJetFinder",
  input_collection = 'good_gen_jets',
  output_collection = 'leading_gen_jet',
  key_func = pt
)



def barrelCut(ptc):
  return abs(ptc.eta()) < barrelEta

def endcapCut(ptc):
  return (abs(ptc.eta()) > barrelEta and abs(ptc.eta()) < detectorEta)

barrelMuonSelector = cfg.Analyzer(
  Selector,
  'barrelMuonSelector',
  output = 'leading_gen_muon_barrel',
  input_objects = 'leading_gen_muon',
  filter_func = barrelCut 
)

endcapMuonSelector = cfg.Analyzer(
  Selector,
  'endcapMuonSelector',
  output = 'leading_gen_muon_endcap',
  input_objects = 'leading_gen_muon',
  filter_func = endcapCut
)

barrelElectronSelector = cfg.Analyzer(
  Selector,
  'barrelElectronSelector',
  output = 'leading_gen_electron_barrel',
  input_objects = 'leading_gen_electron',
  filter_func = barrelCut 
)

endcapElectronSelector = cfg.Analyzer(
  Selector,
  'endcapElectronSelector',
  output = 'leading_gen_electron_endcap',
  input_objects = 'leading_gen_electron',
  filter_func = endcapCut
)

barrelPhotonSelector = cfg.Analyzer(
  Selector,
  'barrelPhotonSelector',
  output = 'leading_gen_photon_barrel',
  input_objects = 'leading_gen_photon',
  filter_func = barrelCut 
)

endcapPhotonSelector = cfg.Analyzer(
  Selector,
  'endcapPhotonSelector',
  output = 'leading_gen_photon_endcap',
  input_objects = 'leading_gen_photon',
  filter_func = endcapCut
)

barrelEGammaSelector = cfg.Analyzer(
  Selector,
  'barrelEGammaSelector',
  output = 'leading_gen_egamma_barrel',
  input_objects = 'leading_gen_egamma',
  filter_func = barrelCut 
)

endcapEGammaSelector = cfg.Analyzer(
  Selector,
  'endcapEGammaSelector',
  output = 'leading_gen_egamma_endcap',
  input_objects = 'leading_gen_egamma',
  filter_func = endcapCut
)

barrelJetSelector = cfg.Analyzer(
  Selector,
  'barrelJetSelector',
  output = 'leading_gen_jet_barrel',
  input_objects = 'leading_gen_jet',
  filter_func = barrelCut 
)

endcapJetSelector = cfg.Analyzer(
  Selector,
  'endcapJetSelector',
  output = 'leading_gen_jet_endcap',
  input_objects = 'leading_gen_jet',
  filter_func = endcapCut
)

barrelMuonRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'barrelMuonRate',
  file_label = 'ratePlotFile',
  plot_name = 'genMuonBarrelTriggerRate',
  plot_title = 'abs(#eta) < ' + str(barrelEta) + ' trigger rate',
  input_objects = 'leading_gen_muon_barrel',
  bins = steps,
  normalise = False
)

endcapMuonRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'endcapMuonRate',
  file_label = 'ratePlotFile',
  plot_name = 'genMuonEndcapTriggerRate',
  plot_title = str(barrelEta) + ' < abs(#eta) < ' + str(detectorEta) + ' trigger rate',
  input_objects = 'leading_gen_muon_endcap',
  bins = steps,
  normalise = False
)

barrelElectronRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'barrelElectronRate',
  file_label = 'ratePlotFile',
  plot_name = 'genElectronBarrelTriggerRate',
  plot_title = 'abs(#eta) < ' + str(barrelEta) + ' trigger rate',
  input_objects = 'leading_gen_electron_barrel',
  bins = steps,
  normalise = False
)

endcapElectronRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'endcapElectronRate',
  file_label = 'ratePlotFile',
  plot_name = 'genElectronEndcapTriggerRate',
  plot_title = str(barrelEta) + ' < abs(#eta) < ' + str(detectorEta) + ' trigger rate',
  input_objects = 'leading_gen_electron_endcap',
  bins = steps,
  normalise = False
)

barrelPhotonRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'barrelPhotonRate',
  file_label = 'ratePlotFile',
  plot_name = 'genPhotonBarrelTriggerRate',
  plot_title = 'abs(#eta) < ' + str(barrelEta) + ' trigger rate',
  input_objects = 'leading_gen_photon_barrel',
  bins = steps,
  normalise = False
)

endcapPhotonRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'endcapPhotonRate',
  file_label = 'ratePlotFile',
  plot_name = 'genPhotonEndcapTriggerRate',
  plot_title = str(barrelEta) + ' < abs(#eta) < ' + str(detectorEta) + ' trigger rate',
  input_objects = 'leading_gen_photon_endcap',
  bins = steps,
  normalise = False
)

barrelEGammaRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'barrelEGammaRate',
  file_label = 'ratePlotFile',
  plot_name = 'genEGammaBarrelTriggerRate',
  plot_title = 'abs(#eta) < ' + str(barrelEta) + ' trigger rate',
  input_objects = 'leading_gen_egamma_barrel',
  bins = steps,
  normalise = False
)

endcapEGammaRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'endcapEGammaRate',
  file_label = 'ratePlotFile',
  plot_name = 'genEGammaEndcapTriggerRate',
  plot_title = str(barrelEta) + ' < abs(#eta) < ' + str(detectorEta) + ' trigger rate',
  input_objects = 'leading_gen_egamma_endcap',
  bins = steps,
  normalise = False
)

barrelJetRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'barrelJetRate',
  file_label = 'ratePlotFile',
  plot_name = 'genJetBarrelTriggerRate',
  plot_title = 'abs(#eta) < ' + str(barrelEta) + ' trigger rate',
  input_objects = 'leading_gen_jet_barrel',
  bins = steps,
  normalise = False
)

endcapJetRate = cfg.Analyzer(
  RatePlotProducer,
  instance_label = 'endcapJetRate',
  file_label = 'ratePlotFile',
  plot_name = 'genJetEndcapTriggerRate',
  plot_title = str(barrelEta) + ' < abs(#eta) < ' + str(detectorEta) + ' trigger rate',
  input_objects = 'leading_gen_jet_endcap',
  bins = steps,
  normalise = False
)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  genObjectInDetectorSelector,
  muonSelector,
  electronSelector,
  photonSelector,
  egammaSelector,
  genJetInDetectorSelector,
  genMuonRate,
  genElectronRate,
  genPhotonRate,
  genEGammaRate,
  genJetRate,
  leadingPtMuonFinder,
  leadingPtElectronFinder,
  leadingPtPhotonFinder,
  leadingPtEGammaFinder,
  leadingPtJetFinder,
  barrelMuonSelector,
  endcapMuonSelector,
  barrelElectronSelector,
  endcapElectronSelector,
  barrelPhotonSelector,
  endcapPhotonSelector,
  barrelEGammaSelector,
  endcapEGammaSelector,
  barrelJetSelector,
  endcapJetSelector,
  barrelMuonRate,
  endcapMuonRate,
  barrelElectronRate,
  endcapElectronRate,
  barrelPhotonRate,
  endcapPhotonRate,
  barrelEGammaRate,
  endcapEGammaRate,
  barrelJetRate,
  endcapJetRate,
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

