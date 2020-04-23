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
from heppy.analyzers.triggerrates.ParticleTreeProducer import ParticleTreeProducer
from heppy.framework.heppy_loop import _heppyGlobalOptions

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

# Retrieving the sample to analyse

sampleName = _heppyGlobalOptions["sample"]
sample = globals()[sampleName]

#selectedComponents = [
#  MinBiasDistribution_100TeV_DelphesFCC_CMSJets,
#  MinBiasDistribution_13TeV_DelphesCMS_CMSJets,
#  HardQCD_PtBinned_10_30_GeV,
#  HardQCD_PtBinned_30_300_GeV,
#  HardQCD_PtBinned_300_500_GeV,
#  HardQCD_PtBinned_500_700_GeV,
#  HardQCD_PtBinned_700_900_GeV,
#  HardQCD_PtBinned_900_1000_GeV,
#]

selectedComponents = [
  sample
]

#selectedComponents = [
#  MBtest
#]

# Defining pdgids

source = cfg.Analyzer(
  Reader,

  gen_particles = 'skimmedGenParticles',
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

def particleCheckerFactory (ptcName):
  def particleChecker (ptc):
    return (abs(ptc.pdgid()) == pdgIds[ptcName])
  return particleChecker

def etaRestrictor(ptc):
  return abs(ptc.eta()) < 6

etaGenParticleSelector = cfg.Analyzer(
    Selector,
    'eta_genparticle',
    output = 'gen_particles_eta_restricted',
    input_objects = 'gen_particles',
    filter_func = etaRestrictor
)

bQuarkSelector = cfg.Analyzer(
    Selector,
    'sel_bottom',
    output = 'b_quarks',
    input_objects = 'gen_particles_eta_restricted',
    filter_func = particleCheckerFactory("bottom")
)

tfile_service_1 = cfg.Service(
  TFileService,
  'tfile1',
  fname='histograms.root',
  option='recreate'
)

noRestrictionMuonBottomMatcher = cfg.Analyzer(
  Matcher,
  instance_label = 'noRestrictionMuonBottomMatcher',
  delta_r = 15,
  particles = 'muons',
  match_particles = 'b_quarks',
)

looseRestrictionMuonBottomMatcher = cfg.Analyzer(
  Matcher,
  instance_label = 'looseRestrictionMuonBottomMatcher',
  delta_r = 3,
  particles = 'muons',
  match_particles = 'b_quarks',
)

''' Selects around 48% of the noRestriction muons'''
mediumRestrictionMuonBottomMatcher = cfg.Analyzer(
  Matcher,
  instance_label = 'mediumRestrictionMuonBottomMatcher',
  delta_r = 1.5,
  particles = 'muons',
  match_particles = 'b_quarks',
)

''' Selects around 18% of the noRestriction muons'''
tightRestrictionMuonBottomMatcher = cfg.Analyzer(
  Matcher,
  instance_label = 'tightRestrictionMuonBottomMatcher',
  delta_r = 0.5,
  particles = 'muons',
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

def deltaR (ptc):
  return ptc.dr

def isMatched(ptc):
  return ptc.match is not None

matchedNoRestrictionMuonSelector = cfg.Analyzer(
  Selector,
  instance_label = 'matchedNoRestrictionMuonSelector',
  input_objects = 'muons',
  output = 'matchedMuons',
  filter_func = isMatched
)

matchedLooseRestrictionMuonSelector = cfg.Analyzer(
  Selector,
  instance_label = 'matchedLooseRestrictionMuonSelector',
  input_objects = 'muons',
  output = 'matchedMuons',
  filter_func = isMatched
)

matchedMediumRestrictionMuonSelector = cfg.Analyzer(
  Selector,
  instance_label = 'matchedMediumRestrictionMuonSelector',
  input_objects = 'muons',
  output = 'matchedMuons',
  filter_func = isMatched
)

matchedTightRestrictionMuonSelector = cfg.Analyzer(
  Selector,
  instance_label = 'matchedTightRestrictionMuonSelector',
  input_objects = 'muons',
  output = 'matchedMuons',
  filter_func = isMatched
)

deltaRNoRestrictionDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'deltaRNoRestrictionDistribution',
  file_label = 'tfile1',
  histo_name = 'deltaRNoRestrictionDistribution',
  histo_title = 'No-restriction muon-bottom #DeltaR distribution',
  min = 0,
  max = 15,
  nbins = 300,
  input_objects = 'matchedMuons',
  value_func = deltaR,
  x_label = "#DeltaR",
  y_label = "# events"
)

pairedNoRestrictionMuonPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedNoRestrictionMuonPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedNoRestrictionMuonPtDistribution',
  histo_title = 'No-restriction matched muon p_{t} distribution',
  min = 0,
  max = 100,
  nbins = 200,
  input_objects = 'matchedMuons',
  value_func = pt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedNoRestrictionMuonEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedNoRestrictionMuonEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedNoRestrictionMuonEtaDistribution',
  histo_title = 'No-restriction matched muon #eta distribution',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = eta,
  x_label = "#eta",
  y_label = "# events"
)

pairedNoRestrictionMuonPhiDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedNoRestrictionMuonPhiDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedNoRestrictionMuonPhiDistribution',
  histo_title = 'No-restriction matched muon #phi distribution',
  min = -3.15,
  max = +3.15,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = phi,
  x_label = "#phi",
  y_label = "# events"
)

pairedNoRestrictionBottomPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedNoRestrictionBottomPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedNoRestrictionBottomPtDistribution',
  histo_title = 'No-restriction matched bottom p_{t} distribution',
  min = 0,
  max = 300,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticlePt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedNoRestrictionBottomEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedNoRestrictionBottomEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedNoRestrictionBottomEtaDistribution',
  histo_title = 'No-restriction matched bottom #eta distribution',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticleEta,
  x_label = "#eta",
  y_label = "# events"
)

pairedNoRestrictionBottomPhiDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedNoRestrictionBottomPhiDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedNoRestrictionBottomPhiDistribution',
  histo_title = 'No-restriction matched bottom #phi distribution',
  min = -3.15,
  max = +3.15,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = phi,
  x_label = "#phi",
  y_label = "# events"
)

deltaRLooseRestrictionDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'deltaRLooseRestrictionDistribution',
  file_label = 'tfile1',
  histo_name = 'deltaRLooseRestrictionDistribution',
  histo_title = 'Loose-restriction muon-bottom #DeltaR distribution',
  min = 0,
  max = 15,
  nbins = 300,
  input_objects = 'matchedMuons',
  value_func = deltaR,
  x_label = "#DeltaR",
  y_label = "# events"
)

pairedLooseRestrictionMuonPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedLooseRestrictionMuonPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedLooseRestrictionMuonPtDistribution',
  histo_title = 'Loose-restriction matched muon p_{t} distribution',
  min = 0,
  max = 100,
  nbins = 200,
  input_objects = 'matchedMuons',
  value_func = pt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedLooseRestrictionMuonEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedLooseRestrictionMuonEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedLooseRestrictionMuonEtaDistribution',
  histo_title = 'Loose-restriction matched muon #eta distribution',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = eta,
  x_label = "#eta",
  y_label = "# events"
)

pairedLooseRestrictionMuonPhiDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedLooseRestrictionMuonPhiDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedLooseRestrictionMuonPhiDistribution',
  histo_title = 'Loose-restriction matched muon #phi distribution',
  min = -3.15,
  max = +3.15,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = phi,
  x_label = "#phi",
  y_label = "# events"
)

pairedLooseRestrictionBottomPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedLooseRestrictionBottomPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedLooseRestrictionBottomPtDistribution',
  histo_title = 'Loose-restriction matched bottom p_{t} distribution',
  min = 0,
  max = 300,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticlePt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedLooseRestrictionBottomEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedLooseRestrictionBottomEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedLooseRestrictionBottomEtaDistribution',
  histo_title = 'Loose-restriction matched bottom #eta distribution',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticleEta,
  x_label = "#eta",
  y_label = "# events"
)

pairedLooseRestrictionBottomPhiDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedLooseRestrictionBottomPhiDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedLooseRestrictionBottomPhiDistribution',
  histo_title = 'Loose-restriction matched bottom #phi distribution',
  min = -3.15,
  max = +3.15,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = phi,
  x_label = "#phi",
  y_label = "# events"
)

deltaRMediumRestrictionDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'deltaRMediumRestrictionDistribution',
  file_label = 'tfile1',
  histo_name = 'deltaRMediumRestrictionDistribution',
  histo_title = 'Medium-restriction muon-bottom #DeltaR distribution',
  min = 0,
  max = 15,
  nbins = 300,
  input_objects = 'matchedMuons',
  value_func = deltaR,
  x_label = "#DeltaR",
  y_label = "# events"
)

pairedMediumRestrictionMuonPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedMediumRestrictionMuonPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedMediumRestrictionMuonPtDistribution',
  histo_title = 'Medium-restriction matched muon p_{t} distribution',
  min = 0,
  max = 100,
  nbins = 200,
  input_objects = 'matchedMuons',
  value_func = pt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedMediumRestrictionMuonEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedMediumRestrictionMuonEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedMediumRestrictionMuonEtaDistribution',
  histo_title = 'Medium-restriction matched muon #eta distribution',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = eta,
  x_label = "#eta",
  y_label = "# events"
)

pairedMediumRestrictionMuonPhiDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedMediumRestrictionMuonPhiDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedMediumRestrictionMuonPhiDistribution',
  histo_title = 'Medium-restriction matched muon #phi distribution',
  min = -3.15,
  max = +3.15,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = phi,
  x_label = "#phi",
  y_label = "# events"
)

pairedMediumRestrictionBottomPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedMediumRestrictionBottomPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedMediumRestrictionBottomPtDistribution',
  histo_title = 'Medium-restriction matched bottom p_{t} distribution',
  min = 0,
  max = 300,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticlePt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedMediumRestrictionBottomEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedMediumRestrictionBottomEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedMediumRestrictionBottomEtaDistribution',
  histo_title = 'Medium-restriction matched bottom #eta distribution',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticleEta,
  x_label = "#eta",
  y_label = "# events"
)

pairedMediumRestrictionBottomPhiDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedMediumRestrictionBottomPhiDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedMediumRestrictionBottomPhiDistribution',
  histo_title = 'Medium-restriction matched bottom #phi distribution',
  min = -3.15,
  max = +3.15,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = phi,
  x_label = "#phi",
  y_label = "# events"
)

deltaRTightRestrictionDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'deltaRTightRestrictionDistribution',
  file_label = 'tfile1',
  histo_name = 'deltaRTightRestrictionDistribution',
  histo_title = 'Tight-restriction muon-bottom #DeltaR distribution',
  min = 0,
  max = 15,
  nbins = 300,
  input_objects = 'matchedMuons',
  value_func = deltaR,
  x_label = "#DeltaR",
  y_label = "# events"
)

pairedTightRestrictionMuonPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedTightRestrictionMuonPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedTightRestrictionMuonPtDistribution',
  histo_title = 'Tight-restriction matched muon p_{t} distribution',
  min = 0,
  max = 100,
  nbins = 200,
  input_objects = 'matchedMuons',
  value_func = pt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedTightRestrictionMuonEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedTightRestrictionMuonEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedTightRestrictionMuonEtaDistribution',
  histo_title = 'Tight-restriction matched muon #eta distribution',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = eta,
  x_label = "#eta",
  y_label = "# events"
)

pairedTightRestrictionMuonPhiDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedTightRestrictionMuonPhiDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedTightRestrictionMuonPhiDistribution',
  histo_title = 'Tight-restriction matched muon #phi distribution',
  min = -3.15,
  max = +3.15,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = phi,
  x_label = "#phi",
  y_label = "# events"
)

pairedTightRestrictionBottomPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedTightRestrictionBottomPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedTightRestrictionBottomPtDistribution',
  histo_title = 'Tight-restriction matched bottom p_{t} distribution',
  min = 0,
  max = 300,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticlePt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedTightRestrictionBottomEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedTightRestrictionBottomEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedTightRestrictionBottomEtaDistribution',
  histo_title = 'Tight-restriction matched bottom #eta distribution',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticleEta,
  x_label = "#eta",
  y_label = "# events"
)

pairedTightRestrictionBottomPhiDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedTightRestrictionBottomPhiDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedTightRestrictionBottomPhiDistribution',
  histo_title = 'Tight-restriction matched bottom #phi distribution',
  min = -3.15,
  max = +3.15,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = phi,
  x_label = "#phi",
  y_label = "# events"
)

muonPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label='muonPtDistribution',
  file_label = 'tfile1',
  histo_name = 'muonPtDistribution',
  histo_title = 'Muon p_{t} distribution',
  min = 0,
  max = 2000,
  nbins = 400,
  input_objects = 'muons',
  value_func = pt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

muonEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label='muonEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'muonEtaDistribution',
  histo_title = 'Muon #eta distribution',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'muons',
  value_func = eta,
  x_label = "#eta",
  y_label = "# events"
)

muonPhiDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label='muonPhiDistribution',
  file_label = 'tfile1',
  histo_name = 'muonPhiDistribution',
  histo_title = 'Muon #phi distribution',
  min = -3.15,
  max = +3.15,
  nbins = 100,
  input_objects = 'muons',
  value_func = phi,
  x_label = "#phi",
  y_label = "# events"
)

bottomPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'bottomPtDistribution',
  file_label = 'tfile1',
  histo_name = 'bottomPtDistribution',
  histo_title = 'Bottom p_{t} distribution',
  min = 0,
  max = 2000,
  nbins = 400,
  input_objects = 'b_quarks',
  value_func = pt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

bottomEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'bottomEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'bottomEtaDistribution',
  histo_title = 'Bottom #eta distribution',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'b_quarks',
  value_func = eta,
  x_label = "#eta",
  y_label = "# events"
)

bottomPhiDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label='bottomPhiDistribution',
  file_label = 'tfile1',
  histo_name = 'bottomPhiDistribution',
  histo_title = 'Bottom #phi distribution',
  min = -3.15,
  max = +3.15,
  nbins = 100,
  input_objects = 'b_quarks',
  value_func = phi,
  x_label = "#phi",
  y_label = "# events"
)

muonBottomTree = cfg.Analyzer(
    MatchedParticlesTreeProducer,
    file_label = "tfile1",
    tree_name = 'muonBottomTree',
    tree_title = 'Tree containing info about matched bottom and muons',
    matched_particle_collection = 'matchedMuons',
  )

bottomTree = cfg.Analyzer(
    ParticleTreeProducer,
    file_label = "tfile1",
    tree_name = 'bottomTree',
    tree_title = 'Tree containing info about bottoms',
    collection = 'b_quarks',
  )

muonTree = cfg.Analyzer(
    ParticleTreeProducer,
    file_label = "tfile1",
    tree_name = 'muonTree',
    tree_title = 'Tree containing info about muons',
    collection = 'muons',
  )

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  etaGenParticleSelector,
  bQuarkSelector,
  noRestrictionMuonBottomMatcher,
  matchedNoRestrictionMuonSelector,
  muonBottomTree,
  bottomTree,
  muonTree,
  deltaRNoRestrictionDistribution,
  pairedNoRestrictionMuonPtDistribution,
  pairedNoRestrictionMuonEtaDistribution,
  pairedNoRestrictionMuonPhiDistribution,
  pairedNoRestrictionBottomPtDistribution,
  pairedNoRestrictionBottomEtaDistribution,
  pairedNoRestrictionBottomPhiDistribution,
  looseRestrictionMuonBottomMatcher,
  matchedLooseRestrictionMuonSelector,
  deltaRLooseRestrictionDistribution,
  pairedLooseRestrictionMuonPtDistribution,
  pairedLooseRestrictionMuonEtaDistribution,
  pairedLooseRestrictionMuonPhiDistribution,
  pairedLooseRestrictionBottomPtDistribution,
  pairedLooseRestrictionBottomEtaDistribution,
  pairedLooseRestrictionBottomPhiDistribution,
  mediumRestrictionMuonBottomMatcher,
  matchedMediumRestrictionMuonSelector,
  deltaRMediumRestrictionDistribution,
  pairedMediumRestrictionMuonPtDistribution,
  pairedMediumRestrictionMuonEtaDistribution,
  pairedMediumRestrictionMuonPhiDistribution,
  pairedMediumRestrictionBottomPtDistribution,
  pairedMediumRestrictionBottomEtaDistribution,
  pairedMediumRestrictionBottomPhiDistribution,
  tightRestrictionMuonBottomMatcher,
  matchedTightRestrictionMuonSelector,
  deltaRTightRestrictionDistribution,
  pairedTightRestrictionMuonPtDistribution,
  pairedTightRestrictionMuonEtaDistribution,
  pairedTightRestrictionMuonPhiDistribution,
  pairedTightRestrictionBottomPtDistribution,
  pairedTightRestrictionBottomEtaDistribution,
  pairedTightRestrictionBottomPhiDistribution,
  muonPtDistribution,
  bottomPtDistribution,
  muonEtaDistribution,
  muonPhiDistribution,
  bottomEtaDistribution,
  bottomPhiDistribution,
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
