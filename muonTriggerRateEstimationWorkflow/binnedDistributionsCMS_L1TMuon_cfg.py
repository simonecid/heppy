import os
import copy
import heppy.framework.config as cfg
from heppy.samples.mySamples import *
import logging
from heppy.framework.chain import Chain as Events
from heppy.framework.services.tfile import TFileService
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
from heppy.framework.looper import Looper
from heppy.analyzers.Matcher import Matcher
from heppy.analyzers.Selector import Selector
from heppy.analyzers.triggerrates.MatchedParticlesTreeProducer import MatchedParticlesTreeProducer
from heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions import MatchedObjectBinnedDistributions
from heppy.analyzers.triggerrates.MatchedObjectBinnedCumulativeDistributions import MatchedObjectBinnedCumulativeDistributions
from heppy.analyzers.triggerrates.CMSMatchingReader import CMSMatchingReader
from heppy.analyzers.triggerrates.ObjectFinder import ObjectFinder
from heppy.analyzers.triggerrates.HistogrammerCumulative import HistogrammerCumulative
from heppy.framework.heppy_loop import _heppyGlobalOptions
from math import sqrt

# next 2 lines necessary to deal with reimports from ipython
#logging.shutdown()
#reload(logging)
#logging.basicConfig(level=logging.WARNING)

#Object name
objectName = "L1T Muon"
matchedObjectName = "Gen Muon"
#sampleName = "l1tGenJetMatching_QCD_15_3000_NoPU_Phase1_L11Obj_To_GenJet_Match_ClosestDR_L1TEGamma_GenJet"
sampleName = "l1tMuonGenMuonMatching_SingleMu_FlatPt_8to100_QualityCut_WQualityBranch"
ptBins = [0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]
muonMinimumPtInBarrel = float(_heppyGlobalOptions["minimumPtInBarrel"])
muonMinimumPtInEndcap = float(_heppyGlobalOptions["minimumPtInEndcap"])
barrelEta = float(_heppyGlobalOptions["barrelEta"])
deltaR2Matching = float(_heppyGlobalOptions["deltaR2Matching"])
deltaEtaMatching = float(_heppyGlobalOptions["deltaEtaMatching"])

if "binning" in _heppyGlobalOptions:
  import ast
  ptBins = ast.literal_eval(_heppyGlobalOptions["binning"])

# Retrieving the sample to analyse

#if specified in sample, a specific set will be used, otherwise the full set will be employed
if "sample" in _heppyGlobalOptions:
  sampleName = _heppyGlobalOptions["sample"]
if sampleName == "all":
  selectedComponents = [
    cmsMatching_QCD_15_3000_L1TMuon_GenJet,
    cmsMatching_QCD_15_3000_L1TEGamma_GenJet,
    cmsMatching_QCD_15_3000_L1TTau_GenJet,
  ]
else:  
  sample = globals()[sampleName]
  selectedComponents = [
    sample
  ]

# Defining pdgids

source = cfg.Analyzer(
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

def deltaPt(ptc):
  return ptc.pt() - ptc.match.pt()

def eta (ptc):
  return ptc.eta()

def phi (ptc):
  return ptc.phi()

def matchedParticlePt (ptc):
  return ptc.match.pt()

def matchedParticleEta (ptc):
  return ptc.match.eta()

def ptRatioWithMatched (ptc):
  return ptc.pt()/ptc.match.pt()

def deltaR (ptc):
  return sqrt(ptc.deltaR2)

def isMatched(ptc):
  return ptc.match is not None

def qualityCut(ptc):
  return ptc.quality >=int(_heppyGlobalOptions["quality"])

def quality(ptc):
  return ptc.quality

def dr2Selection(ptc):
  return (abs(ptc.deltaR2) < deltaR2Matching) and (abs(ptc.eta() - ptc.match.eta()) < deltaEtaMatching) # dr < 0.5

def genMuInDetector(ptc):
  if (abs(ptc.match.eta()) < barrelEta):
    #It is OK if the momentum is high enough to not start spiralling
    return (ptc.match.pt() > muonMinimumPtInBarrel)
  else:
    return (ptc.match.pt() > muonMinimumPtInEndcap)

kinematicCutSelector = cfg.Analyzer(
  Selector,
  'kinematicCutSelector',
  output = 'trigger_objects_in_detector',
  input_objects = 'trigger_objects',
  filter_func = genMuInDetector
)

muonQualityCut = cfg.Analyzer(
  Selector,
  'muonQualityCut',
  output = 'good_trigger_objects',
  input_objects = 'trigger_objects_in_detector',
  filter_func = qualityCut
)

tightRestrictionMatchSelector = cfg.Analyzer(
  Selector,
  'tightRestrictionMatchSelector',
  output = 'matched_trigger_object',
  input_objects = 'good_trigger_objects',
  filter_func = dr2Selection 
)

#ptBins = []
#for x in xrange(0, 130, 10):
#  ptBins.append(x)

objectPtDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'objectPtDistributionBinnedInMatchedObject',
  histo_name = 'objectPtDistributionBinnedInMatchedObject',
  histo_title = 'p_{t}^{' + objectName + '} distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = ptBins,
  nbins = 200,
  min = 0,
  max = 100,
  file_label = "tfile1",
  plot_func = pt,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{" + objectName + "} [GeV]",
  y_label = "# events",
)

objectPtCumulativeDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedCumulativeDistributions,
  instance_label = 'objectPtCumulativeDistributionBinnedInMatchedObject',
  histo_name = 'objectPtCumulativeDistributionBinnedInMatchedObject',
  histo_title = 'p_{t}^{' + objectName + '} cumulative distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = ptBins,
  nbins = 200,
  min = 0,
  max = 100,
  file_label = "tfile1",
  plot_func = pt,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{" + objectName + "} [GeV]",
  y_label = "# events",
  inverted = True
)

matchedObjectPtDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'matchedObjectPtDistributionBinnedInMatchedObject',
  histo_name = 'matchedObjectPtDistributionBinnedInMatchedObject',
  histo_title = 'p_{t}^{' + matchedObjectName + '} distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = ptBins,
  nbins = 200,
  min = 0,
  max = 200,
  file_label = "tfile1",
  plot_func = matchedParticlePt,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{" + objectName + "} [GeV]",
  y_label = "# events",
)

deltaPtDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'deltaPtDistributionBinnedInMatchedObject',
  histo_name = 'deltaPtDistributionBinnedInMatchedObject',
  histo_title = 'p_{t}^{' + objectName + '} - p_{t}^{' + matchedObjectName +'} distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = ptBins,
  nbins = 800,
  min = -200,
  max = 200,
  file_label = "tfile1",
  plot_func = deltaPt,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{" + objectName + "} - p_{t}^{match} [GeV]",
  y_label = "# events",
)

objectEtaDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'objectEtaDistributionBinnedInMatchedObject',
  histo_name = 'objectEtaDistributionBinnedInMatchedObject',
  histo_title = '#eta^{' + objectName + '} distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = ptBins,
  nbins = 200,
  min = -10,
  max = +10,
  file_label = "tfile1",
  plot_func = eta,
  bin_func = pt,
  log_y = False,
  x_label = "#eta",
  y_label = "# events"
)

matchedObjectEtaDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'matchedObjectEtaDistributionBinnedInMatchedObject',
  histo_name = 'matchedObjectEtaDistributionBinnedInMatchedObject',
  histo_title = '#eta^{' + matchedObjectName + '} distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = ptBins,
  nbins = 200,
  min = -10,
  max = +10,
  file_label = "tfile1",
  plot_func = matchedParticleEta,
  bin_func = pt,
  log_y = False,
  x_label = "#eta",
  y_label = "# events"
)

objectMatchedObjectPtRatioDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'objectMatchedObjectPtRatioDistributionBinnedInMatchedObject',
  histo_name = 'objectMatchedObjectPtRatioDistributionBinnedInMatchedObject',
  histo_title = 'p_{t}^{' + objectName + '}/p_{t}^{' + matchedObjectName +'} distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = ptBins,
  nbins = 800,
  min = 0,
  max = 20,
  file_label = "tfile1",
  plot_func = ptRatioWithMatched,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{" + objectName + "}/p_{t}^{' + matchedObjectName +'}",
  y_label = "# events"
)

deltaRDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'deltaRDistributionBinnedInMatchedObject',
  histo_name = 'deltaRDistributionBinnedInMatchedObject',
  histo_title = '#DeltaR distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'matched_trigger_object',
  binning = ptBins,
  nbins = 500,
  min = 0,
  max = 5,
  file_label = "tfile1",
  plot_func = deltaR,
  bin_func = pt,
  log_y = False,
  x_label = "#DeltaR",
  y_label = "# events"
)

objectPtDistribution = cfg.Analyzer(
  Histogrammer,
  'objectPtDistribution',
  file_label = 'tfile1',
  histo_name = 'objectPtDistribution',
  histo_title = 'p_{t}^{' + objectName + '} distribution',
  min = 0,
  max = 100,
  nbins = 200,
  input_objects = 'matched_trigger_object',
  value_func = pt,
  x_label = "p_{t}^{" + objectName + "}",
  y_label = "\# events"
)

objectQualityDistribution = cfg.Analyzer(
  Histogrammer,
  'objectQualityDistribution',
  file_label = 'tfile1',
  histo_name = 'objectQualityDistribution',
  histo_title = 'Quality^{' + objectName + '} distribution',
  min = 0,
  max = 20,
  nbins = 20,
  input_objects = 'matched_trigger_object',
  value_func = quality,
  x_label = "Quality^{" + objectName + "}",
  y_label = "\# events"
)

matchedObjectPtDistribution = cfg.Analyzer(
  Histogrammer,
  'matchedObjectPtDistribution',
  file_label = 'tfile1',
  histo_name = 'matchedObjectPtDistribution',
  histo_title = 'p_{t}^{' + matchedObjectName + '} distribution',
  min = 0,
  max = 200,
  nbins = 200,
  input_objects = 'matched_trigger_object',
  value_func = matchedParticlePt,
  x_label = "p_{t}^{" + objectName + "}",
  y_label = "\# events"
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  kinematicCutSelector,
  muonQualityCut,
  tightRestrictionMatchSelector,
  objectPtDistributionBinnedInMatchedObject,
  objectMatchedObjectPtRatioDistributionBinnedInMatchedObject,
  objectEtaDistributionBinnedInMatchedObject,
  matchedObjectEtaDistributionBinnedInMatchedObject,
  deltaRDistributionBinnedInMatchedObject,
  deltaPtDistributionBinnedInMatchedObject,
  objectPtDistribution,
  objectQualityDistribution,
  matchedObjectPtDistribution,
  matchedObjectPtDistributionBinnedInMatchedObject,
  objectPtCumulativeDistributionBinnedInMatchedObject,
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
