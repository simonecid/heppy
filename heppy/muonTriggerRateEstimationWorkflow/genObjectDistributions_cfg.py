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


#Object name
triggerObjectName = "L1TMuon"
genObjectName = "GenMuon"
sampleName = "l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch"
muon_ptBins = [0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]

if "binning" in _heppyGlobalOptions:
  import ast
  muon_ptBins = ast.literal_eval(_heppyGlobalOptions["binning"])

if "sample" in _heppyGlobalOptions:
  sampleName = _heppyGlobalOptions["sample"]
# Retrieving the sample to analyse:
  sample = getattr(import_module("heppy.samples.mySamples"), sampleName)
  selectedComponents = [
    sample
  ]

# Defining pdgids

def dr2Selection(event):
  return abs(event.trigger_objects[0].deltaR2) < 0.25 #dr < 0.5

def qualityCut(event):
  return event.trigger_objects[0].quality >= 8

tightRestrictionMatchFilter = cfg.Analyzer(
  Filter,
  'tightRestrictionMatchFilter',
  filter_func = dr2Selection 
)

qualityFilter = cfg.Analyzer(
  Filter,
  'qualityFilter',
  filter_func = qualityCut
)

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

def matchedObjectPt (ptc):
  return ptc.match.pt()

smearedPtDistribution = cfg.Analyzer(
  Histogrammer,
  'smearedPt' +selectedComponents[0].gen_object + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'smearedPt' + selectedComponents[0].gen_object +'Distribution',
  histo_title = "Smeared " + selectedComponents[0].gen_object + ' transverse momentum distribution',
  min = 0,
  max = 200,
  nbins = 400,
  input_objects = 'l1tMuons',
  value_func = pt,
  log_y = True
)

coarseBinnedSmearedPtDistribution = cfg.Analyzer(
  Histogrammer,
  'coarseBinnedSmearedPt' +selectedComponents[0].gen_object + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'coarseBinnedSmearedPt' +selectedComponents[0].gen_object + 'Distribution',
  histo_title = "Smeared " + selectedComponents[0].gen_object + ' transverse momentum distribution',
  min = 0,
  max = 200,
  nbins = 20,
  input_objects = 'l1tMuons',
  value_func = pt,
  log_y = True
)

ptDistribution = cfg.Analyzer(
  Histogrammer,
  'pt' + selectedComponents[0].trigger_object + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'pt' + selectedComponents[0].trigger_object +'Distribution',
  histo_title = selectedComponents[0].trigger_object + ' transverse momentum distribution',
  min = 0,
  max = 200,
  nbins = 400,
  input_objects = 'trigger_objects',
  value_func = pt,
  log_y = True
)

coarseBinnedPtDistribution = cfg.Analyzer(
  Histogrammer,
  'coarseBinnedPt' + selectedComponents[0].trigger_object + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'coarseBinnedPt' + selectedComponents[0].trigger_object + 'Distribution',
  histo_title = selectedComponents[0].trigger_object + ' transverse momentum distribution',
  min = 0,
  max = 200,
  nbins = 20,
  input_objects = 'trigger_objects',
  value_func = pt,
  log_y = True
)

muonSmearer = cfg.Analyzer(
  Smearer,
  'muonSmearer',
  input_collection = 'gen_objects',
  output_collection = 'l1tMuons',
  convolution_file = convolutionFileName,
  convolution_histogram_prefix = "deltaPtDistributionBinnedInMatchedObject",
  bins = muon_ptBins,
  object_x_range = (-100, 200)
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  cmsMatchingSource,
  tightRestrictionMatchFilter,
  qualityFilter,
  muonSmearer,
  ptDistribution,
  coarseBinnedPtDistribution,
  smearedPtDistribution,
  coarseBinnedSmearedPtDistribution,
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
