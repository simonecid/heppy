'''Trasforms a jet into another object using a sort of MC algorithm.'''

from heppy.framework.analyzer import Analyzer
import collections
from numpy.random import RandomState
import pdb
from ROOT import TFile
from bisect import bisect_right
from heppy.particles.TriggerObject import TriggerObject

class Smearer  (Analyzer):
  '''Applies a numerical smearing to objects

  conv_factors = [
    0.029308043220380775,
    0.06426457403006641,
    0.14613328197089104,
    0.21841666245386987,
    0.25974951690955767,
    0.282851667305481,
    0.28482391739625457,
    0.27709889793617865,
    0.2656639099824761,
    0.24455606291222728,
    0.22786674964121972,
    0.21203451546770294,
    0.20330056813057987,
    0.19320973397442628,
    0.1857066950053135,
    0.1844090076500377
  ]
  
  Example:  

  from heppy.analyzers.triggerrates.Smearer import Smearer  
  jetToElectronTrasformer = cfg.Analyzer(
    Smearer ,
    input_collection = 'jets',
    output_collection = 'l1tEGamma',
    distribution_file = "convFile.root",
    smearing_distribution_prefix = "l1tObjectPtDistributionBinnedInGenJet",
    bins = [0, 10, 20, 30, 40, 50, 60],
    object_x_range = (0, 200)
  )
  
  * input_collection : input collection containing the jets
  * output_collection : output collection which the converted jet will be stored in, i.e. the type of object the jet will be converted to
  * convolution_file : file containing the jet-to-object convolution curves
  * convolution_histogram_prefix : prefix in the convolution file, it will be followed by _10_20, if 10 is the low bin and 20 is the high bin
  * bins : bins of the convolution file
  * object_x_range : range in which the momentum of the genrated object will be located, helps in generating new object faster if the TH1F is very big
  '''

  def beginLoop(self, setup):
    super(Smearer, self).beginLoop(setup)
    self.rng = RandomState()
    self.rng.seed()
    self.convolutionHistograms = []
    self.convolutionFile = TFile(self.cfg_ana.convolution_file)
    for x in xrange(0, len(self.cfg_ana.bins) - 1):
      self.convolutionHistograms.append(self.convolutionFile.Get(self.cfg_ana.convolution_histogram_prefix + "_" + str(self.cfg_ana.bins[x]) + "_" + str(self.cfg_ana.bins[x+1])))
  # End beginLoop

  def process(self, event):
    
    jets = getattr(event, self.cfg_ana.input_collection)
    output_collection = []

    # jetIdx = 0

    for jet in jets:
      jetPt = jet.pt()
      factorIndex = bisect_right(self.cfg_ana.bins, jetPt) - 1
      if factorIndex >= len(self.cfg_ana.bins) - 1:
        continue
      
      #Creating a new object with the same properties
      trgObject = TriggerObject(pt = jetPt, phi = jet.phi(), eta = jet.eta())
      # Getting the quantity to add in order to smear
      # I will use a hit-miss mc on the corresponding TH1F object
      convolutionHistogram = self.convolutionHistograms[factorIndex]

      convolutionHistogramMaximum = convolutionHistogram.GetMaximum()

      xRange = getattr(self.cfg_ana, "object_x_range", (convolutionHistogram.GetXaxis().GetXmin(), convolutionHistogram.GetXaxis().GetXmax()))
      yRange = (convolutionHistogram.GetMinimum(), convolutionHistogram.GetMaximum())

      isHit = False

      while not isHit:
      
        rndX = self.rng.uniform(xRange[0], xRange[1])
        rndY = self.rng.uniform(yRange[0], yRange[1])

        # Retrieving the prob of having that pt
        ptProb = convolutionHistogram.GetBinContent(convolutionHistogram.FindBin(rndX))
        # Hit?

        #print "Try ", rndX, rndY, "<", rndX, ptProb
        if rndY < ptProb:
          # Hit! Summing the smearing effect
          trgObject._pt += rndX
          isHit = True
      
      output_collection.append(trgObject)

    setattr(event, self.cfg_ana.output_collection, output_collection)
  # End process