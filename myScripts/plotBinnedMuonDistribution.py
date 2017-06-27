''' Prepares muon distributions binned in the matched jet pt '''

from ROOT import TFile
from ROOT import TH1F
from ROOT import TTree
from ROOT import TCanvas
from ROOT import TLegend

#matchedMuonFile = TFile("muonMatching/MinBiasDistribution_100TeV_DelphesFCC_CMSJets.root")
matchedMuonFile = TFile("_testMuonMatch/HardQCD_PtBinned_10_30_GeV/histograms.root ")
matchedMuonTree = matchedMuonFile.Get("noRestrictionMuonJetTree")

muonPlotSettings = lambda: 0
muonPlotSettings.nBins = 100
muonPlotSettings.min = 0
muonPlotSettings.max = 100
muonPlotSettings.deltaRMax = 3

# Setting up jetPtBins and histograms
jetPtBins = [0, 30, 45, 60, 90, 150]
histograms = []

for x in xrange(0, len(jetPtBins) - 1):
  aHistogram = TH1F("muonPtDistribution" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]),
    "Muon p_{t} distribution binned in p^{jet}_{t}",
    muonPlotSettings.nBins,
    muonPlotSettings.min,
    muonPlotSettings.max
  )
  histograms.append(aHistogram)
  # Creating a consistent marker styling
  aHistogram.SetMarkerColor((x % 8) + 1) # colours from 1 (blk) to 8 (dark green)
  aHistogram.SetMarkerStyle(20 + x //8) # every 8 bins shift marker and go back to previous set of colors
  aHistogram.SetLineColor(1)
  aHistogram.SetStats(False)
  aHistogram.GetXaxis().SetRangeUser(0, 30)
  aHistogram.GetXaxis().SetTitle("p^{#mu}_{t}")
  aHistogram.GetXaxis().SetTitleOffset(1.10)
  aHistogram.GetYaxis().SetTitle("a.u.")


# Browsing tree

for iEv in xrange(0, matchedMuonTree.GetEntries()):
  
  if iEv % 1000 == 0: print "Processing event", iEv, "out of", matchedMuonTree.GetEntries()
  matchedMuonTree.GetEvent(iEv)
  
  if matchedMuonTree.dr < muonPlotSettings.deltaRMax:
    for x in xrange(0, len(jetPtBins) - 1):
      if (matchedMuonTree.matchedJet_pt > jetPtBins[x]) and (matchedMuonTree.matchedJet_pt < jetPtBins[x+1]):
        histograms[x].Fill(matchedMuonTree.matchedMuon_pt)

canvas = TCanvas()
canvas.SetLogy()
legend = TLegend(0.65,0.7,0.90,0.9)

# Normalising plots and plotting them
for x in xrange(0, len(histograms)):  
  histogram = histograms[x]
  if histogram.GetEntries() == 0: 
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  histogram.Scale(1/histogram.GetEntries())
  histogram.Draw("PE SAME")
  legend.AddEntry(histogram,
  str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]),
  "p")

legend.Draw()

canvas.Print("matchedMuonPtDistributionBinnedInJetPt.png", "png")