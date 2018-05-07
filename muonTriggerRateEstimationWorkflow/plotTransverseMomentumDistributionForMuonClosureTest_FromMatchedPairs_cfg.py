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
from heppy.analyzers.triggerrates.Transformer import Transformer
from heppy.analyzers.triggerrates.HistogrammerCumulative import HistogrammerCumulative
from heppy.framework.heppy_loop import _heppyGlobalOptions
from heppy.analyzers.Filter import Filter
import ast

quality = int(_heppyGlobalOptions["quality"])
detectorEta = float(_heppyGlobalOptions["detectorEta"])
minimumPtInBarrel = float(_heppyGlobalOptions["minimumPtInBarrel"])
minimumPtInEndcap = float(_heppyGlobalOptions["minimumPtInEndcap"])
barrelEta = float(_heppyGlobalOptions["barrelEta"])
deltaR2Matching = float(_heppyGlobalOptions["deltaR2Matching"])

#Object name
triggerObjectName = "L1TMuon"
genObjectName = "GenMuon"
sampleName = "l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch"
convolutionFileName = "_binnedDistributions/distributionWithQuality8/histograms.root"
muon_ptBins = [0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]

if "probabilityFile" in _heppyGlobalOptions:
  probabilityFile = _heppyGlobalOptions["probabilityFile"]
  probabilityHistogram = _heppyGlobalOptions["probabilityHistogram"]
else: 
  probabilityFile = ""
  probabilityHistogram = ""

if "binning" in _heppyGlobalOptions:
  import ast
  muon_ptBins = ast.literal_eval(_heppyGlobalOptions["binning"])

if "convolutionFileName" in _heppyGlobalOptions:
  convolutionFileName = _heppyGlobalOptions["convolutionFileName"]

if "sample" in _heppyGlobalOptions:
  sampleName = _heppyGlobalOptions["sample"]

if sampleName == "delphesMuonSample":
  delphesMuonSample = cfg.MCComponent(
    'delphesMuonSample',
    tree_name = "genMuonSimL1TMuonTree",
    files = [_heppyGlobalOptions["sampleFileName"]],
    gen_object = "muon",
    trigger_object = "SimL1TMuon",
  )
  selectedComponents = [
    delphesMuonSample
  ]
selectedComponents = []

# Retrieving the sample to analyse

def isGenMuonWithinDetectorAcceptance(ptc):
  # pass if in barrel momentum is lower than threshold
  if ((abs(ptc.eta()) < barrelEta) and (ptc.pt() > minimumPtInBarrel)):
    return True
  # If not in barrel check if it is in the endcap acceptance
  if ((abs(ptc.eta()) >= barrelEta) and (abs(ptc.eta()) < detectorEta) and (ptc.pt() > minimumPtInEndcap)): 
    return True
  return False

# Defining pdgids

def goodGenMuonSelection(event):
  # If no trigger object we are not interested in the qualirty or match
  # But we want to check that the gen mu falls into the detector
  if not event.trigger_objects:
    return isGenMuonWithinDetectorAcceptance(event.gen_objects[0])
  return (isGenMuonWithinDetectorAcceptance(event.gen_objects[0]) and (abs(event.trigger_objects[0].deltaR2) < deltaR2Matching)) 

def qualityCut(event):
  if not event.trigger_objects:
    return True
  return event.trigger_objects[0].quality >= quality

goodGenMuonFilter = cfg.Analyzer(
  Filter,
  'goodGenMuonFilter',
  filter_func = goodGenMuonSelection 
)

qualityFilter = cfg.Analyzer(
  Filter,
  'qualityFilter',
  filter_func = qualityCut
)

def hasBeenSmeared(event):
  return event.gen_objects[0].match is not None

smearedFilter = cfg.Analyzer(
  Filter,
  'smearedFilter',
  filter_func = hasBeenSmeared
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

genPtDistribution = cfg.Analyzer(
  Histogrammer,
  'pt'+_heppyGlobalOptions["genObjectName"] + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'pt' + _heppyGlobalOptions["genObjectName"] +'Distribution',
  histo_title = _heppyGlobalOptions["genObjectName"] + ' transverse momentum distribution',
  min = 0,
  max = 200,
  nbins = 400,
  input_objects = 'gen_objects',
  value_func = pt,
  log_y = True
)


smearedPtDistribution = cfg.Analyzer(
  Histogrammer,
  'smearedPt' +_heppyGlobalOptions["genObjectName"] + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'smearedPt' + _heppyGlobalOptions["genObjectName"] +'Distribution',
  histo_title = "Smeared " + _heppyGlobalOptions["genObjectName"] + ' transverse momentum distribution',
  min = 0,
  max = 200,
  nbins = 400,
  input_objects = 'l1tMuons',
  value_func = pt,
  log_y = True
)

acceptedGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  'acceptedGenPt'+_heppyGlobalOptions["genObjectName"] + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'pt' + _heppyGlobalOptions["genObjectName"] +'Distribution',
  histo_title = _heppyGlobalOptions["genObjectName"] + ' transverse momentum distribution',
  min = 0,
  max = 200,
  nbins = 400,
  input_objects = 'gen_objects',
  value_func = pt,
  log_y = True
)

coarseBinnedSmearedPtDistribution = cfg.Analyzer(
  Histogrammer,
  'coarseBinnedSmearedPt' +_heppyGlobalOptions["genObjectName"] + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'coarseBinnedSmearedPt' +_heppyGlobalOptions["genObjectName"] + 'Distribution',
  histo_title = "Smeared " + _heppyGlobalOptions["genObjectName"] + ' transverse momentum distribution',
  bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 260],
  input_objects = 'l1tMuons',
  value_func = pt,
  log_y = True
)

ptDistribution = cfg.Analyzer(
  Histogrammer,
  'pt' + _heppyGlobalOptions["triggerObjectName"] + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'pt' + _heppyGlobalOptions["triggerObjectName"] +'Distribution',
  histo_title = _heppyGlobalOptions["triggerObjectName"] + ' transverse momentum distribution',
  min = 0,
  max = 200,
  nbins = 400,
  input_objects = 'trigger_objects',
  value_func = pt,
  log_y = True
)

coarseBinnedPtDistribution = cfg.Analyzer(
  Histogrammer,
  'coarseBinnedPt' + _heppyGlobalOptions["triggerObjectName"] + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'coarseBinnedPt' + _heppyGlobalOptions["triggerObjectName"] + 'Distribution',
  histo_title = _heppyGlobalOptions["triggerObjectName"] + ' transverse momentum distribution',
  bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 260],
  input_objects = 'trigger_objects',
  value_func = pt,
  log_y = True
)

muonSmearer = cfg.Analyzer(
  Transformer,
  'muonSmearer',
  input_collection = 'gen_objects',
  output_collection = 'l1tMuons',
  convolution_file = convolutionFileName,
  convolution_histogram_prefix = "objectPtDistributionBinnedInMatchedObject",
  bins = muon_ptBins,
  object_x_range = (-100, 200),
  probability_file = probabilityFile,
  probability_histogram = probabilityHistogram
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  cmsMatchingSource,
  genPtDistribution,
  goodGenMuonFilter,
  qualityFilter,
  muonSmearer,
  smearedFilter,
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
