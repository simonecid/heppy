import os
import copy
import heppy.framework.config as cfg
from heppy.test.minBiasSamples import *
import logging
from heppy.analyzers.fcc.Reader import Reader
from EventStore import EventStore as Events
from heppy.framework.services.tfile import TFileService
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
from heppy.framework.looper import Looper
from heppy.analyzers.Matcher import Matcher
from heppy.analyzers.Selector import Selector
from heppy.analyzers.triggerrates.MatchedParticlesTreeProducer import MatchedParticlesTreeProducer

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

selectedComponents = [
  MinBiasDistribution_100TeV_DelphesFCC_CMSJets,
  MinBiasDistribution_13TeV_DelphesCMS_CMSJets
]

#selectedComponents = [
#  MBtest
#]

# Defining pdgids

source = cfg.Analyzer(
  Reader,

  gen_particles = 'skimmedGenParticles',
  #gen_vertices = 'genVertices',

  gen_jets = 'genJets',

  jets = 'jets',
  #bTags = 'bTags',
  #cTags = 'cTags',
  #tauTags = 'tauTags',

  electrons = 'electrons',
  electronITags = 'electronITags',

  muons = 'muons',
  muonITags = 'muonITags',

  photons = 'photons',
  met = 'met',
)

tfile_service_1 = cfg.Service(
  TFileService,
  'tfile1',
  fname='histograms.root',
  option='recreate'
)

noRestrictionMuonJetMatcher = cfg.Analyzer(
  Matcher,
  instance_label = 'noRestrictionMuonJetMatcher',
  delta_r = 10,
  particles = 'muons',
  match_particles = 'jets',
)

''' Selects around 48% of the noRestriction muons'''
looseRestrictionMuonJetMatcher = cfg.Analyzer(
  Matcher,
  instance_label = 'looseRestrictionMuonJetMatcher',
  delta_r = 1.5,
  particles = 'muons',
  match_particles = 'jets',
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
  histo_title = 'No-restriction nuon-jet #DeltaR distribution',
  min = 0,
  max = 10,
  nbins = 200,
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

pairedNoRestrictionJetPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedNoRestrictionJetPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedNoRestrictionJetPtDistribution',
  histo_title = 'No-restriction matched jet p_{t} distribution',
  min = 0,
  max = 300,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticlePt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedNoRestrictionJetEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedNoRestrictionJetEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedNoRestrictionJetEtaDistribution',
  histo_title = 'No-restriction matched jet #eta distribution',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticleEta,
  x_label = "#eta",
  y_label = "# events"
)

deltaRLooseRestrictionDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'deltaRLooseRestrictionDistribution',
  file_label = 'tfile1',
  histo_name = 'deltaRLooseRestrictionDistribution',
  histo_title = 'Loose-restriction muon-jet #DeltaR distribution',
  min = 0,
  max = 10,
  nbins = 200,
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

pairedLooseRestrictionJetPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedLooseRestrictionJetPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedLooseRestrictionJetPtDistribution',
  histo_title = 'Loose-restriction matched jet p_{t} distribution',
  min = 0,
  max = 300,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticlePt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedLooseRestrictionJetEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedLooseRestrictionJetEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedLooseRestrictionJetEtaDistribution',
  histo_title = 'Loose-restriction matched jet #eta distribution',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticleEta,
  x_label = "#eta",
  y_label = "# events"
)

deltaRTightRestrictionDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'deltaRTightRestrictionDistribution',
  file_label = 'tfile1',
  histo_name = 'deltaRTightRestrictionDistribution',
  histo_title = 'Tight-restriction muon-jet #DeltaR distribution',
  min = 0,
  max = 10,
  nbins = 200,
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

pairedTightRestrictionJetPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedTightRestrictionJetPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedTightRestrictionJetPtDistribution',
  histo_title = 'Tight-restriction matched jet p_{t} distribution',
  min = 0,
  max = 300,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticlePt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedTightRestrictionJetEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedTightRestrictionJetEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedTightRestrictionJetEtaDistribution',
  histo_title = 'Tight-restriction matched jet #eta distribution',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticleEta,
  x_label = "#eta",
  y_label = "# events"
)

muonPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label='muonPtDistribution',
  file_label = 'tfile1',
  histo_name = 'muonPtDistribution',
  histo_title = 'Muon p_{t} distribution',
  min = 0,
  max = 100,
  nbins = 200,
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

jetPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'jetPtDistribution',
  file_label = 'tfile1',
  histo_name = 'jetPtDistribution',
  histo_title = 'Jet p_{t} distribution',
  min = 0,
  max = 300,
  nbins = 100,
  input_objects = 'jets',
  value_func = pt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

jetEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'jetEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'jetEtaDistribution',
  histo_title = 'Jet #eta distribution',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'jets',
  value_func = eta,
  x_label = "#eta",
  y_label = "# events"
)

noRestrictionMuonJetTree = cfg.Analyzer(
    MatchedParticlesTreeProducer,
    file_label = "tfile1",
    tree_name = 'noRestrictionMuonJetTree',
    tree_title = 'Tree containing info about matched jet and muons',
    matched_particle_collection = 'matchedMuons',
  )

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  noRestrictionMuonJetMatcher,
  matchedNoRestrictionMuonSelector,
  noRestrictionMuonJetTree,
  deltaRNoRestrictionDistribution,
  pairedNoRestrictionMuonPtDistribution,
  pairedNoRestrictionMuonEtaDistribution,
  pairedNoRestrictionJetPtDistribution,
  pairedNoRestrictionJetEtaDistribution,
  looseRestrictionMuonJetMatcher,
  matchedLooseRestrictionMuonSelector,
  deltaRLooseRestrictionDistribution,
  pairedLooseRestrictionMuonPtDistribution,
  pairedLooseRestrictionMuonEtaDistribution,
  pairedLooseRestrictionJetPtDistribution,
  pairedLooseRestrictionJetEtaDistribution,
  tightRestrictionMuonJetMatcher,
  matchedTightRestrictionMuonSelector,
  deltaRTightRestrictionDistribution,
  pairedTightRestrictionMuonPtDistribution,
  pairedTightRestrictionMuonEtaDistribution,
  pairedTightRestrictionJetPtDistribution,
  pairedTightRestrictionJetEtaDistribution,
  muonPtDistribution,
  jetPtDistribution,
  muonEtaDistribution,
  jetEtaDistribution
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
