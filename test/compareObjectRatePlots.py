'''
  Receives a ROOT file with trigger rates as an argument and creates plots where rates from objects and from jet are compared
'''

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
jetRatePlot = triggerRatesFile.Get("jetTriggerRate")
jetToMuonRatePlot = triggerRatesFile.Get("jetToMuonTriggerRate")
jetToElectronRatePlot = triggerRatesFile.Get("jetToElectronTriggerRate")
jetToPhotonRatePlot = triggerRatesFile.Get("jetToPhotonTriggerRate")
jetToMETRatePlot = triggerRatesFile.Get("jetToMETTriggerRate")

# Setting colours 
# Black
jetRatePlot.SetLineColor(1)
muonRatePlot.SetLineColor(1)
electronRatePlot.SetLineColor(1)
photonRatePlot.SetLineColor(1)
metRatePlot.SetLineColor(1)
# Red
jetToMuonRatePlot.SetLineColor(2)
jetToElectronRatePlot.SetLineColor(2)
jetToPhotonRatePlot.SetLineColor(2)
jetToMETRatePlot.SetLineColor(2)


# Adding a legend

electronCompareCanvas = TCanvas("electronCompareCanvas", "canvas")
electronCompareCanvas.SetLogy(True)
muonCompareCanvas = TCanvas("muonCompareCanvas", "canvas")
muonCompareCanvas.SetLogy(True)
photonCompareCanvas = TCanvas("photonCompareCanvas", "canvas")
photonCompareCanvas.SetLogy(True)
metCompareCanvas = TCanvas("metCompareCanvas", "canvas")
metCompareCanvas.SetLogy(True)


electronCompareLegend = TLegend(0.7,0.7,0.48,0.9)
electronCompareLegend.SetHeader("Single electron rates")
electronCompareLegend.AddEntry(electronRatePlot,"Electron objects","l")
electronCompareLegend.AddEntry(jetToElectronRatePlot,"Electrons from jets","l")

muonCompareLegend = TLegend(0.7,0.7,0.48,0.9)
muonCompareLegend.SetHeader("Single muon rates")
muonCompareLegend.AddEntry(muonRatePlot,"Muon objects","l")
muonCompareLegend.AddEntry(jetToMuonRatePlot,"Muons from jets","l")

photonCompareLegend = TLegend(0.7,0.7,0.48,0.9)
photonCompareLegend.SetHeader("Single photon rates")
photonCompareLegend.AddEntry(photonRatePlot,"Photon objects","l")
photonCompareLegend.AddEntry(jetToPhotonRatePlot,"Photons from jets","l")

metCompareLegend = TLegend(0.7,0.7,0.48,0.9)
metCompareLegend.SetHeader("Single MET rates")
metCompareLegend.AddEntry(metRatePlot,"MET objects","l")
metCompareLegend.AddEntry(jetToMETRatePlot,"MET from jets","l")

electronCompareCanvas.cd()
electronRatePlot.GetYaxis().SetRangeUser(1e4, 1e10)
electronRatePlot.Draw("")
jetToElectronRatePlot.Draw("SAME")
electronCompareLegend.Draw()
electronCompareCanvas.Update()
electronCompareCanvas.Print("electronRates.svg", "svg")

muonCompareCanvas.cd()
muonRatePlot.GetYaxis().SetRangeUser(1e4, 1e10)
muonRatePlot.Draw("")
jetToMuonRatePlot.Draw("SAME")
muonCompareLegend.Draw()
muonCompareCanvas.Update()
muonCompareCanvas.Draw()
muonCompareCanvas.Print("muonRates.svg", "svg")

photonCompareCanvas.cd()
photonRatePlot.GetYaxis().SetRangeUser(1e4, 1e10)
photonRatePlot.Draw("")
jetToPhotonRatePlot.Draw("SAME")
photonCompareLegend.Draw()
photonCompareCanvas.Update()
photonCompareCanvas.Draw()
photonCompareCanvas.Print("photonRates.svg", "svg")

metCompareCanvas.cd()
metRatePlot.GetYaxis().SetRangeUser(1e4, 1e10)
metRatePlot.Draw("")
jetToMETRatePlot.Draw("SAME")
metCompareLegend.Draw()
metCompareCanvas.Update()
metCompareCanvas.Draw()
metCompareCanvas.Print("metRates.svg", "svg")

#xMax = jetRatePlot.GetXaxis().GetXmax()
#xMin = jetRatePlot.GetXaxis().GetXmin()
#
#line = TLine(xMin, 1e6, xMax, 1e6)
#line.SetLineColor(46)
#line.Draw()
#
#canvas.Update()
#canvas.Draw()

raw_input()