'''Produces a plot showing the fraction of accepted events against a triggerable quantity.'''

from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile
from ROOT import TH1F
from ROOT import TGraphErrors
from ROOT import TCanvas
from ROOT import TLine
from array import array
from numpy import power
from scipy.optimize import fsolve
import numpy as np
from math import sqrt

from bisect import insort

import collections

class EfficiencyPlotProducer(Analyzer):

  '''Analyzer creating a rate plot and saving it to ROOT and SVG format.
  
  Example::
  
    def pt (ptc):
      return ptc.pt()

    efficiency = cfg.Analyzer(
      EfficiencyPlotProducer,
      file_label = 'tfile1',
      plot_name = 'efficiency',
      plot_title = 'An efficiency plot',
      input_objects = 'jets',
      min = 0,
      max = 300,
      nbins = 100,
      cfg_ana.value_func = pt
    )
    
  * file_label: (Facultative) Name of a TFileService. If specified, the histogram will be saved in that root file, otherwise it will be saved in a <plot_name>.png and <plot_name>.root file
  * plot_name: Name of the plot (Key in the output root file).
  * plot_title: Title of the plot.
  * input_objects: name of the particle collection
  * min: Minimum of the histogram
  * max: Maximum of the histogram
  * nbins: Number of bins
  * cfg_ana.value_func : function that returns the value to store in the histogram
  '''

  def beginLoop(self, setup):
    super(EfficiencyPlotProducer, self).beginLoop(setup)
    
    self.hasTFileService = hasattr(self.cfg_ana, "file_label")
    if self.hasTFileService:
      servname = '_'.join(['heppy.framework.services.tfile.TFileService',
                          self.cfg_ana.file_label
                      ])
      tfileservice = setup.services[servname]
      self.rootfile = tfileservice.file
    else:
      self.rootfile = TFile('/'.join([self.dirName,
                                      self.cfg_ana.plot_name + '.root']),
                            'recreate')
    
    self.histogram = TH1F(self.cfg_ana.plot_name, self.cfg_ana.plot_title, self.cfg_ana.nbins, self.cfg_ana.min, self.cfg_ana.max)

  def process(self, event):
    '''Process the event.
      event must contain
    
    * self.cfg_ana.input_objects: collection of objects to be selected
       These objects must be usable by the filtering function
       self.cfg_ana.trigger_func.
    '''

    input_collection = getattr(event, self.cfg_ana.input_objects)

    maxValue = 0

    if not isinstance(input_collection, collections.Iterable):
      maxValue = self.cfg_ana.value_func(input_collection)
    elif isinstance(input_collection, collections.Mapping):
      for key, val in input_collection.iteritems():
        maxValue = max(maxValue, self.cfg_ana.value_func(val))
    else: 
      for obj in input_collection:
        maxValue = max(maxValue, self.cfg_ana.value_func(obj))

    stepSize = (self.cfg_ana.max - self.cfg_ana.min)/self.cfg_ana.nbins
    
    binIdx = 1
    for binValue in np.arange(self.cfg_ana.min, self.cfg_ana.max, stepSize):
      if maxValue >= binValue:
        self.histogram.AddBinContent(binIdx)
      binIdx += 1

  def write(self, setup):

    #Rescaling to efficiency
    normalisation = 1/self.histogram.GetBinContent(1)
    #Rescaling everything to have rates
    self.histogram.Scale(normalisation)

    efficiencyPlot = TGraphErrors(self.histogram)
    efficiencyPlot.SetName(self.cfg_ana.plot_name+"_errors")
    efficiencyPlot.SetTitle(self.cfg_ana.plot_title)

    for index in xrange(0, len(efficiencyPlot.GetX())):
      efficiencyPlot.SetPointError(index, 
                                   efficiencyPlot.GetEX()[index], 
                                   sqrt(efficiencyPlot.GetY()[index] * normalisation)
                                  )
    
    c1 = TCanvas ("canvas_" + self.cfg_ana.plot_name, self.cfg_ana.plot_title, 600, 600)
    c1.SetGridx()
    c1.SetGridy()
    efficiencyPlot.Draw("AP")
    c1.Update()
    c1.Write()
    c1.Print(self.cfg_ana.plot_name + ".svg", "svg")
    efficiencyPlot.Write()

    #self.rootfile.Close()
