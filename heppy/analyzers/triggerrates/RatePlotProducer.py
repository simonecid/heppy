'''Produces a rate plot'''

from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile
from ROOT import TH1F
from ROOT import TCanvas
from ROOT import TLine
from array import array
from numpy import power

from bisect import insort

import collections

class RatePlotProducer(Analyzer):

  '''Analyzer creating a rate plot and saving it to ROOT and SVG format.
  
  Example::
  
    rate = cfg.Analyzer(
      RatePlotProducer,
      file_label = 'tfile1',
      plot_name = 'rate',
      plot_title = 'A rate plot',
      instantaneous_luminosity = 3e35,
      cross_section = 100,
      input_objects = 'jets',
      bins = [30, 40, 50, 60],
      yscale = 1e6,
      pileup = 180,
      scale_factors = [3, 5, 4]
    )
    
  * file_label: (Facultative) Name of a TFileService. If specified, the histogram will be saved in that root file, otherwise it will be saved in a <plot_name>.png and <plot_name>.root file
  * plot_name: Name of the plot (Key in the output root file).
  * plot_title: Title of the plot.
  * bins: Array containing the bins to be tested
  * instantaneous_luminosity: instantaneous luminosity in cm^-2 s^-1
  * cross_section: cross section in mb
  * input_objects: name of the particle collection
  * yscale: y level of the reference line
  * pileup: pile-up level, used to estimate where the single-object rate can be approximated as a trigger rate
  * scale_factors: custom factors to be applied to the bin, 1 is assumed in case of missing parameter or if less factors than bins are provided
  '''
  
  '''Generates a threshold function'''
  def thresholdTriggerGenerator(self, threshold):
    def thresholdTrigger(ptc):
      return ptc.pt() > threshold
    return thresholdTrigger
    
  def beginLoop(self, setup):
    super(RatePlotProducer, self).beginLoop(setup)
    
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

    self.bins = array("f", self.cfg_ana.bins)
    self.histogram = TH1F(self.cfg_ana.plot_name, self.cfg_ana.plot_title, len(self.bins) - 1 , self.bins)
    self.numberOfEvents = 0 

    # Sorted array of pt, used to find the estimate the probability that 2 jets above a certain
    # threshold will appear in the same event

  def process(self, event):
    '''Process the event.
      event must contain
    
    * self.cfg_ana.input_objects: collection of objects to be selected
       These objects must be usable by the filtering function
       self.cfg_ana.trigger_func.
    '''

    input_collection = getattr(event, self.cfg_ana.input_objects)

    self.numberOfEvents += 1

    #We want accept events without objects if the threshold is 0 or less
    startIdx = 0

    #Adding events for that thresholds
    for x in xrange(0, len(self.bins) - 1):
      if self.bins[x] <= 0:
        self.histogram.AddBinContent(x+1)
        startIdx = x + 1
      else:
        # stop here, no more below 0 bins
        break

    #startIdx keeps track of where the positive thresholds start

    # MET is not iterable, it is a single object
    # We treat here single objects
    if not isinstance(input_collection, collections.Iterable):

      for x in xrange(startIdx, len(self.bins) - 1):
        # Preparing the check function
          trigger_func = self.thresholdTriggerGenerator(self.bins[x])
          # Checking if the object passes the trigger
          if trigger_func(input_collection):
            self.histogram.AddBinContent(x+1)
          else:
          #If no item passes the threshold I can stop
            break

    elif isinstance(input_collection, collections.Mapping):
  
      # Iterating through all the objects
      for x in xrange(startIdx, len(self.bins) - 1):
        # Checking what thresholds are satisfied
        isPassed = False
        for key, val in input_collection.iteritems():

          # Preparing the check function
          trigger_func = self.thresholdTriggerGenerator(self.bins[x])
          # Checking if the object passes the trigger
          if trigger_func(val):
            self.histogram.AddBinContent(x+1)
            isPassed = True
            # We don't need to check for other objects
            break

        if not isPassed:
          #If no objects passes the threshold I can stop
          break     
      
    else:
      for x in xrange(startIdx, len(self.bins) - 1):
        # Checking what thresholds are satisfied
        isPassed = False
        for obj in input_collection:
          # Preparing the check function
          trigger_func = self.thresholdTriggerGenerator(self.bins[x])
          # Checking if the object passes the trigger
          if trigger_func(obj):
            self.histogram.AddBinContent(x+1)
            isPassed = True
            # We don't need to check for other objects
            break

        if not isPassed:
          #If no objects passes the threshold I can stop
          break

  def write(self, setup):

    #Rescaling to corresponding rate
    if getattr(self.cfg_ana, "normalise", False):
      expected_rate = self.cfg_ana.instantaneous_luminosity * 1e-27 * self.cfg_ana.cross_section
      normalisation = expected_rate/self.numberOfEvents
      #Rescaling everything to have rates
      self.histogram.Scale(normalisation)

    if hasattr(self.cfg_ana, "scale_factors"):
      for x in xrange(0, len(self.cfg_ana.scale_factors)):
        self.histogram.SetBinContent(x+1, self.histogram.GetBinContent(x+1)*self.cfg_ana.scale_factors[x])
    
    #self.histogram.Write()
    xMax = self.histogram.GetXaxis().GetXmax()
    xMin = self.histogram.GetXaxis().GetXmin()
    yMin = self.histogram.GetMinimum()
    yMax = self.histogram.GetMaximum()


    c1 = TCanvas ("canvas_" + self.cfg_ana.plot_name, self.cfg_ana.plot_title, 600, 600)
    c1.SetGridx()
    c1.SetGridy()
    self.histogram.Draw("")
    c1.SetLogy(True)
    self.histogram.Write()


    #self.rootfile.Close()
