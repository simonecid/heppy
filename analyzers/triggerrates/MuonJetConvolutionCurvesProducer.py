'''Compute the event variable M3'''

from heppy.framework.analyzer import Analyzer
from ROOT import TFile
from ROOT import TH1F
from ROOT import TTree
from ROOT import TCanvas
from ROOT import TLegend
import collections

class MuonJetConvolutionCurvesProducer(Analyzer):
  '''Computes convolution curves for mun coming from hadron decays in jets
  
  Example::

  def pt(ptc):
    return ptc.pt()
  
  muonJetConvolutionCurvesProducer = cfg.Analyzer(
    MuonJetConvolutionCurvesProducer,
    histo_name = 'muonPtDistributionBinnedInJetPt',
    histo_title = 'p_{t}^{#mu} distribution binned in p^{jet}_{t}',
    instance_label = 'muonJetConvolutionCurvesProducer',
    matched_muons = 'matched_muons',
    jet_bins = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000],
    nbins = 1000
    min = 0,
    max = 1000,
    file_label = "myfile",
    value_func = pt,
    log_y = True,
    x_label = "p_{t}^{#mu} [GeV]",
    y_label = "\# events"
  )

  * matched_muons: collection of muon matched to jets via the heppy matcher
  * jet_bins: binning for jets
  * nbins: number of bins in the convolution function plot
  * min: minimum in the convolution function plot
  * max: maximum in the convolution function plot
  * file_label: name of a TFileService where the plots will be saved in
  * value_func: what to plot
  * log_y: log scale?
  * x_label (y): label for x (y) axis.
  '''

  def beginLoop(self, setup):
    super(MuonJetConvolutionCurvesProducer, self).beginLoop(setup)
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

    for x in xrange(0, len(self.cfg_ana.jet_bins) - 1):
      aHistogram = TH1F(self.cfg_ana.histo_name + "_" + str(self.cfg_ana.jet_bins[x]) + "_" + str(self.cfg_ana.jet_bins[x+1]),
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
      aHistogram.GetXaxis().SetTitle("p^{#mu}_{t}")
      aHistogram.GetXaxis().SetTitleOffset(1.10)
      aHistogram.GetYaxis().SetTitle("a.u.")
      self.binnedHistograms.append(aHistogram)
    
  
  def process(self, event):
    
    matched_muons = getattr(event, self.cfg_ana.matched_muons)
    if isinstance(matched_muons, collections.Mapping):
      for key, val in matched_muons.iteritems():
        value = self.cfg_ana.value_func(val)
        if value is not None:
          for x in xrange(0, len(self.cfg_ana.jet_bins) - 1):
            matchedJet_pt = val.match.pt()
            if (matchedJet_pt > self.cfg_ana.jet_bins[x]) and (matchedJet_pt < self.cfg_ana.jet_bins[x+1]):
              self.binnedHistograms[x].Fill(value)
    else:
      for obj in matched_muons:
        value = self.cfg_ana.value_func(obj)
        if value is not None:
          for x in xrange(0, len(self.cfg_ana.jet_bins) - 1):
            matchedJet_pt = obj.match.pt()
            if (matchedJet_pt > self.cfg_ana.jet_bins[x]) and (matchedJet_pt < self.cfg_ana.jet_bins[x+1]):
              self.binnedHistograms[x].Fill(value)

  def write(self, setup):
    self.rootfile.cd()
    canvas = TCanvas (self.cfg_ana.histo_name, self.cfg_ana.histo_title , 600, 600)
    canvas.cd()
    for x in xrange(0, len(self.binnedHistograms)):
      histogram = self.binnedHistograms[x]
      if histogram.GetEntries() == 0:
        continue
      histogram.Draw("AP")
      histogram.Write()
