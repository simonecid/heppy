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

steps = []
for x in xrange(0, 300, 10):
  steps.append(x)

comp = cfg.Component(
  'myTestScript',
  #files = ["../FCCSW/mininumBiasDelphesSimulation_PU180_2evts.root"]
  #files = ["../FCCSW/mininumBiasDelphesSimulation_PU25_10evts.root"]
  files = ["../FCCSW/minimumBias_10000evts.root"]
  #files = ["../FCCSW/DelphesSim_ff_W_taunu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_Z_tautau_1000events.root"]
  #files = ["../FCCSW/minimumBias_13TeV_100000evts.root"]
  #files = [
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.0.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.10.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.11.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.12.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.13.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.14.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.15.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.16.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.17.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.18.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.19.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.1.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.2.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.3.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.4.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.5.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.6.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.7.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.8.root",
    #"/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.9.root"
  #]
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

from heppy.framework.services.tfile import TFileService
tfile_service_1 = cfg.Service(
  TFileService,
  'tfile1',
  fname='plots.root',
  option='recreate'
)

from ROOT import gSystem
gSystem.Load("libdatamodelDict")

from EventStore import EventStore as Events

def pt (ptc):
  return ptc.pt()

def eta (ptc):
  return ptc.eta()

from heppy.analyzers.triggerrates.Histogrammer_2D import Histogrammer_2D

jetDistribution = cfg.Analyzer(
  Histogrammer_2D,
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
  jetDistribution
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

