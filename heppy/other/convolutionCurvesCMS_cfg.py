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

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

#Object name
triggerObjectName = "L1T obj"
sampleName = "cmsMatching_QCD_15_3000_L1TEGamma_GenJet"

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
  return ptc.pt

def eta (ptc):
  return ptc.eta

def phi (ptc):
  return ptc.phi

def matchedParticlePt (ptc):
  return ptc.match.pt

def matchedParticleEta (ptc):
  return ptc.match.eta

def ptRatioWithMatched (ptc):
  return ptc.pt/ptc.match.pt

def deltaR (ptc):
  return ptc.deltaR2

def isMatched(ptc):
  return ptc.match is not None

def dr2AndPtSelection(ptc):
  return abs(ptc.deltaR2) < 0.25

tightRestrictionMatchSelector = cfg.Analyzer(
  Selector,
  'tightRestrictionMatchSelector',
  output = 'matched_trigger_object',
  input_objects = 'trigger_objects',
  filter_func = dr2AndPtSelection 
)

genJetPtBins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120]

#genJetPtBins = []
#for x in xrange(0, 130, 10):
#  genJetPtBins.append(x)

l1tObjectPtDistributionBinnedInGenJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'l1tObjectPtDistributionBinnedInGenJet',
  histo_name = 'l1tObjectPtDistributionBinnedInGenJet',
  histo_title = 'p_{t}^{' + triggerObjectName + '} distribution binned in p^{gen jet}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = genJetPtBins,
  nbins = 2000,
  min = 0,
  max = 2000,
  file_label = "tfile1",
  plot_func = pt,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{" + triggerObjectName + "} [GeV]",
  y_label = "# events",
  normalise = True
)

l1tObjectEtaDistributionBinnedInGenJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'l1tObjectEtaDistributionBinnedInGenJet',
  histo_name = 'l1tObjectEtaDistributionBinnedInGenJet',
  histo_title = '#eta^{' + triggerObjectName + '} distribution binned in p^{gen jet}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = genJetPtBins,
  nbins = 100,
  min = -10,
  max = +10,
  file_label = "tfile1",
  plot_func = eta,
  bin_func = pt,
  log_y = False,
  x_label = "#eta",
  y_label = "# events"
)

l1tObjectGenJetPtRatioDistributionBinnedInGenJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'l1tObjectGenJetPtRatioDistributionBinnedInGenJet',
  histo_name = 'l1tObjectGenJetPtRatioDistributionBinnedInGenJet',
  histo_title = 'p_{t}^{' + triggerObjectName + '}/p_{t}^{gen jet} distribution binned in p^{gen jet}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = genJetPtBins,
  nbins = 800,
  min = 0,
  max = 20,
  file_label = "tfile1",
  plot_func = ptRatioWithMatched,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{" + triggerObjectName + "}/p_{t}^{gen jet}",
  y_label = "# events"
)

deltaRDistributionBinnedInGenJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'deltaRDistributionBinnedInGenJet',
  histo_name = 'deltaRDistributionBinnedInGenJet',
  histo_title = '#DeltaR distribution binned in p^{gen jet}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = genJetPtBins,
  nbins = 300,
  min = 0,
  max = 15,
  file_label = "tfile1",
  plot_func = deltaR,
  bin_func = pt,
  log_y = False,
  x_label = "#DeltaR",
  y_label = "# events"
)

l1tObjectPtDistribution = cfg.Analyzer(
  Histogrammer,
  'l1tObjectPtDistribution',
  file_label = 'tfile1',
  histo_name = 'l1tObjectPtDistribution',
  histo_title = 'p_{t}^{' + triggerObjectName + '} distribution',
  min = 0,
  max = 300,
  nbins = 600,
  input_objects = 'matched_trigger_object',
  value_func = pt,
  x_label = "p_{t}^{" + triggerObjectName + "}",
  y_label = "\# events"
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  tightRestrictionMatchSelector,
  l1tObjectPtDistributionBinnedInGenJet,
  l1tObjectGenJetPtRatioDistributionBinnedInGenJet,
  l1tObjectEtaDistributionBinnedInGenJet,
  deltaRDistributionBinnedInGenJet,
  l1tObjectPtDistribution
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
