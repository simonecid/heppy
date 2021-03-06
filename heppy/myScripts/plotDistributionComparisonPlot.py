''' Creates a comparison plot with ratio '''

from ROOT import TFile
from ROOT import TH1F
from ROOT import TTree
from ROOT import TPaveText
from ROOT import TCanvas
from ROOT import TPad
from ROOT import TGraphErrors
from ROOT import TMultiGraph
from ROOT import TLegend
from ROOT import TGaxis
from ROOT import TLine
from ROOT import gPad
from math import sqrt

chiSquaredWarningThreshold = 1

'''List of files containing the plots to compare'''

'''List of files containing the plots to compare'''



# From here on it works by magic, and I am the magician :P

def plotDistributionComparisonPlot(cfg):

  multiGraph = TMultiGraph()
  multiGraph.SetName("triggerRateMultiGraph")

  tfiles = [
  ]

  histograms = [
  ]

  canvas = TCanvas("canvas", "canvas", 800, 800)
  '''Contains the legend'''
  legend = TLegend(0.3, 0.7, 0.90, 0.9)
  '''Maximum value container, used to scale histograms'''
  maximumY = float("-inf")

  pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
  pad1.SetBottomMargin(0.05) # Upper and lower plot are joined
  #pad1.SetBottomMargin(0) # Upper and lower plot are joined
  pad1.SetGridx()         # Vertical grid
  pad1.Draw()             # Draw the upper pad: pad1
  pad1.cd()               # pad1 becomes the current pad

  for histogramFileNameAndTitle in cfg.plots:
    tfile = TFile(histogramFileNameAndTitle[0])
    tfiles.append(tfile)
    histogram = tfile.Get(histogramFileNameAndTitle[1])
    histograms.append(histogram)
    if histogram.ClassName() == "TH1F":
      histogram.SetStats(0)          # No statistics on upper plot
    maximumY = histogram.GetMaximum() if histogram.GetMaximum() > maximumY else maximumY
    legend.AddEntry(histogram, histogramFileNameAndTitle[2], "l")

  # histograms[0] settings
  histograms[0].SetMarkerColor(4)
  histograms[0].SetLineColor(4)
  histograms[0].SetLineWidth(1)

  # Y axis histograms[0] plot settings
  histograms[0].GetYaxis().SetTitleSize(20)
  histograms[0].GetYaxis().SetTitleFont(43)
  histograms[0].GetYaxis().SetTitleOffset(1.55)


  #histograms[0].Scale(1./histograms[0].GetEntries())
  if histograms[0].ClassName() == "TH1F":
    histograms[0].Draw("SAME HIST")         # Draw histograms[1] on top of histograms[0]
  else:
    histograms[0].Draw("SAME APE")         # Draw histograms[1] on top of histograms[0]
    #multiGraph.Add(histograms[0])


  if getattr(cfg, "xRange", None) is not None:
    histograms[0].GetXaxis().SetRangeUser(cfg.xRange[0], cfg.xRange[1])
    gPad.RedrawAxis()

  if getattr(cfg, "xAxisLabel", None) is not None:
    histograms[0].GetXaxis().SetTitle(cfg.xAxisLabel)
    gPad.RedrawAxis()
  
  if getattr(cfg, "yAxisLabel", None) is not None:
    histograms[0].GetYaxis().SetTitle(cfg.yAxisLabel)
    gPad.RedrawAxis()
    
  if getattr(cfg, "yRange", None) is not None:
    histograms[0].GetYaxis().SetRangeUser(cfg.yRange[0], cfg.yRange[1])
    gPad.RedrawAxis()
  else:
    maximumY *= 1.1
    histograms[0].GetYaxis().SetRangeUser(1e-6, maximumY)
    
  if getattr(cfg, "logY", False):
    canvas.SetLogy()

  # histograms[1] settings
  histograms[1].SetMarkerColor(2)
  histograms[1].SetLineColor(2)
  histograms[1].SetLineWidth(1)
  #histograms[1].Scale(1./histograms[1].GetEntries())
  if histograms[1].ClassName() == "TH1F":
    histograms[1].Draw("SAME HIST")         # Draw histograms[1] on top of histograms[0]
  else:
    histograms[1].Draw("SAME PE")         # Draw histograms[1] on top of histograms[0]
    #multiGraph.Add(histograms[1])

  #if multiGraph.GetListOfGraphs() != None:
  #  multiGraph.Draw("SAME PE")

  # Do not draw the Y axis label on the upper plot and redraw a small
  # axis instead, in order to avoid the first label (0) to be clipped.
  #histograms[0].GetYaxis().SetLabelSize(0.)
  #axis = TGaxis( 0, 20, 0, maximumY, 20, maximumY, 510,"")
  #axis.SetLabelFont(43) # Absolute font size in pixel (precision 3)
  #axis.SetLabelSize(15)
  #axis.Draw()

  # Adding a small text with the chi-squared

  chiSquared = 0
  if (histograms[0].ClassName() == "TGraph") or (histograms[0].ClassName() == "TGraphErrors"):
    numberOfBins = histograms[0].GetN()
    numberOfDegreesOfFreedom = numberOfBins
  else:
    numberOfBins = histograms[0].GetNbinsX()
    numberOfDegreesOfFreedom = numberOfBins


  for x in xrange(1, numberOfBins+1): # numberOfBins contains last bin, numberOfBins+1 contains the overflow (latter excluded), underflow also excluded
    if (histograms[0].ClassName() == "TGraph") or (histograms[0].ClassName() == "TGraphErrors"):
      binContent0 = histograms[0].GetY()[x-1]
    else:
      binContent0 = histograms[0].GetBinContent(x)
    if (histograms[1].ClassName() == "TGraph") or (histograms[1].ClassName() == "TGraphErrors"):
      binContent1 = histograms[1].GetY()[x-1]
    else:
      binContent1 = histograms[1].GetBinContent(x)
    bin0ErrorSquared = binContent0
    bin1ErrorSquared = binContent1
    #bin1ErrorSquared = 0
    if (binContent0 == 0) and (binContent1 == 0):
      numberOfDegreesOfFreedom -= 1 #No data means one less degree of freedom
    else:
      binDifferenceSquared = (binContent0 - binContent1)**2
      chiSquaredTerm = binDifferenceSquared/(bin0ErrorSquared + bin1ErrorSquared)
      chiSquared += chiSquaredTerm
      if chiSquaredTerm > chiSquaredWarningThreshold:
        if (histograms[0].ClassName() == "TGraph") or (histograms[0].ClassName() == "TGraphErrors"):
          print "Bin", x, "-", histograms[0].GetX()[x-1], "has a CS=", chiSquaredTerm
        else:
          print "Bin", x, "-", histograms[0].GetBinCenter(x), "has a CS=", chiSquaredTerm

  chiSquareLabel = TPaveText(0.7, 0.6, 0.9, 0.4)
  chiSquareLabel.AddText("#chi^{2}/ndf = " + str(chiSquared) + "/" + str(numberOfDegreesOfFreedom) + " = " + str(chiSquared/numberOfDegreesOfFreedom))
  chiSquareLabel.Draw()
  print "FINAL CS IS", format(chiSquared, ".2f") + "/" + str(numberOfDegreesOfFreedom) + " = " + format(chiSquared/numberOfDegreesOfFreedom, ".2f")
  legend.SetHeader("#chi^{2}/ndf = " + format(chiSquared, ".2f") + "/" + str(numberOfDegreesOfFreedom) + " = " + format(chiSquared/numberOfDegreesOfFreedom, ".2f"), "C")
  legend.Draw()
  # lower plot will be in pad
  canvas.cd() # Go back to the main canvas before defining pad2
  pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
  pad2.SetTopMargin(0)
  pad2.SetBottomMargin(0.2)
  pad2.SetGridx() # vertical grid
  pad2.Draw()
  pad2.cd() # pad2 becomes the current pad
  pad2.SetGridy()


  # Define the ratio plot
  ratioPlot = TGraphErrors(histograms[0])
  ratioPlot.SetName("ratioPlot")
  graph_histo0 = TGraphErrors(histograms[0])
  graph_histo1 = TGraphErrors(histograms[1])
  ratioPlot.SetLineColor(1)
  ratioPlot.SetMinimum(0.6)  # Define Y ..
  ratioPlot.SetMaximum(1.5) # .. range
  #ratioPlot.Sumw2()
  #ratioPlot.SetStats(0)      # No statistics on lower plot

  #Dividing point by point

  for index in xrange(0, ratioPlot.GetN()):
    if graph_histo1.GetY()[index] == 0:
      ratioPlot.GetY()[index] = 0
      ratioPlot.GetEY()[index] = 0
    else:
      ratioPlot.GetY()[index] /= graph_histo1.GetY()[index]
      ratioPlot.GetEY()[index] = sqrt(((graph_histo1.GetY()[index])**2 * (graph_histo0.GetEY()[index])**2 + (graph_histo0.GetY()[index])**2 * (graph_histo1.GetEY()[index])**2)/(graph_histo1.GetY()[index])**4)
  
  ratioPlot.SetMarkerStyle(21)

  if getattr(cfg, "xRange", None) is not None:
    ratioPlot.GetXaxis().SetRangeUser(cfg.xRange[0], cfg.xRange[1])
    gPad.RedrawAxis()

  if getattr(cfg, "yRangeRatio", None) is not None:
    ratioPlot.GetYaxis().SetRangeUser(cfg.yRangeRatio[0], cfg.yRangeRatio[1])
    gPad.RedrawAxis()

  ratioPlot.Draw("APE")       # Draw the ratio plot

  line0 = TLine(ratioPlot.GetXaxis().GetXmin(), 1, ratioPlot.GetXaxis().GetXmax(), 1)
  line0.SetLineColor(2)
  line0.SetLineWidth(2)
  line0.SetLineStyle(2)
  line0.Draw()

  # Ratio plot (ratioPlot) settings
  ratioPlot.SetTitle("") # Remove the ratio title

  # Y axis ratio plot settings
  ratioPlot.GetYaxis().SetTitle("Ratio #frac{blue}{red}")
  ratioPlot.GetYaxis().SetNdivisions(505)
  ratioPlot.GetYaxis().SetTitleSize(20)
  ratioPlot.GetYaxis().SetTitleFont(43)
  ratioPlot.GetYaxis().SetTitleOffset(1.55)
  ratioPlot.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  ratioPlot.GetYaxis().SetLabelSize(15)

  # X axis ratio plot settings
  ratioPlot.GetXaxis().SetTitleSize(20)
  ratioPlot.GetXaxis().SetTitleFont(43)
  ratioPlot.GetXaxis().SetTitleOffset(4.)
  ratioPlot.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
  ratioPlot.GetXaxis().SetLabelSize(15)

  
  xRangeBinning = getattr(cfg, "simplifiedRatioPlotXRangeBinning", None)
  if xRangeBinning is not None:
    simplifiedRatioPlot = TGraphErrors(len(xRangeBinning) - 1)
    simplifiedRatioPlot.SetName("simplifiedRatioPlot")
    ratioPlotIndex = 0
    
    for idx in xrange(0, simplifiedRatioPlot.GetN()):
      yAverage = 0.
      yMax = float("-inf")
      yMin = float("+inf")

      nPoints = 0.
      simplifiedRatioPlot.GetX()[idx] = (xRangeBinning[idx] + xRangeBinning[idx + 1])/2.
      simplifiedRatioPlot.GetEX()[idx] = (xRangeBinning[idx + 1] - xRangeBinning[idx])/2.
      
      while (ratioPlot.GetX()[ratioPlotIndex] < xRangeBinning[idx]):
        ratioPlotIndex += 1
      while ((ratioPlotIndex < ratioPlot.GetN()) and (ratioPlot.GetX()[ratioPlotIndex] < xRangeBinning[idx + 1]) and (ratioPlot.GetX()[ratioPlotIndex] >= xRangeBinning[idx])):
        yAverage += ratioPlot.GetY()[ratioPlotIndex]
        if (yMax < ratioPlot.GetY()[ratioPlotIndex] + ratioPlot.GetEY()[ratioPlotIndex]):
          yMax = ratioPlot.GetY()[ratioPlotIndex] + ratioPlot.GetEY()[ratioPlotIndex]
        if (yMin > ratioPlot.GetY()[ratioPlotIndex] - ratioPlot.GetEY()[ratioPlotIndex]):
          yMin = ratioPlot.GetY()[ratioPlotIndex] - ratioPlot.GetEY()[ratioPlotIndex]
        nPoints += 1.
        ratioPlotIndex += 1
      
      simplifiedRatioPlot.GetY()[idx] = yAverage/nPoints
      simplifiedRatioPlot.GetEY()[idx] = (yMax - yMin)/2.

  saveFile = TFile(cfg.saveFileName, "RECREATE")
  saveFile.cd()
  canvas.Write()
  histograms[0].Write()
  histograms[1].Write()
  if multiGraph.GetListOfGraphs() != None:
    multiGraph.Write()
  ratioPlot.Write()
  if xRangeBinning is not None:
    simplifiedRatioPlot.Write()
  saveFile.Close()
  for tfile in tfiles:
    tfile.Close()


if __name__ == "__main__":

  cfg = lambda x: 1
  cfg.plots = [
    #Files here
    # ["MinBiasDistribution_13TeV_DelphesCMS_CMSJets_GenJetPTDistribution/genJetPtDistribution_Normalised.root", "ptSimL1TMuonDistribution", "MinBias"],
    #["_closureTest/l1tMuonGenMuonMatching_SingleMu_FlatPt_8to100_QualityCut_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtSimL1TMuonDistribution", "SimL1TMuon"],
    ["_MinBias_CMSSWTune/distributions_fromcmssw.root",
     "genJetPtDistribution_CMSSW", "CMSSW"],
    ["_MinBias_CMSSWTune/distributions_fromdelphes.root",
     "genJetPtDistribution_Delphes", "DELPHES"],
    #["_closureTest/l1tMuonGenMuonMatching_SingleMu_FlatPt_8to100_QualityCut_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtL1TMuonDistribution", "Original L1TMuon"],
  ]
  cfg.saveFileName = "comparisonResult.root"
  cfg.draw = True
  #cfg.xRange = (0, 50)
  cfg.xRange = (0, 500)
  cfg.xAxisLabel = "p_{t} [GeV]"
  cfg.yAxisLabel = "# events"
  cfg.yRange = (2e-1, 1e6)
  cfg.yRangeRatio = (0, 2)
  cfg.logY = True
  

  plotDistributionComparisonPlot(cfg)

# Old conf. kept because handy for copypasting
# filesAndDistributionNames = {
#  #Files here
#  #"_muonTriggerRates/cmsMatching_SingleNeutrinoPU140_L1TMuon/ratePlots.root": "triggerRate",
#  #"_muonTriggerRates/NeutrinoGun_MuonTriggerRate_Binning_Set_3_PtCut_1.5GeV/ratePlot_Normalised.root": "muonTriggerRate",
#  #"_muonTriggerRates/NeutrinoGun_MuonTriggerRate_Binning_Set_1/NeutrinoGunPU140_MuonTriggerRate_Normalised.root": "muonTriggerRate",
#  #"_muonTriggerRates/NeutrinoGun_MuonTriggerRate_Binning_Set_2/NeutrinoGunPU140_MuonTriggerRate_Normalised.root": "muonTriggerRate",
#  #"_muonTriggerRates/NeutrinoGun_MuonTriggerRate_Binning_Set_3/NeutrinoGunPU140_MuonTriggerRate_Normalised.root": "muonTriggerRate",
#  #"_muonTriggerRates/NeutrinoGun_MuonTriggerRate_Binning_Wrong_Set/NeutrinoGunPU140_MuonTriggerRate_Normalised.root": "muonTriggerRate",
#  #"_closureTest/GenMuonDistribution/histograms.root": "ptGenMuonDistribution",
#  #"_closureTest/NeutrinoGun_13TeV_PU140_DelphesCMS_MuonPtDistribution/NeutrinoGun13TeV_PU140_MuonPtDistribution_Normalised.root": "ptDelphesMuonDistribution",
#  "_closureTest/L1TMuonDistribution/histograms.root": "coarseBinnedPtL1TMuonDistribution",
#  "_closureTest/SimL1TMuonDistribution_Binning_Set_3_HighStatistics_v2/histograms.root": "coarseBinnedPtSimL1TMuonDistribution",
#}
