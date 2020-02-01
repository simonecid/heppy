''' Creates a comparison plot with ratio '''

from ROOT import TFile
from ROOT import TH1F
from ROOT import TTree
from ROOT import TPaveText
from ROOT import TCanvas
from ROOT import TPad
from ROOT import TLegend
from ROOT import TGaxis
from ROOT import TLine

# From here on it works by magic, and I am the magician :P

def plotDistributionComparisonPlot(cfg):

  tfiles = [
  ]

  histograms = [
  ]

  canvas = TCanvas("canvas", "canvas", 800, 800)
  '''Contains the legend'''
  legend = TLegend(0.3, 0.7, 0.90, 0.9)
  '''Maximum value container, used to scale histograms'''
  maximumY = float("-inf")
  minimumY = float("+inf")

  colorIdx = 1
  
  for histogramFileNameAndTitle in cfg.plots:
    tfile = TFile(histogramFileNameAndTitle[0])
    tfiles.append(tfile)
    histogram = tfile.Get(histogramFileNameAndTitle[1])
    histograms.append(histogram)
    histogram.SetStats(0)          # No statistics on upper plot
    histogram.SetMarkerColor(colorIdx)
    histogram.SetLineColor(colorIdx)
    histogram.SetLineWidth(1)
    maximumY = histogram.GetMaximum() if histogram.GetMaximum() > maximumY else maximumY
    minimumY = histogram.GetMinimum() if histogram.GetMinimum() > minimumY else minimumY
    legend.AddEntry(histogram, histogramFileNameAndTitle[2], "l")
    # Y axis histograms[0] plot settings
    histogram.GetYaxis().SetTitleSize(20)
    histogram.GetYaxis().SetTitleFont(43)
    histogram.GetYaxis().SetTitleOffset(1.55)
    histogram.Draw("SAME HIST")       
    colorIdx += 1
    if colorIdx == 5: #Excluding the terrible yellow on white background.
      colorIdx += 1

  maximumY *= 1.1
  minimumY *= 0.9
  histograms[0].GetYaxis().SetRangeUser(minimumY, maximumY)
  legend.Draw()

  # Do not draw the Y axis label on the upper plot and redraw a small
  # axis instead, in order to avoid the first label (0) to be clipped.
  #histograms[0].GetYaxis().SetLabelSize(0.)
  #axis = TGaxis( 0, 20, 0, maximumY, 20, maximumY, 510,"")
  #axis.SetLabelFont(43) # Absolute font size in pixel (precision 3)
  #axis.SetLabelSize(15)
  #axis.Draw()

  saveFile = TFile(cfg.saveFileName, "RECREATE")
  saveFile.cd()
  canvas.Write()
  for histogram in histograms:
    histogram.Write()
  saveFile.Close()
  for tfile in tfiles:
    tfile.Close()

if __name__ == "__main__":

  cfg = lambda x: 1
  cfg.plots = [
    #Files here
    # ["MinBiasDistribution_13TeV_DelphesCMS_CMSJets_GenJetPTDistribution/genJetPtDistribution_Normalised.root", "ptSimL1TMuonDistribution", "MinBias"],
    #["_closureTest/l1tMuonGenMuonMatching_SingleMu_FlatPt_8to100_QualityCut_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtSimL1TMuonDistribution", "SimL1TMuon"],
    #["_closureTest/l1tMuonGenMuonMatching_SingleMu_FlatPt_8to100_QualityCut_WQualityBranch_L1TMuon_vs_SimL1TMuon_PtDistribution/histograms.root", "coarseBinnedPtL1TMuonDistribution", "Original L1TMuon"],
    ["_jetTriggerRate_BarrelOnly_HardPtCut10GeV/HardPtCut10/genJet_l1tJet_MinimumBias_14TeV_GenParticles_500kevents_RatePlots_PU140RatePlot.root", "fullPURatePlot", "Sim-L1TJets PU140 and hard pt cut of 10"],
    ["_jetTriggerRate_BarrelOnly_HardPtCut10GeV/HardPtCut15/genJet_l1tJet_MinimumBias_14TeV_GenParticles_500kevents_RatePlots_PU140RatePlot.root", "fullPURatePlot", "Sim-L1TJets PU140 and hard pt cut of 15"],
    ["_jetTriggerRate_BarrelOnly_HardPtCut10GeV/HardPtCut20/genJet_l1tJet_MinimumBias_14TeV_GenParticles_500kevents_RatePlots_PU140RatePlot.root", "fullPURatePlot", "Sim-L1TJets PU140 and hard pt cut of 20"],
    ["_jetTriggerRate_BarrelOnly_HardPtCut10GeV/HardPtCut30/genJet_l1tJet_MinimumBias_14TeV_GenParticles_500kevents_RatePlots_PU140RatePlot.root", "fullPURatePlot", "Sim-L1TJets PU140 and hard pt cut of 30"],
    ["_jetTriggerRate_BarrelOnly_HardPtCut10GeV/cmsMatching_SingleNeutrinoPU140_BarrelOnly_LeadingL1TJet_CMSTriggerRate/ratePlots.root", "triggerRate", "CMS rate"],

  ]
  cfg.saveFileName = "comparisonResult.root"

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