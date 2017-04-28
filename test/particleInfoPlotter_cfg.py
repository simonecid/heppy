'''Plots pt and leading pt in the event for every particle in the root file at both reco and gen levels'''

import os
import copy
import heppy.framework.config as cfg

from heppy.analyzers.Selector import Selector

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

comp = cfg.Component(
  'EWProductionAndHiggs',
  #files = ["../FCCSW/DelphesSim_ff_H_WW_enuenu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_H_WW_munumunu_1000events.root"]
  files = ["../FCCSW/DelphesSim_ff_H_ZZ_eeee_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_H_ZZ_mumumumu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_W_enu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_W_munu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_W_taunu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_Z_ee_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_Z_mumu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_Z_tautau_1000events.root"]
  #files = ["../FCCSW/mininumBiasDelphesSimulation_PU25_10evts.root"]
  #files = ["../FCCSW/minimumBias_10000evts.root"]
)
selectedComponents = [comp]

# Defining pdgids

pdgIds = {
  'electron-': 11,
  'muon-': 13,
  'tau-': 15,
  'photon': 22
}

from heppy.analyzers.fcc.Reader import Reader
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
  Creates partticle checker functions. 
  The function checks the absolute value of the pdgId to identify the class of particle and verifies that it is in the |eta|<6 region.
  It does not distinguish between particles and anti-particles
'''

def particleCheckerFactory (ptcName):
  def particleChecker (ptc):
    return (abs(ptc.pdgid()) == pdgIds[ptcName])
  return particleChecker

# All my stuff will be saved in this file

from ROOT import gSystem
gSystem.Load("libdatamodelDict")

from EventStore import EventStore as Events

from heppy.framework.services.tfile import TFileService
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

etaGenJetSelector = cfg.Analyzer(
    Selector,
    'eta_genjet',
    output = 'gen_jets_eta_restricted',
    input_objects = 'gen_jets',
    filter_func = etaRestrictor
)

# Defining analysers for electrons

from heppy.analyzers.triggerrates.Histogrammer import Histogrammer

electronRecoPtDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'electronRecoPtDistribution',
  histo_title = 'Electron transverse momentum distribution (reco level)',
  min = 0,
  max = 500,
  nbins = 100,
  input_objects = 'electrons',
  value_func = pt,
  log_y = True
)

from heppy.analyzers.triggerrates.LeadingQuantityHistogrammer import LeadingQuantityHistogrammer

electronLeadingRecoPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  file_label = 'tfile1',
  histo_name = 'electronLeadingRecoPtDistribution',
  histo_title = 'Electron leading transverse momentum distribution (reco level)',
  min = 0,
  max = 500,
  nbins = 100,
  input_objects = 'electrons',
  key_func = pt,
  value_func = pt,
  log_y = True
)

electronLeadingRecoEtaDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  file_label = 'tfile1',
  histo_name = 'electronLeadingRecoEtaDistribution',
  histo_title = 'Electron leading eta distribution (reco level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'electrons',
  key_func = pt,
  value_func = eta,
  log_y = True
)

electronSelector = cfg.Analyzer(
    Selector,
    'sel_electrons',
    output = 'gen_electrons',
    input_objects = 'gen_particles',
    filter_func = particleCheckerFactory("electron-")
)

electronGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'electronGenPtDistribution',
  histo_title = 'Electron transverse momentum distribution (gen level)',
  min = 0,
  max = 100,
  nbins = 100,
  input_objects = 'gen_electrons',
  value_func = pt,
  log_y = True
)

# Muons

muonRecoPtDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'muonRecoPtDistribution',
  histo_title = 'Muon transverse momentum distribution (reco level)',
  min = 0,
  max = 500,
  nbins = 100,
  input_objects = 'muons',
  value_func = pt,
  log_y = True
)

muonLeadingRecoPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  file_label = 'tfile1',
  histo_name = 'muonLeadingRecoPtDistribution',
  histo_title = 'Muon leading transverse momentum distribution (reco level)',
  min = 0,
  max = 500,
  nbins = 100,
  input_objects = 'muons',
  key_func = pt,
  value_func = pt,
  log_y = True
)

muonLeadingRecoEtaDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  file_label = 'tfile1',
  histo_name = 'muonLeadingRecoEtaDistribution',
  histo_title = 'Muon leading eta distribution (reco level)',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'muons',
  key_func = pt,
  value_func = eta,
  log_y = True
)

muonSelector = cfg.Analyzer(
    Selector,
    'sel_muons',
    output = 'gen_muons',
    input_objects = 'gen_particles_eta_restricted',
    filter_func = particleCheckerFactory("muon-")
)

muonGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'muonGenPtDistribution',
  histo_title = 'Muon transverse momentum distribution (gen level)',
  min = 0,
  max = 100,
  nbins = 100,
  input_objects = 'gen_muons',
  value_func = pt,
  log_y = True
)

# Taus, only possible at gen level

tauSelector = cfg.Analyzer(
    Selector,
    'sel_taus',
    output = 'gen_taus',
    input_objects = 'gen_particles_eta_restricted',
    filter_func = particleCheckerFactory("tau-")
)

tauGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'tauGenPtDistribution',
  histo_title = 'Tau transverse momentum distribution (gen level)',
  min = 0,
  max = 100,
  nbins = 100,
  input_objects = 'gen_taus',
  value_func = pt,
  log_y = True
)

# Photons

photonRecoPtDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'photonRecoPtDistribution',
  histo_title = 'Photon transverse momentum distribution (reco level)',
  min = 0,
  max = 500,
  nbins = 100,
  input_objects = 'photons',
  value_func = pt,
  log_y = True
)

photonLeadingRecoPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  file_label = 'tfile1',
  histo_name = 'photonLeadingRecoPtDistribution',
  histo_title = 'Photon leading transverse momentum distribution (reco level)',
  min = 0,
  max = 500,
  nbins = 100,
  input_objects = 'photons',
  key_func = pt,
  value_func = pt,
  log_y = True
)

photonLeadingRecoEtaDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  file_label = 'tfile1',
  histo_name = 'photonLeadingRecoEtaDistribution',
  histo_title = 'Photon leading eta distribution (reco level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'photons',
  key_func = pt,
  value_func = eta,
  log_y = True
)

photonSelector = cfg.Analyzer(
    Selector,
    'sel_photons',
    output = 'gen_photons',
    input_objects = 'gen_particles_eta_restricted',
    filter_func = particleCheckerFactory("photon")
)

photonGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'photonGenPtDistribution',
  histo_title = 'Photon transverse momentum distribution (gen level)',
  min = 0,
  max = 100,
  nbins = 100,
  input_objects = 'gen_photons',
  value_func = pt,
  log_y = True
)

# Jets

jetRecoPtDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'jetRecoPtDistribution',
  histo_title = 'Jet transverse momentum distribution (reco level)',
  min = 0,
  max = 500,
  nbins = 100,
  input_objects = 'jets',
  value_func = pt,
  log_y = True
)

jetLeadingRecoPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  file_label = 'tfile1',
  histo_name = 'jetLeadingRecoPtDistribution',
  histo_title = 'Jet leading transverse momentum distribution (reco level)',
  min = 0,
  max = 500,
  nbins = 100,
  input_objects = 'jets',
  key_func = pt,
  value_func = pt,
  log_y = True
)

jetLeadingRecoEtaDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  file_label = 'tfile1',
  histo_name = 'jetLeadingRecoEtaDistribution',
  histo_title = 'Jet leading eta distribution (reco level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'jets',
  key_func = pt,
  value_func = eta,
  log_y = True
)

jetGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'jetGenPtDistribution',
  histo_title = 'Jet transverse momentum distribution (gen level)',
  min = 0,
  max = 500,
  nbins = 100,
  input_objects = 'gen_jets_eta_restricted',
  value_func = pt,
  log_y = True
)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  etaGenParticleSelector,
  etaGenJetSelector,
  electronSelector,
  muonSelector,
  tauSelector,
  photonSelector,
  electronRecoPtDistribution,
  electronLeadingRecoPtDistribution,
  electronLeadingRecoEtaDistribution,
  electronGenPtDistribution,
  muonRecoPtDistribution,
  muonLeadingRecoPtDistribution,
  muonLeadingRecoEtaDistribution,
  muonGenPtDistribution,
  tauGenPtDistribution,
  photonRecoPtDistribution,
  photonLeadingRecoPtDistribution,
  photonLeadingRecoEtaDistribution,
  photonGenPtDistribution,
  jetRecoPtDistribution,
  jetLeadingRecoPtDistribution,
  jetLeadingRecoEtaDistribution,
  jetGenPtDistribution
] )


config = cfg.Config(
  components = selectedComponents,
  sequence = sequence,
  services = [tfile_service_1],
  events_class = Events
)

if __name__ == '__main__':
  import sys
  from heppy.framework.looper import Looper

  def next():
      loop.process(loop.iEvent+1)

  loop = Looper( 'looper', config,
                 nEvents=100,
                 nPrint=0,
                 timeReport=True)
  loop.process(6)
  print loop.event
