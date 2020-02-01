'''Trasforms a jet into another object using a sort of MC algorithm.'''

from heppy.framework.analyzer import Analyzer
import collections
from numpy.random import RandomState
import pdb
from ROOT import TFile
from bisect import bisect_right
from copy import deepcopy

class LeadingObjectFinder  (Analyzer):
  '''Finds the leading object based on a specific key value and puts it in another collection.

  Example:  

  from heppy.analyzers.triggerrates.LeadingObjectFinder import LeadingObjectFinder  
  leadingPtJetFinder = cfg.Analyzer(
    LeadingObjectFinder ,
    input_collection = 'jets',
    output_collection = 'leading_jet',
    key_func = pt
  )
  
  * input_collection : input collection containing the jets
  * output_collection : output collection which the leading object will be stored in
  * key_func : function that returns the value used to determine the leading object (typically pt for the trigger)

  NOTE: A property 'match' is added to the input object to connect it to the smeared version
  '''

  def beginLoop(self, setup):
    super(LeadingObjectFinder, self).beginLoop(setup)
  # End beginLoop

  def process(self, event):
    
    input_collection = getattr(event, self.cfg_ana.input_collection)
    output_collection = []

    maximumKey = float("-inf")

    if isinstance(input_collection, collections.Mapping):
      for key, val in input_collection.iteritems():
        if self.cfg_ana.key_func(val) > maximumKey:
          maximumKey = self.cfg_ana.key_func(val)
          leadingObject = {key: val}
    else:
      for obj in input_collection:
        if self.cfg_ana.key_func(obj) > maximumKey:
          maximumKey = self.cfg_ana.key_func(obj)
          leadingObject = obj

    if maximumKey > float("-inf"):
      output_collection.append(leadingObject)    

    setattr(event, self.cfg_ana.output_collection, output_collection)
  # End process