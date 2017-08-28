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
from heppy.analyzers.triggerrates.JetTransformer import JetTransformer  

logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

# Retrieving the sample to analyse

sampleName = "NeutrinoGun_NoTau_13TeV_DelphesCMS"

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

conv_factors = [0.011819013935167239, 0.031229420147026607, 0.05894886980069262, 0.0907587832763081, 0.12402859051977241, 0.15813355388380312, 0.19814191561633573, 0.23492730751504826, 0.26182982128567617, 0.2845614757205836, 0.2970284287607943, 0.29759263057788055, 0.29220468675274985, 0.2753409348224655, 0.24452178272228595, 0.21978538702676634, 0.19757806594173402, 0.18528040586864117, 0.1688296130655273, 0.1591269021552021, 0.15380284573651345]
genJetPtBins = [0, 5, 7, 9, 11, 13, 15, 18, 21, 24, 27, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120]

jetToL1TEGammaTrasformer = cfg.Analyzer(
  JetTransformer ,
  'jetToL1TEGammaTrasformer',
  jet_collection = 'gen_jets',
  output_objects = 'l1tEGamma',
  convolution_file = "_l1tObjectGenJetMatching/cmsMatching_QCD_15_3000_L1TEGamma_GenJet/histograms.root",
  convolution_histogram_prefix = "l1tEGammaPtDistributionBinnedInGenJet",
  bins = genJetPtBins,
  conversion_factors = conv_factors,
  object_x_range = (0, 260)
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

triggerRate = cfg.Analyzer(
  RatePlotProducerPileUp,
  instance_label = 'triggerRate',
  file_label = 'ratePlotFile',
  plot_name = 'triggerRate',
  plot_title = 'Trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'l1tEGamma',
  bins = steps,
  yscale = mySettings.yScale,
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  jetToL1TEGammaTrasformer,
  triggerRate
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

