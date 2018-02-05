'''Plots pt and leading pt in the event for every particle in the root file at both reco and gen levels'''

import os
import copy
import heppy.framework.config as cfg
from heppy.samples.mySamples import *
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
from heppy.samples.sample_MinimumBias_NoTau_14TeV_GenParticles import *
from heppy.samples.sample_NeutrinoGun_PU140_14TeV_OnlyGenParticleClassification_JetPTMin_3_PropagatedGenJetAtECAL import *
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


#sampleName = _heppyGlobalOptions["sample"]
#sample = globals()[sampleName]

test_classification = cfg.MCComponent(
  'test_classification_1kevents',
  files = ["../FCCSW/test_classification_1kevents.root"]
)

selectedComponents = [
    NeutrinoGun_PU140_14TeV_OnlyGenParticleClassification_JetPTMin_3_PropagatedGenJetAtECAL
]

# Defining pdgids

pdgIds = {
  'electron-': 11,
  'muon-': 13,
  'tau-': 15,
  'photon': 22
}

source = cfg.Analyzer(
  Reader,

  #gen_particles = 'skimmedGenParticles',

  gen_jets = 'nonPropagatedGenJets',
  jets = 'propagatedGenJets',

  #electrons = 'genElectrons',

  #muons = 'genMuons',

  #photons = 'genPhotons',
  #met = 'genMET',
)

'''
  Creates particle checker functions. 
  The function checks the absolute value of the pdgId to identify the class of particle and verifies that it is in the |eta|<6 region.
  It does not distinguish between particles and anti-particles
'''

def particleCheckerFactory (ptcName):
  def particleChecker (ptc):
    if (abs(ptc.pdgid()) == pdgIds[ptcName]):
      import pdb; pdb.set_trace()
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

# Restricting gen particles and jets in the abs(eta) < 6 region

def etaRestrictor(ptc):
  return abs(ptc.eta()) < 5.1
#def etaRestrictor(ptc):
#  return True

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

#====================================================
# Defining analysers for electrons
#====================================================


electronRecoPtDistribution = cfg.Analyzer(
  Histogrammer,
  'electronRecoPtDistribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'electronRecoPtDistribution',
  histo_title = 'Electron transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'electrons',
  value_func = pt,
  log_y = True
)


electronLeadingRecoPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'electronLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'electronLeadingRecoPtDistribution',
  histo_title = 'Electron leading transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'electrons',
  key_func = pt,
  value_func = pt,
  log_y = True
)

electronLeadingRecoEtaDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'electronLeadingRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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

electronSubLeadingRecoPtDistribution = cfg.Analyzer(
  SubLeadingQuantityHistogrammer,
  'electronSubLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'electronSubLeadingRecoPtDistribution',
  histo_title = 'Electron sub-leading transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'electrons',
  key_func = pt,
  value_func = pt,
  log_y = True
)

electronSubLeadingRecoEtaDistribution = cfg.Analyzer(
  SubLeadingQuantityHistogrammer,
  'electronSubLeadingRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'electronSubLeadingRecoEtaDistribution',
  histo_title = 'Electron sub-leading eta distribution (reco level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'electrons',
  key_func = pt,
  value_func = eta,
  log_y = True
)

electronRecoEtaDistribution = cfg.Analyzer(
  Histogrammer,
  'electronRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'electronRecoEtaDistribution',
  histo_title = 'Electron eta distribution (reco level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'electrons',
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
  'electronGenPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'electronGenPtDistribution',
  histo_title = 'Electron transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'gen_electrons',
  value_func = pt,
  log_y = True
)

#====================================================
# Muons
#====================================================

muonRecoPtDistribution = cfg.Analyzer(
  Histogrammer,
  'muonRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'muonRecoPtDistribution',
  histo_title = 'Muon transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'muons',
  value_func = pt,
  log_y = True
)

muonLeadingRecoPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'muonLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'muonLeadingRecoPtDistribution',
  histo_title = 'Muon leading transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'muons',
  key_func = pt,
  value_func = pt,
  log_y = True
)

muonLeadingRecoEtaDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'muonLeadingRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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

muonSubLeadingRecoPtDistribution = cfg.Analyzer(
  SubLeadingQuantityHistogrammer,
  'muonSubLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'muonSubLeadingRecoPtDistribution',
  histo_title = 'Muon sub-leading transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'muons',
  key_func = pt,
  value_func = pt,
  log_y = True
)

muonSubLeadingRecoEtaDistribution = cfg.Analyzer(
  SubLeadingQuantityHistogrammer,
  'muonSubLeadingRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'muonSubLeadingRecoEtaDistribution',
  histo_title = 'Muon sub-leading eta distribution (reco level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'muons',
  key_func = pt,
  value_func = eta,
  log_y = True
)

muonRecoEtaDistribution = cfg.Analyzer(
  Histogrammer,
  'muonRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'muonRecoEtaDistribution',
  histo_title = 'Muon eta distribution (reco level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'muons',
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
  'muonGenPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'muonGenPtDistribution',
  histo_title = 'Muon transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 4000,
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
  'tauGenPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'tauGenPtDistribution',
  histo_title = 'Tau transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'gen_taus',
  value_func = pt,
  log_y = True
)

#====================================================
# Photons
#====================================================

photonRecoPtDistribution = cfg.Analyzer(
  Histogrammer,
  'photonRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'photonRecoPtDistribution',
  histo_title = 'Photon transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'photons',
  value_func = pt,
  log_y = True
)

photonLeadingRecoPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'photonLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'photonLeadingRecoPtDistribution',
  histo_title = 'Photon leading transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'photons',
  key_func = pt,
  value_func = pt,
  log_y = True
)

photonLeadingRecoEtaDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'photonLeadingRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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

photonSubLeadingRecoPtDistribution = cfg.Analyzer(
  SubLeadingQuantityHistogrammer,
  'photonSubLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'photonSubLeadingRecoPtDistribution',
  histo_title = 'Photon sub-leading transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'photons',
  key_func = pt,
  value_func = pt,
  log_y = True
)

photonSubLeadingRecoEtaDistribution = cfg.Analyzer(
  SubLeadingQuantityHistogrammer,
  'photonSubLeadingRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'photonSubLeadingRecoEtaDistribution',
  histo_title = 'Photon sub-leading eta distribution (reco level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'photons',
  key_func = pt,
  value_func = eta,
  log_y = True
)

photonRecoEtaDistribution = cfg.Analyzer(
  Histogrammer,
  'photonRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'photonRecoEtaDistribution',
  histo_title = 'Photon eta distribution (reco level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'photons',
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
  'photonGenPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'photonGenPtDistribution',
  histo_title = 'Photon transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'gen_photons',
  value_func = pt,
  log_y = True
)

#====================================================
# Jets
#====================================================

jetRecoPtDistribution = cfg.Analyzer(
  Histogrammer,
  'jetRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'jetRecoPtDistribution',
  histo_title = 'Jet transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'jets',
  value_func = pt,
  log_y = True
)

jetLeadingRecoPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'jetLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'jetLeadingRecoPtDistribution',
  histo_title = 'Jet leading transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'jets',
  key_func = pt,
  value_func = pt,
  log_y = True
)

jetLeadingRecoEtaDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'jetLeadingRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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

jetSubLeadingRecoPtDistribution = cfg.Analyzer(
  SubLeadingQuantityHistogrammer,
  'jetSubLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'jetSubLeadingRecoPtDistribution',
  histo_title = 'Jet sub-leading transverse momentum distribution (reco level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'jets',
  key_func = pt,
  value_func = pt,
  log_y = True
)

jetSubLeadingRecoEtaDistribution = cfg.Analyzer(
  SubLeadingQuantityHistogrammer,
  'jetSubLeadingRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'jetSubLeadingRecoEtaDistribution',
  histo_title = 'Jet sub-leading eta distribution (reco level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'jets',
  key_func = pt,
  value_func = eta,
  log_y = True
)

jetRecoEtaDistribution = cfg.Analyzer(
  Histogrammer,
  'jetRecoEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'jetRecoEtaDistribution',
  histo_title = 'Jet eta distribution (reco level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'jets',
  value_func = eta,
  log_y = True
)

jetGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  'jetGenPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'jetGenPtDistribution',
  histo_title = 'Jet transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'gen_jets',
  value_func = pt,
  log_y = True
)

jetRecoPtEtaDistribution = cfg.Analyzer(
  Histogrammer_2D,
  'jetRecoPtEtaDistribution',
  file_label = 'tfile1',
  histo_name = 'jetPtEtaDistribution',
  histo_title = 'Jet transverse momentum and eta distribution',
  input_objects = 'jets',
  x_min = 0,
  x_max = 500,
  x_nbins = 100,
  x_value_func = pt,
  x_label = "pt [GeV]",
  y_min = -10,
  y_max = 10,
  y_nbins = 100,
  y_value_func = eta,
  y_label = "#eta",
  z_label = "# events"
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  #etaGenParticleSelector,
  #etaGenJetSelector,
  #electronSelector,
  #muonSelector,
  #tauSelector,
  #photonSelector,
  #electronRecoPtDistribution,
  #electronLeadingRecoPtDistribution,
  #electronLeadingRecoEtaDistribution,
  #electronSubLeadingRecoPtDistribution,
  #electronSubLeadingRecoEtaDistribution,
  #electronRecoEtaDistribution,
  #electronGenPtDistribution,
  #muonRecoPtDistribution,
  #muonLeadingRecoPtDistribution,
  #muonLeadingRecoEtaDistribution,
  #muonRecoEtaDistribution,
  #muonGenPtDistribution,
  #tauGenPtDistribution,
  #photonRecoPtDistribution,
  #photonLeadingRecoPtDistribution,
  #photonSubLeadingRecoPtDistribution,
  #photonLeadingRecoEtaDistribution,
  #photonSubLeadingRecoEtaDistribution,
  #photonRecoEtaDistribution,
  #photonGenPtDistribution,
  jetRecoPtDistribution,
  #jetLeadingRecoPtDistribution,
  #jetSubLeadingRecoPtDistribution,
  #jetLeadingRecoEtaDistribution,
  #jetSubLeadingRecoEtaDistribution,
  #jetRecoEtaDistribution,
  jetGenPtDistribution,
  #jetRecoPtEtaDistribution
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
