'''Test analyzer creating a simple root tree.'''

from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile
from ROOT import TH1F
from ROOT import TCanvas
from array import array
import collections

class RatePlotProducer(Analyzer):

  '''Analyzer creating a rate plot.
  
  Example::
  
    rate = cfg.Analyzer(
      RatePlotProducer,
      plot_name = 'rate',
      plot_title = 'A rate plot',
      instantaneous_luminosity = 3e35,
      cross_section = 100,
      input_objects = 'jets',
      thresholds = [30, 40, 50, 60]
    )
    
  @param plot_name: Name of the plot (Key in the output root file).
  @param plot_title: Title of the plot.
  @param thresholds: Array containing the threshold to be tested
  @param instantaneous_luminosity: instantaneous luminosity in cm^-2 s^-1
  @param cross_section: cross section in mb
  @param input_objects: name of the particle collection
  '''
  
  '''Generates a threshold function'''
  def thresholdTriggerGenerator(self, threshold):
    def thresholdTrigger(ptc):
      return ptc.pt() > threshold
    return thresholdTrigger
    
  def beginLoop(self, setup):
    super(RatePlotProducer, self).beginLoop(setup)
    self.rootfile = TFile('/'.join([self.dirName,
                                    'tree.root']),
                          'recreate')

    bins = array("f", self.cfg_ana.thresholds)
    self.histogram = TH1F(self.cfg_ana.plot_name, self.cfg_ana.plot_title, len(bins) - 1 , bins)
    self.numberOfEvents = 0 

  def process(self, event):
    '''Process the event.
      event must contain
    
    * self.cfg_ana.input_objects: collection of objects to be selected
       These objects must be usable by the filtering function
       self.cfg_ana.trigger_func.
    '''

    input_collection = getattr(event, self.cfg_ana.input_objects)

    self.numberOfEvents += 1
        
    if isinstance(input_collection, collections.Mapping):
      
      # Iterating through all the jets
      for x in range(0, len(self.cfg_ana.thresholds) - 1):
        # Checking what thresholds are satisfied
        isPassed = False
        for key, val in input_collection.iteritems():
          # Preparing the check function
          trigger_func = self.thresholdTriggerGenerator(self.cfg_ana.thresholds[x])
          # Checking if the jet passes the trigger
          if trigger_func(val):
            self.histogram.AddBinContent(x+1);
            isPassed = True
            # We don't need to check for other jets
            break

        if not isPassed:
          #If no jets passes the threshold I can stop
          break
      
    else:
      for x in range(0, len(self.cfg_ana.thresholds) - 1):
        # Checking what thresholds are satisfied
        isPassed = False
        for obj in input_collection:
          # Preparing the check function
          trigger_func = self.thresholdTriggerGenerator(self.cfg_ana.thresholds[x])
          # Checking if the jet passes the trigger
          if trigger_func(obj):
            self.histogram.AddBinContent(x+1);
            isPassed = True
            # We don't need to check for other jets
            break

        if not isPassed:
          #If no jets passes the threshold I can stop
          break

  def write(self, setup):

    #Rescaling to corresponding rate

    print "The number of events is ", self.numberOfEvents
    
    expected_rate = self.cfg_ana.instantaneous_luminosity * 1e-27 * self.cfg_ana.cross_section
    normalisation = expected_rate/self.numberOfEvents
    #Rescaling everything to have rates
    self.histogram.Scale(normalisation)
    
    self.histogram.Write()
    self.rootfile.Write()
    c1 = TCanvas ("c1", "c1", 600, 600)
    c1.SetGridx()
    c1.SetGridy()
    self.histogram.Draw("")
    c1.Update()
    c1.Print("rate_VS_JetPt.png", "png")

    self.rootfile.Close()
