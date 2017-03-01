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
  files = ["../FCCSW/minBiasSimulationOutput_1000evts.root", "../FCCSW/minBiasSimulationOutput_10000evts.root" ]
)
selectedComponents = [comp]

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
  Reader,

  #gen_particles = 'genParticles',
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

from heppy.analyzers.triggerrates.PtPrinter import PtPrinter
ptPrinter = cfg.Analyzer(
  PtPrinter,
  input_objects = 'jets',
)

# Closure that returns a single object threshold trigger
# I love this <3

def thresholdTriggerGenerator (threshold):
  def thresholdTrigger (ptc):
    return ptc.pt() > threshold
  return thresholdTrigger

from heppy.analyzers.triggerrates.SingleObjectTrigger import SingleObjectTrigger
jetTrigger = cfg.Analyzer(
  SingleObjectTrigger,
  'jetTrigger',
  input_objects = 'jets',
  trigger_func = thresholdTriggerGenerator(40)
)

steps = []

for x in xrange(30, 210, 5):
  steps.append(x)

# creating an output tree
from heppy.analyzers.triggerrates.TreeProducer import TreeProducer
tree = cfg.Analyzer(
  TreeProducer,
  tree_name = 'tree',
  tree_title = 'Trigger rates',
  input_objects = 'jets',
  thresholds = steps  
)

from heppy.framework.services.tfile import TFileService
tfile_service_1 = cfg.Service(
  TFileService,
  'tfile1',
  fname='histograms.root',
  option='recreate'
)

def pt (ptc):
  return ptc.pt()

from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
ptDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'jetPtDistribution',
  histo_title = 'Jet transverse momentum distribution',
  min = 0,
  max = 200,
  nbins = 100,
  input_objects = 'jets',
  value_func = pt
)

def eta (ptc):
  return ptc.eta()

etaDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'jetEtaDistribution',
  histo_title = 'Jet pseudo-rapidity distribution',
  min = -10,
  max = +10,
  nbins = 100,
  input_objects = 'jets',
  value_func = eta
)

def phi (ptc):
  return ptc.phi()

phiDistribution = cfg.Analyzer(
  Histogrammer,
  file_label = 'tfile1',
  histo_name = 'jetPhiDistribution',
  histo_title = 'Jet phi distribution',
  min = -3.15,
  max = +3.15,
  nbins = 100,
  input_objects = 'jets',
  value_func = phi
)

from heppy.analyzers.triggerrates.RatePlotProducer import RatePlotProducer
rate = cfg.Analyzer(
  RatePlotProducer,
  plot_name = 'rate',
  plot_title = 'Jet trigger rate',
  instantaneous_luminosity = 3e35,
  input_objects = 'jets',
  cross_section = 100,
  thresholds = steps
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  ptDistribution,
  etaDistribution,
  phiDistribution,
  rate,
  tree
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

