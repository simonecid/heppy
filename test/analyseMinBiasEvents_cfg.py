import os
import copy
import heppy.framework.config as cfg
import logging
from ROOT import gSystem
#from heppy.framework.chain import Chain as Events
from EventStore import EventStore as Events
from heppy.framework.services.tfile import TFileService
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
from heppy.analyzers.triggerrates.LeadingQuantityHistogrammer import LeadingQuantityHistogrammer
from heppy.analyzers.triggerrates.NumberOfParticlesDistribution import NumberOfParticlesDistribution
from heppy.framework.looper import Looper
from heppy.analyzers.Matcher import Matcher
from heppy.analyzers.Selector import Selector
from heppy.analyzers.triggerrates.MatchedParticlesTreeProducer import MatchedParticlesTreeProducer
from heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions import MatchedObjectBinnedDistributions
from heppy.analyzers.fcc.Reader import Reader
from heppy.analyzers.triggerrates.ObjectFinder import ObjectFinder
from heppy.analyzers.triggerrates.HistogrammerCumulative import HistogrammerCumulative
from heppy.analyzers.triggerrates.ParticleTreeProducer import ParticleTreeProducer
from heppy.samples.sample_MinimumBias_NoTau_14TeV_GenParticles_CMSSWTune_WPropagation import MinimumBias_14TeV_GenParticles_full_CMSSWTune_WPropagation_1MEvents
from heppy.framework.heppy_loop import _heppyGlobalOptions
#from heppy.samples.sample_NeutrinoGun_PU140_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWTune import NeutrinoGun_PU140_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWTune
from heppy.samples.sample_QCD_Pt_15to3000_Tune4C_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWtune import QCD_Pt_15to3000_Tune4C_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWtune_Pythia_8_223_v2_400kevents
from math import sqrt

gSystem.Load("libdatamodelDict")

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

#Object name
objectName = "L1T EGamma"
matchedObjectName = "Gen jet"
sampleName = "cmsMatching_SingleNeutrinoPU140_GenJet"

# Retrieving the sample to analyse

#if specified in sample, a specific set will be used, otherwise the full set will be employed
#if "sample" in _heppyGlobalOptions:
#  sampleName = _heppyGlobalOptions["sample"]
#if sampleName == "all":
#  selectedComponents = [
#    cmsMatching_QCD_15_3000_L1TMuon_GenJet,
#    cmsMatching_QCD_15_3000_L1TEGamma_GenJet,
#    cmsMatching_QCD_15_3000_L1TTau_GenJet,
#  ]
#else:  
#  sample = globals()[sampleName]
#  selectedComponents = [
#      MinimumBias_14TeV_GenParticles_full
#  ]

#sample = globals()[sampleName]

#MBtest = cfg.MCComponent(
#  'testpileup_PU140_14TeV_300events',
#  files=["/six/sb17498/FCC/FCCSW/testpileup_PU140_14TeV_300events.root"]
#)

MBtest = cfg.MCComponent(
  'testpileup_PU140_14TeV_12events_2',
  files=["/hdfs/FCC-hh/NeutrinoGun_PU140_14TeV_OnlyGenParticleClassification_CMSSWTune/events_NeutrinoGun_PU140_NoTau_100events_14TeV_CMSSWTune_3662892.0.root"]
)

#MBtest = cfg.MCComponent(
#  'testpileup_MB_14TeV_50kevents_fromHEPMC',
#  files=["/six/sb17498/FCC/FCCSW/testpileup_MB_14TeV_50000events_fromhepmc.root"]
#)

#MBtest = cfg.MCComponent(
#    'testpileup_PU0_14TeV_7000events',
#  files=["/six/sb17498/FCC/FCCSW/testpileup_PU0_14TeV_7000events.root"]
#)

#MBtest = cfg.MCComponent(
#  'MBSample_14TeV',
#  files=[
#    "/hdfs/FCC-hh/MinimumBias_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWtune_WPropagation/events_MinimumBias_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWtune_PropagatedJets_3572668.0.root",
#    "/hdfs/FCC-hh/MinimumBias_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWtune_WPropagation/events_MinimumBias_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWtune_PropagatedJets_3572668.10.root",
#    "/hdfs/FCC-hh/MinimumBias_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWtune_WPropagation/events_MinimumBias_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWtune_PropagatedJets_3572668.11.root",
#  ],
#)


#selectedComponents = [
#    NeutrinoGun_PU140_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWTune
#]

#selectedComponents = [
#  MinimumBias_14TeV_GenParticles_full_CMSSWTune_WPropagation_1MEvents
#]

selectedComponents = [
    QCD_Pt_15to3000_Tune4C_14TeV_OnlyGenParticleClassification_JetPTMin_3_CMSSWtune_Pythia_8_223_v2_400kevents
]

''' Returns pt'''
def pt (ptc):
      return ptc.pt()

'''Returns eta'''
def eta (ptc):
      return ptc.eta()

# Defining pdgids

source = cfg.Analyzer(
    Reader,

    #gen_particles = 'skimmedGenParticles',

    gen_jets='nonPropagatedGenJets',

    #electrons = 'genElectrons',

    muons = 'genMuons',

    #photons = 'genPhotons',
    #met = 'genMET',
)


tfile_service_1 = cfg.Service(
    TFileService,
    'tfile1',
    fname='distributions.root',
    option='recreate'
)

# I want to plot 
# Number of jets, inclusive pt and leading pt for jets w/o nu, and muons


##########################
#         JETS           #
##########################

genJetPtDistribution = cfg.Analyzer(
  Histogrammer,
  'genJetPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'genJetPtDistribution',
  histo_title = 'Jet transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'gen_jets',
  value_func = pt,
  log_y = True
)

genJetEtaDistribution = cfg.Analyzer(
  Histogrammer,
  'genJetEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'genJetEtaDistribution',
  histo_title = 'Jet eta distribution (gen level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'gen_jets',
  value_func = eta,
  log_y = True
)

genJetLeadingPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'genJetLeadingPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'genJetLeadingPtDistribution',
  histo_title = 'Jet leading transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'gen_jets',
  key_func = pt,
  value_func = pt,
  log_y = True
)

genJetLeadingEtaDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'genJetLeadingEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'genJetLeadingEtaDistribution',
  histo_title = 'Jet leading eta distribution (gen level)',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'gen_jets',
  key_func = pt,
  value_func = eta,
  log_y = True
)

numberOfGenJetsInEventDistribution = cfg.Analyzer(
  NumberOfParticlesDistribution,
  'numberOfGenJetsInEventDistribution',
  file_label = 'tfile1',
  histo_name='numberOfGenJetsInEventDistribution',
  histo_title = 'Number of gen jets per event',
  min = 0,
  max = 100,
  nbins = 100,
  input_objects = 'gen_jets',
)

##########################
#         MUONS          #
##########################

genMuonPtDistribution = cfg.Analyzer(
  Histogrammer,
  'genMuonPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'genMuonPtDistribution',
  histo_title = 'Muon transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'muons',
  value_func = pt,
  log_y = True
)

genMuonEtaDistribution = cfg.Analyzer(
  Histogrammer,
  'genMuonEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'genMuonEtaDistribution',
  histo_title = 'Muon eta distribution (gen level)',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'muons',
  value_func = eta,
  log_y = True
)

genMuonLeadingPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'genMuonLeadingPtDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'genMuonLeadingPtDistribution',
  histo_title = 'Muon leading transverse momentum distribution (gen level)',
  min = 0,
  max = 2000,
  nbins = 4000,
  input_objects = 'muons',
  key_func = pt,
  value_func = pt,
  log_y = True
)

genMuonLeadingEtaDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'genMuonLeadingEtaDistribution',
  file_label = 'tfile1',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'genMuonLeadingEtaDistribution',
  histo_title = 'Muon leading eta distribution (gen level)',
  min = -10,
  max = 10,
  nbins = 100,
  input_objects = 'muons',
  key_func = pt,
  value_func = eta,
  log_y = True
)

numberOfGenMuonsInEventDistribution = cfg.Analyzer(
  NumberOfParticlesDistribution,
  'numberOfGenMuonsInEventDistribution',
  file_label = 'tfile1',
  histo_name='numberOfGenMuonsInEventDistribution',
  histo_title = 'Number of muons per event',
  min = 0,
  max = 100,
  nbins = 100,
  input_objects = 'muons',
)

muonTree = cfg.Analyzer(
  ParticleTreeProducer,
  file_label = "tfile1",
  tree_name = 'muonTree',
  tree_title = 'Tree containing info about muons',
  collection = "muons"
)

jetTree = cfg.Analyzer(
  ParticleTreeProducer,
  file_label = "tfile1",
  tree_name = 'jetTree',
  tree_title = 'Tree containing info about jets',
  collection = "gen_jets"
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  genJetPtDistribution,
  genJetLeadingPtDistribution,
  genJetEtaDistribution,
  genJetLeadingEtaDistribution,
  numberOfGenJetsInEventDistribution,
  genMuonPtDistribution,
  genMuonLeadingPtDistribution,
  genMuonEtaDistribution,
  genMuonLeadingEtaDistribution,
  numberOfGenMuonsInEventDistribution,
  muonTree,
  jetTree
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
