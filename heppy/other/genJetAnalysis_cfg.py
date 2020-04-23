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
from math import sqrt

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


tfile_service_1 = cfg.Service(
  TFileService,
  'tfile1',
  fname='histograms.root',
  option='recreate'
)

def pt (ptc):
  return ptc.pt()

def deltaPt(ptc):
  return ptc.pt() - ptc.match.pt()

def eta (ptc):
  return ptc.eta()

def phi (ptc):
  return ptc.phi()

def matchedParticlePt (ptc):
  return ptc.match.pt()

def matchedParticleEta (ptc):
  return ptc.match.eta()

def ptRatioWithMatched (ptc):
  return ptc.pt()/ptc.match.pt()

def deltaR (ptc):
  return sqrt(ptc.deltaR2)

def isMatched(ptc):
  return ptc.match is not None

def dr2Selection(ptc):
  return abs(ptc.deltaR2) < 0.25 #dr < 0.5

genJetPtDistribution = cfg.Analyzer(
  Histogrammer,
  'genJetPtDistribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'genJetPtDistribution',
  histo_title = 'Gen jet transverse momentum distribution',
  min = 0,
  max = 400,
  nbins = 400,
  input_objects = 'gen_objects',
  value_func = pt,
  log_y = True
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  genJetPtDistribution
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
