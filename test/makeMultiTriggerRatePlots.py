from ROOT import TFile
from ROOT import TMultiGraph
from ROOT import TGraph
from ROOT import TLegend
from ROOT import TCanvas
from ROOT import gStyle
from ROOT import TLine

import sys

gStyle.SetOptStat(0)

# Opening TFile

triggerRatesFile = TFile(sys.argv[1])

# Loading histograms
jetRatePlot = triggerRatesFile.Get("jetTriggerRate")
muonRatePlot = triggerRatesFile.Get("muonTriggerRate")
electronRatePlot = triggerRatesFile.Get("electronTriggerRate")
photonRatePlot = triggerRatesFile.Get("photonTriggerRate")
metRatePlot = triggerRatesFile.Get("metTriggerRate")

# Setting colours 
# Black
jetRatePlot.SetLineColor(1)
# Red
muonRatePlot.SetLineColor(2)
# Green
electronRatePlot.SetLineColor(3)
# Blue
photonRatePlot.SetLineColor(4)
# Purple
metRatePlot.SetLineColor(6)

# Adding a legend

canvas = TCanvas("c1", "canvas")
canvas.SetLogy(True)

leg = TLegend(0.7,0.7,0.48,0.9)
leg.SetHeader("Single object rates")
leg.AddEntry(jetRatePlot,"Jets","l")
leg.AddEntry(muonRatePlot,"Muons","l")
leg.AddEntry(electronRatePlot,"Electrons","l")
leg.AddEntry(photonRatePlot,"Photons","l")
leg.AddEntry(metRatePlot,"MET","l")

jetRatePlot.Draw()
muonRatePlot.Draw("SAME")
electronRatePlot.Draw("SAME")
photonRatePlot.Draw("SAME")
metRatePlot.Draw("SAME")
leg.Draw()

xMax = jetRatePlot.GetXaxis().GetXmax()
xMin = jetRatePlot.GetXaxis().GetXmin()

line = TLine(xMin, 1e6, xMax, 1e6)
line.SetLineColor(46)
line.Draw()

canvas.Update()
canvas.Draw()

raw_input()