'''Trasforms a jet into another object using a sort of MC algorithm.'''

from heppy.framework.analyzer import Analyzer
import collections
from numpy.random import RandomState

class JetTransformer  (Analyzer):
  '''Transforms a jet into another object with a certaing probability.
  
  Example: 

  Let's suppose that a 10-20 GeV jet has a 5% prob to become an electron, and a 20-30% has a 1%. 
  We would have:

  jetToElectron = []
  jetToElectron.append(1) # 0-10 GeV
  jetToElectron.append(0.05) #10-20 GeV
  jetToElectron.append(0.01) #20-30 GeV

  from heppy.analyzers.JetTransformer   import JetTransformer  
  jetToElectronTrasformer = cfg.Analyzer(
    JetTransformer ,
    output_objects = 'electrons',
    conversion_factors = jetToElectron,
  )
  
  * conversion_factors : jet-to-object conversion factors, first will be always ignored. It is at steps of 10 GeV.
  * output_objects : output collection which the jet will be stored in, i.e. the type of object the jet will be converted to
  
  '''

  def beginLoop(self, setup):
    super(JetTransformer, self).beginLoop(setup)
    self.rng = RandomState()
    self.rng.seed()

  def process(self, event):
    '''event must contain
    
    * self.cfg_ana.output_objects: collection of objects to be selected
       These objects must be usable by the filtering function
       self.cfg_ana.trigger_func.
    '''
    output_collection = getattr(event, self.cfg_ana.input_objects)
    jets = event.jets

    jetIdx = 0

    for jet in jets:
      jetPt = jet.pt()
      if jetPt >= 10 :
        # Getting the corresponding index
        factorIndex = int(jet.pt()/10)
        # Checking if it must be converted
        if self.rng.uniform(0, 1) < self.conversion_factors[factorIndex] : 
          # It has to be converted: I will remove the object from the jet collection and add it to the output one
          output_collection.append(jet)
          del jet[jetIdx]
      
      jetIdx += 1