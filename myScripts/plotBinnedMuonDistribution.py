''' Prepares muon distributions binned in the matched jet pt '''

from ROOT import TFile
from ROOT import TH1F
from ROOT import TTree
from ROOT import TCanvas
from ROOT import TLegend

#matchedMuonFile = TFile("muonMatching/MinBiasDistribution_100TeV_DelphesFCC_CMSJets.root")
#matchedMuonFile = TFile("_muonMatching/muonMatching_HardQCD_PtBinned_700_900_GeV/HardQCD_PtBinned_700_900_GeV.root")
matchedMuonFile = TFile("_muonMatching/muonMatching_100TeV.root")
matchedMuonTree = matchedMuonFile.Get("muonJetTree")

muonPtPlotSettings = lambda: 0
muonPtPlotSettings.nBins = 800
muonPtPlotSettings.min = 0
muonPtPlotSettings.max = 800
muonPtPlotSettings.deltaRMax = 0.5

jetPtPlotSettings = lambda: 0
jetPtPlotSettings.nBins = 2500
jetPtPlotSettings.min = 0
jetPtPlotSettings.max = 2500

muonJetPtRatioPlotSettings = lambda: 0
muonJetPtRatioPlotSettings.nBins = 60
muonJetPtRatioPlotSettings.min = 0
muonJetPtRatioPlotSettings.max = 1.5
muonJetPtRatioPlotSettings.deltaRMax = muonPtPlotSettings.deltaRMax


# Setting up jetPtBins and histograms
jetPtBins = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000]
binnedMuonPtNormalisedDistributionHistograms = []
binnedMuonPtDistributionHistograms = []
binnedJetPtDistributionHistograms = []
muonJetPtRatioHistograms = []

for x in xrange(0, len(jetPtBins) - 1):
  aHistogram = TH1F("muonPtNormalisedDistribution" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]),
    "Muon p_{t} normalised distribution binned in p^{jet}_{t}",
    muonPtPlotSettings.nBins,
    muonPtPlotSettings.min,
    muonPtPlotSettings.max
  )
  # Creating a consistent marker styling
  aHistogram.SetMarkerColor((x % 8) + 1) # colours from 1 (blk) to 8 (dark green)
  aHistogram.SetMarkerStyle(20 + x //8) # every 8 bins shift marker and go back to previous set of colors
  aHistogram.SetLineColor((x % 8) + 1)
  aHistogram.SetStats(False)
  aHistogram.GetXaxis().SetTitle("p^{#mu}_{t}")
  aHistogram.GetXaxis().SetTitleOffset(1.10)
  aHistogram.GetYaxis().SetTitle("a.u.")
  binnedMuonPtNormalisedDistributionHistograms.append(aHistogram)
  
  aHistogram = TH1F("muonPtDistribution" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]),
    "Muon p_{t} distribution binned in p^{jet}_{t}",
    muonPtPlotSettings.nBins,
    muonPtPlotSettings.min,
    muonPtPlotSettings.max
  )
  # Creating a consistent marker styling
  aHistogram.SetMarkerColor((x % 8) + 1) # colours from 1 (blk) to 8 (dark green)
  aHistogram.SetMarkerStyle(20 + x //8) # every 8 bins shift marker and go back to previous set of colors
  aHistogram.SetLineColor((x % 8) + 1)
  aHistogram.SetStats(False)
  aHistogram.GetXaxis().SetTitle("p^{#mu}_{t}")
  aHistogram.GetXaxis().SetTitleOffset(1.10)
  aHistogram.GetYaxis().SetTitle("# of events")
  binnedMuonPtDistributionHistograms.append(aHistogram)

  aHistogram = TH1F("jetPtDistribution" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]),
    "Jet p_{t} distribution binned in p^{jet}_{t}",
    jetPtPlotSettings.nBins,
    jetPtPlotSettings.min,
    jetPtPlotSettings.max
  )
  # Creating a consistent marker styling
  aHistogram.SetMarkerColor((x % 8) + 1) # colours from 1 (blk) to 8 (dark green)
  aHistogram.SetMarkerStyle(20 + x //8) # every 8 bins shift marker and go back to previous set of colors
  aHistogram.SetLineColor((x % 8) + 1)
  aHistogram.SetStats(False)
  aHistogram.GetXaxis().SetTitle("p^{jet}_{t}")
  aHistogram.GetXaxis().SetTitleOffset(1.10)
  aHistogram.GetYaxis().SetTitle("# of events")
  binnedJetPtDistributionHistograms.append(aHistogram)

  aHistogram = TH1F("muonJetPtRatioNormalisedDistribution" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]),
    "p_{t}^{#mu}/p_{t}^{jet} distribution binned in p^{jet}_{t}",
    muonJetPtRatioPlotSettings.nBins,
    muonJetPtRatioPlotSettings.min,
    muonJetPtRatioPlotSettings.max
  )
  # Creating a consistent marker styling
  aHistogram.SetMarkerColor((x % 8) + 1) # colours from 1 (blk) to 8 (dark green)
  aHistogram.SetMarkerStyle(20 + x //8) # every 8 bins shift marker and go back to previous set of colors
  aHistogram.SetLineColor((x % 8) + 1)
  aHistogram.SetStats(False)
  aHistogram.GetXaxis().SetTitle("#frac{p_{t}^{#mu}}{p_{t}^{jet}}")
  aHistogram.GetXaxis().SetTitleOffset(1.10)
  aHistogram.GetYaxis().SetTitle("a.u.")
  muonJetPtRatioHistograms.append(aHistogram)

# Browsing tree

for iEv in xrange(0, matchedMuonTree.GetEntries()):
  
  if iEv % 10000 == 0: 
    print "Processing event", iEv, "out of", matchedMuonTree.GetEntries(), "-", float(iEv)/float(matchedMuonTree.GetEntries()), "%"
  
  matchedMuonTree.GetEvent(iEv)
  
  if matchedMuonTree.dr < muonPtPlotSettings.deltaRMax:
    for x in xrange(0, len(jetPtBins) - 1):
      if (matchedMuonTree.matchedJet_pt > jetPtBins[x]) and (matchedMuonTree.matchedJet_pt < jetPtBins[x+1]):
        binnedMuonPtNormalisedDistributionHistograms[x].Fill(matchedMuonTree.matchedMuon_pt)
        binnedMuonPtDistributionHistograms[x].Fill(matchedMuonTree.matchedMuon_pt)
        binnedJetPtDistributionHistograms[x].Fill(matchedMuonTree.matchedJet_pt)

  if matchedMuonTree.dr < muonJetPtRatioPlotSettings.deltaRMax:
    for x in xrange(0, len(jetPtBins) - 1):
      if (matchedMuonTree.matchedJet_pt > jetPtBins[x]) and (matchedMuonTree.matchedJet_pt < jetPtBins[x+1]):
        muonJetPtRatioHistograms[x].Fill(matchedMuonTree.matchedMuon_pt/matchedMuonTree.matchedJet_pt)

canvasNormalisedMuonPt = TCanvas()
canvasNormalisedMuonPt.SetLogy()
canvasMuonPt = TCanvas()
canvasMuonPt.SetLogy()
canvasJetPt = TCanvas()
canvasJetPt.SetLogy()
canvasMuonJetPtRatio = TCanvas()
#canvasMuonJetPtRatio.SetLogy()
legendNormalisedMuonPt = TLegend(0.65, 0.7, 0.90, 0.9)
legendMuonPt = TLegend(0.65, 0.7, 0.90, 0.9)
legendJetPt = TLegend(0.65, 0.7, 0.90, 0.9)
legendMuonJetPtRatio = TLegend(0.65, 0.7, 0.90, 0.9)

saveFile = TFile("binnedMatchedMuonDistributions.root", "RECREATE")
saveFile.cd()

maximumY_muonJetPtRatioHistograms = float("-inf")
maximumY_muonNormalisedPtHistograms = float("-inf")
maximumY_muonPtHistograms = float("-inf")
maximumY_jetPtHistograms = float("-inf")

# Normalising plots and plotting them
for x in xrange(0, len(binnedMuonPtNormalisedDistributionHistograms)):  
  canvasNormalisedMuonPt.cd()
  histogram = binnedMuonPtNormalisedDistributionHistograms[x]
  if histogram.GetEntries() == 0:
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  histogram.Scale(1/histogram.GetEntries())
  maximumY_muonNormalisedPtHistograms = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_muonNormalisedPtHistograms else maximumY_muonNormalisedPtHistograms
  histogram.Draw("HIST SAME")
  legendNormalisedMuonPt.AddEntry(histogram,
    str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]),
    "p"
  )
  histogram.Write()
  
  canvasMuonPt.cd()
  histogram = binnedMuonPtDistributionHistograms[x]
  if histogram.GetEntries() == 0:
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  maximumY_muonPtHistograms = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_muonPtHistograms else maximumY_muonPtHistograms
  histogram.Draw("HIST SAME")
  legendMuonPt.AddEntry(histogram,
    str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]),
    "p"
  )
  histogram.Write()

  canvasJetPt.cd()
  histogram = binnedJetPtDistributionHistograms[x]
  if histogram.GetEntries() == 0:
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  maximumY_jetPtHistograms = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_jetPtHistograms else maximumY_jetPtHistograms
  histogram.Draw("HIST SAME")
  legendJetPt.AddEntry(histogram,
    str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]),
    "p"
  )
  histogram.Write()

  canvasMuonJetPtRatio.cd()
  histogram = muonJetPtRatioHistograms[x]
  if histogram.GetEntries() == 0:
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  histogram.Scale(1/histogram.GetEntries())
  maximumY_muonJetPtRatioHistograms = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_muonJetPtRatioHistograms else maximumY_muonJetPtRatioHistograms
  histogram.Draw("HIST SAME")
  legendMuonJetPtRatio.AddEntry(histogram,
    str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]),
    "p"
  )
  histogram.Write()

maximumY_muonJetPtRatioHistograms *= 1.1
maximumY_muonNormalisedPtHistograms *= 1.1
maximumY_muonPtHistograms *= 1.1
maximumY_jetPtHistograms *= 1.1
muonJetPtRatioHistograms[0].GetYaxis().SetRangeUser(1e-6, maximumY_muonJetPtRatioHistograms)
binnedMuonPtNormalisedDistributionHistograms[0].GetYaxis().SetRangeUser(1e-6, maximumY_muonNormalisedPtHistograms)
binnedMuonPtDistributionHistograms[0].GetYaxis().SetRangeUser(0.1, maximumY_muonPtHistograms)
binnedJetPtDistributionHistograms[0].GetYaxis().SetRangeUser(0.1, maximumY_jetPtHistograms)

canvasNormalisedMuonPt.cd()
legendNormalisedMuonPt.Draw()
canvasMuonPt.cd()
legendMuonPt.Draw()
canvasJetPt.cd()
legendJetPt.Draw()
canvasMuonJetPtRatio.cd()
legendMuonJetPtRatio.Draw()

canvasNormalisedMuonPt.Print("matchedMuonNormalisedPtDistributionBinnedInJetPt.png", "png")
canvasMuonPt.Print("matchedMuonPtDistributionBinnedInJetPt.png", "png")
canvasJetPt.Print("matchedJetPtDistributionBinnedInJetPt.png", "png")
canvasMuonJetPtRatio.Print("matchedMuonJetPtRatioDistributionBinnedInJetPt.png", "png")

saveFile.Close()
