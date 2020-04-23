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
mySettings.pileup = 140 # FCC
#mySettings.pileup = 40 # LHC
mySettings.yScale = 1e6
'''Cross section of the event in mb'''
mySettings.crossSection = 100 # FCC
#mySettings.crossSection = 60 # LHC
'''Instantaneous lumi in cm^-2 s^-1'''
mySettings.instantaneousLuminosity = 30e34 # FCC
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

for x in xrange(0, 600, 10):
  steps.append(x)
  jet_to_electron_scale.append(0)
  jet_to_photon_scale.append(0)
  jet_to_muon_scale.append(0)
  jet_to_MET_scale.append(0)

jet_to_electron_scale[0] = 1
jet_to_electron_scale[1] = 8.00E-03
jet_to_electron_scale[2] = 6.75E-04
jet_to_electron_scale[3] = 4.89E-04
jet_to_electron_scale[4] = 6.13E-04
jet_to_electron_scale[5] = 8.21E-04
jet_to_electron_scale[6] = 9.69E-04
jet_to_electron_scale[7] = 1.13E-03
jet_to_electron_scale[8] = 1.29E-03
jet_to_electron_scale[9] = 1.45E-03
jet_to_electron_scale[10] = 1.62E-03
jet_to_electron_scale[11] = 1.78E-03
jet_to_electron_scale[12] = 1.94E-03
jet_to_electron_scale[13] = 2.10E-03
jet_to_electron_scale[14] = 2.26E-03
jet_to_electron_scale[15] = 2.42E-03
jet_to_electron_scale[16] = 2.58E-03
jet_to_electron_scale[17] = 2.75E-03
jet_to_electron_scale[18] = 2.91E-03
jet_to_electron_scale[19] = 3.07E-03
jet_to_electron_scale[20] = 3.23E-03
jet_to_electron_scale[21] = 3.39E-03
jet_to_electron_scale[22] = 3.55E-03
jet_to_electron_scale[24] = 3.71E-03
jet_to_electron_scale[23] = 3.88E-03
jet_to_electron_scale[25] = 4.04E-03
jet_to_electron_scale[26] = 4.20E-03
jet_to_electron_scale[27] = 4.36E-03
jet_to_electron_scale[28] = 4.52E-03
jet_to_electron_scale[28] = 4.68E-03
jet_to_electron_scale[29] = 4.85E-03
jet_to_electron_scale[30] = 5.01E-03
jet_to_electron_scale[31] = 5.17E-03
jet_to_electron_scale[32] = 5.33E-03
jet_to_electron_scale[33] = 5.49E-03
jet_to_electron_scale[34] = 5.65E-03
jet_to_electron_scale[35] = 5.81E-03
jet_to_electron_scale[36] = 5.98E-03
jet_to_electron_scale[37] = 6.14E-03
jet_to_electron_scale[38] = 6.30E-03
jet_to_electron_scale[39] = 6.46E-03
jet_to_electron_scale[40] = 6.62E-03
jet_to_electron_scale[41] = 6.78E-03
jet_to_electron_scale[42] = 6.94E-03
jet_to_electron_scale[43] = 7.11E-03
jet_to_electron_scale[44] = 7.27E-03
jet_to_electron_scale[45] = 7.43E-03
jet_to_electron_scale[46] = 7.59E-03
jet_to_electron_scale[47] = 7.75E-03
jet_to_electron_scale[48] = 7.91E-03
jet_to_electron_scale[49] = 8.08E-03

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
jet_to_muon_scale[6] = 2.14E-04
jet_to_muon_scale[7] = 2.50E-04
jet_to_muon_scale[8] = 2.86E-04
jet_to_muon_scale[9] = 3.21E-04
jet_to_muon_scale[10] = 3.57E-04
jet_to_muon_scale[11] = 3.93E-04
jet_to_muon_scale[12] = 4.29E-04
jet_to_muon_scale[13] = 4.64E-04
jet_to_muon_scale[14] = 5.00E-04
jet_to_muon_scale[15] = 5.36E-04
jet_to_muon_scale[16] = 5.72E-04
jet_to_muon_scale[17] = 6.07E-04
jet_to_muon_scale[18] = 6.43E-04
jet_to_muon_scale[19] = 6.79E-04
jet_to_muon_scale[20] = 7.14E-04
jet_to_muon_scale[21] = 7.50E-04
jet_to_muon_scale[22] = 7.86E-04
jet_to_muon_scale[24] = 8.22E-04
jet_to_muon_scale[23] = 8.57E-04
jet_to_muon_scale[25] = 8.93E-04
jet_to_muon_scale[26] = 9.29E-04
jet_to_muon_scale[27] = 9.64E-04
jet_to_muon_scale[28] = 1.00E-03
jet_to_muon_scale[28] = 1.04E-03
jet_to_muon_scale[29] = 1.07E-03
jet_to_muon_scale[30] = 1.11E-03
jet_to_muon_scale[31] = 1.14E-03
jet_to_muon_scale[32] = 1.18E-03
jet_to_muon_scale[33] = 1.21E-03
jet_to_muon_scale[34] = 1.25E-03
jet_to_muon_scale[35] = 1.29E-03
jet_to_muon_scale[36] = 1.32E-03
jet_to_muon_scale[37] = 1.36E-03
jet_to_muon_scale[38] = 1.39E-03
jet_to_muon_scale[39] = 1.43E-03
jet_to_muon_scale[40] = 1.46E-03
jet_to_muon_scale[41] = 1.50E-03
jet_to_muon_scale[42] = 1.54E-03
jet_to_muon_scale[43] = 1.57E-03
jet_to_muon_scale[44] = 1.61E-03
jet_to_muon_scale[45] = 1.64E-03
jet_to_muon_scale[46] = 1.68E-03
jet_to_muon_scale[47] = 1.71E-03
jet_to_muon_scale[48] = 1.75E-03
jet_to_muon_scale[49] = 1.79E-03

jet_to_MET_scale[0] = 1
jet_to_MET_scale[1] = 5.50E-01
jet_to_MET_scale[2] = 1.55E-01
jet_to_MET_scale[3] = 9.20E-02
jet_to_MET_scale[4] = 6.29E-02
jet_to_MET_scale[5] = 3.29E-02
jet_to_MET_scale[6] = 3.29E-02
jet_to_MET_scale[7] = 3.68E-02
jet_to_MET_scale[8] = 5.37E-02
jet_to_MET_scale[9] = 5.58E-02
jet_to_MET_scale[10] = 6.20E-02
jet_to_MET_scale[11] = 6.82E-02
jet_to_MET_scale[12] = 7.44E-02
jet_to_MET_scale[13] = 8.06E-02
jet_to_MET_scale[14] = 8.68E-02
jet_to_MET_scale[15] = 9.30E-02
jet_to_MET_scale[16] = 9.92E-02
jet_to_MET_scale[17] = 1.05E-01
jet_to_MET_scale[18] = 1.12E-01
jet_to_MET_scale[19] = 1.18E-01
jet_to_MET_scale[20] = 1.24E-01
jet_to_MET_scale[21] = 1.30E-01
jet_to_MET_scale[22] = 1.36E-01
jet_to_MET_scale[24] = 1.43E-01
jet_to_MET_scale[23] = 1.49E-01
jet_to_MET_scale[25] = 1.55E-01
jet_to_MET_scale[26] = 1.61E-01
jet_to_MET_scale[27] = 1.67E-01
jet_to_MET_scale[28] = 1.74E-01
jet_to_MET_scale[28] = 1.80E-01
jet_to_MET_scale[29] = 1.86E-01
jet_to_MET_scale[30] = 1.92E-01
jet_to_MET_scale[31] = 1.98E-01
jet_to_MET_scale[32] = 2.05E-01
jet_to_MET_scale[33] = 2.11E-01
jet_to_MET_scale[34] = 2.17E-01
jet_to_MET_scale[35] = 2.23E-01
jet_to_MET_scale[36] = 2.29E-01
jet_to_MET_scale[37] = 2.36E-01
jet_to_MET_scale[38] = 2.42E-01
jet_to_MET_scale[39] = 2.48E-01
jet_to_MET_scale[40] = 2.54E-01
jet_to_MET_scale[41] = 2.60E-01
jet_to_MET_scale[42] = 2.67E-01
jet_to_MET_scale[43] = 2.73E-01
jet_to_MET_scale[44] = 2.79E-01
jet_to_MET_scale[45] = 2.85E-01
jet_to_MET_scale[46] = 2.91E-01
jet_to_MET_scale[47] = 2.98E-01
jet_to_MET_scale[48] = 3.04E-01
jet_to_MET_scale[49] = 3.10E-01

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

