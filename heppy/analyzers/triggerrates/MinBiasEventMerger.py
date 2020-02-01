'''Merge information from different MinBias events to generate a pile-up event'''

from heppy.framework.analyzer import Analyzer
from ROOT import TH1I
import collections
from ROOT import TCanvas
from numpy.random import poisson

class MinBiasEventMerger(Analyzer):
  '''Merge information from different MinBias events to generate a pile-up event

  The class generates a random number according to the poisson distribution, accumulates data in a list until that number of events has been processed.
  The Analyzer stops the flow until the number of events has been reached. 
  When that number has been reached true is returned, the buffers gets emptied, another random number is generated and a new events begins to be built.

  Example::

  MinBiasEventMerger = cfg.Analyzer(
    MinBiasEventMerger,
    input_objects = ['genparticles'],
    pileup = 180,
    output_objects = ['mergedgenparticles']
  )
  
  * input_objects: Collection of names, these objects will be merged in the new event

  * output_objects: Collection of names, the corresponding name will be used as output of the merge

  * pileup: average pileup level

  '''

  def beginLoop(self, setup):
    super(MinBiasEventMerger, self).beginLoop(setup)
    self.numberOfStoredEvents = 0
    self.pileup = self.cfg_ana.pileup
    self.numberOfEventsToBeStored = 0
    
    for outName in self.cfg_ana.output_objects:
      setattr(self, outName, [])
      
  def process(self, event):

    if self.numberOfEventsToBeStored == 0:
      self.numberOfEventsToBeStored = poisson(self.pileup)
    
    for x in xrange(0, len(self.cfg_ana.input_objects)):
      inName = self.cfg_ana.input_objects[x]
      outName = self.cfg_ana.output_objects[x]
      input_collection = getattr(event, inName)
      output_collection = getattr(self, outName)
      if isinstance(input_collection, collections.Mapping):
        for key, val in input_collection.iteritems():
          output_collection.append(val)
      else:
        for obj in input_collection:
          output_collection.append(obj)

    # Check whether we have stored enough events
    self.numberOfStoredEvents += 1
    if self.numberOfStoredEvents == self.numberOfEventsToBeStored:
      # Returning stuff
      for outName in self.cfg_ana.output_objects:
        output_collection = getattr(self, outName)
        setattr(event, outName, output_collection)
        # Resetting internal variables
        setattr(self, outName, [])

      self.numberOfEventsToBeStored = 0
      self.numberOfStoredEvents = 0
      #The other analyzers may work
      return True

    else:
      # If we have not accumulated enough events we break the event loop and proceed to the following event
      return False