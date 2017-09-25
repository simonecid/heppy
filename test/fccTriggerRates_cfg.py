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
from heppy.analyzers.triggerrates.Transformer import Transformer  
from heppy.analyzers.triggerrates.Smearer import Smearer
from importlib import import_module
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
from heppy.analyzers.triggerrates.LeadingQuantityHistogrammer import LeadingQuantityHistogrammer



logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

# Retrieving the sample to analyse

sampleName = "NeutrinoGun_NoTau_13TeV_DelphesCMS_JetPTMin_5"

#if specified in sample, a specific set will be used, otherwise the full set will be employed
if "sample" in _heppyGlobalOptions:
  sampleName = _heppyGlobalOptions["sample"]

sample = getattr(import_module("heppy.test.sample_NeutrinoGun_NoTau_13TeV_DelphesCMS_JetPTMin_5"), sampleName)
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

conv_factors = [0.011819013935167239, 0.031229420147026607, 0.05894886980069262, 0.0907587832763081, 0.12402859051977241, 0.15813355388380312, 0.19814191561633573, 0.23492730751504826, 0.26182982128567617, 0.2845614757205836, 0.2970284287607943, 0.29759263057788055, 0.29220468675274985, 0.2753409348224655, 0.24452178272228595, 0.21978538702676634, 0.19757806594173402, 0.18528040586864117, 0.1688296130655273, 0.1591269021552021, 0.15380284573651345]
genJetPtBins = [0, 5, 7, 9, 11, 13, 15, 18, 21, 24, 27, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120]
muon_conv_factors = [1, 1, 1, 1, 1, 1]
muon_ptBins = [0, 10, 20, 30, 40, 50, 60]

jetToL1TEGammaTrasformer = cfg.Analyzer(
  Transformer ,
  'jetToL1TEGammaTrasformer',
  input_collection = 'gen_jets',
  output_collection = 'l1tEGamma',
  convolution_file = "_l1tObjectGenJetMatching/cmsMatching_QCD_15_3000_L1TEGamma_GenJet/histograms.root",
  convolution_histogram_prefix = "l1tEGammaPtDistributionBinnedInGenJet",
  bins = genJetPtBins,
  conversion_factors = conv_factors,
  object_x_range = (0, 260)
)

muonSmearer = cfg.Analyzer(
  Smearer ,
  'muonSmearer',
  input_collection = 'muons',
  output_collection = 'l1tMuons',
  convolution_file = "_muonTriggerRates//cmsMatching_QCD_15_3000_L1TMuon_GenMuon/histograms.root",
  convolution_histogram_prefix = "deltaRDistributionBinnedInGenMuon",
  bins = muon_ptBins,
  object_x_range = (-100, 200)
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

l1tEGammaTriggerRate = cfg.Analyzer(
  RatePlotProducerPileUp,
  instance_label = 'l1tEGammaTriggerRate',
  file_label = 'ratePlotFile',
  plot_name = 'l1tEGammaTriggerRate',
  plot_title = 'L1T EGamma trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'l1tEGamma',
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
  input_objects = 'l1tMuons',
  bins = steps,
  yscale = mySettings.yScale,
  normalise = False
)

def pt (ptc):
  return ptc.pt()
  
genJetPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'genJetPtDistribution',
  file_label = 'ratePlotFile',
  histo_name = 'genJetPtDistribution',
  histo_title = 'Gen-Jet transverse momentum distribution',
  min = 0,
  max = 300,
  nbins = 300,
  input_objects = 'gen_jets',
  value_func = pt,
  x_label = "pt [GeV]",
  y_label = "\# events"
)

l1tEGammaPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'l1tEGammaPtDistribution',
  file_label = 'ratePlotFile',
  histo_name = 'l1tEGammaPtDistribution',
  histo_title = 'L1TEGamma transverse momentum distribution',
  min = 0,
  max = 300,
  nbins = 300,
  input_objects = 'l1tEGamma',
  value_func = pt,
  x_label = "pt [GeV]",
  y_label = "\# events"
)

l1tEGammaLeadingPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  instance_label = 'l1tEGammaLeadingPtDistribution',
  file_label = 'ratePlotFile',
  histo_name = 'l1tEGammaLeadingPtDistribution',
  histo_title = 'L1TEGamma leading transverse momentum distribution',
  min = 0,
  max = 300,
  nbins = 300,
  input_objects = 'l1tEGamma',
  key_func = pt,
  value_func = pt,
  x_label = "pt [GeV]",
  y_label = "\# events"
)

genJetLeadingPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  instance_label = 'genJetLeadingPtDistribution',
  file_label = 'ratePlotFile',
  histo_name = 'genJetLeadingPtDistribution',
  histo_title = 'Gen-Jet leading transverse momentum distribution',
  min = 0,
  max = 300,
  nbins = 300,
  input_objects = 'gen_jets',
  value_func = pt,
  key_func = pt,
  x_label = "pt [GeV]",
  y_label = "\# events"
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  muonSmearer,
  #jetToL1TEGammaTrasformer,
  #genJetPtDistribution,
  #l1tEGammaPtDistribution,
  #genJetLeadingPtDistribution,
  #l1tEGammaLeadingPtDistribution,
  muonRate,
  #l1tEGammaTriggerRate
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

