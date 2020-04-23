import os
import copy
import heppy.framework.config as cfg

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

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

from heppy.analyzers.triggerrates.MinBiasEventMerger import MinBiasEventMerger

eventMerger = cfg.Analyzer(
  MinBiasEventMerger,
  input_objects = ['charged_gen_particles'],
  pileup = 180,
  output_objects = ['merged_charged_gen_particles']
)

from heppy.analyzers.Selector import Selector

def isCharged(ptc):
  # Apparently q is the charge :S 
  return ptc.q() != 0

chargedParticleSelector = cfg.Analyzer(
    Selector,
    'sel_charged',
    output = 'charged_gen_particles',
    input_objects = 'gen_particles',
    filter_func = isCharged
)

from heppy.analyzers.triggerrates.NumberOfParticlesDistribution import NumberOfParticlesDistribution

numberOfParticlesDistribution = cfg.Analyzer(
  NumberOfParticlesDistribution,
  histo_name = 'numberOfChargedGenParticles',
  histo_title = 'Distribution of the number of generated charged particles on 10k min bias events at PU 0',
  min = 300,
  max = 800,
  nbins = 100,
  input_objects = 'merged_charged_gen_particles'
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  chargedParticleSelector,
  eventMerger,
  numberOfParticlesDistribution
] )


config = cfg.Config(
  components = selectedComponents,
  sequence = sequence,
  services = [],
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

