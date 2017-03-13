import os
import copy
import heppy.framework.config as cfg

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

mySettings = lambda a: None
mySettings.pileup = 180
mySettings.yScale = 1e6
mySettings.crossSection = 100


comp = cfg.Component(
  'minBias',
  #files = ["../FCCSW/mininumBiasDelphesSimulation_PU180_2evts.root"]
  #files = ["../FCCSW/mininumBiasDelphesSimulation_PU25_10evts.root"]
  files = ["../FCCSW/minimumBias_10000evts.root"]
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

for x in xrange(0, 300, 5):
  steps.append(x)

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
  instantaneous_luminosity = 5e34,
  input_objects = 'jets',
  cross_section = mySettings.crossSection,
  thresholds = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup
)

electronRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'electronTriggerRate',
  plot_title = 'Electron trigger rate',
  instantaneous_luminosity = 5e34,
  input_objects = 'electrons',
  cross_section = mySettings.crossSection,
  thresholds = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup
)

muonRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'muonTriggerRate',
  plot_title = 'Muon trigger rate',
  instantaneous_luminosity = 5e34,
  input_objects = 'muons',
  cross_section = mySettings.crossSection,
  thresholds = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup
)

photonRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'photonTriggerRate',
  plot_title = 'Photon trigger rate',
  instantaneous_luminosity = 5e34,
  input_objects = 'photons',
  cross_section = mySettings.crossSection,
  thresholds = steps,
  yscale = mySettings.yScale,
  pileup = mySettings.pileup
)

metRate = cfg.Analyzer(
  RatePlotProducer,
  file_label = 'ratePlotFile',
  plot_name = 'metTriggerRate',
  plot_title = 'MET trigger rate',
  instantaneous_luminosity = 5e34,
  input_objects = 'met',
  cross_section = mySettings.crossSection,
  thresholds = steps,
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
  metRate
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

