'''Trasforms a jet into another object using a sort of MC algorithm.'''

from heppy.framework.analyzer import Analyzer
import collections
from numpy.random import RandomState
import pdb

class JetTransformer  (Analyzer):
  '''Transforms a jet into another object with a certaing probability.
  
  Example: 

  Let's suppose that a 10-20 GeV jet has a 5% prob to become an electron, and a 20-30 has a 1%. 
  We would have:

  jetToElectron = []
  jetToElectron.append(1) # 0-10 GeV
  jetToElectron.append(0.05) #10-20 GeV
  jetToElectron.append(0.01) #20-30 GeV

  from heppy.analyzers.triggerrates.JetTransformer import JetTransformer  
  jetToElectronTrasformer = cfg.Analyzer(
    JetTransformer ,
    jet_collection = 'jets',
    output_objects = 'electrons',
    conversion_factors = jetToElectron
  )
  
  * jet_objects : input collection containing the jets
  * conversion_factors : jet-to-object conversion factors, first will be always ignored. It is at steps of 10 GeV.
  * output_objects : output collection which the jet will be stored in, i.e. the type of object the jet will be converted to
  
  '''

  def beginLoop(self, setup):
    super(JetTransformer, self).beginLoop(setup)
    self.rng = RandomState()
    self.rng.seed()

  def process(self, event):
    
    jets = getattr(event, self.cfg_ana.jet_collection)
    output_collection = getattr(event, self.cfg_ana.output_objects)
    conversion_factors = self.cfg_ana.conversion_factors

    jetIdx = 0

    if len(jets) > 0:
      pdb.set_trace()

    for jet in jets:
      jetPt = jet.pt()
      if jetPt >= 10 :
        # Getting the corresponding index
        factorIndex = int(jet.pt()/10)
        # Checking if it must be converted
        if factorIndex >= len(conversion_factors):
          continue

        if self.rng.uniform(0, 1) < conversion_factors[factorIndex] : 
          # It has to be converted: I will remove the object from the jet collection and add it to the output one
          print "A jet with", jet.pt(), "has been converted to", self.cfg_ana.output_objects
          output_collection.append(jet)
          # del jets[jetIdx]
      
      jetIdx += 1