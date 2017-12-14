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

triggerObjectName = _heppyGlobalOptions["triggerObjectName"]
genObjectName = _heppyGlobalOptions["genObjectName"]
quality = int(_heppyGlobalOptions["quality"])
minimumPtInBarrel= float(_heppyGlobalOptions["minimumPtInBarrel"])
minimumPtInEndcap= float(_heppyGlobalOptions["minimumPtInEndcap"])
minimumPtInForward= float(_heppyGlobalOptions["minimumPtInForward"])
barrelEta= float(_heppyGlobalOptions["barrelEta"])
endcapEta= float(_heppyGlobalOptions["endcapEta"])
detectorEta= float(_heppyGlobalOptions["detectorEta"])
deltaR2Matching = float(_heppyGlobalOptions["deltaR2Matching"])

sampleName = "l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1_WQualityBranch"
convolutionFileName = "_binnedDistributions/distributionWithQuality8/histograms.root"
ptBins = [0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]

if "probabilityFile" in _heppyGlobalOptions:
  probabilityFile = _heppyGlobalOptions["probabilityFile"]
  probabilityHistogram = _heppyGlobalOptions["probabilityHistogram"]
else: 
  probabilityFile = ""
  probabilityHistogram = ""

if "binning" in _heppyGlobalOptions:
  import ast
  ptBins = ast.literal_eval(_heppyGlobalOptions["binning"])

if "convolutionFileName" in _heppyGlobalOptions:
  convolutionFileName = _heppyGlobalOptions["convolutionFileName"]

if "sample" in _heppyGlobalOptions:
  sampleName = _heppyGlobalOptions["sample"]

if sampleName == "delphesSample":
  delphesSample = cfg.MCComponent(
    'delphesSample',
    tree_name = _heppyGlobalOptions["treeName"],
    files = [_heppyGlobalOptions["sampleFileName"]],
    gen_object = genObjectName,
    trigger_object = triggerObjectName,
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

# Retrieving the sample to analyse

def isGenObjectWithinDetectorAcceptance(ptc):
  # pass if in barrel momentum is lower than threshold
  if ((abs(ptc.eta()) < barrelEta) and (ptc.pt() > minimumPtInBarrel)):
    return True
  # If not in barrel check if it is in the endcap acceptance
  if ((abs(ptc.eta()) >= barrelEta) and (abs(ptc.eta()) < endcapEta) and (ptc.pt() > minimumPtInEndcap)): 
    return True
  # If not in endcap check if it is in the forward acceptance
  if ((abs(ptc.eta()) >= endcapEta) and (abs(ptc.eta()) < detectorEta) and (ptc.pt() > minimumPtInForward)): 
    return True

  return False

# Defining pdgids

def goodGenObjectSelection(event):
  # If no trigger object we are not interested in the qualirty or match
  # But we want to check that the gen mu falls into the detector
  if not event.trigger_objects:
    return isGenObjectWithinDetectorAcceptance(event.gen_objects[0])
  return (isGenObjectWithinDetectorAcceptance(event.gen_objects[0]) and (abs(event.trigger_objects[0].deltaR2) < deltaR2Matching)) #dr < 0.5

def qualityCut(event):
  if not event.trigger_objects:
    return True
  return event.trigger_objects[0].quality >= quality

goodGenObjectFilter = cfg.Analyzer(
  Filter,
  'goodGenObjectFilter',
  filter_func = goodGenObjectSelection 
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

def deltaPt (ptc):
  return ptc.pt() - ptc.match.pt()

def matchedObjectPt (ptc):
  return ptc.match.pt()

genPtDistribution = cfg.Analyzer(
  Histogrammer,
  'pt' + genObjectName + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'pt' + genObjectName +'Distribution',
  histo_title = genObjectName + ' transverse momentum distribution',
  min = 0,
  max = 500,
  nbins = 1000,
  input_objects = 'gen_objects',
  value_func = pt,
  log_y = True
)


smearedPtDistribution = cfg.Analyzer(
  Histogrammer,
  'smearedPt' + genObjectName + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'smearedPt' + genObjectName +'Distribution',
  histo_title = "Smeared " + genObjectName + ' transverse momentum distribution',
  min = 0,
  max = 500,
  nbins = 1000,
  input_objects = triggerObjectName,
  value_func = pt,
  log_y = True
)

acceptedGenPtDistribution = cfg.Analyzer(
  Histogrammer,
  'acceptedGenPt'+ genObjectName + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'pt' + genObjectName +'Distribution',
  histo_title = genObjectName + ' transverse momentum distribution',
  min = 0,
  max = 500,
  nbins = 1000,
  input_objects = 'gen_objects',
  value_func = pt,
  log_y = True
)

coarseBinnedSmearedPtDistribution = cfg.Analyzer(
  Histogrammer,
  'coarseBinnedSmearedPt' + genObjectName + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'coarseBinnedSmearedPt' + genObjectName + 'Distribution',
  histo_title = "Smeared " + genObjectName + ' transverse momentum distribution',
  bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 340, 400],
  input_objects = triggerObjectName,
  value_func = pt,
  log_y = True
)

ptDistribution = cfg.Analyzer(
  Histogrammer,
  'pt' + triggerObjectName + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'pt' + triggerObjectName +'Distribution',
  histo_title = triggerObjectName + ' transverse momentum distribution',
  min = 0,
  max = 500,
  nbins = 1000,
  input_objects = 'trigger_objects',
  value_func = pt,
  log_y = True
)

coarseBinnedPtDistribution = cfg.Analyzer(
  Histogrammer,
  'coarseBinnedPt' + triggerObjectName + 'Distribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'coarseBinnedPt' + triggerObjectName + 'Distribution',
  histo_title = triggerObjectName + ' transverse momentum distribution',
  bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 340, 400],
  input_objects = 'good_trigger_objects',
  value_func = pt,
  log_y = True
)

coarseBinnedPtBarrelDistribution = cfg.Analyzer(
  Histogrammer,
  'coarseBinnedPt' + triggerObjectName + 'BarrelDistribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'coarseBinnedPt' + triggerObjectName + 'BarrelDistribution',
  histo_title = triggerObjectName + ' transverse momentum distribution in abs(#eta) < ' + str(barrelEta),
  bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 340, 400],
  input_objects = 'trigger_objects_barrel',
  value_func = pt,
  log_y = True
)

coarseBinnedPtEndcapDistribution = cfg.Analyzer(
  Histogrammer,
  'coarseBinnedPt' + triggerObjectName + 'EndcapDistribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'coarseBinnedPt' + triggerObjectName + 'EndcapDistribution',
  histo_title = triggerObjectName + ' transverse momentum distribution in ' + str(barrelEta) + ' < abs(#eta) < ' + str(detectorEta),
  bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 340, 400],
  input_objects = 'trigger_objects_endcap',
  value_func = pt,
  log_y = True
)

coarseBinnedPtForwardDistribution = cfg.Analyzer(
  Histogrammer,
  'coarseBinnedPt' + triggerObjectName + 'ForwardDistribution',
  file_label = 'tfile1',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'coarseBinnedPt' + triggerObjectName + 'ForwardDistribution',
  histo_title = triggerObjectName + ' transverse momentum distribution in ' + str(barrelEta) + ' < abs(#eta) < ' + str(detectorEta),
  bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 220, 240, 260, 280, 300, 340, 400],
  input_objects = 'trigger_objects_forward',
  value_func = pt,
  log_y = True
)

smearJetToTriggerObject = cfg.Analyzer(
  Smearer,
  'smearJetToTriggerObject',
  input_collection = 'gen_objects',
  output_collection = triggerObjectName,
  convolution_file = convolutionFileName,
  convolution_histogram_prefix = "deltaPtDistributionBinnedInMatchedObject",
  bins = ptBins,
  object_x_range = (-300, 300),
  probability_file = probabilityFile,
  probability_histogram = probabilityHistogram
)

def isSmeared(ptc):
  return ptc.match is not None

smearedSelector = cfg.Analyzer(
  Selector,
  'smearedSelector',
  output = 'smeared_gen_objects',
  input_objects = 'gen_objects',
  filter_func = isSmeared
)

def isMatchSmeared(ptc):
  return ptc.match.match is not None

matchSmearedSelector = cfg.Analyzer(
  Selector,
  'matchSmearedSelector',
  output = 'good_trigger_objects',
  input_objects = 'trigger_objects',
  filter_func = isMatchSmeared
)

genJetSimL1TObjectTree = cfg.Analyzer(
  MatchedParticlesTreeProducer,
  'genJetSimL1TObjectTree',
  file_label = "tfile1",
  tree_name = 'genJetSimL1TObjectTree',
  tree_title = 'Tree containing info about matched gen and Sim' + triggerObjectName,
  particle_collection = 'smeared_gen_objects',
  matched_particle_name = "Sim" + triggerObjectName,
  particle_name = "genJet"
)

smearedObjectDeltaPtDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'smearedObjectDeltaPtDistributionBinnedInMatchedObject',
  histo_name = 'smearedObjectDeltaPtDistributionBinnedInMatchedObject',
  histo_title = 'p_{t}^{Sim' + triggerObjectName + '} distribution binned in p^{' + genObjectName +'}_{t}',
  matched_collection = triggerObjectName,
  binning = ptBins,
  nbins = 1600,
  min = -400,
  max = 400,
  file_label = "tfile1",
  plot_func = deltaPt,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{Sim" + triggerObjectName + "} [GeV]",
  y_label = "# events",
)

l1tObjectDeltaPtDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'l1tObjectDeltaPtDistributionBinnedInMatchedObject',
  histo_name = 'l1tObjectDeltaPtDistributionBinnedInMatchedObject',
  histo_title = 'p_{t}^{' + triggerObjectName + '} distribution binned in p^{' + genObjectName +'}_{t}',
  matched_collection = 'trigger_objects',
  binning = ptBins,
  nbins = 1600,
  min = -400,
  max = 400,
  file_label = "tfile1",
  plot_func = deltaPt,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{" + triggerObjectName + "} [GeV]",
  y_label = "# events",
)

def barrelCut(ptc):
  return abs(ptc.eta()) < barrelEta

def endcapCut(ptc):
  return (abs(ptc.eta()) > barrelEta and abs(ptc.eta()) < endcapEta)

def forwardCut(ptc):
  return (abs(ptc.eta()) > endcapEta and abs(ptc.eta()) < detectorEta)

def detectorCut(ptc):
  return (abs(ptc.eta()) < detectorEta)

barrelSelector = cfg.Analyzer(
  Selector,
  'barrelSelector',
  output = 'trigger_objects_barrel',
  input_objects = 'trigger_objects',
  filter_func = barrelCut 
)

endcapSelector = cfg.Analyzer(
  Selector,
  'endcapSelector',
  output = 'trigger_objects_endcap',
  input_objects = 'trigger_objects',
  filter_func = endcapCut
)

forwardSelector = cfg.Analyzer(
  Selector,
  'forwardSelector',
  output = 'trigger_objects_forward',
  input_objects = 'trigger_objects',
  filter_func = forwardCut
)

detectorSelector = cfg.Analyzer(
  Selector,
  'detectorSelector',
  output = 'trigger_objects_detector',
  input_objects = 'trigger_objects',
  filter_func = detectorCut
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  cmsMatchingSource,
  barrelSelector,
  endcapSelector,
  forwardSelector,
  detectorSelector,
  goodGenObjectFilter,
  qualityFilter,
  genPtDistribution,
  smearJetToTriggerObject,
  ptDistribution,
  smearedSelector,
  matchSmearedSelector,
  coarseBinnedPtDistribution,
  genJetSimL1TObjectTree,
  smearedPtDistribution,
  coarseBinnedSmearedPtDistribution,
  coarseBinnedPtBarrelDistribution,
  coarseBinnedPtEndcapDistribution,
  coarseBinnedPtForwardDistribution,
  smearedObjectDeltaPtDistributionBinnedInMatchedObject,
  l1tObjectDeltaPtDistributionBinnedInMatchedObject
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
