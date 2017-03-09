'''Test analyzer creating a simple root tree.'''

from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile
from ROOT import TH1I
from ROOT import TCanvas
from array import array
import collections

class TreeProducer(Analyzer):

  '''Analyzer creating a root tree.
  
  Example::
  
    tree = cfg.Analyzer(
      TreeProducer,
      tree_name = 'events',
      tree_title = 'A simple test tree'
    )
  
  The TTree is written to the file C{tree.root} in the analyzer directory.
  
  * tree_name: Name of the tree (Key in the output root file).
  * tree_title: Title of the tree.
  * thresholds: Array containing the threshold to be tested
  '''
  
  '''Generates a threshold function'''
  def thresholdTriggerGenerator(self, threshold):
    def thresholdTrigger(ptc):
      return ptc.pt() > threshold
    return thresholdTrigger
    
  def beginLoop(self, setup):
    super(TreeProducer, self).beginLoop(setup)
    self.rootfile = TFile('/'.join([self.dirName,
                                    'tree.root']),
                          'recreate')

    bins = array("f", self.cfg_ana.thresholds)
    self.histogram = TH1I("numberOfEvents_VS_JetPt", "Number of events vs jet minimum transverse momentum", len(bins) - 1 , bins)

  def process(self, event):
    '''Process the event.
      event must contain
    
    * self.cfg_ana.input_objects: collection of objects to be selected
       These objects must be usable by the filtering function
       self.cfg_ana.trigger_func.
    '''

    input_collection = getattr(event, self.cfg_ana.input_objects)
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
    self.histogram.Write()
    self.rootfile.Write()
    c1 = TCanvas ("c1", "c1", 600, 600)
    c1.SetGridx()
    c1.SetGridy()
    self.histogram.Draw("")
    c1.Update()
    c1.Print("numberOfEvents_VS_JetPt.png", "png")

    self.rootfile.Close()
