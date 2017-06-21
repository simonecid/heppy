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

muonJetMatcher = cfg.Analyzer(
  Matcher,
  instance_label = 'muonJetMatcher',
  delta_r = 10,
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

matchedMuonSelector = cfg.Analyzer(
  Selector,
  instance_label = 'matchedMuonSelector',
  input_objects = 'muons',
  output = 'matchedMuons',
  filter_func = isMatched
)

deltaRDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'deltaRDistribution',
  file_label = 'tfile1',
  histo_name = 'deltaRDistribution',
  histo_title = 'Muon-jet #DeltaR distribution',
  min = 0,
  max = 10,
  nbins = 200,
  input_objects = 'matchedMuons',
  value_func = deltaR,
  x_label = "#DeltaR",
  y_label = "# events"
)

pairedMuonPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label='pairedMuonPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedMuonPtDistribution',
  histo_title = 'Matched muon p_{t} distribution',
  min = 0,
  max = 100,
  nbins = 200,
  input_objects = 'matchedMuons',
  value_func = pt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedMuonEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label='pairedMuonEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedMuonEtaDistribution',
  histo_title = 'Matched muon #eta distribution',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = eta,
  x_label = "#eta",
  y_label = "# events"
)

pairedJetPtDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedJetPtDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedJetPtDistribution',
  histo_title = 'Matched jet p_{t} distribution',
  min = 0,
  max = 300,
  nbins = 100,
  input_objects = 'matchedMuons',
  value_func = matchedParticlePt,
  x_label = "p_{t} [GeV]",
  y_label = "# events"
)

pairedJetEtaDistribution = cfg.Analyzer(
  Histogrammer,
  instance_label = 'pairedJetEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'pairedJetEtaDistribution',
  histo_title = 'Matched jet #eta distribution',
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

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  muonJetMatcher,
  matchedMuonSelector,
  deltaRDistribution,
  pairedMuonPtDistribution,
  pairedMuonEtaDistribution,
  pairedJetPtDistribution,
  pairedJetEtaDistribution,
  muonPtDistribution,
  jetPtDistribution,
  muonEtaDistribution,
  jetEtaDistribution,
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
