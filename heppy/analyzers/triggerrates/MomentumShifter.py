'''Trasforms a jet into another object using a sort of MC algorithm.'''

from heppy.framework.analyzer import Analyzer
import collections
from numpy.random import RandomState
import pdb
from ROOT import TFile
from bisect import bisect_right
from copy import deepcopy

class MomentumShifter  (Analyzer):
  '''Applies a shift to the momentum of a object

  Example:  

  from heppy.analyzers.triggerrates.MomentumShifter import MomentumShifter  
  momemntum = cfg.Analyzer(
    MomentumShifter ,
    input_collection = 'jets',
    output_collection = 'pileup_jet',
    shift = 15.
  )
  
  * input_collection : input collection containing the jets
  * output_collection : output collection which the converted jet will be stored in, i.e. the type of object the jet will be converted to
  * shift : shift in GeV

  '''

  def beginLoop(self, setup):
    super(MomentumShifter, self).beginLoop(setup)
    self.shift = self.cfg_ana.shift
  # End beginLoop

  def process(self, event):
    
    jets = getattr(event, self.cfg_ana.input_collection)
    output_collection = []
    
    # jetIdx = 0

    for jet in jets:
      jetPt = jet.pt()
      jetEta = jet.eta()
      jetPhi = jet.phi()
      jetE = jet.e()
      
      #Creating a new object with the shifted momentum
      shiftedObject = deepcopy(jet)
      shiftedObject._tlv.SetPtEtaPhiE(jetPt + self.shift, jetEta, jetPhi, jetE)
      output_collection.append(shiftedObject)

    setattr(event, self.cfg_ana.output_collection, output_collection)
  # End process