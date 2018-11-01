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
from heppy.analyzers.Filter import Filter
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
objectName = _heppyGlobalOptions["triggerObjectName"] #L1T Muon
matchedObjectName = _heppyGlobalOptions["genObjectName"] #Gen Muon
#sampleName = "l1tGenJetMatching_QCD_15_3000_NoPU_Phase1_L11Obj_To_GenJet_Match_ClosestDR_L1TEGamma_GenJet"
sampleName = "l1tMuonGenMuonMatching_SingleMu_FlatPt_8to100_QualityCut_WQualityBranch"
ptBins = [0, 1.5, 3, 5, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]
minimumPtInBarrel = float(_heppyGlobalOptions["minimumPtInBarrel"])
minimumPtInEndcap = float(_heppyGlobalOptions["minimumPtInEndcap"])
minimumPtInForward = float(_heppyGlobalOptions["minimumPtInForward"])
barrelEta = float(_heppyGlobalOptions["barrelEta"])
endcapEta = float(_heppyGlobalOptions["endcapEta"])
detectorEta = float(_heppyGlobalOptions["detectorEta"])
deltaR2Matching = float(_heppyGlobalOptions["deltaR2Matching"])
qualityThreshold = int(_heppyGlobalOptions["quality"])


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

def deltaPt(ptc):
  return ptc.pt() - ptc.match.pt()

def deltaPtRatio(ptc):
  return (ptc.pt() - ptc.match.pt())/ptc.match.pt()

def pt(ptc):
  return ptc.pt()

def deltaEta (ptc):
  return ptc.eta() - ptc.match.eta()

def eta (ptc):
  return ptc.eta()

def deltaPhi (ptc):
  return ptc.phi() - ptc.match.phi()

def isMatched(ptc):
  return ptc.match is not None

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
  return event.trigger_objects[0].quality >= qualityThreshold

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

#ptBins = []
#for x in xrange(0, 130, 10):
#  ptBins.append(x)

deltaPtDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'deltaPtDistributionBinnedInMatchedObject',
  histo_name = 'deltaPtDistributionBinnedInMatchedObject',
  histo_title = 'p_{t}^{' + objectName + '} - p_{t}^{' + matchedObjectName +'} distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'trigger_objects',
  binning = ptBins,
  nbins = 1600,
  min = -400,
  max = 400,
  file_label = "tfile1",
  plot_func = deltaPt,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{" + objectName + "} - p_{t}^{" + matchedObjectName + "} [GeV]",
  y_label = "# events",
)

deltaPtRatioDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'deltaPtRatioDistributionBinnedInMatchedObject',
  histo_name = 'deltaPtRatioDistributionBinnedInMatchedObject',
  histo_title = '#frac{#Delta p_{t}}{p_{t}^{' + matchedObjectName +  '}} distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'trigger_objects',
  binning = ptBins,
  nbins = 1600,
  min = -400,
  max = 400,
  file_label = "tfile1",
  plot_func = deltaPtRatio,
  bin_func = pt,
  log_y = False,
  x_label = "p_{t}^{" + objectName + "} - p_{t}^{" + matchedObjectName + "} [GeV]",
  y_label = "# events",
)

deltaEtaDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'deltaEtaDistributionBinnedInMatchedObject',
  histo_name = 'deltaEtaDistributionBinnedInMatchedObject',
  histo_title = '#Delta #eta distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'trigger_objects',
  binning = ptBins,
  nbins = 400,
  min = -2,
  max = +2,
  file_label = "tfile1",
  plot_func = deltaEta,
  bin_func = pt,
  log_y = False,
  x_label = "#eta^{" + objectName + "} - #eta^{" + matchedObjectName + "}",
  y_label = "# events"
)

etaDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'etaDistributionBinnedInMatchedObject',
  histo_name = 'etaDistributionBinnedInMatchedObject',
  histo_title = '#eta^{' + objectName + '} distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'trigger_objects',
  binning = ptBins,
  nbins = 400,
  min = -2,
  max = +2,
  file_label = "tfile1",
  plot_func = eta,
  bin_func = pt,
  log_y = False,
  x_label = "#eta^{" + objectName + "}",
  y_label = "# events"
)

deltaPhiDistributionBinnedInMatchedObject = cfg.Analyzer(
  MatchedObjectBinnedDistributions,
  instance_label = 'deltaPhiDistributionBinnedInMatchedObject',
  histo_name = 'deltaPhiDistributionBinnedInMatchedObject',
  histo_title = '#DeltaR distribution binned in p^{' + matchedObjectName +'}_{t}',
  matched_collection = 'trigger_objects',
  binning = ptBins,
  nbins = 628,
  min = -3.14,
  max = 3.14,
  file_label = "tfile1",
  plot_func = deltaPhi,
  bin_func = pt,
  log_y = False,
  x_label = "#phi^{" + objectName + "} - #phi^{" + matchedObjectName + "}",
  y_label = "# events"
)

genJetL1TObjectTree = cfg.Analyzer(
  MatchedParticlesTreeProducer,
  'genJetL1TObjectTree',
  file_label = "tfile1",
  tree_name = 'genJetL1TObjectTree',
  tree_title = 'Tree containing info about matched gen and ' + objectName,
  particle_collection = 'trigger_objects',
  matched_particle_name = objectName,
  particle_name = "genJet"
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  goodGenObjectFilter,
  qualityFilter,
  etaDistributionBinnedInMatchedObject,
  deltaEtaDistributionBinnedInMatchedObject,
  deltaPhiDistributionBinnedInMatchedObject,
  deltaPtRatioDistributionBinnedInMatchedObject,
  genJetL1TObjectTree
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
