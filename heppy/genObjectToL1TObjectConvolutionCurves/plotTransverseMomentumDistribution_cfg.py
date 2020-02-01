import os
import copy
import heppy.framework.config as cfg
#from heppy.samples.mySamples import *
import logging
#from EventStore import EventStore as Events
from heppy.framework.chain import Chain as Events
from heppy.framework.services.tfile import TFileService
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
from heppy.framework.looper import Looper
from heppy.analyzers.Matcher import Matcher
from heppy.analyzers.Selector import Selector
from heppy.analyzers.triggerrates.MatchedParticlesTreeProducer import MatchedParticlesTreeProducer
from heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions import MatchedObjectBinnedDistributions
from heppy.analyzers.triggerrates.ObjectFinder import ObjectFinder
from heppy.analyzers.fcc.Reader import Reader
from importlib import import_module
from heppy.analyzers.triggerrates.CMSMatchingReader import CMSMatchingReader
from heppy.analyzers.triggerrates.Smearer import Smearer
from heppy.analyzers.triggerrates.HistogrammerCumulative import HistogrammerCumulative
from heppy.framework.heppy_loop import _heppyGlobalOptions
from heppy.analyzers.Filter import Filter
import ast


sampleName = "l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch"
if "sample" in _heppyGlobalOptions:
  sampleName = _heppyGlobalOptions["sample"]

if sampleName == "delphesSample":
  objectName = _heppyGlobalOptions["objectName"]
  delphesSample = cfg.MCComponent(
    'delphesSample',
    tree_name = _heppyGlobalOptions["treeName"],
    files = [_heppyGlobalOptions["sampleFileName"]],
    gen_object = objectName,
  )
  selectedComponents = [
    delphesSample
  ]
else:
# Retrieving the sample to analyse:
  sampleName = _heppyGlobalOptions["sample"]
  sample = getattr(import_module("heppy.samples.mySamples"), sampleName)
  selectedComponents = [
    sample
  ]

cmsMatchingSource = cfg.Analyzer(
  CMSMatchingReader,
)

tfile_service_1 = cfg.Service(
  TFileService,
  'tfile1',
  fname='histograms.root',
  option='recreate'
)

def pt (ptc):
  return ptc.pt()

ptDistribution = cfg.Analyzer(
  Histogrammer,
  'pt' + selectedComponents[0].gen_object + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'pt' + selectedComponents[0].gen_object +'Distribution',
  histo_title = selectedComponents[0].gen_object + ' transverse momentum distribution',
  min = 0,
  max = 500,
  nbins = 1000,
  input_objects = 'gen_objects',
  value_func = pt,
  log_y = True
)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  cmsMatchingSource,
  ptDistribution,
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
