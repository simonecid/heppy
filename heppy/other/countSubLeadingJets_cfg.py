import os
import copy
import heppy.framework.config as cfg
from heppy.samples.sample_MinimumBias_NoTau_100TeV_GenParticles_CMSSWTune_WPropagation import MinimumBias_100TeV_GenParticles_CMSSWTune_WPropagation_1MEvents
from heppy.samples.sample_MinimumBias_NoTau_14TeV_GenParticles_CMSSWTune_WPropagation import MinimumBias_14TeV_GenParticles_full_CMSSWTune_WPropagation_1MEvents
import logging
from ROOT import gSystem
#from heppy.framework.chain import Chain as Events
from EventStore import EventStore as Events
from heppy.framework.services.tfile import TFileService
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
from heppy.analyzers.triggerrates.LeadingQuantityHistogrammer import LeadingQuantityHistogrammer
from heppy.analyzers.triggerrates.NumberOfParticlesDistribution import NumberOfParticlesDistribution
from heppy.framework.looper import Looper
from heppy.analyzers.Matcher import Matcher
from heppy.analyzers.Selector import Selector
from heppy.analyzers.triggerrates.MatchedParticlesTreeProducer import MatchedParticlesTreeProducer
from heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions import MatchedObjectBinnedDistributions
from heppy.analyzers.fcc.Reader import Reader
from heppy.analyzers.triggerrates.ObjectFinder import ObjectFinder
from heppy.analyzers.triggerrates.HistogrammerCumulative import HistogrammerCumulative
from heppy.analyzers.triggerrates.ParticleTreeProducer import ParticleTreeProducer
from heppy.analyzers.triggerrates.NumberOfParticlesDistributionVsLeadingPt import NumberOfParticlesDistributionVsLeadingPt
from heppy.framework.heppy_loop import _heppyGlobalOptions
from math import sqrt

gSystem.Load("libdatamodelDict")

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

#Object name
objectName = "L1T EGamma"
matchedObjectName = "Gen jet"
sampleName = "cmsMatching_SingleNeutrinoPU140_GenJet"

# Retrieving the sample to analyse

#if specified in sample, a specific set will be used, otherwise the full set will be employed
#if "sample" in _heppyGlobalOptions:
#  sampleName = _heppyGlobalOptions["sample"]
#if sampleName == "all":
#  selectedComponents = [
#    cmsMatching_QCD_15_3000_L1TMuon_GenJet,
#    cmsMatching_QCD_15_3000_L1TEGamma_GenJet,
#    cmsMatching_QCD_15_3000_L1TTau_GenJet,
#  ]
#else:  
#  sample = globals()[sampleName]
#  selectedComponents = [
#      MinimumBias_14TeV_GenParticles_full
#  ]

#sample = globals()[sampleName]
selectedComponents = [
    MinimumBias_14TeV_GenParticles_full_CMSSWTune_WPropagation_1MEvents
]

''' Returns pt'''
def pt (ptc):
      return ptc.pt()

'''Returns eta'''
def eta (ptc):
      return ptc.eta()

# Defining pdgids

source = cfg.Analyzer(
    Reader,

    #gen_particles = 'skimmedGenParticles',

    gen_jets='nonPropagatedGenJets',

    #electrons = 'genElectrons',

    #muons = 'genMuons',

    #photons = 'genPhotons',
    #met = 'genMET',
)


tfile_service_1 = cfg.Service(
    TFileService,
    'tfile1',
    fname='distributions.root',
    option='recreate'
)

# I want to plot 
# Number of jets, inclusive pt and leading pt for jets w/o nu, and muons

numberOfParticlesDistribution = cfg.Analyzer(
  NumberOfParticlesDistributionVsLeadingPt,
  file_label = 'tfile1',
  histo_name = 'numberOfGenJetsVsPt',
  histo_title = 'Number of gen jets',
  bins = [0.8, 1.1, 1.4, 1.7, 2.5, 3, 3.5, 3.9, 5, 5.5, 6, 7, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200, 250, 300, 350, 400],
  objects_to_count = 'gen_jets',
  leading_objects = 'gen_jets',
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  numberOfParticlesDistribution 
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
