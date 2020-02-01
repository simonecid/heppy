'''Compute the event variable M3'''

from heppy.framework.analyzer import Analyzer
from ROOT import TFile
from ROOT import TH1F
from ROOT import TTree
from ROOT import TCanvas
from ROOT import TLegend
import collections

class MatchedObjectBinnedDistributions(Analyzer):
  '''Considers a pair of matched objects and draws a specific quantity binned in another quantity of the matched object
  
  Example::

  I want the pt distribution of muon coming from hadron decays in jet.
  I first perform a match with the heppy.matcher, then I select the matched muons with a selector.
  I take the collecton in output from selector and I pass it to this analyser. 
  The analysed will take the pt of the muon and the pt of the jet and will make the binned distributions.

  def pt(ptc):
    return ptc.pt()
  
  muonJetConvolutionCurvesProducer = cfg.Analyzer(
    MatchedObjectBinnedDistributions,
    histo_name = 'muonPtDistributionBinnedInJetPt',
    histo_title = 'p_{t}^{#mu} distribution binned in p^{jet}_{t}',
    instance_label = 'muonJetConvolutionCurvesProducer',
    matched_collection = 'matched_muons',
    binning = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
    nbins = 1000
    min = 0,
    max = 1000,
    file_label = "myfile",
    plot_func = pt,
    self.cfg_ana.bin_func = pt,
    log_y = True,
    x_label = "p_{t}^{#mu} [GeV]",
    y_label = "\# events",
    normalise = True
  )

  * matched_collection: collection of muon matched to jets via the heppy matcher
  * binning: binning for jets
  * nbins: number of bins in the convolution function plot
  * min: minimum in the convolution function plot
  * max: maximum in the convolution function plot
  * file_label: name of a TFileService where the plots will be saved in
  * plot_func: what to plot
  * self.cfg_ana.bin_func: key in binning
  * log_y: log scale?
  * x_label (y): label for x (y) axis.
  * normalisation: normalisation to apply to the conv histograms, every bin will multiplied by this number
  '''

  def beginLoop(self, setup):
    super(MatchedObjectBinnedDistributions, self).beginLoop(setup)
    self.hasTFileService = hasattr(self.cfg_ana, "file_label")
    if self.hasTFileService:
      servname = '_'.join(['heppy.framework.services.tfile.TFileService',
                          self.cfg_ana.file_label
                      ])
      tfileservice = setup.services[servname]
      self.rootfile = tfileservice.file
    else:
      self.rootfile = TFile('/'.join([self.dirName,
                                      self.cfg_ana.histo_name + '.root']),
                            'recreate')
    
    self.binnedHistograms = []

    for x in xrange(0, len(self.cfg_ana.binning) - 1):
      aHistogram = TH1F(self.cfg_ana.histo_name + "_" + str(self.cfg_ana.binning[x]) + "_" + str(self.cfg_ana.binning[x+1]),
        self.cfg_ana.histo_title,
        self.cfg_ana.nbins,
        self.cfg_ana.min,
        self.cfg_ana.max
      )
      # Creating a consistent marker styling
      aHistogram.SetMarkerColor((x % 8) + 1) # colours from 1 (blk) to 8 (dark green)
      aHistogram.SetMarkerStyle(20 + x // 8) # every 8 bins shift marker and go back to previous set of colors
      aHistogram.SetLineColor((x % 8) + 1)
      aHistogram.SetLineStyle(1 + x // 8) # every 8 bins shift line and go back to previous set of colors
      aHistogram.SetStats(False)
      aHistogram.GetXaxis().SetTitle(self.cfg_ana.x_label)
      aHistogram.GetXaxis().SetTitleOffset(1.10)
      aHistogram.GetYaxis().SetTitle(self.cfg_ana.y_label)
      self.binnedHistograms.append(aHistogram)
    
  
  def process(self, event):
    
    matched_collection = getattr(event, self.cfg_ana.matched_collection)
    if isinstance(matched_collection, collections.Mapping):
      for key, val in matched_collection.iteritems():
        value = self.cfg_ana.plot_func(val)
        if value is not None:
          for x in xrange(0, len(self.cfg_ana.binning) - 1):
            bin_value = self.cfg_ana.bin_func(val.match)
            if (bin_value >= self.cfg_ana.binning[x]) and (bin_value < self.cfg_ana.binning[x+1]):
              self.binnedHistograms[x].Fill(value)
    else:
      for obj in matched_collection:
        value = self.cfg_ana.plot_func(obj)
        if value is not None:
          for x in xrange(0, len(self.cfg_ana.binning) - 1):
            bin_value = self.cfg_ana.bin_func(obj.match)
            if (bin_value >= self.cfg_ana.binning[x]) and (bin_value < self.cfg_ana.binning[x+1]):
              self.binnedHistograms[x].Fill(value)

  def write(self, setup):
    self.rootfile.cd()
#    canvas = TCanvas (self.cfg_ana.histo_name, self.cfg_ana.histo_title , 600, 600)
#    canvas.cd()
    for x in xrange(0, len(self.binnedHistograms)):
      histogram = self.binnedHistograms[x]
      if histogram.GetEntries() == 0:
        continue
#      histogram.Draw("AP")
#      histogram.Write()
      if getattr(self.cfg_ana, "normalise", False):
        histogram.Scale(1.0/histogram.GetEntries())
      
      if getattr(self.cfg_ana, "smooth", False):
        numberOfSmooth = 0
        for binidx in xrange(1, histogram.GetNbinsX()+1):
          if histogram.GetBinContent(binidx) > 0:
            numberOfSmooth += 1
        histogram.Smooth(numberOfSmooth)