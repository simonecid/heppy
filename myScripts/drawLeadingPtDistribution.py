from ROOT import TFile
from ROOT import TLatex
from ROOT import TH1I
from ROOT import TH1F
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TGraph
from ROOT import TGraphErrors
from math import sqrt
from ROOT import TMultiGraph
from ROOT import TLine
from ROOT import TPaveText

distributionFile = TFile("DelphesSim_ff_W_enu_1000events/EWProductionAndHiggs/distributions.root")

canvas = TCanvas()
canvas.SetLogy()

leadingRecoPtDistribution = distributionFile.Get("electronLeadingRecoPtDistribution")
leadingRecoPtDistribution.SetTitle("Electron leading p_{t} distribution in W #rightarrow e#nu_{e}")
leadingRecoPtDistribution.SetStats(0)
leadingRecoPtDistribution.GetXaxis().SetRangeUser(0, 150)
leadingRecoPtDistribution.GetXaxis().SetTitle("p_{t} [GeV]")
leadingRecoPtDistribution.GetYaxis().SetTitle("Number of events")
leadingRecoPtDistribution.GetXaxis().SetTitleOffset(1.2)
leadingRecoPtDistribution.GetYaxis().SetTitleOffset(1.2)
leadingRecoPtDistribution.SetMarkerStyle(21)
leadingRecoPtDistribution.SetMarkerColor(4)
leadingRecoPtDistribution.SetLineColor(1)

leadingRecoPtDistribution.Draw("PE")

# Lumi and energy info
text = TPaveText(0.5, 0.84, 0.9, 0.9, "NDC")
text.AddText("L_{inst} = 5 #times 10^{34} cm^{-2} s^{-1}   #sqrt{s} = 100 TeV")
text.Draw()

canvas.Print("leadingRecoPtDistribution.svg", "svg")
canvas.Print("leadingRecoPtDistribution.pdf", "pdf")
canvas.Print("leadingRecoPtDistribution.png", "png")