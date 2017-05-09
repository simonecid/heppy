import os
import copy
import heppy.framework.config as cfg

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

mySettings = lambda a: None
'''Pile up level for that kind of event'''
mySettings.pileup = 180 # FCC
#mySettings.pileup = 40 # LHC
mySettings.yScale = 1e6
'''Cross section of the event in mb'''
mySettings.crossSection = 100 # FCC
#mySettings.crossSection = 60 # LHC
'''Instantaneous lumi in cm^-2 s^-1'''
mySettings.instantaneousLuminosity = 5e34 # FCC
#mySettings.instantaneousLuminosity = 1.15e34 # LHC


comp = cfg.Component(
  'minBias',
  #files = ["../FCCSW/mininumBiasDelphesSimulation_PU180_2evts.root"]
  #files = ["../FCCSW/mininumBiasDelphesSimulation_PU25_10evts.root"]
  #files = ["../FCCSW/minimumBias_10000evts.root"]
  #files = ["../FCCSW/minimumBias_13TeV_100000evts.root"]
  files = [
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.0.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.10.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.11.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.12.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.13.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.14.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.15.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.16.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.17.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.18.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.19.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.1.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.2.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.3.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.4.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.5.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.6.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.7.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.8.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.9.root"
  ]
)
selectedComponents = [comp]

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
  Reader,

  gen_particles = 'skimmedGenParticles',
  #gen_vertices = 'genVertices',

  gen_jets = 'genJets',

  jets = 'jets',
  bTags = 'bTags',
  cTags = 'cTags',
  tauTags = 'tauTags',

  electrons = 'electrons',
  electronITags = 'electronITags',

  muons = 'muons',
  muonITags = 'muonITags',

  photons = 'photons',
  met = 'met',
)

from ROOT import gSystem
gSystem.Load("libdatamodelDict")

from EventStore import EventStore as Events

steps = []
jet_to_electron_scale = []
jet_to_photon_scale = []
jet_to_muon_scale = []
jet_to_MET_scale = []

for x in xrange(0, 300, 10):
  steps.append(x)
  jet_to_electron_scale.append(0)
  jet_to_photon_scale.append(0)
  jet_to_muon_scale.append(0)
  jet_to_MET_scale.append(0)

jet_to_electron_scale[0] = 1
jet_to_electron_scale[1] = 8.00E-03
jet_to_electron_scale[2] = 7.50E-04
jet_to_electron_scale[3] = 4.89E-04
jet_to_electron_scale[4] = 6.13E-04
jet_to_electron_scale[5] = 8.21E-04
jet_to_electron_scale[6] = 9.59E-04
jet_to_electron_scale[7] = 1.11E-03
jet_to_electron_scale[8] = 1.27E-03
jet_to_electron_scale[9] = 1.43E-03
jet_to_electron_scale[10] = 1.58E-03
jet_to_electron_scale[11] = 1.74E-03
jet_to_electron_scale[12] = 1.89E-03
jet_to_electron_scale[13] = 2.05E-03
jet_to_electron_scale[14] = 2.21E-03

jet_to_photon_scale[0] = 1
jet_to_photon_scale[1] = 2.50E-02
jet_to_photon_scale[2] = 6.50E-05
jet_to_photon_scale[3] = 4.03E-05
jet_to_photon_scale[4] = 3.07E-05
jet_to_photon_scale[5] = 0

jet_to_muon_scale[0] = 1
jet_to_muon_scale[1] = 1.38E-03
jet_to_muon_scale[2] = 1.25E-04
jet_to_muon_scale[3] = 1.15E-04
jet_to_muon_scale[4] = 1.23E-04
jet_to_muon_scale[5] = 2.30E-04
jet_to_muon_scale[6] = 2.00E-04
jet_to_muon_scale[7] = 2.29E-04
jet_to_muon_scale[8] = 2.58E-04
jet_to_muon_scale[9] = 2.88E-04
jet_to_muon_scale[10] = 3.17E-04
jet_to_muon_scale[11] = 3.46E-04
jet_to_muon_scale[12] = 3.75E-04
jet_to_muon_scale[13] = 4.04E-04
jet_to_muon_scale[14] = 4.34E-04

jet_to_MET_scale[0] = 1
jet_to_MET_scale[1] = 5.50E-01
jet_to_MET_scale[2] = 1.55E-01
jet_to_MET_scale[3] = 9.20E-02
jet_to_MET_scale[4] = 6.29E-02
jet_to_MET_scale[5] = 3.29E-02
jet_to_MET_scale[6] = 3.29E-02
jet_to_MET_scale[7] = 3.68E-02
jet_to_MET_scale[8] = 5.37E-02
jet_to_MET_scale[9] = 5.44E-02
jet_to_MET_scale[10]  6.01E-02
jet_to_MET_scale[11] = 6.59E-02
jet_to_MET_scale[12] = 7.16E-02
jet_to_MET_scale[13] = 7.74E-02
jet_to_MET_scale[14] = 8.31E-02

# File in which all the rate plots will be stored 

from heppy.framework.services.tfile import TFileService
tfile_service_1 = cfg.Service(
  TFileService,
  'ratePlotFile',
  fname='ratePlots.root',
  option='recreate'
)

from heppy.analyzers.triggerrates.RatePlotProducer import RatePlotProducer
jetRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'jetTriggerRate',
  plot_title = 'Jet trigger rate',
  instantaneous_luminosity = mySettings.instantaneousLuminosity,
  input_objects = 'jets',
  cross_section = mySettings.crossSection,
  bins = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup
)

jetToElectronRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'jetToElectronTriggerRate',
  plot_title = 'Electron trigger rate from jets',
  instantaneous_luminosity = mySettings.instantaneousLuminosity,
  input_objects = 'jets',
  cross_section = mySettings.crossSection,
  bins = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup,
  scale_factors = jet_to_electron_scale
)

jetToPhotonRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'jetToPhotonTriggerRate',
  plot_title = 'Photon trigger rate from jets',
  instantaneous_luminosity = mySettings.instantaneousLuminosity,
  input_objects = 'jets',
  cross_section = mySettings.crossSection,
  bins = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup,
  scale_factors = jet_to_photon_scale
)

jetToMuonRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'jetToMuonTriggerRate',
  plot_title = 'Muon trigger rate from jets',
  instantaneous_luminosity = mySettings.instantaneousLuminosity,
  input_objects = 'jets',
  cross_section = mySettings.crossSection,
  bins = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup,
  scale_factors = jet_to_muon_scale
)

jetToMETRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'jetToMETTriggerRate',
  plot_title = 'MET trigger rate from jets',
  instantaneous_luminosity = mySettings.instantaneousLuminosity,
  input_objects = 'jets',
  cross_section = mySettings.crossSection,
  bins = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup,
  scale_factors = jet_to_MET_scale
)

electronRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'electronTriggerRate',
  plot_title = 'Electron trigger rate',
  instantaneous_luminosity = mySettings.instantaneousLuminosity,
  input_objects = 'electrons',
  cross_section = mySettings.crossSection,
  bins = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup
)

muonRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'muonTriggerRate',
  plot_title = 'Muon trigger rate',
  instantaneous_luminosity = mySettings.instantaneousLuminosity,
  input_objects = 'muons',
  cross_section = mySettings.crossSection,
  bins = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup
)

photonRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'photonTriggerRate',
  plot_title = 'Photon trigger rate',
  instantaneous_luminosity = mySettings.instantaneousLuminosity,
  input_objects = 'photons',
  cross_section = mySettings.crossSection,
  bins = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup
)

metRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'metTriggerRate',
  plot_title = 'MET trigger rate',
  instantaneous_luminosity = mySettings.instantaneousLuminosity,
  input_objects = 'met',
  cross_section = mySettings.crossSection,
  bins = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  jetRate,
  muonRate,
  photonRate,
  electronRate,
  metRate,
  jetToMuonRate,
  jetToPhotonRate,
  jetToElectronRate,
  jetToMETRate
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

