''' Prepares muon distributions binned in the matched jet pt '''

from ROOT import TFile
from ROOT import TH1F
from ROOT import TTree
from ROOT import TCanvas
from ROOT import TLegend

#convolutionFile = TFile("_muonTriggerRate_BarrelCut5.5_EndcapCut1.5_Iteration2/binnedDistributions.root")
convolutionFile = TFile(
    "_muonTriggerStudies_NewJetToMuon/_jetToMuonStudy/genJet_l1tMuon_convolutionCurves_JetToMuon/histograms.root")

'''List of every distribution to plot'''
distributionNames = [
  "objectPtDistributionBinnedInMatchedObject",
  #"objectMatchedObjectPtRatioDistributionBinnedInMatchedObject",
  #"matchedObjectEtaDistributionBinnedInMatchedObject",
  #"objectEtaDistributionBinnedInMatchedObject",
  "deltaRDistributionBinnedInMatchedObject",
  "deltaPtDistributionBinnedInMatchedObject",
  #"matchedObjectPtDistributionBinnedInMatchedObject"
]

'''Bins of binned distributions'''
#ptBins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
#ptBins = [3, 5, 10, 20, 30, 40]
#ptBins = [1.5, 2.3, 3, 4, 5, 5.5]
ptBins = [3, 3.5, 3.9, 5, 5.5, 6, 7, 8, 11, 15, 20]
#ptBins = [20, 25, 30, 35, 40, 45, 50, 60, 70]

# JET BINNING
#ptBins = [25, 50, 75, 100, 150, 200, 250, 300, 400, 500]
#ptBins = [10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 100]
#ptBins = [25, 30, 35, 40, 50, 60, 70, 80]
#ptBins = [1.5, 2.3, 3, 4]
#ptBins = [3, 4, 5, 7, 10, 15, 20, 25]

# MUON BINNING
#ptBins = [0, 1.5, 2.3, 3, 4, 5, 5.5, 6, 7, 8, 11, 15, 20, 30, 40, 50, 70, 100, 140, 200]

'''Contains the distributions'''
distributions = {}
'''Contains the canvases'''
canvases = {}
'''Contains the legends'''
legends = {}
'''Maximum value container, used to scale histograms'''
maximumYs = {}

saveFile = TFile("binnedDistributions.root", "RECREATE")
saveFile.cd()

#'''Ratio of ratio is computed considering the first bin as a reference, since it has an higher statistic'''
#muonJetAbsoluteSecondOrderPtRatioHistograms = []
#'''Ratio of ratio is computed considering the previous bin as a reference, it might show some interesting trend'''
#muonJetProgressiveSecondOrderPtRatioHistograms = []
#numberOfBottomQuarkHistograms = []

for name in distributionNames:
  # --- Preparing the data structure ---
  #Distribution histogram container
  distributions.update({
    name: []
  })
  #Canvas container
  canvas_tmp = TCanvas("canvas_" + name, "canvas_" + name)
  canvas_tmp.SetLogy(False)
  canvases.update({
    name: canvas_tmp
  })
  #Legend container
  legend_tmp = TLegend(0.65, 0.7, 0.90, 0.9)
  legends.update({
    name: legend_tmp
  })
  #Maximum value container
  maximumYs.update({
    name: float("-inf")
  })

  # --- Filling the structure


  for x in xrange(0, len(ptBins) - 1):
    aHistogram = convolutionFile.Get(name + "_" + str(ptBins[x]) + "_" + str(ptBins[x+1]))
    distributions[name].append(aHistogram)
    
    #aHistogram = aHistogram.Clone("bottomJetAbsoluteSecondOrderPtRatioDistributionBinnedInMatchedJet_" + str(ptBins[x]) + "_" + str(ptBins[x+1]))
    #muonJetAbsoluteSecondOrderPtRatioHistograms.append(aHistogram)
    #
    #aHistogram = aHistogram.Clone("bottomJetProgressiveSecondOrderPtRatioDistributionBinnedInMatchedJet_" + str(ptBins[x]) + "_" + str(ptBins[x+1]))
    #muonJetProgressiveSecondOrderPtRatioHistograms.append(aHistogram)

    # Normalising plots and plotting them
    canvas_tmp = canvases[name]
    canvas_tmp.cd()
    histogram = distributions[name][x]
    if histogram.GetEntries() == 0:
      print "Bin", str(ptBins[x]) + " < p_{t}^{jet} < " + str(ptBins[x+1]), "is empty"
      continue
    else:
      print "Bin", str(ptBins[x]) + " < p_{t}^{jet} < " + str(ptBins[x+1]), "contains", str(histogram.GetEntries()), "entries"
    histogram.Scale(1/histogram.GetEntries())
    histogram.GetYaxis().SetTitle("a.u.")
    maximumYs[name] = histogram.GetMaximum() if histogram.GetMaximum() > maximumYs[name] else maximumYs[name]
    histogram.Draw("HIST SAME")
    legends[name].AddEntry(histogram,
      str(ptBins[x]) + " < p_{t}^{gen muon} < " + str(ptBins[x+1]),
      "l"
    )
    histogram.Write()

for maxY in maximumYs.values():
  maxY *= 1.1

for name in distributionNames:
  distributions[name][0].GetYaxis().SetRangeUser(1e-6, maximumYs[name])
  canvases[name].cd()
  legends[name].Draw()
  canvases[name].Write()
  canvases[name].Update()

#canvasMuonJetAbsoluteSecondOrderPtRatio.cd()
#legendMuonJetAbsoluteSecondOrderPtRatio.Draw()
#canvasMuonJetAbsoluteSecondOrderPtRatio.Write()
#canvasMuonJetProgressiveSecondOrderPtRatio.cd()
#legendMuonJetProgressiveSecondOrderPtRatio.Draw()
#canvasMuonJetProgressiveSecondOrderPtRatio.Write()

#canvasNormalisedMuonPt.Print("matchedMuonNormalisedPtDistributionBinnedInJetPt.png", "png")
#canvasMuonPt.Print("matchedMuonPtDistributionBinnedInJetPt.png", "png")
#canvasJetPt.Print("matchedJetPtDistributionBinnedInJetPt.png", "png")
#canvasMuonJetPtRatio.Print("matchedMuonJetPtRatioDistributionBinnedInJetPt.png", "png")

saveFile.Close()
