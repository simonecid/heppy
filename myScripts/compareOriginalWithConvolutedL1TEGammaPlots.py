from ROOT import TFile
from ROOT import TLegend
from ROOT import TCanvas
from ROOT import gStyle
from ROOT import TLine
from ROOT import TChain
from ROOT import TH1F

canvas = TCanvas()
canvas.SetLogy()  

fileL1TEGammaFromGenJet = TFile("_jetToL1TConversion/cmsMatching_QCD_15_3000_GenJet_Merged_Histograms.root")
fileL1TEGammaFromGenJet.Get("l1tEGammaPtHistogram").Draw()
histogramL1TEGammaFromGenJet = fileL1TEGammaFromGenJet.Get("l1tEGammaPtHistogram")
histogramL1TEGammaFromGenJet.SetTitle("histogramL1TEGammaFromGenJet")
histogramL1TEGammaFromGenJet.SetLineColor(1)
histogramL1TEGammaFromGenJet.SetMarkerStyle(20)
histogramL1TEGammaFromGenJet.SetMarkerColor(4)
histogramL1TEGammaFromGenJet.SetMarkerSize(1)
histogramL1TEGammaFromGenJet.Scale(1./histogramL1TEGammaFromGenJet.GetEntries())
histogramL1TEGammaFromGenJet.Draw("")

chainL1TEGammaGenJet = TChain ("MatchGenJetWithL1Objects/matchedL1TEGammaGenJetTree")
chainL1TEGammaGenJet.Add("/hdfs/FCC-hh/l1tGenJetMatching_QCD_15_3000_NoPU_Phase1_L11Obj_To_GenJet_Match_ClosestDR/*")
histogramOriginalL1TEGamma = histogramL1TEGammaFromGenJet.Clone("histogramOriginalL1TEGamma")
histogramOriginalL1TEGamma.Reset()
histogramOriginalL1TEGamma.SetTitle("histogramOriginalL1TEGamma")
histogramOriginalL1TEGamma.SetLineColor(1)
histogramOriginalL1TEGamma.SetMarkerColor(2)
histogramOriginalL1TEGamma.SetMarkerSize(1)
histogramOriginalL1TEGamma.SetMarkerStyle(20)
chainL1TEGammaGenJet.Draw("l1tEGamma_pt >> histogramOriginalL1TEGamma", "genJet_pt < 120", "SAME")
histogramOriginalL1TEGamma.Scale(1./histogramOriginalL1TEGamma.GetEntries())
canvas.Update()

histogramL1TEGammaFromGenJet.GetXaxis().SetRangeUser(0, 50)
histogramL1TEGammaFromGenJet.GetYaxis().SetRangeUser(1e-5, 0.5)

canvas.BuildLegend()