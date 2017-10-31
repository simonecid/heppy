import os
import copy
import heppy.framework.config as cfg
from heppy.framework.heppy_loop import _heppyGlobalOptions
import logging
# next 2 lines necessary to deal with reimports from ipython
from heppy.analyzers.triggerrates.CMSMatchingReader import CMSMatchingReader
from ROOT import gSystem
from heppy.framework.chain import Chain as Events
from heppy.framework.services.tfile import TFileService
from heppy.analyzers.triggerrates.RatePlotProducerPileUp import RatePlotProducerPileUp
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
from heppy.analyzers.triggerrates.LeadingQuantityHistogrammer import LeadingQuantityHistogrammer
from heppy.analyzers.Selector import Selector
import sys
from heppy.framework.looper import Looper
from heppy.test.mySamples import *

logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

# Retrieving the sample to analyse

sampleName = "cmsMatching_SingleNeutrinoPU140_LeadingL1TMuon_QualityCut8"

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

mySettings = lambda a: None
mySettings.yScale = 1e6
'''Instantaneous lumi in cm^-2 s^-1'''
mySettings.bunchCrossingFrequency = 31.6e6 # 2808 bunches

source = cfg.Analyzer(
  CMSMatchingReader,
)

steps = []

x = 0
while x <= 100:
  steps.append(x)
  x += 0.5

def pt(ptc):
  return ptc.pt()

# File in which all the rate plots will be stored 

tfile_service_1 = cfg.Service(
  TFileService,
  'ratePlotFile',
  fname='ratePlots.root',
  option='recreate'
)

def barrelCut(ptc):
  return abs(ptc.eta()) < 1.1

def endcapCut(ptc):
  return (abs(ptc.eta()) > 1.1 and abs(ptc.eta()) < 2.4)

barrelSelector = cfg.Analyzer(
  Selector,
  'barrelSelector',
  output = 'gen_objects_barrel',
  input_objects = 'gen_objects',
  filter_func = barrelCut 
)

endcapSelector = cfg.Analyzer(
  Selector,
  'endcapSelector',
  output = 'gen_objects_endcap',
  input_objects = 'gen_objects',
  filter_func = endcapCut
)

triggerRate = cfg.Analyzer(
  RatePlotProducerPileUp,
  instance_label = 'triggerRate',
  file_label = 'ratePlotFile',
  plot_name = 'triggerRate',
  plot_title = 'Trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'gen_objects',
  bins = steps,
  yscale = mySettings.yScale,
  normalise = True
)

barrelTriggerRate = cfg.Analyzer(
  RatePlotProducerPileUp,
  instance_label = 'barrelTriggerRate',
  file_label = 'ratePlotFile',
  plot_name = 'barrelTriggerRate',
  plot_title = 'abs(#eta) < 1.1 trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'gen_objects_barrel',
  bins = steps,
  yscale = mySettings.yScale,
  normalise = True
)

endcapTriggerRate = cfg.Analyzer(
  RatePlotProducerPileUp,
  instance_label = 'endcapTriggerRate',
  file_label = 'ratePlotFile',
  plot_name = 'endcapTriggerRate',
  plot_title = '1.1 < abs(#eta) < 2.4 trigger rate',
  zerobias_rate = mySettings.bunchCrossingFrequency,
  input_objects = 'gen_objects_endcap',
  bins = steps,
  yscale = mySettings.yScale,
  normalise = True
)

ptDistribution = cfg.Analyzer(
  Histogrammer,
  'ptDistribution',
  file_label = 'ratePlotFile',
  x_label= "pt [GeV]",
  y_label = "# events",
  histo_name = 'ptDistribution',
  histo_title = 'Transverse momentum distribution',
  min = 0,
  max = 100,
  nbins = 100,
  input_objects = 'gen_objects',
  value_func = pt,
  log_y = True
)


leadingPtDistribution = cfg.Analyzer(
  LeadingQuantityHistogrammer,
  'leadingPtDistribution',
  file_label = 'ratePlotFile',
  x_label = "pt [GeV]",
  y_label = "# events",
  histo_name = 'leadingPtDistribution',
  histo_title = 'Leading transverse momentum distribution',
  min = 0,
  max = 100,
  nbins = 100,
  input_objects = 'gen_objects',
  key_func = pt,
  value_func = pt,
  log_y = True
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  barrelSelector,
  endcapSelector,
  barrelTriggerRate,
  endcapTriggerRate,
  triggerRate,
  ptDistribution,
  leadingPtDistribution
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
  loop.process(6)
  print loop.event

