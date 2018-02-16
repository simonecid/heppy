'''Trasforms a jet into another object using a sort of MC algorithm.'''

from heppy.framework.analyzer import Analyzer
import collections
from numpy.random import RandomState
import pdb
from ROOT import TFile
from bisect import bisect_right
from copy import deepcopy

class Transformer  (Analyzer):
  '''Applies a numerical smearing to objects

    Example:  

    from heppy.analyzers.triggerrates.Smearer import Smearer  
    jetToElectronTrasformer = cfg.Analyzer(
      Transformer ,
      input_collection = 'jets',
      output_collection = 'l1tEGamma',
      distribution_file = "convFile.root",
      smearing_distribution_prefix = "l1tObjectPtDistributionBinnedInGenJet",
      bins = [0, 10, 20, 30, 40, 50, 60],
      object_x_range = (0, 200),
      probability_file = "probFile.root",
      probability_histogram = "efficiencyPlot"
    )
    
    * input_collection : input collection containing the jets
    * output_collection : output collection which the converted jet will be stored in, i.e. the type of object the jet will be converted to
    * convolution_file : file containing the jet-to-object convolution curves
    * convolution_histogram_prefix : prefix in the convolution file, it will be followed by _10_20, if 10 is the low bin and 20 is the high bin
    * bins : bins of the convolution file
    * object_x_range : range in which the momentum of the genrated object will be located, helps in generating new object faster if the TH1F is very big
    * probability_file : file containing the binned fraction of object to smear (a sort of trasformation probability). If omitted assumed to be 1.
    * probability_histogram : name of the histogram containing the probabilities

    NOTE: A property 'match' is added to the input object to connect it to the transformed version
  '''

  def beginLoop(self, setup):
    super(Transformer, self).beginLoop(setup)
    self.rng = RandomState()
    self.rng.seed()
    self.convolutionHistograms = []
    self.convolutionFile = TFile(self.cfg_ana.convolution_file)
    for x in xrange(0, len(self.cfg_ana.bins) - 1):
      self.convolutionHistograms.append(self.convolutionFile.Get(self.cfg_ana.convolution_histogram_prefix + "_" + str(self.cfg_ana.bins[x]) + "_" + str(self.cfg_ana.bins[x+1])))
    
    self.probabilityFileName = getattr(self.cfg_ana, "probability_file", "")
    if self.probabilityFileName != "":
      self.probabilityFile = TFile(self.probabilityFileName)
      self.probabilityHistogram = self.probabilityFile.Get(
          self.cfg_ana.probability_histogram)
    else:
      self.probabilityFile = None
      self.probabilityHistogram = None
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
      factorIndex = bisect_right(self.cfg_ana.bins, jetPt) - 1
      if factorIndex >= len(self.cfg_ana.bins) - 1:
        jet.match = None
        continue
      
      rndNumber = self.rng.uniform(0, 1)

      if self.probabilityHistogram is None:
        isMisidentified = True
      else:  
        isMisidentified = rndNumber < self.probabilityHistogram.GetBinContent(factorIndex + 1)

      if not isMisidentified:
        jet.match = None
        continue

      #Creating a new object with the same properties
      trgObject = deepcopy(jet)
      # Getting the quantity to add in order to smear
      # I will use the root method which uses the cumulative probability function
      # Reference https://root.cern.ch/doc/master/TH1_8cxx_source.html#l04710
      convolutionHistogram = self.convolutionHistograms[factorIndex]
      rndX = convolutionHistogram.GetRandom()
      trgObject._tlv.SetPtEtaPhiE(rndX, jetEta, jetPhi, jetE)
      jet.match = trgObject
      jet.matches = [trgObject]
      jet.dr = 0
      trgObject.matches = [jet]
      trgObject.match = jet
      output_collection.append(trgObject)

    setattr(event, self.cfg_ana.output_collection, output_collection)
  # End process