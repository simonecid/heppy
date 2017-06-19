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
  'MinBiasDistribution_13TeV_DelphesCMS',
  #files = ["../FCCSW/DelphesSim_ff_H_WW_enuenu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_H_WW_munumunu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_H_ZZ_eeee_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_H_ZZ_mumumumu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_W_enu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_W_munu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_W_taunu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_Z_ee_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_Z_mumu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_Z_tautau_1000events.root"]
  #files = ["../FCCSW/mininumBiasDelphesSimulation_PU25_10evts.root"]
  #files = ["../FCCSW/minimumBias_10000evts.root"]
  #files = [
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.0.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.10.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.11.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.12.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.13.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.14.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.15.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.16.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.17.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.18.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.19.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.1.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.2.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.3.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.4.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.5.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.6.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.7.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.8.root",
  #  "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.9.root"
  #]
  #files = [
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.0.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.10.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.11.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.12.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.13.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.14.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.15.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.16.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.17.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.18.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.19.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.1.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.2.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.3.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.4.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.5.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.6.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.7.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.8.root",
  #  "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.9.root"
  #]
  files = [
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.0.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.10.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.11.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.12.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.13.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.14.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.15.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.16.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.17.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.18.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.19.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.1.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.2.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.3.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.4.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.5.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.6.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.7.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.8.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.9.root",
  ]
  #files = [
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.0.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.10.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.11.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.12.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.13.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.14.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.15.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.16.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.17.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.18.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.19.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.1.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.2.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.3.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.4.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.5.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.6.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.7.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.8.root",
  #  "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.9.root",
  #]
  #files = [
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.0.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.10.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.11.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.12.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.13.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.14.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.15.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.16.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.17.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.18.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.19.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.1.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.2.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.3.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.4.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.5.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.6.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.7.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.8.root",
  #  "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.9.root",
  #]
)

# Max 4 jobs
comp.splitFactor = len(comp.files) if len(comp.files) < 4 else 4

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
  Creates particle checker functions. 
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
  'electronRecoPtDistribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
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
  'electronLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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
  max = 100,
  nbins = 100,
  input_objects = 'gen_electrons',
  value_func = pt,
  log_y = True
)

# Muons

muonRecoPtDistribution = cfg.Analyzer(
  Histogrammer,
  'muonRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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
  'muonLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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
  'tauGenPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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
  'photonRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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
  'photonLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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
  max = 100,
  nbins = 100,
  input_objects = 'gen_photons',
  value_func = pt,
  log_y = True
)

# Jets

jetRecoPtDistribution = cfg.Analyzer(
  Histogrammer,
  'jetRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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
  'jetLeadingRecoPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
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

jetGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  'jetGenPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'jetGenPtDistribution',
  histo_title = 'Jet transverse momentum distribution (gen level)',
  min = 0,
  max = 500,
  nbins = 100,
  input_objects = 'gen_jets_eta_restricted',
  value_func = pt,
  log_y = True
)

from heppy.analyzers.triggerrates.Histogrammer_2D import Histogrammer_2D

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
  z_label = "\# events"
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
  jetGenPtDistribution,
  jetRecoPtEtaDistribution
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
