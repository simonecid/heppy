'''Merge information from different MinBias events to generate a pile-up event'''

from heppy.framework.analyzer import Analyzer
from ROOT import TH1I
import collections
from ROOT import TCanvas
from numpy.random import poisson

class CollectionMerger(Analyzer):
  '''Merge information from different collections to form a unique list

  Example::

  collectionMerger = cfg.Analyzer(
    CollectionMerger,
    input_collections = ['l1tMuons', "fakeMuons"],
    output_collection = 'l1tMuons'
  )
  
  * input_collections: Collection of names, these objects will be merged in the new event
  * output_collection: name of the merged collection

  '''

  def beginLoop(self, setup):
    super(CollectionMerger, self).beginLoop(setup)
      
  def process(self, event):

    outputList = []

    for collection in self.cfg_ana.input_collections:
      outputList.extend(getattr(event, collection))

    setattr(event, self.cfg_ana.output_collection, outputList)