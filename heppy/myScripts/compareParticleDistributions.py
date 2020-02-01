'''Compare the pt distribution between 13 and 100 TeV'''

from ROOT import TFile
from ROOT import TH1I
from ROOT import TH1F
from ROOT import gStyle
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TLatex

gStyle.SetOptStat(0)

canvas = TCanvas()
canvas.SetLogy()
#canvas.SetLogx()

# Opening files
file_100TeV = TFile("minBias_100TeV_particleDistributions/MinBiasDistribution_100TeV.root")
file_13TeV = TFile("minBias_13TeV_particleDistributions/MinBiasDistribution_13TeV.root")
file_13TeV_DelphesCMS = TFile("minBias_13TeV_DelphesCMS_particleDistributions/MinBiasDistribution_13TeV_DelphesCMS.root")
file_13TeV_DelphesFCC_CMSJets = TFile("minBias_13TeV_DelphesFCC_CMSJets_particleDistributions/MinBiasDistribution_13TeV_DelphesFCC_CMSJets.root")
file_100TeV_DelphesFCC_CMSJets = TFile("minBias_100TeV_DelphesFCC_CMSJets_particleDistributions/MinBiasDistribution_100TeV_DelphesFCC_CMSJets.root")

# Retrieving plots
jetRecoPtDistribution_TH1I_100TeV = file_100TeV.Get("jetRecoPtDistribution")
jetRecoPtDistribution_TH1I_13TeV = file_13TeV.Get("jetRecoPtDistribution")
jetRecoPtDistribution_TH1I_13TeV_DelphesCMS = file_13TeV_DelphesCMS.Get("jetRecoPtDistribution")
jetRecoPtDistribution_TH1I_13TeV_DelphesFCC_CMSJets = file_13TeV_DelphesFCC_CMSJets.Get("jetRecoPtDistribution")
jetRecoPtDistribution_TH1I_100TeV_DelphesFCC_CMSJets = file_100TeV_DelphesFCC_CMSJets.Get("jetRecoPtDistribution")

# Converting to float histogram
jetRecoPtDistribution_TH1F_100TeV = TH1F()
jetRecoPtDistribution_TH1F_13TeV = TH1F()
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS = TH1F()
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets = TH1F()
jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets = TH1F()
jetRecoPtDistribution_TH1F_100TeV.Add(jetRecoPtDistribution_TH1I_100TeV)
jetRecoPtDistribution_TH1F_13TeV.Add(jetRecoPtDistribution_TH1I_13TeV)
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.Add(jetRecoPtDistribution_TH1I_13TeV_DelphesCMS)
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.Add(jetRecoPtDistribution_TH1I_13TeV_DelphesFCC_CMSJets)
jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.Add(jetRecoPtDistribution_TH1I_100TeV_DelphesFCC_CMSJets)

# Normalising distributions
jetRecoPtDistribution_TH1F_100TeV.Scale(1./jetRecoPtDistribution_TH1F_100TeV.GetEntries())
jetRecoPtDistribution_TH1F_13TeV.Scale(1./jetRecoPtDistribution_TH1F_13TeV.GetEntries())
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.Scale(1./jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.GetEntries())
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.Scale(1./jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.GetEntries())
jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.Scale(1./jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.GetEntries())

# Making the plot fancy
jetRecoPtDistribution_TH1F_100TeV.SetStats(0)
jetRecoPtDistribution_TH1F_100TeV.GetXaxis().SetRangeUser(0, 400)
jetRecoPtDistribution_TH1F_100TeV.GetYaxis().SetRangeUser(1e-5, 0.5)
jetRecoPtDistribution_TH1F_100TeV.GetXaxis().SetTitle("p_{t} [GeV]")
jetRecoPtDistribution_TH1F_100TeV.GetYaxis().SetTitle("a.u.")
jetRecoPtDistribution_TH1F_100TeV.GetXaxis().SetTitleOffset(1.2)
jetRecoPtDistribution_TH1F_100TeV.GetYaxis().SetTitleOffset(1.2)
jetRecoPtDistribution_TH1F_100TeV.SetMarkerStyle(21)
jetRecoPtDistribution_TH1F_100TeV.SetMarkerColor(2)
jetRecoPtDistribution_TH1F_100TeV.SetLineColor(1)
jetRecoPtDistribution_TH1F_100TeV.SetTitle("Jet p_{t} distribution")
jetRecoPtDistribution_TH1F_100TeV.Draw("PE")

jetRecoPtDistribution_TH1F_13TeV.SetStats(0)
jetRecoPtDistribution_TH1F_13TeV.GetXaxis().SetRangeUser(0, 400)
jetRecoPtDistribution_TH1F_13TeV.GetXaxis().SetTitle("p_{t} [GeV]")
jetRecoPtDistribution_TH1F_13TeV.GetYaxis().SetTitle("a.u.")
jetRecoPtDistribution_TH1F_13TeV.GetXaxis().SetTitleOffset(1.2)
jetRecoPtDistribution_TH1F_13TeV.GetYaxis().SetTitleOffset(1.2)
jetRecoPtDistribution_TH1F_13TeV.SetMarkerStyle(21)
jetRecoPtDistribution_TH1F_13TeV.SetMarkerColor(3)
jetRecoPtDistribution_TH1F_13TeV.SetLineColor(1)
jetRecoPtDistribution_TH1F_13TeV.Draw("PE SAME")
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.SetStats(0)
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.SetStats(0)

jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.GetXaxis().SetRangeUser(0, 400)
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.GetXaxis().SetTitle("p_{t} [GeV]")
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.GetYaxis().SetTitle("a.u.")
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.GetXaxis().SetTitleOffset(1.2)
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.GetYaxis().SetTitleOffset(1.2)
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.SetMarkerStyle(22)
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.SetMarkerColor(4)
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.SetLineColor(1)
jetRecoPtDistribution_TH1F_13TeV_DelphesCMS.Draw("PE SAME")

jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.GetXaxis().SetRangeUser(0, 400)
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.GetXaxis().SetTitle("p_{t} [GeV]")
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.GetYaxis().SetTitle("a.u.")
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.GetXaxis().SetTitleOffset(1.2)
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.GetYaxis().SetTitleOffset(1.2)
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.SetMarkerStyle(20)
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.SetMarkerColor(6)
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.SetLineColor(1)
jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets.Draw("PE SAME")

jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.GetXaxis().SetRangeUser(0, 400)
jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.GetXaxis().SetTitle("p_{t} [GeV]")
jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.GetYaxis().SetTitle("a.u.")
jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.GetXaxis().SetTitleOffset(1.2)
jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.GetYaxis().SetTitleOffset(1.2)
jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.SetMarkerStyle(20)
jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.SetMarkerColor(7)
jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.SetLineColor(1)
jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets.Draw("PE SAME")

leg = TLegend(0.55,0.7,0.90,0.9)
leg.AddEntry(jetRecoPtDistribution_TH1F_100TeV,"100 TeV - FCC","P")
leg.AddEntry(jetRecoPtDistribution_TH1F_100TeV_DelphesFCC_CMSJets,"100 TeV - FCC w/ CMS jet reco","P")
leg.AddEntry(jetRecoPtDistribution_TH1F_13TeV,"13 TeV - FCC w/ FCC jet reco","P")
leg.AddEntry(jetRecoPtDistribution_TH1F_13TeV_DelphesCMS,"13 TeV - CMS","P")
leg.AddEntry(jetRecoPtDistribution_TH1F_13TeV_DelphesFCC_CMSJets,"13 TeV - FCC w/ CMS jet reco","P")
leg.Draw()

label_Simulation = TLatex()
label_Simulation.SetTextSize(0.03)
label_Simulation.DrawLatexNDC(0.1, 0.905, "Delphes simulation - Reco level")

canvas.Print("jetPtDistribution_100TeV_VS_13TeV.svg", "svg")
canvas.Print("jetPtDistribution_100TeV_VS_13TeV.png", "png")