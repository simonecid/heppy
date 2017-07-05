import os
import copy
import heppy.framework.config as cfg
from heppy.test.mySamples import *
import logging
from heppy.analyzers.fcc.Reader import Reader
from EventStore import EventStore as Events
from heppy.framework.services.tfile import TFileService
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
from heppy.framework.looper import Looper
from heppy.analyzers.Matcher import Matcher
from heppy.analyzers.Selector import Selector
from heppy.analyzers.triggerrates.MatchedParticlesTreeProducer import MatchedParticlesTreeProducer
from heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions import MatchedObjectBinnedDistributions
from heppy.framework.heppy_loop import _heppyGlobalOptions

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

# Retrieving the sample to analyse

#if specified in sample, a specific set will be used, otherwise the full set will be employed
if "sample" in _heppyGlobalOptions:
  sampleName = _heppyGlobalOptions["sample"]
  if sampleName == "all":
    selectedComponents = [
      MinBiasDistribution_100TeV_DelphesFCC_CMSJets,
      HardQCD_100TeV_PtBinned_10_30_GeV,
      HardQCD_100TeV_PtBinned_30_300_GeV,
      HardQCD_100TeV_PtBinned_300_500_GeV,
      HardQCD_100TeV_PtBinned_500_700_GeV,
      HardQCD_100TeV_PtBinned_700_900_GeV,
      HardQCD_100TeV_PtBinned_900_1000_GeV,
      HardQCD_100TeV_PtBinned_900_1400_GeV,
      HardQCD_100TeV_PtBinned_1400_2000_GeV,
    ]
  else:  
    sample = globals()[sampleName]
    selectedComponents = [
      sample
    ]
else:
  selectedComponents = [
    MinBiasDistribution_100TeV_DelphesFCC_CMSJets,
    HardQCD_100TeV_PtBinned_10_30_GeV,
    HardQCD_100TeV_PtBinned_30_300_GeV,
    HardQCD_100TeV_PtBinned_300_500_GeV,
    HardQCD_100TeV_PtBinned_500_700_GeV,
    HardQCD_100TeV_PtBinned_700_900_GeV,
    HardQCD_100TeV_PtBinned_900_1000_GeV,
    HardQCD_100TeV_PtBinned_900_1400_GeV,
    HardQCD_100TeV_PtBinned_1400_2000_GeV,
  ]

# Defining pdgids

source = cfg.Analyzer(
  Reader,

  #gen_particles = 'skimmedGenParticles',
  #gen_vertices = 'genVertices',

  #gen_jets = 'genJets',

  jets = 'jets',
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

tfile_service_1 = cfg.Service(
  TFileService,
  'tfile1',
  fname='histograms.root',
  option='recreate'
)

''' Selects around 18% of the noRestriction muons'''
tightRestrictionMuonJetMatcher = cfg.Analyzer(
  Matcher,
  instance_label = 'tightRestrictionMuonJetMatcher',
  delta_r = 0.5,
  particles = 'muons',
  match_particles = 'jets',
)

def pt (ptc):
  return ptc.pt()

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
  return ptc.dr

def isMatched(ptc):
  return ptc.match is not None

matchedTightRestrictionMuonSelector = cfg.Analyzer(
  Selector,
  instance_label = 'matchedTightRestrictionMuonSelector',
  input_objects = 'muons',
  output = 'matched_muons',
  filter_func = isMatched
)

muonPtDistributionBinnedInMatchedJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'muonPtDistributionBinnedInMatchedJet',
  histo_name = 'muonPtDistributionBinnedInMatchedJet',
  histo_title = 'p_{t}^{#mu} distribution binned in p^{jet}_{t}',
  matched_collection = 'matched_muons',
  binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
  nbins = 1000,
  min = 0,
  max = 1000,
  file_label = "tfile1",
  value_func = pt,
  bin_func = pt,
  log_y = True,
  x_label = "p_{t}^{#mu} [GeV]",
  y_label = "\# events"
)

muonEtaDistributionBinnedInMatchedJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'muonEtaDistributionBinnedInMatchedJet',
  histo_name = 'muonEtaDistributionBinnedInMatchedJet',
  histo_title = '#eta^{#mu} distribution binned in p^{jet}_{t}',
  matched_collection = 'matched_muons',
  binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
  nbins = 100,
  min = -10,
  max = +10,
  file_label = "tfile1",
  value_func = eta,
  bin_func = pt,
  log_y = True,
  x_label = "#eta",
  y_label = "\# events"
)

jetPtDistributionBinnedInMatchedJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'jetPtDistributionBinnedInMatchedJet',
  histo_name = 'jetPtDistributionBinnedInMatchedJet',
  histo_title = 'p_{t}^{jet} distribution binned in p^{jet}_{t}',
  matched_collection = 'matched_muons',
  binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
  nbins = 2500,
  min = 0,
  max = 2500,
  file_label = "tfile1",
  value_func = matchedParticlePt,
  bin_func = pt,
  log_y = True,
  x_label = "p_{t}^{jet} [GeV]",
  y_label = "\# events"
)

muonJetPtRatioDistributionBinnedInMatchedJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'muonJetPtRatioDistributionBinnedInMatchedJet',
  histo_name = 'muonJetPtRatioDistributionBinnedInMatchedJet',
  histo_title = 'p_{t}^{#mu}/p_{t}^{jet} distribution binned in p^{jet}_{t}',
  matched_collection = 'matched_muons',
  binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
  nbins = 60,
  min = 0,
  max = 1.5,
  file_label = "tfile1",
  value_func = ptRatioWithMatched,
  bin_func = pt,
  log_y = True,
  x_label = "p_{t}^{#mu}/p_{t}^{jet}",
  y_label = "\# events"
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  tightRestrictionMuonJetMatcher,
  matchedTightRestrictionMuonSelector,
  muonPtDistributionBinnedInMatchedJet,
  muonEtaDistributionBinnedInMatchedJet,
  jetPtDistributionBinnedInMatchedJet,
  muonJetPtRatioDistributionBinnedInMatchedJet,
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
