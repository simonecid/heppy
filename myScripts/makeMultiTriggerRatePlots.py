'''
  Receives a ROOT file with trigger rates as an argument and plots them altogether
'''

from ROOT import TFile
from ROOT import TMultiGraph
from ROOT import TGraphErrors
from ROOT import TLegend
from ROOT import TCanvas
from ROOT import gStyle
from ROOT import TLine
from ROOT import TPaveText

import sys

gStyle.SetOptStat(0)

mySettings = lambda a: None
'''Pile up level for that kind of event'''
mySettings.pileup = 180 # FCC
#mySettings.pileup = 40 # LHC
mySettings.yScale = 1e6
'''Cross section of the event in mb'''
mySettings.crossSection = 100 # FCC
#mySettings.crossSection = 60 # LHC
'''Instantaneous lumi in cm^-2 s^-1'''
mySettings.instantaneousLuminosity = 5e34 # FCC
#mySettings.instantaneousLuminosity = 1.15e34 # LHC

# Opening TFile

triggerRatesFile = TFile(sys.argv[1])

# Loading histograms
jetRatePlot_Histo = triggerRatesFile.Get("jetTriggerRate")
jetRatePlot = TGraphErrors(jetRatePlot_Histo)
jetToMuonRatePlot_Histo = triggerRatesFile.Get("jetToMuonTriggerRate")
jetToMuonRatePlot = TGraphErrors(jetToMuonRatePlot_Histo)
jetToElectronRatePlot_Histo = triggerRatesFile.Get("jetToElectronTriggerRate")
jetToElectronRatePlot = TGraphErrors(jetToElectronRatePlot_Histo)
# jetToPhotonRatePlot_Histo = triggerRatesFile.Get("photonTriggerRate")
# jetToPhotonRatePlot = TGraphErrors(#_Histo)
jetToMETRatePlot_Histo = triggerRatesFile.Get("jetToMETTriggerRate")
jetToMETRatePlot = TGraphErrors(jetToMETRatePlot_Histo)

# Setting up error bars

jetRatePlot.SetPointError(0, 5, 7071067)
jetRatePlot.SetPointError(1, 5, 1702321)
jetRatePlot.SetPointError(2, 5, 1702321)
jetRatePlot.SetPointError(3, 5, 1702321)
jetRatePlot.SetPointError(4, 5, 1074011)
jetRatePlot.SetPointError(5, 5, 724292)
jetRatePlot.SetPointError(6, 5, 518844)
jetRatePlot.SetPointError(7, 5, 391024)
jetRatePlot.SetPointError(8, 5, 308382)
jetRatePlot.SetPointError(9, 5, 25000)
jetRatePlot.SetPointError(10, 5, 206155)
jetRatePlot.SetPointError(11, 5, 178605)
jetRatePlot.SetPointError(12, 5, 15000)
jetRatePlot.SetPointError(13, 5, 126885)
jetRatePlot.SetPointError(14, 5, 113578)
jetRatePlot.SetPointError(15, 5, 96436)
jetRatePlot.SetPointError(16, 5, 82462)
jetRatePlot.SetPointError(17, 5, 71414)
jetRatePlot.SetPointError(18, 5, 62449)
jetRatePlot.SetPointError(19, 5, 59160)
jetRatePlot.SetPointError(20, 5, 57445)
jetRatePlot.SetPointError(21, 5, 51961)
jetRatePlot.SetPointError(22, 5, 5000)
jetRatePlot.SetPointError(23, 5, 42426)
jetRatePlot.SetPointError(24, 5, 4000)
jetRatePlot.SetPointError(25, 5, 38729)
jetRatePlot.SetPointError(26, 5, 36055)
jetRatePlot.SetPointError(27, 5, 33166)
jetRatePlot.SetPointError(28, 5, 33166)

ratePlot = TMultiGraph()

# Setting colours 
# Black
jetRatePlot.SetLineColor(1)
# Red
jetToMuonRatePlot.SetLineColor(2)
# Green
jetToElectronRatePlot.SetLineColor(3)
# Blue
jetToMETRatePlot.SetLineColor(4)

# Adding a legend

canvas = TCanvas("c1", "canvas")
canvas.SetLogy(True)

leg = TLegend(0.65,0.7,0.90,0.9)
leg.SetHeader("Single object rates")
leg.AddEntry(jetRatePlot,"Jets","l")
leg.AddEntry(jetToMETRatePlot,"MET","l")
leg.AddEntry(jetToElectronRatePlot,"Electrons","l")
leg.AddEntry(jetToMuonRatePlot,"Muons","l")

## Removing stat info
#jetRatePlot.SetStats(False)
#jetToMuonRatePlot.SetStats(False)
#jetToElectronRatePlot.SetStats(False)
## jetToPhotonRatePlot.SetStats(False)
#jetToMETRatePlot.SetStats(False)

# Plotting stuff
ratePlot.Add(jetRatePlot, "AP")
ratePlot.Add(jetToMuonRatePlot, "AP")
ratePlot.Add(jetToElectronRatePlot, "AP")
# ratePlot.Add(jetToPhotonRatePlot, "AP")
ratePlot.Add(jetToMETRatePlot, "AP")
ratePlot.Draw("AP")
leg.Draw()

# Plot ranges
ratePlot.GetYaxis().SetRangeUser(1e2, 1e10)
ratePlot.GetXaxis().SetRangeUser(0, 150)

# Lumi and energy info
text = TPaveText(0.2, 0.83, 0.64, 0.9, "NDC")
text.AddText("L_{inst} = 5 #times 10^{34} cm^{-2} s^{-1} - #sqrt{s} = 100 TeV")
text.Draw()

# Plot labels
ratePlot.SetTitle("Object rate simulation")
ratePlot.GetXaxis().SetTitle("p_{t} [GeV]")
ratePlot.GetYaxis().SetTitle("Rate [Hz]")

# Adding a reference line at 1 MHz

mhzLine = TLine(0, mySettings.yScale, 150, mySettings.yScale)
mhzLine.SetLineColor(2)
mhzLine.SetLineStyle(2)
mhzLine.Draw()

canvas.Update()
canvas.Draw()