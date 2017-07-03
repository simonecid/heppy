'''
  Compare 
'''

from ROOT import TFile
from ROOT import TMultiGraph
from ROOT import TGraph
from ROOT import TLegend
from ROOT import TCanvas
from ROOT import gStyle
from ROOT import TLine
from ROOT import TH1F
from array import array

import sys

gStyle.SetOptStat(0)

muonFile = TFile("_muonMatching_13TeV/muonMatching_13TeV.root")
#muonFile = TFile("_testMuonMatch/HardQCD_PtBinned_10_30_GeV/histograms.root")
#muonFile = TFile("_testMuonMatch/_MBtest/histograms.root")

###############################################################################
# PT
###############################################################################

# Loading the plots from file
muonPtDistribution = muonFile.Get("muonPtDistribution")
pairedNoRestrictionMuonPtDistribution = muonFile.Get("pairedNoRestrictionMuonPtDistribution")
pairedLooseRestrictionMuonPtDistribution = muonFile.Get("pairedLooseRestrictionMuonPtDistribution")
pairedMediumRestrictionMuonPtDistribution = muonFile.Get("pairedMediumRestrictionMuonPtDistribution")
pairedTightRestrictionMuonPtDistribution = muonFile.Get("pairedTightRestrictionMuonPtDistribution")

muonPtDistribution.SetStats(False)
pairedNoRestrictionMuonPtDistribution.SetStats(False)
pairedLooseRestrictionMuonPtDistribution.SetStats(False)
pairedMediumRestrictionMuonPtDistribution.SetStats(False)
pairedTightRestrictionMuonPtDistribution.SetStats(False)

canvasMuonPt = TCanvas()

# Normalising the plots
muonPtDistribution.SetMarkerColor(1)
muonPtDistribution.SetMarkerStyle(21)
pairedNoRestrictionMuonPtDistribution.SetMarkerColor(2)
pairedNoRestrictionMuonPtDistribution.SetMarkerStyle(22)
pairedLooseRestrictionMuonPtDistribution.SetMarkerColor(3)
pairedLooseRestrictionMuonPtDistribution.SetMarkerStyle(22)
pairedMediumRestrictionMuonPtDistribution.SetMarkerColor(6)
pairedMediumRestrictionMuonPtDistribution.SetMarkerStyle(22)
pairedTightRestrictionMuonPtDistribution.SetMarkerColor(4)
pairedTightRestrictionMuonPtDistribution.SetMarkerStyle(22)

#muonPtDistribution.GetXaxis().SetRangeUser(0, 30)

muonPtDistribution.Draw("PE")
pairedNoRestrictionMuonPtDistribution.Draw("PE SAME")
pairedLooseRestrictionMuonPtDistribution.Draw("PE SAME")
pairedMediumRestrictionMuonPtDistribution.Draw("PE SAME")
pairedTightRestrictionMuonPtDistribution.Draw("PE SAME")

legMuonPt = TLegend(0.65,0.7,0.90,0.9)
legMuonPt.AddEntry(muonPtDistribution,"Full distribution","p")
legMuonPt.AddEntry(pairedNoRestrictionMuonPtDistribution,"#DeltaR_{max}=15","p")
legMuonPt.AddEntry(pairedLooseRestrictionMuonPtDistribution,"#DeltaR_{max}=3","p")
legMuonPt.AddEntry(pairedMediumRestrictionMuonPtDistribution,"#DeltaR_{max}=1.5","p")
legMuonPt.AddEntry(pairedTightRestrictionMuonPtDistribution,"#DeltaR_{max}=0.5","p")
legMuonPt.Draw()

canvasMuonPt.Print("matchedMuonNumberOfEventPtDistribution.png", "png")

canvasSelectionEfficiency = TCanvas()

canvasSelectionEfficiency.SetLogy()

pairedNoRestrictionMuonFractionPtDistribution = pairedNoRestrictionMuonPtDistribution.Clone("pairedNoRestrictionMuonFractionPtDistribution")
pairedLooseRestrictionMuonFractionPtDistribution = pairedLooseRestrictionMuonPtDistribution.Clone("pairedLooseRestrictionMuonFractionPtDistribution")
pairedMediumRestrictionMuonFractionPtDistribution = pairedMediumRestrictionMuonPtDistribution.Clone("pairedMediumRestrictionMuonFractionPtDistribution")
pairedTightRestrictionMuonFractionPtDistribution = pairedTightRestrictionMuonPtDistribution.Clone("pairedTightRestrictionMuonFractionPtDistribution")

pairedNoRestrictionMuonFractionPtDistribution.SetTitle("Fraction of accepted events")
pairedNoRestrictionMuonFractionPtDistribution.GetYaxis().SetTitle("% of accepted events")

pairedNoRestrictionMuonFractionPtDistribution.Divide(muonPtDistribution)
pairedLooseRestrictionMuonFractionPtDistribution.Divide(muonPtDistribution)
pairedMediumRestrictionMuonFractionPtDistribution.Divide(muonPtDistribution)
pairedTightRestrictionMuonFractionPtDistribution.Divide(muonPtDistribution)

pairedNoRestrictionMuonFractionPtDistribution.SetLineColor(2)
pairedLooseRestrictionMuonFractionPtDistribution.SetLineColor(3)
pairedMediumRestrictionMuonFractionPtDistribution.SetLineColor(6)
pairedTightRestrictionMuonFractionPtDistribution.SetLineColor(4)

pairedNoRestrictionMuonFractionPtDistribution.Draw("HIST")
pairedLooseRestrictionMuonFractionPtDistribution.Draw("HIST SAME")
pairedMediumRestrictionMuonFractionPtDistribution.Draw("HIST SAME")
pairedTightRestrictionMuonFractionPtDistribution.Draw("HIST SAME")

legMuonPt = TLegend(0.65,0.7,0.90,0.9)
legMuonPt.AddEntry(muonPtDistribution,"Full distribution","p")
legMuonPt.AddEntry(pairedNoRestrictionMuonPtDistribution,"#DeltaR_{max}=15","p")
legMuonPt.AddEntry(pairedLooseRestrictionMuonPtDistribution,"#DeltaR_{max}=3","p")
legMuonPt.AddEntry(pairedMediumRestrictionMuonPtDistribution,"#DeltaR_{max}=1.5","p")
legMuonPt.AddEntry(pairedTightRestrictionMuonPtDistribution,"#DeltaR_{max}=0.5","p")
legMuonPt.Draw()

canvasMuonPt.Print("matchedMuonFractionOfEventPtDistribution.png", "png")

canvasMuonPt.cd()

muonPtDistribution.Scale(1./muonPtDistribution.GetEntries())
pairedNoRestrictionMuonPtDistribution.Scale(1./pairedNoRestrictionMuonPtDistribution.GetEntries())
pairedLooseRestrictionMuonPtDistribution.Scale(1./pairedLooseRestrictionMuonPtDistribution.GetEntries())
pairedMediumRestrictionMuonPtDistribution.Scale(1./pairedMediumRestrictionMuonPtDistribution.GetEntries())
pairedTightRestrictionMuonPtDistribution.Scale(1./pairedTightRestrictionMuonPtDistribution.GetEntries())

muonPtDistribution.Draw("PE")
pairedNoRestrictionMuonPtDistribution.Draw("PE SAME")
pairedLooseRestrictionMuonPtDistribution.Draw("PE SAME")
pairedMediumRestrictionMuonPtDistribution.Draw("PE SAME")
pairedTightRestrictionMuonPtDistribution.Draw("PE SAME")

legMuonPt.Draw()

canvasMuonPt.Print("matchedMuonEtaDistribution.png", "png")

#muonPtDistribution.SetLineColor(1)
#pairedNoRestrictionMuonPtDistribution.SetLineColor(2)
#pairedLooseRestrictionMuonPtDistribution.SetLineColor(3)
#pairedTightRestrictionMuonPtDistribution.SetLineColor(4)
#muonPtDistribution.Draw("HIST")
#pairedNoRestrictionMuonPtDistribution.Draw("HIST SAME")
#pairedLooseRestrictionMuonPtDistribution.Draw("HIST SAME")
#pairedTightRestrictionMuonPtDistribution.Draw("HIST SAME")

canvasJetPt = TCanvas()
canvasJetPt.cd()

canvasJetPt.SetLogy()

jetPtDistribution = muonFile.Get("jetPtDistribution")
pairedNoRestrictionJetPtDistribution = muonFile.Get("pairedNoRestrictionJetPtDistribution")
pairedLooseRestrictionJetPtDistribution = muonFile.Get("pairedLooseRestrictionJetPtDistribution")
pairedMediumRestrictionJetPtDistribution = muonFile.Get("pairedMediumRestrictionJetPtDistribution")
pairedTightRestrictionJetPtDistribution = muonFile.Get("pairedTightRestrictionJetPtDistribution")

jetPtDistribution.SetStats(False)
pairedNoRestrictionJetPtDistribution.SetStats(False)
pairedLooseRestrictionJetPtDistribution.SetStats(False)
pairedMediumRestrictionJetPtDistribution.SetStats(False)
pairedTightRestrictionJetPtDistribution.SetStats(False)

jetPtDistribution.SetMarkerColor(1)
jetPtDistribution.SetMarkerStyle(21)
pairedNoRestrictionJetPtDistribution.SetMarkerColor(2)
pairedNoRestrictionJetPtDistribution.SetMarkerStyle(22)
pairedLooseRestrictionJetPtDistribution.SetMarkerColor(3)
pairedLooseRestrictionJetPtDistribution.SetMarkerStyle(22)
pairedMediumRestrictionJetPtDistribution.SetMarkerColor(6)
pairedMediumRestrictionJetPtDistribution.SetMarkerStyle(22)
pairedTightRestrictionJetPtDistribution.SetMarkerColor(4)
pairedTightRestrictionJetPtDistribution.SetMarkerStyle(22)
jetPtDistribution.Draw("PE")
pairedNoRestrictionJetPtDistribution.Draw("PE SAME")
pairedLooseRestrictionJetPtDistribution.Draw("PE SAME")
pairedMediumRestrictionJetPtDistribution.Draw("PE SAME")
pairedTightRestrictionJetPtDistribution.Draw("PE SAME")

legJetPt = TLegend(0.65,0.7,0.90,0.9)
legJetPt.AddEntry(jetPtDistribution,"Full distribution","p")
legJetPt.AddEntry(pairedNoRestrictionJetPtDistribution,"#DeltaR_{max}=15","p")
legJetPt.AddEntry(pairedLooseRestrictionJetPtDistribution,"#DeltaR_{max}=3","p")
legJetPt.AddEntry(pairedMediumRestrictionJetPtDistribution,"#DeltaR_{max}=1.5","p")
legJetPt.AddEntry(pairedTightRestrictionJetPtDistribution,"#DeltaR_{max}=0.5","p")
legJetPt.Draw()

canvasJetPt.Print("matchedJetNumberOfEventPtDistribution.png", "png")

jetPtDistribution.Scale(1./jetPtDistribution.GetEntries())
pairedNoRestrictionJetPtDistribution.Scale(1./pairedNoRestrictionJetPtDistribution.GetEntries())
pairedLooseRestrictionJetPtDistribution.Scale(1./pairedLooseRestrictionJetPtDistribution.GetEntries())
pairedMediumRestrictionJetPtDistribution.Scale(1./pairedMediumRestrictionJetPtDistribution.GetEntries())
pairedTightRestrictionJetPtDistribution.Scale(1./pairedTightRestrictionJetPtDistribution.GetEntries())
jetPtDistribution.Draw("PE")
pairedNoRestrictionJetPtDistribution.Draw("PE SAME")
pairedLooseRestrictionJetPtDistribution.Draw("PE SAME")
pairedMediumRestrictionJetPtDistribution.Draw("PE SAME")
pairedTightRestrictionJetPtDistribution.Draw("PE SAME")

legJetPt.Draw()
canvasJetPt.Print("matchedJetPtDistribution.png", "png")

#jetPtDistribution.SetLineColor(1)
#pairedNoRestrictionJetPtDistribution.SetLineColor(2)
#pairedLooseRestrictionJetPtDistribution.SetLineColor(3)
#pairedTightRestrictionJetPtDistribution.SetLineColor(4)
#jetPtDistribution.Draw("HIST")
#pairedNoRestrictionJetPtDistribution.Draw("HIST SAME")
#pairedLooseRestrictionJetPtDistribution.Draw("HIST SAME")
#pairedTightRestrictionJetPtDistribution.Draw("HIST SAME")

###############################################################################
# ETA
###############################################################################

# Loading the plots from file
muonEtaDistribution = muonFile.Get("muonEtaDistribution")
pairedNoRestrictionMuonEtaDistribution = muonFile.Get("pairedNoRestrictionMuonEtaDistribution")
pairedLooseRestrictionMuonEtaDistribution = muonFile.Get("pairedLooseRestrictionMuonEtaDistribution")
pairedMediumRestrictionMuonEtaDistribution = muonFile.Get("pairedMediumRestrictionMuonEtaDistribution")
pairedTightRestrictionMuonEtaDistribution = muonFile.Get("pairedTightRestrictionMuonEtaDistribution")

muonEtaDistribution.SetStats(False)
pairedNoRestrictionMuonEtaDistribution.SetStats(False)
pairedLooseRestrictionMuonEtaDistribution.SetStats(False)
pairedMediumRestrictionMuonEtaDistribution.SetStats(False)
pairedTightRestrictionMuonEtaDistribution.SetStats(False)

canvasMuonEta = TCanvas()

canvasMuonEta.SetLogy()

# Normalising the plots
muonEtaDistribution.SetMarkerColor(1)
muonEtaDistribution.SetMarkerStyle(21)
pairedNoRestrictionMuonEtaDistribution.SetMarkerColor(2)
pairedNoRestrictionMuonEtaDistribution.SetMarkerStyle(22)
pairedLooseRestrictionMuonEtaDistribution.SetMarkerColor(3)
pairedLooseRestrictionMuonEtaDistribution.SetMarkerStyle(22)
pairedMediumRestrictionMuonEtaDistribution.SetMarkerColor(6)
pairedMediumRestrictionMuonEtaDistribution.SetMarkerStyle(22)
pairedTightRestrictionMuonEtaDistribution.SetMarkerColor(4)
pairedTightRestrictionMuonEtaDistribution.SetMarkerStyle(22)

muonEtaDistribution.Draw("PE")
pairedNoRestrictionMuonEtaDistribution.Draw("PE SAME")
pairedLooseRestrictionMuonEtaDistribution.Draw("PE SAME")
pairedMediumRestrictionMuonEtaDistribution.Draw("PE SAME")
pairedTightRestrictionMuonEtaDistribution.Draw("PE SAME")

legMuonEta = TLegend(0.65,0.7,0.90,0.9)
legMuonEta.AddEntry(muonEtaDistribution,"Full distribution","p")
legMuonEta.AddEntry(pairedNoRestrictionMuonEtaDistribution,"#DeltaR_{max}=15","p")
legMuonEta.AddEntry(pairedLooseRestrictionMuonEtaDistribution,"#DeltaR_{max}=3","p")
legMuonEta.AddEntry(pairedMediumRestrictionMuonEtaDistribution,"#DeltaR_{max}=1.5","p")
legMuonEta.AddEntry(pairedTightRestrictionMuonEtaDistribution,"#DeltaR_{max}=0.5","p")
legMuonEta.Draw()

canvasMuonEta.Print("matchedMuonNumberOfEventEtaDistribution.png", "png")

muonEtaDistribution.Scale(1./muonEtaDistribution.GetEntries())
pairedNoRestrictionMuonEtaDistribution.Scale(1./pairedNoRestrictionMuonEtaDistribution.GetEntries())
pairedLooseRestrictionMuonEtaDistribution.Scale(1./pairedLooseRestrictionMuonEtaDistribution.GetEntries())
pairedMediumRestrictionMuonEtaDistribution.Scale(1./pairedMediumRestrictionMuonEtaDistribution.GetEntries())
pairedTightRestrictionMuonEtaDistribution.Scale(1./pairedTightRestrictionMuonEtaDistribution.GetEntries())

muonEtaDistribution.Draw("PE")
pairedNoRestrictionMuonEtaDistribution.Draw("PE SAME")
pairedLooseRestrictionMuonEtaDistribution.Draw("PE SAME")
pairedMediumRestrictionMuonEtaDistribution.Draw("PE SAME")
pairedTightRestrictionMuonEtaDistribution.Draw("PE SAME")

legMuonEta.Draw()

canvasMuonEta.Print("matchedMuonEtaDistribution.png", "png")

#muonEtaDistribution.SetLineColor(1)
#pairedNoRestrictionMuonEtaDistribution.SetLineColor(2)
#pairedLooseRestrictionMuonEtaDistribution.SetLineColor(3)
#pairedTightRestrictionMuonEtaDistribution.SetLineColor(4)
#muonEtaDistribution.Draw("HIST")
#pairedNoRestrictionMuonEtaDistribution.Draw("HIST SAME")
#pairedLooseRestrictionMuonEtaDistribution.Draw("HIST SAME")
#pairedTightRestrictionMuonEtaDistribution.Draw("HIST SAME")

canvasJetEta = TCanvas()
canvasJetEta.cd()

canvasJetEta.SetLogy()

jetEtaDistribution = muonFile.Get("jetEtaDistribution")
pairedNoRestrictionJetEtaDistribution = muonFile.Get("pairedNoRestrictionJetEtaDistribution")
pairedLooseRestrictionJetEtaDistribution = muonFile.Get("pairedLooseRestrictionJetEtaDistribution")
pairedMediumRestrictionJetEtaDistribution = muonFile.Get("pairedMediumRestrictionJetEtaDistribution")
pairedTightRestrictionJetEtaDistribution = muonFile.Get("pairedTightRestrictionJetEtaDistribution")

jetEtaDistribution.SetStats(False)
pairedNoRestrictionJetEtaDistribution.SetStats(False)
pairedLooseRestrictionJetEtaDistribution.SetStats(False)
pairedMediumRestrictionJetEtaDistribution.SetStats(False)
pairedTightRestrictionJetEtaDistribution.SetStats(False)

jetEtaDistribution.SetMarkerColor(1)
jetEtaDistribution.SetMarkerStyle(21)
pairedNoRestrictionJetEtaDistribution.SetMarkerColor(2)
pairedNoRestrictionJetEtaDistribution.SetMarkerStyle(22)
pairedLooseRestrictionJetEtaDistribution.SetMarkerColor(3)
pairedLooseRestrictionJetEtaDistribution.SetMarkerStyle(22)
pairedMediumRestrictionJetEtaDistribution.SetMarkerColor(6)
pairedMediumRestrictionJetEtaDistribution.SetMarkerStyle(22)
pairedTightRestrictionJetEtaDistribution.SetMarkerColor(4)
pairedTightRestrictionJetEtaDistribution.SetMarkerStyle(22)
jetEtaDistribution.Draw("PE")
pairedNoRestrictionJetEtaDistribution.Draw("PE SAME")
pairedLooseRestrictionJetEtaDistribution.Draw("PE SAME")
pairedMediumRestrictionJetEtaDistribution.Draw("PE SAME")
pairedTightRestrictionJetEtaDistribution.Draw("PE SAME")

legJetEta = TLegend(0.65,0.7,0.90,0.9)
legJetEta.AddEntry(jetEtaDistribution,"Full distribution","p")
legJetEta.AddEntry(pairedNoRestrictionJetEtaDistribution,"#DeltaR_{max}=15","p")
legJetEta.AddEntry(pairedLooseRestrictionJetEtaDistribution,"#DeltaR_{max}=3","p")
legJetEta.AddEntry(pairedMediumRestrictionJetEtaDistribution,"#DeltaR_{max}=1.5","p")
legJetEta.AddEntry(pairedTightRestrictionJetEtaDistribution,"#DeltaR_{max}=0.5","p")
legJetEta.Draw()

canvasJetEta.Print("matchedJetNumberOfEventEtaDistribution.png", "png")

jetEtaDistribution.Scale(1./jetEtaDistribution.GetEntries())
pairedNoRestrictionJetEtaDistribution.Scale(1./pairedNoRestrictionJetEtaDistribution.GetEntries())
pairedLooseRestrictionJetEtaDistribution.Scale(1./pairedLooseRestrictionJetEtaDistribution.GetEntries())
pairedMediumRestrictionJetEtaDistribution.Scale(1./pairedMediumRestrictionJetEtaDistribution.GetEntries())
pairedTightRestrictionJetEtaDistribution.Scale(1./pairedTightRestrictionJetEtaDistribution.GetEntries())
jetEtaDistribution.Draw("PE")
pairedNoRestrictionJetEtaDistribution.Draw("PE SAME")
pairedLooseRestrictionJetEtaDistribution.Draw("PE SAME")
pairedMediumRestrictionJetEtaDistribution.Draw("PE SAME")
pairedTightRestrictionJetEtaDistribution.Draw("PE SAME")

legJetEta.Draw()

canvasJetEta.Print("matchedJetEtaDistribution.png", "png")

#jetEtaDistribution.SetLineColor(1)
#pairedNoRestrictionJetEtaDistribution.SetLineColor(2)
#pairedLooseRestrictionJetEtaDistribution.SetLineColor(3)
#pairedTightRestrictionJetEtaDistribution.SetLineColor(4)
#jetEtaDistribution.Draw("HIST")
#pairedNoRestrictionJetEtaDistribution.Draw("HIST SAME")
#pairedLooseRestrictionJetEtaDistribution.Draw("HIST SAME")
#pairedTightRestrictionJetEtaDistribution.Draw("HIST SAME")

###############################################################################
# PHI
###############################################################################

# Loading the plots from file
muonPhiDistribution = muonFile.Get("muonPhiDistribution")
pairedNoRestrictionMuonPhiDistribution = muonFile.Get("pairedNoRestrictionMuonPhiDistribution")
pairedLooseRestrictionMuonPhiDistribution = muonFile.Get("pairedLooseRestrictionMuonPhiDistribution")
pairedMediumRestrictionMuonPhiDistribution = muonFile.Get("pairedMediumRestrictionMuonPhiDistribution")
pairedTightRestrictionMuonPhiDistribution = muonFile.Get("pairedTightRestrictionMuonPhiDistribution")

muonPhiDistribution.SetStats(False)
pairedNoRestrictionMuonPhiDistribution.SetStats(False)
pairedLooseRestrictionMuonPhiDistribution.SetStats(False)
pairedMediumRestrictionMuonPhiDistribution.SetStats(False)
pairedTightRestrictionMuonPhiDistribution.SetStats(False)

canvasMuonPhi = TCanvas()

canvasMuonPhi.SetLogy()

# Normalising the plots
muonPhiDistribution.SetMarkerColor(1)
muonPhiDistribution.SetMarkerStyle(21)
pairedNoRestrictionMuonPhiDistribution.SetMarkerColor(2)
pairedNoRestrictionMuonPhiDistribution.SetMarkerStyle(22)
pairedLooseRestrictionMuonPhiDistribution.SetMarkerColor(3)
pairedLooseRestrictionMuonPhiDistribution.SetMarkerStyle(22)
pairedMediumRestrictionMuonPhiDistribution.SetMarkerColor(6)
pairedMediumRestrictionMuonPhiDistribution.SetMarkerStyle(22)
pairedTightRestrictionMuonPhiDistribution.SetMarkerColor(4)
pairedTightRestrictionMuonPhiDistribution.SetMarkerStyle(22)

muonPhiDistribution.Draw("PE")
pairedNoRestrictionMuonPhiDistribution.Draw("PE SAME")
pairedLooseRestrictionMuonPhiDistribution.Draw("PE SAME")
pairedMediumRestrictionMuonPhiDistribution.Draw("PE SAME")
pairedTightRestrictionMuonPhiDistribution.Draw("PE SAME")

legMuonPhi = TLegend(0.65,0.7,0.90,0.9)
legMuonPhi.AddEntry(muonPhiDistribution,"Full distribution","p")
legMuonPhi.AddEntry(pairedNoRestrictionMuonPhiDistribution,"#DeltaR_{max}=15","p")
legMuonPhi.AddEntry(pairedLooseRestrictionMuonPhiDistribution,"#DeltaR_{max}=3","p")
legMuonPhi.AddEntry(pairedMediumRestrictionMuonPhiDistribution,"#DeltaR_{max}=1.5","p")
legMuonPhi.AddEntry(pairedTightRestrictionMuonPhiDistribution,"#DeltaR_{max}=0.5","p")
legMuonPhi.Draw()

canvasMuonPhi.Print("matchedMuonNumberOfEventPhiDistribution.png", "png")

muonPhiDistribution.Scale(1./muonPhiDistribution.GetEntries())
pairedNoRestrictionMuonPhiDistribution.Scale(1./pairedNoRestrictionMuonPhiDistribution.GetEntries())
pairedLooseRestrictionMuonPhiDistribution.Scale(1./pairedLooseRestrictionMuonPhiDistribution.GetEntries())
pairedMediumRestrictionMuonPhiDistribution.Scale(1./pairedMediumRestrictionMuonPhiDistribution.GetEntries())
pairedTightRestrictionMuonPhiDistribution.Scale(1./pairedTightRestrictionMuonPhiDistribution.GetEntries())

muonPhiDistribution.Draw("PE")
pairedNoRestrictionMuonPhiDistribution.Draw("PE SAME")
pairedLooseRestrictionMuonPhiDistribution.Draw("PE SAME")
pairedMediumRestrictionMuonPhiDistribution.Draw("PE SAME")
pairedTightRestrictionMuonPhiDistribution.Draw("PE SAME")

legMuonPhi.Draw()

canvasMuonPhi.Print("matchedMuonPhiDistribution.png", "png")

#muonPhiDistribution.SetLineColor(1)
#pairedNoRestrictionMuonPhiDistribution.SetLineColor(2)
#pairedLooseRestrictionMuonPhiDistribution.SetLineColor(3)
#pairedTightRestrictionMuonPhiDistribution.SetLineColor(4)
#muonPhiDistribution.Draw("HIST")
#pairedNoRestrictionMuonPhiDistribution.Draw("HIST SAME")
#pairedLooseRestrictionMuonPhiDistribution.Draw("HIST SAME")
#pairedTightRestrictionMuonPhiDistribution.Draw("HIST SAME")

canvasJetPhi = TCanvas()
canvasJetPhi.cd()

canvasJetPhi.SetLogy()

jetPhiDistribution = muonFile.Get("jetPhiDistribution")
pairedNoRestrictionJetPhiDistribution = muonFile.Get("pairedNoRestrictionJetPhiDistribution")
pairedLooseRestrictionJetPhiDistribution = muonFile.Get("pairedLooseRestrictionJetPhiDistribution")
pairedMediumRestrictionJetPhiDistribution = muonFile.Get("pairedMediumRestrictionJetPhiDistribution")
pairedTightRestrictionJetPhiDistribution = muonFile.Get("pairedTightRestrictionJetPhiDistribution")

jetPhiDistribution.SetStats(False)
pairedNoRestrictionJetPhiDistribution.SetStats(False)
pairedLooseRestrictionJetPhiDistribution.SetStats(False)
pairedMediumRestrictionJetPhiDistribution.SetStats(False)
pairedTightRestrictionJetPhiDistribution.SetStats(False)

jetPhiDistribution.SetMarkerColor(1)
jetPhiDistribution.SetMarkerStyle(21)
pairedNoRestrictionJetPhiDistribution.SetMarkerColor(2)
pairedNoRestrictionJetPhiDistribution.SetMarkerStyle(22)
pairedLooseRestrictionJetPhiDistribution.SetMarkerColor(3)
pairedLooseRestrictionJetPhiDistribution.SetMarkerStyle(22)
pairedMediumRestrictionJetPhiDistribution.SetMarkerColor(6)
pairedMediumRestrictionJetPhiDistribution.SetMarkerStyle(22)
pairedTightRestrictionJetPhiDistribution.SetMarkerColor(4)
pairedTightRestrictionJetPhiDistribution.SetMarkerStyle(22)
jetPhiDistribution.Draw("PE")
pairedNoRestrictionJetPhiDistribution.Draw("PE SAME")
pairedLooseRestrictionJetPhiDistribution.Draw("PE SAME")
pairedMediumRestrictionJetPhiDistribution.Draw("PE SAME")
pairedTightRestrictionJetPhiDistribution.Draw("PE SAME")

legJetPhi = TLegend(0.65,0.7,0.90,0.9)
legJetPhi.AddEntry(jetPhiDistribution,"Full distribution","p")
legJetPhi.AddEntry(pairedNoRestrictionJetPhiDistribution,"#DeltaR_{max}=15","p")
legJetPhi.AddEntry(pairedLooseRestrictionJetPhiDistribution,"#DeltaR_{max}=3","p")
legJetPhi.AddEntry(pairedMediumRestrictionJetPhiDistribution,"#DeltaR_{max}=1.5","p")
legJetPhi.AddEntry(pairedTightRestrictionJetPhiDistribution,"#DeltaR_{max}=0.5","p")
legJetPhi.Draw()

canvasJetPhi.Print("matchedJetNumberOfEventPhiDistribution.png", "png")

jetPhiDistribution.Scale(1./jetPhiDistribution.GetEntries())
pairedNoRestrictionJetPhiDistribution.Scale(1./pairedNoRestrictionJetPhiDistribution.GetEntries())
pairedLooseRestrictionJetPhiDistribution.Scale(1./pairedLooseRestrictionJetPhiDistribution.GetEntries())
pairedMediumRestrictionJetPhiDistribution.Scale(1./pairedMediumRestrictionJetPhiDistribution.GetEntries())
pairedTightRestrictionJetPhiDistribution.Scale(1./pairedTightRestrictionJetPhiDistribution.GetEntries())
jetPhiDistribution.Draw("PE")
pairedNoRestrictionJetPhiDistribution.Draw("PE SAME")
pairedLooseRestrictionJetPhiDistribution.Draw("PE SAME")
pairedMediumRestrictionJetPhiDistribution.Draw("PE SAME")
pairedTightRestrictionJetPhiDistribution.Draw("PE SAME")

legJetPhi.Draw()

canvasJetPhi.Print("matchedJetPhiDistribution.png", "png")

#jetPhiDistribution.SetLineColor(1)
#pairedNoRestrictionJetPhiDistribution.SetLineColor(2)
#pairedLooseRestrictionJetPhiDistribution.SetLineColor(3)
#pairedTightRestrictionJetPhiDistribution.SetLineColor(4)
#jetPhiDistribution.Draw("HIST")
#pairedNoRestrictionJetPhiDistribution.Draw("HIST SAME")
#pairedLooseRestrictionJetPhiDistribution.Draw("HIST SAME")
#pairedTightRestrictionJetPhiDistribution.Draw("HIST SAME")

###############################################################################
# DELTA R
###############################################################################

canvasDeltaR = TCanvas()

deltaRNoRestrictionDistribution = muonFile.Get("deltaRNoRestrictionDistribution")
deltaRLooseRestrictionDistribution = muonFile.Get("deltaRLooseRestrictionDistribution")
deltaRMediumRestrictionDistribution = muonFile.Get("deltaRMediumRestrictionDistribution")
deltaRTightRestrictionDistribution = muonFile.Get("deltaRTightRestrictionDistribution")

deltaRNoRestrictionDistribution.SetMarkerColor(2)
deltaRLooseRestrictionDistribution.SetMarkerColor(3)
deltaRMediumRestrictionDistribution.SetMarkerColor(6)
deltaRTightRestrictionDistribution.SetMarkerColor(4)
deltaRNoRestrictionDistribution.SetMarkerStyle(21)
deltaRLooseRestrictionDistribution.SetMarkerStyle(21)
deltaRMediumRestrictionDistribution.SetMarkerStyle(21)
deltaRTightRestrictionDistribution.SetMarkerStyle(21)

deltaRNoRestrictionDistribution.SetStats(False)
deltaRLooseRestrictionDistribution.SetStats(False)
deltaRMediumRestrictionDistribution.SetStats(False)
deltaRTightRestrictionDistribution.SetStats(False)

deltaRNoRestrictionDistribution.Draw("PE")
deltaRLooseRestrictionDistribution.Draw("PE SAME")
deltaRMediumRestrictionDistribution.Draw("PE SAME")
deltaRTightRestrictionDistribution.Draw("PE SAME")

legDeltaR = TLegend(0.65,0.7,0.90,0.9)
legDeltaR.AddEntry(deltaRNoRestrictionDistribution,"#DeltaR_{max}=15","p")
legDeltaR.AddEntry(deltaRLooseRestrictionDistribution,"#DeltaR_{max}=3","p")
legDeltaR.AddEntry(deltaRMediumRestrictionDistribution,"#DeltaR_{max}=1.5","p")
legDeltaR.AddEntry(deltaRTightRestrictionDistribution,"#DeltaR_{max}=0.5","p")
legDeltaR.Draw()

canvasDeltaR.Print("deltaRDistribution.png", "png")