'''Applies scaling factors to jet rate plots to obtain rate plots for other objects
A plot containing the efficiency vs pt is needed in input, in a file.
'''

print "Dealing with imports"

from ROOT import TFile
from ROOT import TLatex
from ROOT import TLine
from ROOT import TH1F
from ROOT import TCanvas
from ROOT import TGraph
from ROOT import TLegend
from ROOT import TMultiGraph

print "Loading stuff"

minBias_500kevents_ratePlots = TFile("minBias_500kevents/minBias/ratePlots.root")
DelphesSim_ff_H_WW_enuenu_1000events_efficiency_file = TFile("DelphesSim_ff_H_WW_enuenu_1000events/METEfficiency/efficiency.root")
DelphesSim_ff_H_WW_munumunu_1000events_efficiency_file = TFile("DelphesSim_ff_H_WW_munumunu_1000events/METEfficiency/efficiency.root")
DelphesSim_ff_W_enu_1000events_efficiency_file = TFile("DelphesSim_ff_W_enu_1000events/METEfficiency/efficiency.root")
DelphesSim_ff_W_munu_1000events_efficiency_file = TFile("DelphesSim_ff_W_munu_1000events/METEfficiency/efficiency.root")

metEfficiencyFile = TFile("metTriggerEfficiencies.root", "RECREATE")

minBias_500kevents_ratePlots_jetTriggerRate = minBias_500kevents_ratePlots.Get("jetTriggerRate")

jetToMETTriggerRate = TH1F(
                           "jetToMETTriggerRate",
                           "MET trigger rate from jets",
                           minBias_500kevents_ratePlots_jetTriggerRate.GetNbinsX(),
                           minBias_500kevents_ratePlots_jetTriggerRate.GetXaxis().GetXmin(),
                           minBias_500kevents_ratePlots_jetTriggerRate.GetXaxis().GetXmax()
                         )

jet_to_MET_scale = []
jet_to_MET_scale.append(1)
jet_to_MET_scale.append(5.50E-01)
jet_to_MET_scale.append(1.55E-01)
jet_to_MET_scale.append(9.20E-02)
jet_to_MET_scale.append(6.29E-02)
jet_to_MET_scale.append(3.29E-02)
jet_to_MET_scale.append(3.29E-02)
jet_to_MET_scale.append(3.68E-02)
jet_to_MET_scale.append(5.37E-02)
jet_to_MET_scale.append(5.44E-02)
jet_to_MET_scale.append(6.01E-02)
jet_to_MET_scale.append(6.59E-02)
jet_to_MET_scale.append(7.16E-02)
jet_to_MET_scale.append(7.74E-02)
jet_to_MET_scale.append(8.31E-02)

canvas = TCanvas("canvas", "canvas", 1024, 1024)
canvas.SetGridx()
canvas.SetGridy()
canvas.SetLogy()

metToRate = []

print "Building rate vs MET plot"

for x in xrange(0, len(jet_to_MET_scale)):
  rate = minBias_500kevents_ratePlots_jetTriggerRate.GetBinContent(x+1)*jet_to_MET_scale[x]
  jetToMETTriggerRate.SetBinContent(x+1, rate)
  metToRate.append(rate)
  print x*10, ":", minBias_500kevents_ratePlots_jetTriggerRate.GetBinContent(x+1)*jet_to_MET_scale[x]

jetToMETTriggerRate.Draw("")
canvas.Update()
canvas.Print("jetToMETTriggerRate.svg", "svg")

metToRate[0] = 0

print "Retrieving efficiency vs MET plot"
print "Building efficiency vs rate plots"

canvas.SetLogx(0)
canvas.SetLogy(0)
metTriggerEfficiency_ff_H_WW_enuenu_1000events = DelphesSim_ff_H_WW_enuenu_1000events_efficiency_file.Get("metTriggerEfficiency")
metTriggerEfficiency_ff_H_WW_enuenu_1000events.Draw("")
metTriggerEfficiency_ff_H_WW_enuenu_1000events.GetXaxis().SetTitle("pt [GeV]")
metTriggerEfficiency_ff_H_WW_enuenu_1000events.GetYaxis().SetTitle("Efficiency")
canvas.Update()
canvas.Draw()
canvas.Print("metTriggerEfficiency_ff_H_WW_enuenu_1000events.svg", "svg")

label_20GeV = TLatex(metToRate[2], 1.01, "20 GeV")
label_20GeV.SetTextSize(0.04)
line_20GeV = TLine(metToRate[2], 0, metToRate[2], 1)
line_20GeV.SetLineColor(2)

canvas.SetLogx(1)
canvas.SetLogy(0)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events = TGraph(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetPoint(x - 1, metToRate[x], metTriggerEfficiency_ff_H_WW_enuenu_1000events.GetBinContent(metTriggerEfficiency_ff_H_WW_enuenu_1000events.GetXaxis().FindBin(x*10)))
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetTitle("ff_H_WW_enuenu_1000events")
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetName("efficiencyPlotWithRate_ff_H_WW_enuenu_1000events")
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.Draw("AP")
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.Write()
line_20GeV.Draw()
label_20GeV.Draw()
canvas.Update()
canvas.Print("metEfficiencyPlotWithRate_ff_H_WW_enuenu_1000events.svg", "svg")

canvas.SetLogx(0)
canvas.SetLogy(0)
metTriggerEfficiency_ff_H_WW_munumunu_1000events = DelphesSim_ff_H_WW_munumunu_1000events_efficiency_file.Get("metTriggerEfficiency")
metTriggerEfficiency_ff_H_WW_munumunu_1000events.Draw("")
metTriggerEfficiency_ff_H_WW_munumunu_1000events.GetXaxis().SetTitle("pt [GeV]")
metTriggerEfficiency_ff_H_WW_munumunu_1000events.GetYaxis().SetTitle("Efficiency")
canvas.Update()
canvas.Draw()
canvas.Print("metTriggerEfficiency_ff_H_WW_munumunu_1000events.svg", "svg")

canvas.SetLogx(1)
canvas.SetLogy(0)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events = TGraph(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetPoint(x - 1, metToRate[x], metTriggerEfficiency_ff_H_WW_munumunu_1000events.GetBinContent(metTriggerEfficiency_ff_H_WW_munumunu_1000events.GetXaxis().FindBin(x*10)))
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetTitle("ff_H_WW_munumunu_1000events")
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetName("efficiencyPlotWithRate_ff_H_WW_munumunu_1000events")
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.Draw("AP")
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.Write()
line_20GeV.Draw()
label_20GeV.Draw()
canvas.Update()
canvas.Print("metEfficiencyPlotWithRate_ff_H_WW_munumunu_1000events.svg", "svg")

canvas.SetLogx(0)
canvas.SetLogy(0)
metTriggerEfficiency_ff_W_enu_1000events = DelphesSim_ff_W_enu_1000events_efficiency_file.Get("metTriggerEfficiency")
metTriggerEfficiency_ff_W_enu_1000events.Draw("")
metTriggerEfficiency_ff_W_enu_1000events.GetXaxis().SetTitle("pt [GeV]")
metTriggerEfficiency_ff_W_enu_1000events.GetYaxis().SetTitle("Efficiency")
canvas.Update()
canvas.Draw()
canvas.Print("metTriggerEfficiency_ff_W_enu_1000events.svg", "svg")

canvas.SetLogx(1)
canvas.SetLogy(0)
efficiencyPlotWithRate_ff_W_enu_1000events = TGraph(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_W_enu_1000events.SetPoint(x - 1, metToRate[x], metTriggerEfficiency_ff_W_enu_1000events.GetBinContent(metTriggerEfficiency_ff_W_enu_1000events.GetXaxis().FindBin(x*10)))
efficiencyPlotWithRate_ff_W_enu_1000events.SetTitle("ff_W_enu_1000events")
efficiencyPlotWithRate_ff_W_enu_1000events.SetName("efficiencyPlotWithRate_ff_W_enu_1000events")
efficiencyPlotWithRate_ff_W_enu_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlotWithRate_ff_W_enu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_W_enu_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_W_enu_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_W_enu_1000events.Draw("AP")
efficiencyPlotWithRate_ff_W_enu_1000events.Write()
line_20GeV.Draw()
label_20GeV.Draw()
canvas.Update()
canvas.Print("metEfficiencyPlotWithRate_ff_W_enu_1000events.svg", "svg")

canvas.SetLogx(0)
canvas.SetLogy(0)
metTriggerEfficiency_ff_W_munu_1000events = DelphesSim_ff_W_munu_1000events_efficiency_file.Get("metTriggerEfficiency")
metTriggerEfficiency_ff_W_munu_1000events.Draw("")
metTriggerEfficiency_ff_W_munu_1000events.GetXaxis().SetTitle("pt [GeV]")
metTriggerEfficiency_ff_W_munu_1000events.GetYaxis().SetTitle("Efficiency")
canvas.Update()
canvas.Draw()
canvas.Print("metTriggerEfficiency_ff_W_munu_1000events.svg", "svg")

canvas.SetLogx(1)
canvas.SetLogy(0)
efficiencyPlotWithRate_ff_W_munu_1000events = TGraph(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_W_munu_1000events.SetPoint(x - 1, metToRate[x], metTriggerEfficiency_ff_W_munu_1000events.GetBinContent(metTriggerEfficiency_ff_W_munu_1000events.GetXaxis().FindBin(x*10)))
efficiencyPlotWithRate_ff_W_munu_1000events.SetTitle("ff_W_munu_1000events")
efficiencyPlotWithRate_ff_W_munu_1000events.SetName("efficiencyPlotWithRate_ff_W_munu_1000events")
efficiencyPlotWithRate_ff_W_munu_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlotWithRate_ff_W_munu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_W_munu_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_W_munu_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_W_munu_1000events.Draw("AP")
efficiencyPlotWithRate_ff_W_munu_1000events.Write()
line_20GeV.Draw()
label_20GeV.Draw()
canvas.Update()
canvas.Print("metEfficiencyPlotWithRate_ff_W_munu_1000events.svg", "svg")

metEfficiencyPlotWithRate = TMultiGraph("metEfficiencyPlotWithRate", "EW events collection efficiency vs MET trigger rate")
metEfficiencyPlotWithRate.Add(efficiencyPlotWithRate_ff_H_WW_enuenu_1000events)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetMarkerColor(6)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetLineColor(0)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetFillColor(0)
metEfficiencyPlotWithRate.Add(efficiencyPlotWithRate_ff_H_WW_munumunu_1000events)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetMarkerColor(2)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetLineColor(0)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetFillColor(0)
metEfficiencyPlotWithRate.Add(efficiencyPlotWithRate_ff_W_enu_1000events)
efficiencyPlotWithRate_ff_W_enu_1000events.SetMarkerColor(3)
efficiencyPlotWithRate_ff_W_enu_1000events.SetLineColor(0)
efficiencyPlotWithRate_ff_W_enu_1000events.SetFillColor(0)
metEfficiencyPlotWithRate.Add(efficiencyPlotWithRate_ff_W_munu_1000events)
efficiencyPlotWithRate_ff_W_munu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_W_munu_1000events.SetLineColor(0)
efficiencyPlotWithRate_ff_W_munu_1000events.SetFillColor(0)
metEfficiencyPlotWithRate.Draw("AP")
metEfficiencyPlotWithRate.GetXaxis().SetTitle("Rate [Hz]")
metEfficiencyPlotWithRate.GetYaxis().SetTitle("Efficiency")
line_20GeV.Draw()
label_20GeV.Draw()
canvas.BuildLegend(0.6, 0.35, 0.9, 0.15)
canvas.Update()
canvas.Print("metEfficiencyPlotWithRate.svg", "svg")

metEfficiencyFile.Write()
metEfficiencyFile.Close()

raw_input()