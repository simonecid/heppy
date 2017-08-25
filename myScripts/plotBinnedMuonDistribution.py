''' Prepares muon distributions binned in the matched jet pt '''

from ROOT import TFile
from ROOT import TH1F
from ROOT import TTree
from ROOT import TCanvas
from ROOT import TLegend

convolutionFile = TFile("_convolutionCurvesJetBottom/convolutionCurvesJetBottom.root")

jetPtBins = [30, 60, 100, 200, 300, 450, 600, 750, 1000, 1500, 2000]
binnedMuonPtNormalisedDistributionHistograms = []
binnedDeltaRNormalisedDistributionHistograms = []
binnedMuonPtDistributionHistograms = []
binnedMuonEtaNormalisedDistributionHistograms = []
binnedJetPtDistributionHistograms = []
muonJetPtRatioHistograms = []
muonJetTotalPtRatioHistograms = []
'''Ratio of ratio is computed considering the first bin as a reference, since it has an higher statistic'''
muonJetAbsoluteSecondOrderPtRatioHistograms = []
'''Ratio of ratio is computed considering the previous bin as a reference, it might show some interesting trend'''
muonJetProgressiveSecondOrderPtRatioHistograms = []
numberOfBottomQuarkHistograms = []

# Preparing canvases

canvasNormalisedMuonPt = TCanvas("canvasNormalisedMuonPt", "canvasNormalisedMuonPt")
canvasNormalisedMuonPt.SetLogy(False)
canvasNormalisedDeltaR = TCanvas("canvasNormalisedDeltaR", "canvasNormalisedDeltaR")
canvasNormalisedDeltaR.SetLogy(False)
canvasMuonPt = TCanvas("canvasMuonPt", "canvasMuonPt")
canvasMuonPt.SetLogy(False)
canvasMuonEta = TCanvas("canvasMuonEta", "canvasMuonEta")
canvasMuonEta.SetLogy(False)
canvasJetPt = TCanvas("canvasJetPt", "canvasJetPt")
canvasJetPt.SetLogy(False)
canvasMuonJetPtRatio = TCanvas("canvasMuonJetPtRatio", "canvasMuonJetPtRatio")
canvasMuonJetPtRatio.SetLogy(False)
canvasMuonJetTotalPtRatio = TCanvas("canvasMuonJetTotalPtRatio", "canvasMuonJetTotalPtRatio")
canvasMuonJetTotalPtRatio.SetLogy(False)
canvasMuonJetAbsoluteSecondOrderPtRatio = TCanvas("canvasMuonJetAbsoluteSecondOrderPtRatio", "canvasMuonJetAbsoluteSecondOrderPtRatio")
canvasMuonJetAbsoluteSecondOrderPtRatio.SetLogy(False)
canvasMuonJetProgressiveSecondOrderPtRatio = TCanvas("canvasMuonJetProgressiveSecondOrderPtRatio", "canvasMuonJetProgressiveSecondOrderPtRatio")
canvasMuonJetProgressiveSecondOrderPtRatio.SetLogy(False)
canvasNumberOfBottomQuark = TCanvas("canvasNumberOfBottomQuark", "canvasNumberOfBottomQuark")
canvasNumberOfBottomQuark.SetLogy(False)
legendNormalisedMuonPt = TLegend(0.65, 0.7, 0.90, 0.9)
legendNormalisedDeltaR = TLegend(0.65, 0.7, 0.90, 0.9)
legendMuonPt = TLegend(0.65, 0.7, 0.90, 0.9)
legendMuonEta = TLegend(0.65, 0.7, 0.90, 0.9)
legendJetPt = TLegend(0.65, 0.7, 0.90, 0.9)
legendMuonJetPtRatio = TLegend(0.65, 0.7, 0.90, 0.9)
legendMuonJetTotalPtRatio = TLegend(0.65, 0.7, 0.90, 0.9)
legendMuonJetAbsoluteSecondOrderPtRatio = TLegend(0.65, 0.7, 0.90, 0.9)
legendMuonJetProgressiveSecondOrderPtRatio = TLegend(0.65, 0.7, 0.90, 0.9)
legendNumberOfBottomQuark = TLegend(0.65, 0.7, 0.90, 0.9)

saveFile = TFile("binnedMatchedMuonDistributions.root", "RECREATE")
saveFile.cd()

maximumY_muonJetPtRatioHistograms = float("-inf")
maximumY_muonJetTotalPtRatioHistograms = float("-inf")
maximumY_muonJetAbsoluteSecondOrderPtRatioHistograms = float("-inf")
maximumY_muonJetProgressiveSecondOrderPtRatioHistograms = float("-inf")
maximumY_muonNormalisedPtHistograms = float("-inf")
maximumY_muonNormalisedDeltaRHistograms = float("-inf")
maximumY_muonPtHistograms = float("-inf")
maximumY_muonEtaNormalisedHistograms = float("-inf")
maximumY_jetPtHistograms = float("-inf")
maximumY_numberOfBottomQuarks = float("-inf")

for x in xrange(0, len(jetPtBins) - 1):
  
  aHistogram = convolutionFile.Get("bottomPtDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  binnedMuonPtDistributionHistograms.append(aHistogram)

  aHistogram = aHistogram.Clone("bottomNormalisedPtDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  binnedMuonPtNormalisedDistributionHistograms.append(aHistogram)

  aHistogram = convolutionFile.Get("bottomEtaDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  binnedMuonEtaNormalisedDistributionHistograms.append(aHistogram)
  
  aHistogram = convolutionFile.Get("deltaRDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  binnedDeltaRNormalisedDistributionHistograms.append(aHistogram)

  aHistogram = convolutionFile.Get("jetPtDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  binnedJetPtDistributionHistograms.append(aHistogram)

  aHistogram = convolutionFile.Get("bottomJetPtRatioDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  muonJetPtRatioHistograms.append(aHistogram)
  
  aHistogram = convolutionFile.Get("totalBottomJetPtRatioDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  muonJetTotalPtRatioHistograms.append(aHistogram)
  
  aHistogram = aHistogram.Clone("bottomJetAbsoluteSecondOrderPtRatioDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  muonJetAbsoluteSecondOrderPtRatioHistograms.append(aHistogram)
  
  aHistogram = aHistogram.Clone("bottomJetProgressiveSecondOrderPtRatioDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  muonJetProgressiveSecondOrderPtRatioHistograms.append(aHistogram)
  
  aHistogram = convolutionFile.Get("numberOfBottomQuarksDistributionBinnedInMatchedJet_" + str(jetPtBins[x]) + "_" + str(jetPtBins[x+1]))
  numberOfBottomQuarkHistograms.append(aHistogram)

  # Normalising plots and plotting them
  canvasNormalisedMuonPt.cd()
  histogram = binnedMuonPtNormalisedDistributionHistograms[x]
  if histogram.GetEntries() == 0:
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  histogram.Scale(1/histogram.GetEntries())
  histogram.GetYaxis().SetTitle("a.u.")
  maximumY_muonNormalisedPtHistograms = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_muonNormalisedPtHistograms else maximumY_muonNormalisedPtHistograms
  histogram.Draw("HIST SAME")
  legendNormalisedMuonPt.AddEntry(histogram,
    str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]),
    "l"
  )
  histogram.Write()

  canvasNumberOfBottomQuark.cd()
  histogram = numberOfBottomQuarkHistograms[x]
  if histogram.GetEntries() == 0:
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  histogram.Scale(1/histogram.GetEntries())
  histogram.GetYaxis().SetTitle("a.u.")
  maximumY_numberOfBottomQuarks = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_numberOfBottomQuarks else maximumY_numberOfBottomQuarks
  histogram.Draw("HIST SAME")
  legendNumberOfBottomQuark.AddEntry(histogram,
    str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]),
    "l"
  )
  histogram.Write()

  canvasNormalisedDeltaR.cd()
  histogram = binnedDeltaRNormalisedDistributionHistograms[x]
  if histogram.GetEntries() == 0:
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  histogram.Scale(1/histogram.GetEntries())
  histogram.GetYaxis().SetTitle("a.u.")
  histogram.GetXaxis().SetTitle("#DeltaR")
  histogram.GetXaxis().SetRangeUser(0, 0.7)
  maximumY_muonNormalisedDeltaRHistograms = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_muonNormalisedDeltaRHistograms else maximumY_muonNormalisedDeltaRHistograms
  histogram.Draw("HIST SAME")
  legendNormalisedDeltaR.AddEntry(histogram,
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

  canvasMuonEta.cd()
  histogram = binnedMuonEtaNormalisedDistributionHistograms[x]
  if histogram.GetEntries() == 0:
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  histogram.Scale(1/histogram.GetEntries())
  histogram.GetYaxis().SetTitle("a.u.")
  maximumY_muonEtaNormalisedHistograms = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_muonEtaNormalisedHistograms else maximumY_muonEtaNormalisedHistograms
  histogram.Draw("HIST SAME")
  legendMuonEta.AddEntry(histogram,
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
  histogram.GetYaxis().SetTitle("a.u.")
  maximumY_muonJetPtRatioHistograms = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_muonJetPtRatioHistograms else maximumY_muonJetPtRatioHistograms
  histogram.Draw("HIST SAME")
  legendMuonJetPtRatio.AddEntry(histogram,
    str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]),
    "l"
  )
  histogram.Write()

  canvasMuonJetTotalPtRatio.cd()
  histogram = muonJetTotalPtRatioHistograms[x]
  if histogram.GetEntries() == 0:
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  histogram.Scale(1/histogram.GetEntries())
  histogram.GetYaxis().SetTitle("a.u.")
  maximumY_muonJetTotalPtRatioHistograms = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_muonJetTotalPtRatioHistograms else maximumY_muonJetTotalPtRatioHistograms
  histogram.Draw("HIST SAME")
  legendMuonJetTotalPtRatio.AddEntry(histogram,
    str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]),
    "l"
  )
  histogram.Write()

  canvasMuonJetAbsoluteSecondOrderPtRatio.cd()
  histogram = muonJetAbsoluteSecondOrderPtRatioHistograms[x]
  if histogram.GetEntries() == 0:
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  histogram.Scale(1/histogram.GetEntries())
  histogram.GetYaxis().SetTitle("a.u.")
  histogram.GetYaxis().SetRangeUser(0, 2)
  histogram.SetTitle("Bin-wise absolute ratio of ratios")
  histogram.Divide(muonJetPtRatioHistograms[0])
  maximumY_muonJetAbsoluteSecondOrderPtRatioHistograms = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_muonJetAbsoluteSecondOrderPtRatioHistograms else maximumY_muonJetAbsoluteSecondOrderPtRatioHistograms
  histogram.Draw("HIST SAME")
  legendMuonJetAbsoluteSecondOrderPtRatio.AddEntry(histogram,
    str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]),
    "l"
  )
  histogram.Write()

  canvasMuonJetProgressiveSecondOrderPtRatio.cd()
  histogram = muonJetProgressiveSecondOrderPtRatioHistograms[x]
  if histogram.GetEntries() == 0:
    print "Bin", str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]), "is empty"
    continue
  histogram.Scale(1/histogram.GetEntries())
  histogram.GetYaxis().SetTitle("a.u.")
  histogram.GetYaxis().SetRangeUser(0, 2)
  histogram.SetTitle("Bin-wise progressive ratio of ratios")
  if x > 0:
    histogram.Divide(muonJetPtRatioHistograms[x - 1])
  else:
    histogram.Divide(muonJetPtRatioHistograms[0])
  maximumY_muonJetProgressiveSecondOrderPtRatioHistograms = histogram.GetMaximum() if histogram.GetMaximum() > maximumY_muonJetProgressiveSecondOrderPtRatioHistograms else maximumY_muonJetProgressiveSecondOrderPtRatioHistograms
  histogram.Draw("HIST SAME")
  legendMuonJetProgressiveSecondOrderPtRatio.AddEntry(histogram,
    str(jetPtBins[x]) + " < p_{t}^{jet} < " + str(jetPtBins[x+1]),
    "l"
  )
  histogram.Write()

maximumY_muonJetPtRatioHistograms *= 1.1
maximumY_muonJetTotalPtRatioHistograms *= 1.1
maximumY_muonNormalisedPtHistograms *= 1.1
maximumY_muonNormalisedDeltaRHistograms *= 1.1
maximumY_muonPtHistograms *= 1.1
maximumY_muonEtaNormalisedHistograms *= 1.1
maximumY_jetPtHistograms *= 1.1
maximumY_muonJetAbsoluteSecondOrderPtRatioHistograms *= 1.1
maximumY_muonJetProgressiveSecondOrderPtRatioHistograms *= 1.1
maximumY_numberOfBottomQuarks *= 1.1
muonJetPtRatioHistograms[0].GetYaxis().SetRangeUser(1e-6, maximumY_muonJetPtRatioHistograms)
numberOfBottomQuarkHistograms[0].GetYaxis().SetRangeUser(1e-6, maximumY_numberOfBottomQuarks)
muonJetTotalPtRatioHistograms[0].GetYaxis().SetRangeUser(1e-6, maximumY_muonJetTotalPtRatioHistograms)
muonJetAbsoluteSecondOrderPtRatioHistograms[0].GetYaxis().SetRangeUser(1e-6, maximumY_muonJetAbsoluteSecondOrderPtRatioHistograms)
muonJetProgressiveSecondOrderPtRatioHistograms[0].GetYaxis().SetRangeUser(1e-6, maximumY_muonJetProgressiveSecondOrderPtRatioHistograms)
binnedMuonPtNormalisedDistributionHistograms[0].GetYaxis().SetRangeUser(1e-6, maximumY_muonNormalisedPtHistograms)
binnedDeltaRNormalisedDistributionHistograms[0].GetYaxis().SetRangeUser(1e-6, maximumY_muonNormalisedDeltaRHistograms)
binnedMuonPtDistributionHistograms[0].GetYaxis().SetRangeUser(0.1, maximumY_muonPtHistograms)
binnedMuonEtaNormalisedDistributionHistograms[0].GetYaxis().SetRangeUser(0.1, maximumY_muonEtaNormalisedHistograms)
binnedJetPtDistributionHistograms[0].GetYaxis().SetRangeUser(0.1, maximumY_jetPtHistograms)

canvasNormalisedMuonPt.cd()
legendNormalisedMuonPt.Draw()
canvasNormalisedMuonPt.Write()
canvasNumberOfBottomQuark.cd()
legendNumberOfBottomQuark.Draw()
canvasNumberOfBottomQuark.Write()
canvasNormalisedDeltaR.cd()
legendNormalisedDeltaR.Draw()
canvasNormalisedDeltaR.Write()
canvasMuonPt.cd()
legendMuonPt.Draw()
canvasMuonPt.Write()
canvasMuonEta.cd()
legendMuonEta.Draw()
canvasMuonEta.Write()
canvasJetPt.cd()
legendJetPt.Draw()
canvasJetPt.Write()
canvasMuonJetPtRatio.cd()
legendMuonJetPtRatio.Draw()
canvasMuonJetPtRatio.Write()
canvasMuonJetTotalPtRatio.cd()
legendMuonJetTotalPtRatio.Draw()
canvasMuonJetTotalPtRatio.Write()
canvasMuonJetAbsoluteSecondOrderPtRatio.cd()
legendMuonJetAbsoluteSecondOrderPtRatio.Draw()
canvasMuonJetAbsoluteSecondOrderPtRatio.Write()
canvasMuonJetProgressiveSecondOrderPtRatio.cd()
legendMuonJetProgressiveSecondOrderPtRatio.Draw()
canvasMuonJetProgressiveSecondOrderPtRatio.Write()

canvasNormalisedMuonPt.Update()
canvasNumberOfBottomQuark.Update()
canvasNormalisedDeltaR.Update()
canvasMuonPt.Update()
canvasMuonEta.Update()
canvasJetPt.Update()
canvasMuonJetPtRatio.Update()
canvasMuonJetTotalPtRatio.Update()

#canvasNormalisedMuonPt.Print("matchedMuonNormalisedPtDistributionBinnedInJetPt.png", "png")
#canvasMuonPt.Print("matchedMuonPtDistributionBinnedInJetPt.png", "png")
#canvasJetPt.Print("matchedJetPtDistributionBinnedInJetPt.png", "png")
#canvasMuonJetPtRatio.Print("matchedMuonJetPtRatioDistributionBinnedInJetPt.png", "png")

saveFile.Close()
