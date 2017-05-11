import os
import copy
import heppy.framework.config as cfg

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

comp = cfg.Component(
  'METEfficiency',
  #files = ["../FCCSW/minimumBias_10000evts.root"],
  #files = ["../FCCSW/DelphesSim_ff_H_WW_enuenu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_H_WW_munumunu_1000events.root"]
  #files = ["../FCCSW/DelphesSim_ff_W_enu_1000events.root"]
  files = ["../FCCSW/DelphesSim_ff_W_munu_1000events.root"]
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

from ROOT import gSystem
gSystem.Load("libdatamodelDict")

from EventStore import EventStore as Events

from heppy.framework.services.tfile import TFileService
tfile_service_1 = cfg.Service(
  TFileService,
  'efficiencyFile',
  fname='efficiency.root',
  option='recreate'
)
    
def pt (ptc):
  return ptc.pt()

from heppy.analyzers.triggerrates.EfficiencyPlotProducer import EfficiencyPlotProducer
metEfficiency = cfg.Analyzer(
  EfficiencyPlotProducer,
  file_label = 'efficiencyFile',
  plot_name = 'metTriggerEfficiency',
  plot_title = 'MET trigger efficiency',
  input_objects = 'met',
  min = 0,
  max = 300,
  nbins = 100,
  value_func = pt
)

#electronEfficiency = cfg.Analyzer(
#  EfficiencyPlotProducer,
#  file_label = 'efficiencyFile',
#  plot_name = 'electronTriggerEfficiency',
#  plot_title = 'Electron trigger efficiency',
#  input_objects = 'electrons',
#  min = 0,
#  max = 500,
#  nbins = 100,
#  value_func = pt
#)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  metEfficiency
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

