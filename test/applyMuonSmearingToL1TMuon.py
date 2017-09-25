import os
import copy
import heppy.framework.config as cfg
from heppy.test.mySamples import *
import logging
from heppy.framework.chain import Chain as Events
from heppy.framework.services.tfile import TFileService
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
from heppy.framework.looper import Looper
from heppy.analyzers.Matcher import Matcher
from heppy.analyzers.Selector import Selector
from heppy.analyzers.triggerrates.MatchedParticlesTreeProducer import MatchedParticlesTreeProducer
from heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions import MatchedObjectBinnedDistributions
from heppy.analyzers.triggerrates.CMSMatchingReader import CMSMatchingReader
from heppy.analyzers.triggerrates.ObjectFinder import ObjectFinder
from heppy.analyzers.triggerrates.HistogrammerCumulative import HistogrammerCumulative
from heppy.framework.heppy_loop import _heppyGlobalOptions
from heppy.analyzers.triggerrates.JetTransformer import JetTransformer  

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

#Object name
triggerObjectName = "L1T obj"
sampleName = "cmsMatching_SingleNeutrinoPU140_L1TMuon"

# Retrieving the sample to analyse

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

# Defining pdgids

source = cfg.Analyzer(
  CMSMatchingReader,
)

conv_factors = [1, 1, 1, 1, 1, 1]

ptBins = [0, 10, 20, 30, 40, 50, 60]

muonSmearer = cfg.Analyzer(
  JetTransformer ,
  'muonSmearer',
  jet_collection = 'l1tMuons',
  output_objects = 'l1tEGamma',
  convolution_file = "_l1tObjectGenJetMatching/cmsMatching_QCD_15_3000_L1TEGamma_GenJet/histograms.root",
  convolution_histogram_prefix = "l1tEGammaPtDistributionBinnedInGenJet",
  bins = genJetPtBins,
  conversion_factors = conv_factors,
  object_x_range = (0, 260)
)

def pt(ptc):
  return ptc.pt()
#end pt

tfile_service_1 = cfg.Service(
  TFileService,
  'tfile1',
  fname='histograms.root',
  option='recreate'
)

l1tEGammaPtHistogram = cfg.Analyzer (
  Histogrammer,
  'l1tEGammaPtHistogram',
  file_label = 'tfile1',
  histo_name = 'l1tEGammaPtHistogram',
  histo_title = 'L1T EGamma from Gen-Jets transverse momentum distribution',
  min = 0,
  max = 250,
  nbins = 250,
  input_objects = 'l1tEGamma',
  value_func = pt,
  x_label = "pt [GeV]",
  y_label = "\# events"
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  jetToL1TEGammaTrasformer,
  l1tEGammaPtHistogram
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
  loop.process()
  print loop.event
