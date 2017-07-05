''' Prepares muon distributions binned in the matched jet pt '''

from ROOT import TFile
from ROOT import TH1F
from ROOT import TTree
from ROOT import TCanvas
from ROOT import TLegend

#matchedMuonFile = TFile("muonMatching/MinBiasDistribution_100TeV_DelphesFCC_CMSJets.root")
#matchedMuonFile = TFile("_muonMatching/muonMatching_HardQCD_PtBinned_700_900_GeV/HardQCD_PtBinned_700_900_GeV.root")
#convolutionFile = TFile("_testMuonMatch/histo.root")
convolutionFile = TFile("convolutionCurves_all/convolutionCurves.root")

jetPtBins = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000]
#jetPtBins = [30, 60, 100, 200]
binnedMuonPtNormalisedDistributionHistograms = []
binnedMuonPtDistributionHistograms = []
binnedJetPtDistributionHistograms = []
muonJetPtRatioHistograms = []

canvasNormalisedMuonPt = TCanvas()
canvasNormalisedMuonPt.SetLogy(False)
canvasMuonPt = TCanvas()
canvasMuonPt.SetLogy(False)
canvasJetPt = TCanvas()
canvasJetPt.SetLogy(False)
canvasMuonJetPtRatio = TCanvas()
#canvasMuonJetPtRatio.SetLogy(False)
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

for x in xrange(0, len(jetPtBins) - 1):
  
  aHistogram = convolutionFile.Get("muonPtDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  binnedMuonPtDistributionHistograms.append(aHistogram)

  aHistogram = aHistogram.Clone("muonNormalisedPtDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  binnedMuonPtNormalisedDistributionHistograms.append(aHistogram)

  aHistogram = convolutionFile.Get("jetPtDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  binnedJetPtDistributionHistograms.append(aHistogram)

  aHistogram = convolutionFile.Get("muonJetPtRatioDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  muonJetPtRatioHistograms.append(aHistogram)

  # Normalising plots and plotting them
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
    "l"
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
    "l"
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
    "l"
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
    "l"
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
canvasNormalisedMuonPt.Write()
canvasMuonPt.cd()
legendMuonPt.Draw()
canvasMuonPt.Write()
canvasJetPt.cd()
legendJetPt.Draw()
canvasJetPt.Write()
canvasMuonJetPtRatio.cd()
legendMuonJetPtRatio.Draw()
canvasMuonJetPtRatio.Write()

canvasNormalisedMuonPt.Update()
canvasMuonPt.Update()
canvasJetPt.Update()
canvasMuonJetPtRatio.Update()

#canvasNormalisedMuonPt.Print("matchedMuonNormalisedPtDistributionBinnedInJetPt.png", "png")
#canvasMuonPt.Print("matchedMuonPtDistributionBinnedInJetPt.png", "png")
#canvasJetPt.Print("matchedJetPtDistributionBinnedInJetPt.png", "png")
#canvasMuonJetPtRatio.Print("matchedMuonJetPtRatioDistributionBinnedInJetPt.png", "png")

saveFile.Close()
