from ROOT import TMultiGraph
from ROOT import TGraphErrors
from ROOT import TLegend
from ROOT import TCanvas
from ROOT import gStyle

jetToElectronRatioGraph = TGraphErrors("jetToElectronFactors.dat", "%lg %lg %lg %lg")
jetToMuonRatioGraph = TGraphErrors("jetToMuonFactors.dat", "%lg %lg %lg %lg")
jetToMETRatioGraph = TGraphErrors("jetToMETFactors.dat", "%lg %lg %lg %lg")

jetToElectronRatioGraph.SetMarkerColor(2)
jetToElectronRatioGraph.SetMarkerStyle(21)
jetToMuonRatioGraph.SetMarkerColor(3)
jetToMuonRatioGraph.SetMarkerStyle(21)
jetToMETRatioGraph.SetMarkerColor(4)
jetToMETRatioGraph.SetMarkerStyle(21)

jetToElectronRatioGraph.SetFillStyle(1001)
jetToElectronRatioGraph.SetFillColor(2)
jetToMuonRatioGraph.SetFillStyle(1001)
jetToMuonRatioGraph.SetFillColor(3)
jetToMETRatioGraph.SetFillStyle(1001)
jetToMETRatioGraph.SetFillColor(4)


jetToObjectRatioGraphs = TMultiGraph()

jetToObjectRatioGraphs.Add(jetToElectronRatioGraph, "")
jetToObjectRatioGraphs.Add(jetToMuonRatioGraph, "")
jetToObjectRatioGraphs.Add(jetToMETRatioGraph, "")

canvas = TCanvas()
canvas.SetGrid()
canvas.SetLogy()

jetToObjectRatioGraphs.SetTitle("Jet rejection factors")

legend = TLegend(0.70,0.80,0.98,0.98)
legend.SetHeader("Object type")
legend.AddEntry(jetToMETRatioGraph,"MET","P")
legend.AddEntry(jetToElectronRatioGraph,"Electrons","P")
legend.AddEntry(jetToMuonRatioGraph,"Muons","P")

jetToObjectRatioGraphs.Draw("AP")
legend.Draw()

jetToObjectRatioGraphs.GetXaxis().SetTitle("p_{t} [GeV]")
jetToObjectRatioGraphs.GetXaxis().SetTitleOffset(1.2)
jetToObjectRatioGraphs.GetYaxis().SetTitleOffset(1.2)
jetToObjectRatioGraphs.GetYaxis().SetRangeUser(1e-5, 1)
jetToObjectRatioGraphs.GetXaxis().SetRangeUser(10, 140)
jetToObjectRatioGraphs.GetYaxis().SetTitle("#frac{Object rate}{Jet rate}")

canvas.Print("jetToObjectRatios.svg", "svg")
canvas.Print("jetToObjectRatios.png", "png")
canvas.Print("jetToObjectRatios.pdf", "pdf")
