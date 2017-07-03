'''Plots pt and leading pt in the event for every particle in the root file at both reco and gen levels'''

import os
import copy
import heppy.framework.config as cfg
from heppy.test.mySamples import *
import logging
from heppy.analyzers.Selector import Selector
from heppy.analyzers.fcc.Reader import Reader
from ROOT import gSystem
from EventStore import EventStore as Events
from heppy.framework.services.tfile import TFileService
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
from heppy.analyzers.triggerrates.LeadingQuantityHistogrammer import LeadingQuantityHistogrammer
from heppy.analyzers.triggerrates.SubLeadingQuantityHistogrammer import SubLeadingQuantityHistogrammer
from heppy.analyzers.triggerrates.Histogrammer_2D import Histogrammer_2D
import sys
from heppy.framework.looper import Looper
from heppy.framework.heppy_loop import _heppyGlobalOptions

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

#selectedComponents = [
#  MinBiasDistribution_100TeV_DelphesFCC_CMSJets,
#  MinBiasDistribution_13TeV_DelphesCMS_CMSJets
#]

# Retrieving the sample to analyse

sampleName = _heppyGlobalOptions["sample"]
sample = globals()[sampleName]

selectedComponents = [
  sample
]

# Defining pdgids

pdgIds = {
  'electron-': 11,
  'muon-': 13,
  'tau-': 15,
  'photon': 22,
  'pion+': 211,
  'kaon+': 321,
  'kaon_long': 130,
  'kaon_short': 310,
}

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

'''
  Creates particle checker functions. 
  The function checks the absolute value of the pdgId to identify the class of particle and verifies that it is in the |eta|<6 region.
  It does not distinguish between particles and anti-particles
'''

def particleCheckerFactory (ptcName):
  def particleChecker (ptc):
    return (abs(ptc.pdgid()) == pdgIds[ptcName])
  return particleChecker

# All my stuff will be saved in this file

gSystem.Load("libdatamodelDict")


tfile_service_1 = cfg.Service(
  TFileService,
  'tfile1',
  fname='distributions.root',
  option='recreate'
)

''' Returns pt'''
def pt (ptc):
      return ptc.pt()

'''Returns eta'''
def eta (ptc):
      return ptc.eta()

'''Return PDGID'''
def pdgid(ptc):
  return ptc.pdgid()

# Restricting gen particles and jets in the abs(eta) < 6 region

def etaRestrictor(ptc):
  return abs(ptc.eta()) < 6

etaGenParticleSelector = cfg.Analyzer(
    Selector,
    'eta_genparticle',
    output = 'gen_particles_eta_restricted',
    input_objects = 'gen_particles',
    filter_func = etaRestrictor
)

#====================================================
# Defining analysers
#====================================================

pdgidsDistribution = cfg.Analyzer(
  Histogrammer,
  'pdgidDistribution',
  file_label = 'tfile1',
  x_label = "PGDID",
  y_label = "# particles",
  histo_name = 'pdgidDistribution',
  histo_title = 'PDGID distribution',
  min = -2000,
  max = 2000,
  nbins = 4000,
  input_objects = 'gen_particles_eta_restricted',
  value_func = pdgid,
  log_y = True
)

pionSelector = cfg.Analyzer(
    Selector,
    'sel_pions',
    output = 'gen_pions',
    input_objects = 'gen_particles_eta_restricted',
    filter_func = particleCheckerFactory("pion+")
)

chargedKaonSelector = cfg.Analyzer(
    Selector,
    'sel_charged_kaon',
    output = 'gen_charged_kaons',
    input_objects = 'gen_particles_eta_restricted',
    filter_func = particleCheckerFactory("kaon+")
)

kaonLongSelector = cfg.Analyzer(
    Selector,
    'sel_kaon_long',
    output = 'gen_kaons_long',
    input_objects = 'gen_particles_eta_restricted',
    filter_func = particleCheckerFactory("kaon_long")
)

kaonShortSelector = cfg.Analyzer(
    Selector,
    'sel_kaon_short',
    output = 'gen_kaons_short',
    input_objects = 'gen_particles_eta_restricted',
    filter_func = particleCheckerFactory("kaon_short")
)

pionGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  'pionGenPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'pionGenPtDistribution',
  histo_title = 'Pion transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 400,
  input_objects = 'gen_pions',
  value_func = pt,
  log_y = True
)

pionGenEtaDistribution = cfg.Analyzer(
  Histogrammer,
  'pionGenEtaDistribution',
  file_label = 'tfile1',
  x_label = "#eta",
  y_label = "# events",
  histo_name = 'pionGenEtaDistribution',
  histo_title = 'Pion eta distribution (gen level)',
  min = -10,
  max = 10,
  nbins = 200,
  input_objects = 'gen_pions',
  value_func = eta,
  log_y = True
)

chargedKaonGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  'chargedKaonGenPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'chargedKaonGenPtDistribution',
  histo_title = 'Charged kaon transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 400,
  input_objects = 'gen_charged_kaons',
  value_func = pt,
  log_y = True
)

chargedKaonGenEtaDistribution = cfg.Analyzer(
  Histogrammer,
  'chargedKaonGenEtaDistribution',
  file_label = 'tfile1',
  x_label = "#eta",
  y_label = "# events",
  histo_name = 'chargedKaonGenEtaDistribution',
  histo_title = 'Charged kaon eta distribution (gen level)',
  min = -10,
  max = 10,
  nbins = 200,
  input_objects = 'gen_charged_kaons',
  value_func = eta,
  log_y = True
)

kaonLongGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  'kaonLongGenPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'kaonLongGenPtDistribution',
  histo_title = 'K_{L} transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 400,
  input_objects = 'gen_kaons_long',
  value_func = pt,
  log_y = True
)

kaonLongGenEtaDistribution = cfg.Analyzer(
  Histogrammer,
  'kaonLongGenEtaDistribution',
  file_label = 'tfile1',
  x_label = "#eta",
  y_label = "# events",
  histo_name = 'kaonLongGenEtaDistribution',
  histo_title = 'K_{L} eta distribution (gen level)',
  min = -10,
  max = 10,
  nbins = 200,
  input_objects = 'gen_kaons_long',
  value_func = eta,
  log_y = True
)

kaonShortGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  'kaonShortGenPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'kaonShortGenPtDistribution',
  histo_title = 'K_{S} transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 400,
  input_objects = 'gen_kaons_short',
  value_func = pt,
  log_y = True
)

kaonShortGenEtaDistribution = cfg.Analyzer(
  Histogrammer,
  'kaonShortGenEtaDistribution',
  file_label = 'tfile1',
  x_label = "#eta",
  y_label = "# events",
  histo_name = 'kaonShortGenEtaDistribution',
  histo_title = 'K_{S} eta distribution (gen level)',
  min = -10,
  max = 10,
  nbins = 200,
  input_objects = 'gen_kaons_short',
  value_func = eta,
  log_y = True
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  etaGenParticleSelector,
  pdgidsDistribution,
  pionSelector,
  chargedKaonSelector,
  kaonLongSelector,
  kaonShortSelector,
  pionGenPtDistribution,
  pionGenEtaDistribution,
  chargedKaonGenPtDistribution,
  chargedKaonGenEtaDistribution,
  kaonLongGenPtDistribution,
  kaonLongGenEtaDistribution,
  kaonShortGenPtDistribution,
  kaonShortGenEtaDistribution,
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
