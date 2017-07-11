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
from heppy.analyzers.triggerrates.ObjectFinder import ObjectFinder
from heppy.analyzers.triggerrates.HistogrammerCumulative import HistogrammerCumulative
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

pdgIds = {
  'electron-': 11,
  'muon-': 13,
  'tau-': 15,
  'photon': 22,
  'pion+': 211,
  'kaon+': 321,
  'kaon_long': 130,
  'kaon_short': 310,
  'bottom': 5
}

# Defining pdgids

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

tfile_service_1 = cfg.Service(
  TFileService,
  'tfile1',
  fname='histograms.root',
  option='recreate'
)

tightRestrictionJetBottomMatcher = cfg.Analyzer(
  Matcher,
  instance_label = 'tightRestrictionJetBottomMatcher',
  delta_r = 0.5,
  particles = 'b_quarks',
  match_particles = 'jets',
)

tightRestrictionJetBottomFinder = cfg.Analyzer(
  ObjectFinder,
  instance_label = 'tightRestrictionJetBottomFinder',
  delta_r = 0.5,
  particles = 'jets',
  match_particles = 'b_quarks',
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

def hasMatches(ptc):
  return len(ptc.matches) > 0

def particleCheckerFactory (ptcName):
  def particleChecker (ptc):
    return (abs(ptc.pdgid()) == pdgIds[ptcName])
  return particleChecker

def getFinalStateBQuark (ptc):
  return (abs(ptc.pdgid()) == 5) and (ptc.status() == 71)

matchedTightRestrictionBottomSelector = cfg.Analyzer(
  Selector,
  instance_label = 'matchedTightRestrictionBottomSelector',
  input_objects = 'b_quarks',
  output = 'matched_b_quarks',
  filter_func = isMatched
)

matchedTightRestrictionJetSelector = cfg.Analyzer(
  Selector,
  instance_label = 'matchedTightRestrictionJetSelector',
  input_objects = 'jets',
  output = 'matched_jets',
  filter_func = hasMatches
)

def etaRestrictor(ptc):
  return abs(ptc.eta()) < 6

def etaPtRestrictor(ptc):
  return (abs(ptc.eta()) < 6 and ptc.pt() > 30)


etaGenParticleSelector = cfg.Analyzer(
    Selector,
    'eta_genparticle',
    output = 'gen_particles_eta_restricted',
    input_objects = 'gen_particles',
    filter_func = etaRestrictor
)

genJetSelector = cfg.Analyzer(
    Selector,
    'genJetSelector',
    output = 'jets',
    input_objects = 'gen_jets',
    filter_func = etaPtRestrictor
)

bQuarkSelector = cfg.Analyzer(
    Selector,
    'sel_bottom',
    output = 'b_quarks',
    input_objects = 'gen_particles_eta_restricted',
    filter_func = getFinalStateBQuark
)

bottomPtDistributionBinnedInMatchedJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'bottomPtDistributionBinnedInMatchedJet',
  histo_name = 'bottomPtDistributionBinnedInMatchedJet',
  histo_title = 'p_{t}^{b} distribution binned in p^{jet}_{t}',
  matched_collection = 'matched_b_quarks',
  binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
  nbins = 2000,
  min = 0,
  max = 2000,
  file_label = "tfile1",
  plot_func = pt,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{b} [GeV]",
  y_label = "# events"
)

bottomEtaDistributionBinnedInMatchedJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'bottomEtaDistributionBinnedInMatchedJet',
  histo_name = 'bottomEtaDistributionBinnedInMatchedJet',
  histo_title = '#eta^{b} distribution binned in p^{jet}_{t}',
  matched_collection = 'matched_b_quarks',
  binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
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

jetPtDistributionBinnedInMatchedJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'jetPtDistributionBinnedInMatchedJet',
  histo_name = 'jetPtDistributionBinnedInMatchedJet',
  histo_title = 'p_{jet}^{b} distribution binned in p^{jet}_{t}',
  matched_collection = 'matched_b_quarks',
  binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
  nbins = 2500,
  min = 0,
  max = 2500,
  file_label = "tfile1",
  plot_func = matchedParticlePt,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{jet} [GeV]",
  y_label = "# events"
)

bottomJetPtRatioDistributionBinnedInMatchedJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'bottomJetPtRatioDistributionBinnedInMatchedJet',
  histo_name = 'bottomJetPtRatioDistributionBinnedInMatchedJet',
  histo_title = 'p_{t}^{b}/p_{t}^{jet} distribution binned in p^{jet}_{t}',
  matched_collection = 'matched_b_quarks',
  binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
  nbins = 800,
  min = 0,
  max = 20,
  file_label = "tfile1",
  plot_func = ptRatioWithMatched,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{b}/p_{t}^{jet}",
  y_label = "# events"
)

deltaRDistributionBinnedInMatchedJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'deltaRDistributionBinnedInMatchedJet',
  histo_name = 'deltaRDistributionBinnedInMatchedJet',
  histo_title = '#DeltaR distribution binned in p^{jet}_{t}',
  matched_collection = 'matched_b_quarks',
  binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
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


def totalPtFractionCarriedByMatchedParticles(ptc):
  totFraction = 0
  if len(ptc.matches) > 1:
    for b_q in ptc.matches:
      totFraction += (b_q.pt()/ptc.pt())
    return totFraction
  return None

def totalPtFractionCarriedByMatchedParticles_2(ptc):
  jet = ptc.match
  totFraction = 0
  if not hasattr(jet, "isPtFractionPlotted"):
    jet.isPtFractionPlotted = True
    if len(jet.matches) > 1:
      for b_q in jet.matches:
        totFraction += (b_q.pt()/jet.pt())
      return totFraction
  return None

def numberOfFoundParticles_2(ptc):
  jet = ptc.match
  totFraction = 0
  if not hasattr(jet, "isNumberOfFoundParticlesPlotted"):
    jet.isNumberOfFoundParticlesPlotted = True
    return len(jet.matches)
  return None

totalBottomJetPtRatioDistributionBinnedInMatchedJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'totalBottomJetPtRatioDistributionBinnedInMatchedJet',
  histo_name = 'totalBottomJetPtRatioDistributionBinnedInMatchedJet',
  histo_title = 'Total p_{t} fraction carried by the matched bottom quarks binned in p^{jet}_{t}',
  matched_collection = 'matched_b_quarks',
  binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
  nbins = 800,
  min = 0,
  max = 20,
  file_label = "tfile1",
  plot_func = totalPtFractionCarriedByMatchedParticles_2,
  bin_func = pt,
  log_y = False,
  x_label = "#sum p_{t}^{b} / p_{t}^{jet}",
  y_label = "# events"
)

numberOfBottomQuarksDistributionBinnedInMatchedJet = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'numberOfBottomQuarksDistributionBinnedInMatchedJet',
  histo_name = 'numberOfBottomQuarksDistributionBinnedInMatchedJet',
  histo_title = 'Number of matched bottom quarks binned in p^{jet}_{t}',
  matched_collection = 'matched_b_quarks',
  binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
  min = 0,
  max = 100,
  nbins = 100,
  file_label = "tfile1",
  plot_func = numberOfFoundParticles_2,
  bin_func = pt,
  log_y = False,
  x_label = "# b quarks",
  y_label = "# events"
)

totalPtFractionCarriedByBottomQuarksDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'totalPtFractionCarriedByBottomQuarksDistribution',
  histo_title = 'Total p_{t} fraction carried by the matched bottom quarks',
  min = 0,
  max = 20,
  nbins = 800,
  input_objects = 'matched_jets',
  value_func = totalPtFractionCarriedByMatchedParticles,
  x_label = "#sum p_{t}^{b} / p_{t}^{jet}",
  y_label = "# events"
)

def numberOfFoundParticles(ptc):
  return len(ptc.matches)

bottomJetPtRatioDistributionBinnedInNumberOfFoundBQuarks = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'bottomJetPtRatioDistributionBinnedInNumberOfFoundBQuarks',
  histo_name = 'bottomJetPtRatioDistributionBinnedInNumberOfFoundBQuarks',
  histo_title = 'p_{t}^{b}/p_{t}^{jet} distribution binned in n of found b quarks',
  matched_collection = 'matched_b_quarks',
  binning = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  min = 0,
  max = 20,
  nbins = 800,
  file_label = "tfile1",
  plot_func = ptRatioWithMatched,
  bin_func = numberOfFoundParticles,
  log_y = False,
  x_label = "p_{t}^{b}/p_{t}^{jet}",
  y_label = "# events"
)

numberOfMatchedBottomQuarksDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'numberOfMatchedBottomQuarksDistribution',
  histo_title = 'Number of bottom quarks within the jet cone',
  min = 0,
  max = 100,
  nbins = 100,
  input_objects = 'matched_jets',
  value_func = numberOfFoundParticles,
  x_label = "# b quarks",
  y_label = "# events"
)

bottomJetTree = cfg.Analyzer(
  MatchedParticlesTreeProducer,
  file_label = "tfile1",
  tree_name = 'bottomJetTree',
  tree_title = 'Tree containing info about matched jet and bottoms',
  matched_particle_collection = 'matched_b_quarks',
  particle_name = "b_quark",
  matched_particle_name = "jet"
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  etaGenParticleSelector,
  genJetSelector,
  bQuarkSelector,
  tightRestrictionJetBottomMatcher,
  tightRestrictionJetBottomFinder,
  matchedTightRestrictionBottomSelector,
  matchedTightRestrictionJetSelector,
  jetPtDistributionBinnedInMatchedJet,
  bottomPtDistributionBinnedInMatchedJet,
  bottomJetPtRatioDistributionBinnedInMatchedJet,
  bottomEtaDistributionBinnedInMatchedJet,
  deltaRDistributionBinnedInMatchedJet,
  totalBottomJetPtRatioDistributionBinnedInMatchedJet,
  numberOfBottomQuarksDistributionBinnedInMatchedJet,
  bottomJetPtRatioDistributionBinnedInNumberOfFoundBQuarks,
  totalPtFractionCarriedByBottomQuarksDistribution,
  numberOfMatchedBottomQuarksDistribution,
  bottomJetTree
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
