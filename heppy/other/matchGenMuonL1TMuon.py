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
from heppy.analyzers.triggerrates.Histogrammer import Histogrammer
import sys
from heppy.framework.looper import Looper
from heppy.test.mySamples import *

logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

# Retrieving the sample to analyse

sampleName = "l1tMuonGenMuonMatching_QCD_15_3000_NoPU_Phase1"

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
mySettings.bunchCrossingFrequency = 1/25e-9 # 40 MHz

source = cfg.Analyzer(
  CMSMatchingReader,
  'source',
)

gSystem.Load("libdatamodelDict")


steps = []

x = 0
while x <= 100:
  steps.append(x)
  x += 0.5

# File in which all the rate plots will be stored 

tfile_service_1 = cfg.Service(
  TFileService,
  'dr2PlotFile',
  fname='dr2Plot.root',
  option='recreate'
)

def dr2(ptc):
  return ptc.deltaR2

dr2Plot = cfg.Analyzer(
  Histogrammer,
  file_label = 'dr2PlotFile',
  histo_name = 'dr2Plot',
  histo_title = 'DeltaR2 distribution',
  min = 0,
  max = 25,
  nbins = 250,
  input_objects = 'trigger_objects',
  value_func = dr2,
  x_label = "#DeltaR^{2}",
  y_label = "\# events"
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
  source,
  dr2Plot
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

