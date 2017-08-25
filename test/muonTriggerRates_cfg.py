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
import sys
from heppy.framework.looper import Looper
from heppy.test.mySamples import *

logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

# Retrieving the sample to analyse

sampleName = "NeutrinoGun_OnlyMuons_13TeV_DelphesCMS"

#if specified in sample, a specific set will be used, otherwise the full set will be employed
if "sample" in _heppyGlobalOptions:
  sampleName = _heppyGlobalOptions["sample"]
if sampleName == "all":
  selectedComponents = [
    cmsMatching_QCD_15_3000_L1TMuon_GenJet,
    cmsMatching_QCD_15_3000_L1TEGamma_GenJet,
    cmsMatching_QCD_15_3000_L1TTau_GenJet,
  ]
else:  
  sample = globals()[sampleName]
  selectedComponents = [
    sample
  ]

mySettings = lambda a: None
mySettings.yScale = 1e6
'''Instantaneous lumi in cm^-2 s^-1'''
mySettings.bunchCrossingFrequency = 1/25e-9 # 40 MHz

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

muonRate = cfg.Analyzer(
  RatePlotProducerPileUp,
  instance_label = 'muonRate',
  file_label = 'ratePlotFile',
  plot_name = 'muonTriggerRate',
  plot_title = 'Muon trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'muons',
  bins = steps,
  yscale = mySettings.yScale,
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  muonRate
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

