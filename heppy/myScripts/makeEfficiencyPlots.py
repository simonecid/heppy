'''Build efficiency plots starting from the distributions in output from the particleInfoPlotter heppy script.
'''

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

class ParticleDistributionsFromDelphes(object):

  def __init__(self, fileName):
    self.fileName = fileName
    self.rootFile = TFile(self.fileName)

    self.electronRecoPtDistribution = self.rootFile.Get("electronRecoPtDistribution")
    self.electronLeadingRecoPtDistribution = self.rootFile.Get("electronLeadingRecoPtDistribution")
    self.electronLeadingRecoEtaDistribution = self.rootFile.Get("electronLeadingRecoEtaDistribution")
    self.electronGenPtDistribution = self.rootFile.Get("electronGenPtDistribution")
    self.muonRecoPtDistribution = self.rootFile.Get("muonRecoPtDistribution")
    self.muonLeadingRecoPtDistribution = self.rootFile.Get("muonLeadingRecoPtDistribution")
    self.muonLeadingRecoEtaDistribution = self.rootFile.Get("muonLeadingRecoEtaDistribution")
    self.muonGenPtDistribution = self.rootFile.Get("muonGenPtDistribution")
    self.tauGenPtDistribution = self.rootFile.Get("tauGenPtDistribution")
    self.photonRecoPtDistribution = self.rootFile.Get("photonRecoPtDistribution")
    self.photonLeadingRecoPtDistribution = self.rootFile.Get("photonLeadingRecoPtDistribution")
    self.photonLeadingRecoEtaDistribution = self.rootFile.Get("photonLeadingRecoEtaDistribution")
    self.photonGenPtDistribution = self.rootFile.Get("photonGenPtDistribution")
    self.jetRecoPtDistribution = self.rootFile.Get("jetRecoPtDistribution")
    self.jetLeadingRecoPtDistribution = self.rootFile.Get("jetLeadingRecoPtDistribution")
    self.jetLeadingRecoEtaDistribution = self.rootFile.Get("jetLeadingRecoEtaDistribution")
    self.jetGenPtDistribution = self.rootFile.Get("jetGenPtDistribution")


class HiggsParticleDistributionsPythia(object):

  def __init__(self, fileName):
    self.fileName = fileName
    self.rootFile = TFile(self.fileName)

    self.higgsPtHisto = self.rootFile.Get("higgsPtHisto")
    self.ewBosonPtHisto = self.rootFile.Get("ewBosonPtHisto")
    self.ewBosonLeadingPtHisto = self.rootFile.Get("ewBosonLeadingPtHisto")
    self.ewBosonSubLeadingPtHisto = self.rootFile.Get("ewBosonSubLeadingPtHisto")
    self.chargedLeptonPtHisto = self.rootFile.Get("chargedLeptonPtHisto")
    self.neutralLeptonPtHisto = self.rootFile.Get("neutralLeptonPtHisto")
    self.ewBoson1PtHisto = self.rootFile.Get("ewBoson1PtHisto")
    self.ewBoson2PtHisto = self.rootFile.Get("ewBoson2PtHisto")
    self.lepton1PtHisto = self.rootFile.Get("lepton1PtHisto")
    self.lepton2PtHisto = self.rootFile.Get("lepton2PtHisto")
    self.lepton3PtHisto = self.rootFile.Get("lepton3PtHisto")
    self.lepton4PtHisto = self.rootFile.Get("lepton4PtHisto")
    self.leadingChargedLeptonPtHisto = self.rootFile.Get("leadingChargedLeptonPtHisto")
    self.chargedLeptonLeadingEtaHisto = self.rootFile.Get("chargedLeptonLeadingEtaHisto")
    self.higgsEtaHisto = self.rootFile.Get("higgsEtaHisto")
    self.ewBosonEtaHisto = self.rootFile.Get("ewBosonEtaHisto")
    self.chargedLeptonEtaHisto = self.rootFile.Get("chargedLeptonEtaHisto")
    self.higgsPhiHisto = self.rootFile.Get("higgsPhiHisto")
    self.ewBosonPhiHisto = self.rootFile.Get("ewBosonPhiHisto")
    self.chargedLeptonPhiHisto = self.rootFile.Get("chargedLeptonPhiHisto")

class ResonanceParticleDistributionsPythia(object):

  def __init__(self, fileName):
    self.fileName = fileName
    self.rootFile = TFile(self.fileName)

    self.resonancePtHisto = self.rootFile.Get("resonancePtHisto")
    self.decayPtHisto = self.rootFile.Get("decayPtHisto")
    self.decayLeadingPtHisto = self.rootFile.Get("decayLeadingPtHisto")
    self.decaySubLeadingPtHisto = self.rootFile.Get("decaySubLeadingPtHisto")
    self.decay1PtHisto = self.rootFile.Get("decay1PtHisto")
    self.decay2PtHisto = self.rootFile.Get("decay2PtHisto")
    self.resonanceEtaHisto = self.rootFile.Get("resonanceEtaHisto")
    self.decayEtaHisto = self.rootFile.Get("decayEtaHisto")
    self.decayLeadingEtaHisto = self.rootFile.Get("decayLeadingEtaHisto")
    self.higgsPhiHisto = self.rootFile.Get("higgsPhiHisto")
    self.resonancePhiHisto = self.rootFile.Get("resonancePhiHisto")
    self.decayPhiHisto = self.rootFile.Get("decayPhiHisto")


delphesSim_ff_H_WW_enuenu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_H_WW_enuenu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_H_WW_munumunu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_H_WW_munumunu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_H_ZZ_eeee_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_H_ZZ_eeee_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_H_ZZ_mumumumu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_H_ZZ_mumumumu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_W_enu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_W_enu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_W_munu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_W_munu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_Z_ee_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_Z_ee_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_Z_mumu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_Z_mumu_1000events/EWProductionAndHiggs/distributions.root")

pythia_ff_H_WW_enuenu_1000events = HiggsParticleDistributionsPythia("../pythia8223/pythia-FCC/ff_H_WW_enuenu_1000events/ff_H_WW_enuenu_1000events_plots.root")
pythia_ff_H_WW_munumunu_1000events = HiggsParticleDistributionsPythia("../pythia8223/pythia-FCC/ff_H_WW_munumunu_1000events/ff_H_WW_munumunu_1000events_plots.root")
pythia_ff_H_ZZ_eeee_1000events = HiggsParticleDistributionsPythia("../pythia8223/pythia-FCC/ff_H_ZZ_eeee_1000events/ff_H_ZZ_eeee_1000events_plots.root")
pythia_ff_H_ZZ_mumumumu_1000events = HiggsParticleDistributionsPythia("../pythia8223/pythia-FCC/ff_H_ZZ_mumumumu_1000events/ff_H_ZZ_mumumumu_1000events_plots.root")
pythia_ff_W_enu_1000events = ResonanceParticleDistributionsPythia("../pythia8223/pythia-FCC/ff_W_enu_1000events/ff_W_enu_1000events_plots.root")
pythia_ff_W_munu_1000events = ResonanceParticleDistributionsPythia("../pythia8223/pythia-FCC/ff_W_munu_1000events/ff_W_munu_1000events_plots.root")
pythia_ff_Z_ee_1000events = ResonanceParticleDistributionsPythia("../pythia8223/pythia-FCC/ff_Z_ee_1000events/ff_Z_ee_1000events_plots.root")
pythia_ff_Z_mumu_1000events = ResonanceParticleDistributionsPythia("../pythia8223/pythia-FCC/ff_Z_mumu_1000events/ff_Z_mumu_1000events_plots.root")

canvas = TCanvas("canvas", "canvas", 600, 600)
canvas.SetGridx()
canvas.SetGridy()

# Lumi and energy info
text = TPaveText(0.35, 0.84, 0.75, 0.9, "NDC")
text.AddText("L_{inst} = 5 #times 10^{34} cm^{-2} s^{-1}   #sqrt{s} = 100 TeV")

# ======================================
# ========= BUILDING THE PLOTS =========
# ======================================

# Electrons in HH to WW
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_H_WW_enuenu_1000events = TGraphErrors(delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution)
efficiencyPlot_ff_H_WW_enuenu_1000events.SetTitle("H #rightarrow WW #rightarrow e#nu_{e}e#nu_{e} physics acceptance vs electron trigger threshold")
numberOfEntries_ff_H_WW_enuenu_1000events = delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetEntries()
xArr_ff_H_WW_enuenu_1000events = efficiencyPlot_ff_H_WW_enuenu_1000events.GetX()
efficiencyPlot_ff_H_WW_enuenu_1000events.SetPoint(0, xArr_ff_H_WW_enuenu_1000events[0], numberOfEntries_ff_H_WW_enuenu_1000events)
for binNumber_ff_H_WW_enuenu_1000events in xrange(1, len(xArr_ff_H_WW_enuenu_1000events)):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_H_WW_enuenu_1000events.SetPoint(
                                                        binNumber_ff_H_WW_enuenu_1000events,
                                                        xArr_ff_H_WW_enuenu_1000events[binNumber_ff_H_WW_enuenu_1000events],
                                                        (efficiencyPlot_ff_H_WW_enuenu_1000events.GetY()[binNumber_ff_H_WW_enuenu_1000events - 1] - delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetBinContent(binNumber_ff_H_WW_enuenu_1000events))
                                                    )
# Normalise to 1
for binNumber_ff_H_WW_enuenu_1000events in xrange(0, len(xArr_ff_H_WW_enuenu_1000events)):
  efficiencyPlot_ff_H_WW_enuenu_1000events.SetPoint(
                                                        binNumber_ff_H_WW_enuenu_1000events,
                                                        xArr_ff_H_WW_enuenu_1000events[binNumber_ff_H_WW_enuenu_1000events],
                                                        efficiencyPlot_ff_H_WW_enuenu_1000events.GetY()[binNumber_ff_H_WW_enuenu_1000events]/numberOfEntries_ff_H_WW_enuenu_1000events
                                                    )
  efficiencyPlot_ff_H_WW_enuenu_1000events.SetPointError(
                                                        binNumber_ff_H_WW_enuenu_1000events,
                                                        efficiencyPlot_ff_H_WW_enuenu_1000events.GetEX()[binNumber_ff_H_WW_enuenu_1000events],
                                                        sqrt(efficiencyPlot_ff_H_WW_enuenu_1000events.GetY()[binNumber_ff_H_WW_enuenu_1000events]/numberOfEntries_ff_H_WW_enuenu_1000events)
                                                    )
efficiencyPlot_ff_H_WW_enuenu_1000events.SetMarkerColor(4)  
efficiencyPlot_ff_H_WW_enuenu_1000events.SetMarkerStyle(21)
efficiencyPlot_ff_H_WW_enuenu_1000events.SetLineColor(1)
efficiencyPlot_ff_H_WW_enuenu_1000events.Draw("AP")
text.Draw()
efficiencyPlot_ff_H_WW_enuenu_1000events.GetXaxis().SetTitle("Threshold [GeV]")
efficiencyPlot_ff_H_WW_enuenu_1000events.GetXaxis().SetLimits(0, 150)
efficiencyPlot_ff_H_WW_enuenu_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlot_ff_H_WW_enuenu_1000events.GetYaxis().SetRangeUser(0, 1.1)
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_H_WW_enuenu_1000events.svg", "svg")
canvas.Print("efficiencyPlot_ff_H_WW_enuenu_1000events.png", "png")
canvas.Print("efficiencyPlot_ff_H_WW_enuenu_1000events.pdf", "pdf")

# Muons in HH to WW
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_H_WW_munumunu_1000events = TGraphErrors(delphesSim_ff_H_WW_munumunu_1000events.muonLeadingRecoPtDistribution)
efficiencyPlot_ff_H_WW_munumunu_1000events.SetTitle("H #rightarrow WW #rightarrow #mu#nu_{#mu}#mu#nu_{#mu} physics acceptance vs muon trigger threshold")
numberOfEntries_ff_H_WW_munumunu_1000events = delphesSim_ff_H_WW_munumunu_1000events.muonLeadingRecoPtDistribution.GetEntries()
xArr_ff_H_WW_munumunu_1000events = efficiencyPlot_ff_H_WW_munumunu_1000events.GetX()
efficiencyPlot_ff_H_WW_munumunu_1000events.SetPoint(0, xArr_ff_H_WW_munumunu_1000events[0], numberOfEntries_ff_H_WW_munumunu_1000events)
for binNumber_ff_H_WW_munumunu_1000events in xrange(1, len(xArr_ff_H_WW_munumunu_1000events)):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_H_WW_munumunu_1000events.SetPoint(
                                                        binNumber_ff_H_WW_munumunu_1000events,
                                                        xArr_ff_H_WW_munumunu_1000events[binNumber_ff_H_WW_munumunu_1000events],
                                                        (efficiencyPlot_ff_H_WW_munumunu_1000events.GetY()[binNumber_ff_H_WW_munumunu_1000events - 1] - delphesSim_ff_H_WW_munumunu_1000events.muonLeadingRecoPtDistribution.GetBinContent(binNumber_ff_H_WW_munumunu_1000events))
                                                    )
# Normalise to 1
for binNumber_ff_H_WW_munumunu_1000events in xrange(0, len(xArr_ff_H_WW_munumunu_1000events)):
  efficiencyPlot_ff_H_WW_munumunu_1000events.SetPoint(
                                                        binNumber_ff_H_WW_munumunu_1000events,
                                                        xArr_ff_H_WW_munumunu_1000events[binNumber_ff_H_WW_munumunu_1000events],
                                                        efficiencyPlot_ff_H_WW_munumunu_1000events.GetY()[binNumber_ff_H_WW_munumunu_1000events]/numberOfEntries_ff_H_WW_munumunu_1000events
                                                    )
  efficiencyPlot_ff_H_WW_munumunu_1000events.SetPointError(
                                                        binNumber_ff_H_WW_munumunu_1000events,
                                                        efficiencyPlot_ff_H_WW_munumunu_1000events.GetEX()[binNumber_ff_H_WW_munumunu_1000events],
                                                        sqrt(efficiencyPlot_ff_H_WW_munumunu_1000events.GetY()[binNumber_ff_H_WW_munumunu_1000events]/numberOfEntries_ff_H_WW_munumunu_1000events)
                                                    )
efficiencyPlot_ff_H_WW_munumunu_1000events.SetMarkerColor(4)  
efficiencyPlot_ff_H_WW_munumunu_1000events.SetMarkerStyle(21)
efficiencyPlot_ff_H_WW_munumunu_1000events.SetLineColor(1)
efficiencyPlot_ff_H_WW_munumunu_1000events.Draw("AP")
text.Draw()
efficiencyPlot_ff_H_WW_munumunu_1000events.GetXaxis().SetTitle("Threshold [GeV]")
efficiencyPlot_ff_H_WW_munumunu_1000events.GetXaxis().SetLimits(0, 150)
efficiencyPlot_ff_H_WW_munumunu_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlot_ff_H_WW_munumunu_1000events.GetYaxis().SetRangeUser(0, 1.1)
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_H_WW_munumunu_1000events.svg", "svg")
canvas.Print("efficiencyPlot_ff_H_WW_munumunu_1000events.png", "png")
canvas.Print("efficiencyPlot_ff_H_WW_munumunu_1000events.pdf", "pdf")

# Electrons in HH to ZZ
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_H_ZZ_eeee_1000events = TGraphErrors(delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution)
efficiencyPlot_ff_H_ZZ_eeee_1000events.SetTitle("H #rightarrow ZZ #rightarrow eeee physics acceptance vs electron trigger threshold")
numberOfEntries_ff_H_ZZ_eeee_1000events = delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetEntries()
xArr_ff_H_ZZ_eeee_1000events = efficiencyPlot_ff_H_ZZ_eeee_1000events.GetX()
efficiencyPlot_ff_H_ZZ_eeee_1000events.SetPoint(0, xArr_ff_H_ZZ_eeee_1000events[0], numberOfEntries_ff_H_ZZ_eeee_1000events)
for binNumber_ff_H_ZZ_eeee_1000events in xrange(1, len(xArr_ff_H_ZZ_eeee_1000events)):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_H_ZZ_eeee_1000events.SetPoint(
                                                        binNumber_ff_H_ZZ_eeee_1000events,
                                                        xArr_ff_H_ZZ_eeee_1000events[binNumber_ff_H_ZZ_eeee_1000events],
                                                        (efficiencyPlot_ff_H_ZZ_eeee_1000events.GetY()[binNumber_ff_H_ZZ_eeee_1000events - 1] - delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetBinContent(binNumber_ff_H_ZZ_eeee_1000events))
                                                    )
# Normalise to 1
for binNumber_ff_H_ZZ_eeee_1000events in xrange(0, len(xArr_ff_H_ZZ_eeee_1000events)):
  efficiencyPlot_ff_H_ZZ_eeee_1000events.SetPoint(
                                                        binNumber_ff_H_ZZ_eeee_1000events,
                                                        xArr_ff_H_ZZ_eeee_1000events[binNumber_ff_H_ZZ_eeee_1000events],
                                                        efficiencyPlot_ff_H_ZZ_eeee_1000events.GetY()[binNumber_ff_H_ZZ_eeee_1000events]/numberOfEntries_ff_H_ZZ_eeee_1000events
                                                    )
  efficiencyPlot_ff_H_ZZ_eeee_1000events.SetPointError(
                                                        binNumber_ff_H_ZZ_eeee_1000events,
                                                        efficiencyPlot_ff_H_ZZ_eeee_1000events.GetEX()[binNumber_ff_H_ZZ_eeee_1000events],
                                                        sqrt(efficiencyPlot_ff_H_ZZ_eeee_1000events.GetY()[binNumber_ff_H_ZZ_eeee_1000events]/numberOfEntries_ff_H_ZZ_eeee_1000events)
                                                    )
efficiencyPlot_ff_H_ZZ_eeee_1000events.SetMarkerColor(4)  
efficiencyPlot_ff_H_ZZ_eeee_1000events.SetMarkerStyle(21)
efficiencyPlot_ff_H_ZZ_eeee_1000events.SetLineColor(1)
efficiencyPlot_ff_H_ZZ_eeee_1000events.Draw("AP")
text.Draw()
efficiencyPlot_ff_H_ZZ_eeee_1000events.GetXaxis().SetTitle("Threshold [GeV]")
efficiencyPlot_ff_H_ZZ_eeee_1000events.GetXaxis().SetLimits(0, 150)
efficiencyPlot_ff_H_ZZ_eeee_1000events.GetXaxis().SetRangeUser(0, 150)
efficiencyPlot_ff_H_ZZ_eeee_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlot_ff_H_ZZ_eeee_1000events.GetYaxis().SetRangeUser(0, 1.1)
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_H_ZZ_eeee_1000events.svg", "svg")
canvas.Print("efficiencyPlot_ff_H_ZZ_eeee_1000events.png", "png")
canvas.Print("efficiencyPlot_ff_H_ZZ_eeee_1000events.pdf", "pdf")

# Muons in HH to ZZ
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_H_ZZ_mumumumu_1000events = TGraphErrors(delphesSim_ff_H_ZZ_mumumumu_1000events.muonLeadingRecoPtDistribution)
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetTitle("H #rightarrow ZZ #rightarrow #mu#mu#mu#mu physics acceptance vs muon trigger threshold")
numberOfEntries_ff_H_ZZ_mumumumu_1000events = delphesSim_ff_H_ZZ_mumumumu_1000events.muonLeadingRecoPtDistribution.GetEntries()
xArr_ff_H_ZZ_mumumumu_1000events = efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetX()
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetPoint(0, xArr_ff_H_ZZ_mumumumu_1000events[0], numberOfEntries_ff_H_ZZ_mumumumu_1000events)
for binNumber_ff_H_ZZ_mumumumu_1000events in xrange(1, len(xArr_ff_H_ZZ_mumumumu_1000events)):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetPoint(
                                                        binNumber_ff_H_ZZ_mumumumu_1000events,
                                                        xArr_ff_H_ZZ_mumumumu_1000events[binNumber_ff_H_ZZ_mumumumu_1000events],
                                                        (efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetY()[binNumber_ff_H_ZZ_mumumumu_1000events - 1] - delphesSim_ff_H_ZZ_mumumumu_1000events.muonLeadingRecoPtDistribution.GetBinContent(binNumber_ff_H_ZZ_mumumumu_1000events))
                                                    )
# Normalise to 1
for binNumber_ff_H_ZZ_mumumumu_1000events in xrange(0, len(xArr_ff_H_ZZ_mumumumu_1000events)):
  efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetPoint(
                                                        binNumber_ff_H_ZZ_mumumumu_1000events,
                                                        xArr_ff_H_ZZ_mumumumu_1000events[binNumber_ff_H_ZZ_mumumumu_1000events],
                                                        efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetY()[binNumber_ff_H_ZZ_mumumumu_1000events]/numberOfEntries_ff_H_ZZ_mumumumu_1000events
                                                    )
  efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetPointError(
                                                        binNumber_ff_H_ZZ_mumumumu_1000events,
                                                        efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetEX()[binNumber_ff_H_ZZ_mumumumu_1000events],
                                                        sqrt(efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetY()[binNumber_ff_H_ZZ_mumumumu_1000events]/numberOfEntries_ff_H_ZZ_mumumumu_1000events)
                                                    )
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetMarkerColor(4)  
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetMarkerStyle(21)
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetLineColor(1)
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.Draw("AP")
text.Draw()
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetXaxis().SetTitle("Threshold [GeV]")
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetXaxis().SetLimits(0, 150)
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetYaxis().SetRangeUser(0, 1.1)
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_H_ZZ_mumumumu_1000events.svg", "svg")
canvas.Print("efficiencyPlot_ff_H_ZZ_mumumumu_1000events.png", "png")
canvas.Print("efficiencyPlot_ff_H_ZZ_mumumumu_1000events.pdf", "pdf")

# Electrons in W production
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_W_enu_1000events = TGraphErrors(delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution)
efficiencyPlot_ff_W_enu_1000events.SetTitle("W #rightarrow e#nu_{e} physics acceptance vs electron trigger threshold")
numberOfEntries_ff_W_enu_1000events = delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetEntries()
xArr_ff_W_enu_1000events = efficiencyPlot_ff_W_enu_1000events.GetX()
efficiencyPlot_ff_W_enu_1000events.SetPoint(0, xArr_ff_W_enu_1000events[0], numberOfEntries_ff_W_enu_1000events)
for binNumber_ff_W_enu_1000events in xrange(1, len(xArr_ff_W_enu_1000events)):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_W_enu_1000events.SetPoint(
                                                        binNumber_ff_W_enu_1000events,
                                                        xArr_ff_W_enu_1000events[binNumber_ff_W_enu_1000events],
                                                        (efficiencyPlot_ff_W_enu_1000events.GetY()[binNumber_ff_W_enu_1000events - 1] - delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetBinContent(binNumber_ff_W_enu_1000events))
                                                    )
# Normalise to 1
for binNumber_ff_W_enu_1000events in xrange(0, len(xArr_ff_W_enu_1000events)):
  efficiencyPlot_ff_W_enu_1000events.SetPoint(
                                                        binNumber_ff_W_enu_1000events,
                                                        xArr_ff_W_enu_1000events[binNumber_ff_W_enu_1000events],
                                                        efficiencyPlot_ff_W_enu_1000events.GetY()[binNumber_ff_W_enu_1000events]/numberOfEntries_ff_W_enu_1000events
                                                    )
  efficiencyPlot_ff_W_enu_1000events.SetPointError(
                                                        binNumber_ff_W_enu_1000events,
                                                        efficiencyPlot_ff_W_enu_1000events.GetEX()[binNumber_ff_W_enu_1000events],
                                                        sqrt(efficiencyPlot_ff_W_enu_1000events.GetY()[binNumber_ff_W_enu_1000events]/numberOfEntries_ff_W_enu_1000events)
                                                    )
efficiencyPlot_ff_W_enu_1000events.SetMarkerColor(4)  
efficiencyPlot_ff_W_enu_1000events.SetMarkerStyle(21)
efficiencyPlot_ff_W_enu_1000events.SetLineColor(1)
efficiencyPlot_ff_W_enu_1000events.Draw("AP")
text.Draw()
efficiencyPlot_ff_W_enu_1000events.GetXaxis().SetTitle("Threshold [GeV]")
efficiencyPlot_ff_W_enu_1000events.GetXaxis().SetLimits(0, 150)
efficiencyPlot_ff_W_enu_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlot_ff_W_enu_1000events.GetYaxis().SetRangeUser(0, 1.1)
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_W_enu_1000events.svg", "svg")
canvas.Print("efficiencyPlot_ff_W_enu_1000events.png", "png")
canvas.Print("efficiencyPlot_ff_W_enu_1000events.pdf", "pdf")

# Muons in W production
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_W_munu_1000events = TGraphErrors(delphesSim_ff_W_munu_1000events.muonLeadingRecoPtDistribution)
efficiencyPlot_ff_W_munu_1000events.SetTitle("W #rightarrow #mu#nu_{#mu} physics acceptance vs muon trigger threshold")
numberOfEntries_ff_W_munu_1000events = delphesSim_ff_W_munu_1000events.muonLeadingRecoPtDistribution.GetEntries()
xArr_ff_W_munu_1000events = efficiencyPlot_ff_W_munu_1000events.GetX()
efficiencyPlot_ff_W_munu_1000events.SetPoint(0, xArr_ff_W_munu_1000events[0], numberOfEntries_ff_W_munu_1000events)
for binNumber_ff_W_munu_1000events in xrange(1, len(xArr_ff_W_munu_1000events)):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_W_munu_1000events.SetPoint(
                                                        binNumber_ff_W_munu_1000events,
                                                        xArr_ff_W_munu_1000events[binNumber_ff_W_munu_1000events],
                                                        (efficiencyPlot_ff_W_munu_1000events.GetY()[binNumber_ff_W_munu_1000events - 1] - delphesSim_ff_W_munu_1000events.muonLeadingRecoPtDistribution.GetBinContent(binNumber_ff_W_munu_1000events))
                                                    )
# Normalise to 1
for binNumber_ff_W_munu_1000events in xrange(0, len(xArr_ff_W_munu_1000events)):
  efficiencyPlot_ff_W_munu_1000events.SetPoint(
                                                        binNumber_ff_W_munu_1000events,
                                                        xArr_ff_W_munu_1000events[binNumber_ff_W_munu_1000events],
                                                        efficiencyPlot_ff_W_munu_1000events.GetY()[binNumber_ff_W_munu_1000events]/numberOfEntries_ff_W_munu_1000events
                                                    )
  efficiencyPlot_ff_W_munu_1000events.SetPointError(
                                                        binNumber_ff_W_munu_1000events,
                                                        efficiencyPlot_ff_W_munu_1000events.GetEX()[binNumber_ff_W_munu_1000events],
                                                        sqrt(efficiencyPlot_ff_W_munu_1000events.GetY()[binNumber_ff_W_munu_1000events]/numberOfEntries_ff_W_munu_1000events)
                                                    )
efficiencyPlot_ff_W_munu_1000events.SetMarkerColor(4)  
efficiencyPlot_ff_W_munu_1000events.SetMarkerStyle(21)
efficiencyPlot_ff_W_munu_1000events.SetLineColor(1)
efficiencyPlot_ff_W_munu_1000events.Draw("AP")
text.Draw()
efficiencyPlot_ff_W_munu_1000events.GetXaxis().SetTitle("Threshold [GeV]")
efficiencyPlot_ff_W_munu_1000events.GetXaxis().SetLimits(0, 150)
efficiencyPlot_ff_W_munu_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlot_ff_W_munu_1000events.GetYaxis().SetRangeUser(0, 1.1)
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_W_munu_1000events.svg", "svg")
canvas.Print("efficiencyPlot_ff_W_munu_1000events.png", "png")
canvas.Print("efficiencyPlot_ff_W_munu_1000events.pdf", "pdf")

# Electrons in Z production
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_Z_ee_1000events = TGraphErrors(delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution)
efficiencyPlot_ff_Z_ee_1000events.SetTitle("Z #rightarrow ee physics acceptance vs electron trigger threshold")
numberOfEntries_ff_Z_ee_1000events = delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetEntries()
xArr_ff_Z_ee_1000events = efficiencyPlot_ff_Z_ee_1000events.GetX()
efficiencyPlot_ff_Z_ee_1000events.SetPoint(0, xArr_ff_Z_ee_1000events[0], numberOfEntries_ff_Z_ee_1000events)
for binNumber_ff_Z_ee_1000events in xrange(1, len(xArr_ff_Z_ee_1000events)):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_Z_ee_1000events.SetPoint(
                                                        binNumber_ff_Z_ee_1000events,
                                                        xArr_ff_Z_ee_1000events[binNumber_ff_Z_ee_1000events],
                                                        (efficiencyPlot_ff_Z_ee_1000events.GetY()[binNumber_ff_Z_ee_1000events - 1] - delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetBinContent(binNumber_ff_Z_ee_1000events))
                                                    )
# Normalise to 1
for binNumber_ff_Z_ee_1000events in xrange(0, len(xArr_ff_Z_ee_1000events)):
  efficiencyPlot_ff_Z_ee_1000events.SetPoint(
                                                        binNumber_ff_Z_ee_1000events,
                                                        xArr_ff_Z_ee_1000events[binNumber_ff_Z_ee_1000events],
                                                        efficiencyPlot_ff_Z_ee_1000events.GetY()[binNumber_ff_Z_ee_1000events]/numberOfEntries_ff_Z_ee_1000events
                                                    )
  efficiencyPlot_ff_Z_ee_1000events.SetPointError(
                                                        binNumber_ff_Z_ee_1000events,
                                                        efficiencyPlot_ff_Z_ee_1000events.GetEX()[binNumber_ff_Z_ee_1000events],
                                                        sqrt(efficiencyPlot_ff_Z_ee_1000events.GetY()[binNumber_ff_Z_ee_1000events]/numberOfEntries_ff_Z_ee_1000events)
                                                    )
efficiencyPlot_ff_Z_ee_1000events.SetMarkerColor(4)  
efficiencyPlot_ff_Z_ee_1000events.SetMarkerStyle(21)
efficiencyPlot_ff_Z_ee_1000events.SetLineColor(1)
efficiencyPlot_ff_Z_ee_1000events.Draw("AP")
text.Draw()
efficiencyPlot_ff_Z_ee_1000events.GetXaxis().SetTitle("Threshold [GeV]")
efficiencyPlot_ff_Z_ee_1000events.GetXaxis().SetLimits(0, 150)
efficiencyPlot_ff_Z_ee_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlot_ff_Z_ee_1000events.GetYaxis().SetRangeUser(0, 1.1)
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_Z_ee_1000events.svg", "svg")
canvas.Print("efficiencyPlot_ff_Z_ee_1000events.png", "png")
canvas.Print("efficiencyPlot_ff_Z_ee_1000events.pdf", "pdf")

# Muons in Z production
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_Z_mumu_1000events = TGraphErrors(delphesSim_ff_Z_mumu_1000events.muonLeadingRecoPtDistribution)
efficiencyPlot_ff_Z_mumu_1000events.SetTitle("Z #rightarrow #mu#mu physics acceptance vs muon trigger threshold")
numberOfEntries_ff_Z_mumu_1000events = delphesSim_ff_Z_mumu_1000events.muonLeadingRecoPtDistribution.GetEntries()
xArr_ff_Z_mumu_1000events = efficiencyPlot_ff_Z_mumu_1000events.GetX()
efficiencyPlot_ff_Z_mumu_1000events.SetPoint(0, xArr_ff_Z_mumu_1000events[0], numberOfEntries_ff_Z_mumu_1000events)
for binNumber_ff_Z_mumu_1000events in xrange(1, len(xArr_ff_Z_mumu_1000events)):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_Z_mumu_1000events.SetPoint(
                                                        binNumber_ff_Z_mumu_1000events,
                                                        xArr_ff_Z_mumu_1000events[binNumber_ff_Z_mumu_1000events],
                                                        (efficiencyPlot_ff_Z_mumu_1000events.GetY()[binNumber_ff_Z_mumu_1000events - 1] - delphesSim_ff_Z_mumu_1000events.muonLeadingRecoPtDistribution.GetBinContent(binNumber_ff_Z_mumu_1000events))
                                                    )
# Normalise to 1
for binNumber_ff_Z_mumu_1000events in xrange(0, len(xArr_ff_Z_mumu_1000events)):
  efficiencyPlot_ff_Z_mumu_1000events.SetPoint(
                                                        binNumber_ff_Z_mumu_1000events,
                                                        xArr_ff_Z_mumu_1000events[binNumber_ff_Z_mumu_1000events],
                                                        efficiencyPlot_ff_Z_mumu_1000events.GetY()[binNumber_ff_Z_mumu_1000events]/numberOfEntries_ff_H_ZZ_eeee_1000events
                                                    )
  efficiencyPlot_ff_Z_mumu_1000events.SetPointError(
                                                        binNumber_ff_Z_mumu_1000events,
                                                        efficiencyPlot_ff_Z_mumu_1000events.GetEX()[binNumber_ff_Z_mumu_1000events],
                                                        sqrt(efficiencyPlot_ff_Z_mumu_1000events.GetY()[binNumber_ff_Z_mumu_1000events]/numberOfEntries_ff_Z_mumu_1000events)
                                                    )
efficiencyPlot_ff_Z_mumu_1000events.SetMarkerColor(4)  
efficiencyPlot_ff_Z_mumu_1000events.SetMarkerStyle(21)
efficiencyPlot_ff_Z_mumu_1000events.SetLineColor(1)
efficiencyPlot_ff_Z_mumu_1000events.Draw("AP")
text.Draw()
efficiencyPlot_ff_Z_mumu_1000events.GetXaxis().SetTitle("Threshold [GeV]")
efficiencyPlot_ff_Z_mumu_1000events.GetXaxis().SetLimits(0, 150)
efficiencyPlot_ff_Z_mumu_1000events.GetYaxis().SetTitle("Efficiency")
efficiencyPlot_ff_Z_mumu_1000events.GetYaxis().SetRangeUser(0, 1.1)
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_Z_mumu_1000events.svg", "svg")
canvas.Print("efficiencyPlot_ff_Z_mumu_1000events.png", "png")
canvas.Print("efficiencyPlot_ff_Z_mumu_1000events.pdf", "pdf")

efficiencyPlot_electrons = TMultiGraph("efficiencyPlot_electrons", "")
efficiencyPlot_electrons.Add(efficiencyPlot_ff_H_WW_enuenu_1000events)
efficiencyPlot_ff_H_WW_enuenu_1000events.SetMarkerColor(6)
efficiencyPlot_ff_H_WW_enuenu_1000events.SetLineColor(1)
efficiencyPlot_ff_H_WW_enuenu_1000events.SetFillColor(0)
efficiencyPlot_electrons.Add(efficiencyPlot_ff_H_ZZ_eeee_1000events)
efficiencyPlot_ff_H_ZZ_eeee_1000events.SetMarkerColor(2)
efficiencyPlot_ff_H_ZZ_eeee_1000events.SetLineColor(1)
efficiencyPlot_ff_H_ZZ_eeee_1000events.SetFillColor(0)
efficiencyPlot_electrons.Add(efficiencyPlot_ff_W_enu_1000events)
efficiencyPlot_ff_W_enu_1000events.SetMarkerColor(3)
efficiencyPlot_ff_W_enu_1000events.SetLineColor(1)
efficiencyPlot_ff_W_enu_1000events.SetFillColor(0)
efficiencyPlot_electrons.Add(efficiencyPlot_ff_Z_ee_1000events)
efficiencyPlot_ff_Z_ee_1000events.SetMarkerColor(4)
efficiencyPlot_ff_Z_ee_1000events.SetLineColor(1)
efficiencyPlot_ff_Z_ee_1000events.SetFillColor(0)
efficiencyPlot_electrons.Draw("AP")
efficiencyPlot_electrons.GetYaxis().SetTitle("% accepted events")
efficiencyPlot_electrons.GetYaxis().SetTitleOffset(1.2)
efficiencyPlot_electrons.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlot_electrons.GetXaxis().SetLimits(0, 150)
efficiencyPlot_electrons.GetXaxis().SetTitle("p_{t} [GeV]")

text.SetX1NDC(0.5)
text.SetX2NDC(0.9)
text.Draw()

efficiencyPlot_electrons_legend = TLegend(0.6, 0.6, 0.9, 0.8)
efficiencyPlot_electrons_legend.SetHeader("Physical process")
efficiencyPlot_electrons_legend.AddEntry(efficiencyPlot_ff_H_WW_enuenu_1000events, "H #rightarrow WW #rightarrow e#nu_{e}e#nu_{e}", "P")
efficiencyPlot_electrons_legend.AddEntry(efficiencyPlot_ff_H_ZZ_eeee_1000events, "H #rightarrow ZZ #rightarrow eeee", "P")
efficiencyPlot_electrons_legend.AddEntry(efficiencyPlot_ff_W_enu_1000events, "W #rightarrow e#nu_{e}", "P")
efficiencyPlot_electrons_legend.AddEntry(efficiencyPlot_ff_Z_ee_1000events, "Z #rightarrow ee", "P")
efficiencyPlot_electrons_legend.Draw()
canvas.Update()
canvas.Print("efficiencyPlot_electrons.svg", "svg")
canvas.Print("efficiencyPlot_electrons.png", "png")
canvas.Print("efficiencyPlot_electrons.pdf", "pdf")

efficiencyPlot_muons = TMultiGraph("efficiencyPlot_muons", "")
efficiencyPlot_muons.Add(efficiencyPlot_ff_H_WW_munumunu_1000events)
efficiencyPlot_ff_H_WW_munumunu_1000events.SetMarkerColor(6)
efficiencyPlot_ff_H_WW_munumunu_1000events.SetLineColor(1)
efficiencyPlot_ff_H_WW_munumunu_1000events.SetFillColor(0)
efficiencyPlot_muons.Add(efficiencyPlot_ff_H_ZZ_mumumumu_1000events)
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetMarkerColor(2)
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetLineColor(1)
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetFillColor(0)
efficiencyPlot_muons.Add(efficiencyPlot_ff_W_munu_1000events)
efficiencyPlot_ff_W_munu_1000events.SetMarkerColor(3)
efficiencyPlot_ff_W_munu_1000events.SetLineColor(1)
efficiencyPlot_ff_W_munu_1000events.SetFillColor(0)
efficiencyPlot_muons.Add(efficiencyPlot_ff_Z_mumu_1000events)
efficiencyPlot_ff_Z_mumu_1000events.SetMarkerColor(4)
efficiencyPlot_ff_Z_mumu_1000events.SetLineColor(1)
efficiencyPlot_ff_Z_mumu_1000events.SetFillColor(0)
efficiencyPlot_muons.Draw("AP")
efficiencyPlot_muons.GetYaxis().SetTitle("% accepted events")
efficiencyPlot_muons.GetYaxis().SetTitleOffset(1.2)
efficiencyPlot_muons.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlot_muons.GetXaxis().SetLimits(0, 150)
efficiencyPlot_muons.GetXaxis().SetTitle("p_{t} [GeV]")

text.SetX1NDC(0.5)
text.SetX2NDC(0.9)
text.Draw()

efficiencyPlot_muons_legend = TLegend(0.6, 0.6, 0.9, 0.8)
efficiencyPlot_muons_legend.SetHeader("Physical process")
efficiencyPlot_muons_legend.AddEntry(efficiencyPlot_ff_H_WW_munumunu_1000events, "H #rightarrow WW #rightarrow #mu#nu_{#mu}#mu#nu_{#mu}", "P")
efficiencyPlot_muons_legend.AddEntry(efficiencyPlot_ff_H_ZZ_mumumumu_1000events, "H #rightarrow ZZ #rightarrow #mu#mu#mu#mu", "P")
efficiencyPlot_muons_legend.AddEntry(efficiencyPlot_ff_W_munu_1000events, "W #rightarrow #mu#nu_{#mu}", "P")
efficiencyPlot_muons_legend.AddEntry(efficiencyPlot_ff_Z_mumu_1000events, "Z #rightarrow #mu#mu", "P")
efficiencyPlot_muons_legend.Draw()
canvas.Update()
canvas.Print("efficiencyPlot_muons.svg", "svg")
canvas.Print("efficiencyPlot_muons.png", "png")
canvas.Print("efficiencyPlot_muons.pdf", "pdf")

'''
ptToElectronRate = []
ptToElectronRate.append(0)
ptToElectronRate.append(2.32E+06)
ptToElectronRate.append(217343)
ptToElectronRate.append(141707)
ptToElectronRate.append(70709.5)
ptToElectronRate.append(43069.7)
ptToElectronRate.append(25816.3)
ptToElectronRate.append(16971.9)
ptToElectronRate.append(12077.7)
ptToElectronRate.append(8937.5)
ptToElectronRate.append(6715)
ptToElectronRate.append(5550.6)
ptToElectronRate.append(4252.5)
ptToElectronRate.append(3300.5)
ptToElectronRate.append(2850.9)

ptToElectronRateError = []
ptToElectronRateError.append(0)
ptToElectronRateError.append(620805)
ptToElectronRateError.append(30426)
ptToElectronRateError.append(19778)
ptToElectronRateError.append(16698)
ptToElectronRateError.append(9170)
ptToElectronRateError.append(3516)
ptToElectronRateError.append(2228)
ptToElectronRateError.append(1545)
ptToElectronRateError.append(1132)
ptToElectronRateError.append(860)
ptToElectronRateError.append(718)
ptToElectronRateError.append(569)
ptToElectronRateError.append(460)
ptToElectronRateError.append(411)

ptToMuonRate = []
ptToMuonRate.append(0)
ptToMuonRate.append(544805)
ptToMuonRate.append(50713.3)
ptToMuonRate.append(33325.9)
ptToMuonRate.append(14188)
ptToMuonRate.append(12065.8)
ptToMuonRate.append(5384)
ptToMuonRate.append(3501.41)
ptToMuonRate.append(2453.58)
ptToMuonRate.append(1800)
ptToMuonRate.append(1347.25)
ptToMuonRate.append(1103.74)
ptToMuonRate.append(843.75)
ptToMuonRate.append(650.44)
ptToMuonRate.append(559.86)

ptToMuonRateError = []
ptToMuonRateError.append(0)
ptToMuonRateError.append(93920)
ptToMuonRateError.append(8290)
ptToMuonRateError.append(17119)
ptToMuonRateError.append(5594)
ptToMuonRateError.append(5708)
ptToMuonRateError.append(1573)
ptToMuonRateError.append(1031)
ptToMuonRateError.append(729)
ptToMuonRateError.append(538)
ptToMuonRateError.append(407)
ptToMuonRateError.append(336)
ptToMuonRateError.append(261)
ptToMuonRateError.append(204)
ptToMuonRateError.append(177)
'''



ptToElectronRate = []
ptToElectronRate.append(0)
ptToElectronRate.append(2318320.128)
ptToElectronRate.append(195608.2608)
ptToElectronRate.append(141634.87032)
ptToElectronRate.append(70748.0000000001)
ptToElectronRate.append(43092.1428571428)
ptToElectronRate.append(26085.48)
ptToElectronRate.append(17285.345)
ptToElectronRate.append(12286.92)
ptToElectronRate.append(9084.375)
ptToElectronRate.append(6863.75)
ptToElectronRate.append(5667.035)
ptToElectronRate.append(4360.5)
ptToElectronRate.append(3380.195)
ptToElectronRate.append(2916.69)

ptToElectronRateError = []
ptToElectronRateError.append(0)
ptToElectronRateError.append(620805)
ptToElectronRateError.append(52380)
ptToElectronRateError.append(37927)
ptToElectronRateError.append(18951)
ptToElectronRateError.append(11551)
ptToElectronRateError.append(7001)
ptToElectronRateError.append(4648)
ptToElectronRateError.append(3313)
ptToElectronRateError.append(2459)
ptToElectronRateError.append(1867)
ptToElectronRateError.append(1549)
ptToElectronRateError.append(1203)
ptToElectronRateError.append(943)
ptToElectronRateError.append(821)

ptToMuonRate = []
ptToMuonRate.append(0)
ptToMuonRate.append(398461.272)
ptToMuonRate.append(50713.3)
ptToMuonRate.append(33325.85184)
ptToMuonRate.append(14149.6)
ptToMuonRate.append(12065.8)
ptToMuonRate.append(5769.4944)
ptToMuonRate.append(3823.1116)
ptToMuonRate.append(2717.5776)
ptToMuonRate.append(2009.25)
ptToMuonRate.append(1518.1)
ptToMuonRate.append(1253.4148)
ptToMuonRate.append(964.44)
ptToMuonRate.append(747.6196)
ptToMuonRate.append(645.1032)

ptToMuonRateError = []
ptToMuonRateError.append(0)
ptToMuonRateError.append(204684)
ptToMuonRateError.append(18607)
ptToMuonRateError.append(17119)
ptToMuonRateError.append(7269)
ptToMuonRateError.append(6199)
ptToMuonRateError.append(2965)
ptToMuonRateError.append(1966)
ptToMuonRateError.append(1398)
ptToMuonRateError.append(1035)
ptToMuonRateError.append(783)
ptToMuonRateError.append(647)
ptToMuonRateError.append(499)
ptToMuonRateError.append(388)
ptToMuonRateError.append(336)

canvas.SetLogx(1)

label_30GeV_electrons = TLatex(150000, 1.05, "30 GeV - 140 kHz")
label_30GeV_electrons.SetTextSize(0.03)
label_30GeV_muons = TLatex(37000, 1.05, "30 GeV - 33 kHz")
label_30GeV_muons.SetTextSize(0.03)
line_30GeV_electrons = TLine(141634, 0, 141634, 1.1)
line_30GeV_electrons.SetLineColor(2)
line_30GeV_electrons.SetLineStyle(2)
line_30GeV_muons = TLine(33325.3, 0, 33325.3, 1.1)
line_30GeV_muons.SetLineColor(2)
line_30GeV_muons.SetLineStyle(2)

text.SetX1NDC(0.12)
text.SetX2NDC(0.52)

efficiencyPlotWithRate_ff_H_WW_enuenu_1000events = TGraphErrors(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetPoint(x - 1, ptToElectronRate[x], efficiencyPlot_ff_H_WW_enuenu_1000events.GetY()[x*2])
  efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetPointError(x - 1, ptToElectronRateError[x], sqrt(efficiencyPlot_ff_H_WW_enuenu_1000events.GetY()[x*2]/ numberOfEntries_ff_H_WW_enuenu_1000events))
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetTitle("H #rightarrow WW #rightarrow e#nu_{e}e#nu_{e} physics acceptance vs electron trigger rate")
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetName("efficiencyPlotWithRate_ff_H_WW_enuenu_1000events")
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.GetYaxis().SetTitle("% accepted events")
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.GetYaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.GetXaxis().SetNdivisions(5, 0, 0)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.GetXaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.Draw("AP")
text.Draw()
label_30GeV_electrons.Draw()
line_30GeV_electrons.Draw()
canvas.Update()
canvas.Print("efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.svg", "svg")
canvas.Print("efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.png", "png")
canvas.Print("efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.pdf", "pdf")

efficiencyPlotWithRate_ff_H_WW_munumunu_1000events = TGraphErrors(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetPoint(x - 1, ptToMuonRate[x], efficiencyPlot_ff_H_WW_munumunu_1000events.GetY()[x*2])
  efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetPointError(x - 1, ptToMuonRateError[x], sqrt(efficiencyPlot_ff_H_WW_munumunu_1000events.GetY()[x*2]/ numberOfEntries_ff_H_WW_munumunu_1000events))
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetTitle("H #rightarrow WW #rightarrow #mu#nu_{#mu}#mu#nu_{#mu} physics acceptance vs muon trigger rate")
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetName("efficiencyPlotWithRate_ff_H_WW_munumunu_1000events")
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.GetYaxis().SetTitle("% accepted events")
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.GetYaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.GetXaxis().SetNdivisions(5, 0, 0)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.GetXaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.Draw("AP")
text.Draw()
label_30GeV_muons.Draw()
line_30GeV_muons.Draw()
canvas.Update()
canvas.Print("efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.svg", "svg")
canvas.Print("efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.png", "png")
canvas.Print("efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.pdf", "pdf")

efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events = TGraphErrors(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.SetPoint(x - 1, ptToElectronRate[x], efficiencyPlot_ff_H_ZZ_eeee_1000events.GetY()[x*2])
  efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.SetPointError(x - 1, ptToElectronRateError[x], sqrt(efficiencyPlot_ff_H_ZZ_eeee_1000events.GetY()[x*2]/ numberOfEntries_ff_H_ZZ_eeee_1000events))
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.SetTitle("H #rightarrow ZZ #rightarrow eeee physics acceptance vs electron trigger rate")
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.SetName("efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events")
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.GetYaxis().SetTitle("% accepted events")
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.GetYaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.GetXaxis().SetNdivisions(5, 0, 0)
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.GetXaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.Draw("AP")
text.Draw()
label_30GeV_electrons.Draw()
line_30GeV_electrons.Draw()
canvas.Update()
canvas.Print("efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.svg", "svg")
canvas.Print("efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.png", "png")
canvas.Print("efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.pdf", "pdf")

efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events = TGraphErrors(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.SetPoint(x - 1, ptToMuonRate[x], efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetY()[x*2])
  efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.SetPointError(x - 1, ptToMuonRateError[x], sqrt(efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetY()[x*2]/ numberOfEntries_ff_H_ZZ_mumumumu_1000events))
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.SetTitle("H #rightarrow ZZ #rightarrow #mu#mu#mu#mu physics acceptance vs muon trigger rate")
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.SetName("efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events")
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.GetYaxis().SetTitle("% accepted events")
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.GetYaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.GetXaxis().SetNdivisions(5, 0, 0)
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.GetXaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.Draw("AP")
text.Draw()
label_30GeV_muons.Draw()
line_30GeV_muons.Draw()
canvas.Update()
canvas.Print("efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.svg", "svg")
canvas.Print("efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.png", "png")
canvas.Print("efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.pdf", "pdf")

efficiencyPlotWithRate_ff_W_enu_1000events = TGraphErrors(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_W_enu_1000events.SetPoint(x - 1, ptToElectronRate[x], efficiencyPlot_ff_W_enu_1000events.GetY()[x*2])
  efficiencyPlotWithRate_ff_W_enu_1000events.SetPointError(x - 1, ptToElectronRateError[x], sqrt(efficiencyPlot_ff_W_enu_1000events.GetY()[x*2]/ numberOfEntries_ff_W_enu_1000events))
efficiencyPlotWithRate_ff_W_enu_1000events.SetTitle("W #rightarrow e#nu_{e} physics acceptance vs electron trigger rate")
efficiencyPlotWithRate_ff_W_enu_1000events.SetName("efficiencyPlotWithRate_ff_W_enu_1000events")
efficiencyPlotWithRate_ff_W_enu_1000events.GetYaxis().SetTitle("% accepted events")
efficiencyPlotWithRate_ff_W_enu_1000events.GetYaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_W_enu_1000events.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlotWithRate_ff_W_enu_1000events.GetXaxis().SetNdivisions(5, 0, 0)
efficiencyPlotWithRate_ff_W_enu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_W_enu_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_W_enu_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_W_enu_1000events.GetXaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_W_enu_1000events.Draw("AP")
text.Draw()
label_30GeV_electrons.Draw()
line_30GeV_electrons.Draw()
canvas.Update()
canvas.Print("efficiencyPlotWithRate_ff_W_enu_1000events.svg", "svg")
canvas.Print("efficiencyPlotWithRate_ff_W_enu_1000events.png", "png")
canvas.Print("efficiencyPlotWithRate_ff_W_enu_1000events.pdf", "pdf")

efficiencyPlotWithRate_ff_W_munu_1000events = TGraphErrors(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_W_munu_1000events.SetPoint(x - 1, ptToMuonRate[x], efficiencyPlot_ff_W_munu_1000events.GetY()[x*2])
  efficiencyPlotWithRate_ff_W_munu_1000events.SetPointError(x - 1, ptToMuonRateError[x], sqrt(efficiencyPlot_ff_W_munu_1000events.GetY()[x*2]/ numberOfEntries_ff_W_munu_1000events))
efficiencyPlotWithRate_ff_W_munu_1000events.SetTitle("W #rightarrow #mu#nu_{#mu} physics acceptance vs muon trigger rate")
efficiencyPlotWithRate_ff_W_munu_1000events.SetName("efficiencyPlotWithRate_ff_W_munu_1000events")
efficiencyPlotWithRate_ff_W_munu_1000events.GetYaxis().SetTitle("% accepted events")
efficiencyPlotWithRate_ff_W_munu_1000events.GetYaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_W_munu_1000events.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlotWithRate_ff_W_munu_1000events.GetXaxis().SetNdivisions(5, 0, 0)
efficiencyPlotWithRate_ff_W_munu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_W_munu_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_W_munu_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_W_munu_1000events.GetXaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_W_munu_1000events.Draw("AP")
text.Draw()
label_30GeV_muons.Draw()
line_30GeV_muons.Draw()
canvas.Update()
canvas.Print("efficiencyPlotWithRate_ff_W_munu_1000events.svg", "svg")
canvas.Print("efficiencyPlotWithRate_ff_W_munu_1000events.png", "png")
canvas.Print("efficiencyPlotWithRate_ff_W_munu_1000events.pdf", "pdf")

efficiencyPlotWithRate_ff_Z_ee_1000events = TGraphErrors(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_Z_ee_1000events.SetPoint(x - 1, ptToElectronRate[x], efficiencyPlot_ff_Z_ee_1000events.GetY()[x*2])
  efficiencyPlotWithRate_ff_Z_ee_1000events.SetPointError(x - 1, ptToElectronRateError[x], sqrt(efficiencyPlot_ff_Z_ee_1000events.GetY()[x*2]/ numberOfEntries_ff_Z_ee_1000events))
efficiencyPlotWithRate_ff_Z_ee_1000events.SetTitle("Z #rightarrow ee physics acceptance vs electron trigger rate")
efficiencyPlotWithRate_ff_Z_ee_1000events.SetName("efficiencyPlotWithRate_ff_Z_ee_1000events")
efficiencyPlotWithRate_ff_Z_ee_1000events.GetYaxis().SetTitle("% accepted events")
efficiencyPlotWithRate_ff_Z_ee_1000events.GetYaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_Z_ee_1000events.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlotWithRate_ff_Z_ee_1000events.GetXaxis().SetNdivisions(5, 0, 0)
efficiencyPlotWithRate_ff_Z_ee_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_Z_ee_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_Z_ee_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_Z_ee_1000events.GetXaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_Z_ee_1000events.Draw("AP")
text.Draw()
label_30GeV_electrons.Draw()
line_30GeV_electrons.Draw()
canvas.Update()
canvas.Print("efficiencyPlotWithRate_ff_Z_ee_1000events.svg", "svg")
canvas.Print("efficiencyPlotWithRate_ff_Z_ee_1000events.png", "png")
canvas.Print("efficiencyPlotWithRate_ff_Z_ee_1000events.pdf", "pdf")

efficiencyPlotWithRate_ff_Z_mumu_1000events = TGraphErrors(14)
for x in xrange(1, 15):
  efficiencyPlotWithRate_ff_Z_mumu_1000events.SetPoint(x - 1, ptToMuonRate[x], efficiencyPlot_ff_Z_mumu_1000events.GetY()[x*2])
  efficiencyPlotWithRate_ff_Z_mumu_1000events.SetPointError(x - 1, ptToMuonRateError[x], sqrt(efficiencyPlot_ff_Z_mumu_1000events.GetY()[x*2]/ numberOfEntries_ff_Z_mumu_1000events))
efficiencyPlotWithRate_ff_Z_mumu_1000events.SetTitle("Z #rightarrow #mu#mu physics acceptance vs muon trigger rate")
efficiencyPlotWithRate_ff_Z_mumu_1000events.SetName("efficiencyPlotWithRate_ff_Z_mumu_1000events")
efficiencyPlotWithRate_ff_Z_mumu_1000events.GetYaxis().SetTitle("% accepted events")
efficiencyPlotWithRate_ff_Z_mumu_1000events.GetYaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_Z_mumu_1000events.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlotWithRate_ff_Z_mumu_1000events.GetXaxis().SetNdivisions(5, 0, 0)
efficiencyPlotWithRate_ff_Z_mumu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_Z_mumu_1000events.SetMarkerStyle(21)
efficiencyPlotWithRate_ff_Z_mumu_1000events.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_ff_Z_mumu_1000events.GetXaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_ff_Z_mumu_1000events.Draw("AP")
text.Draw()
label_30GeV_muons.Draw()
line_30GeV_muons.Draw()
canvas.Update()
canvas.Print("efficiencyPlotWithRate_ff_Z_mumu_1000events.svg", "svg")
canvas.Print("efficiencyPlotWithRate_ff_Z_mumu_1000events.png", "png")
canvas.Print("efficiencyPlotWithRate_ff_Z_mumu_1000events.pdf", "pdf")

efficiencyPlotWithRate_electrons = TMultiGraph("efficiencyPlotWithRate_electrons", "")
efficiencyPlotWithRate_electrons.Add(efficiencyPlotWithRate_ff_H_WW_enuenu_1000events)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetMarkerColor(6)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetLineColor(1)
efficiencyPlotWithRate_ff_H_WW_enuenu_1000events.SetFillColor(0)
efficiencyPlotWithRate_electrons.Add(efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events)
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.SetMarkerColor(2)
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.SetLineColor(1)
efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events.SetFillColor(0)
efficiencyPlotWithRate_electrons.Add(efficiencyPlotWithRate_ff_W_enu_1000events)
efficiencyPlotWithRate_ff_W_enu_1000events.SetMarkerColor(3)
efficiencyPlotWithRate_ff_W_enu_1000events.SetLineColor(1)
efficiencyPlotWithRate_ff_W_enu_1000events.SetFillColor(0)
efficiencyPlotWithRate_electrons.Add(efficiencyPlotWithRate_ff_Z_ee_1000events)
efficiencyPlotWithRate_ff_Z_ee_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_Z_ee_1000events.SetLineColor(1)
efficiencyPlotWithRate_ff_Z_ee_1000events.SetFillColor(0)
efficiencyPlotWithRate_electrons.Draw("AP")
efficiencyPlotWithRate_electrons.GetYaxis().SetTitle("% accepted events")
efficiencyPlotWithRate_electrons.GetYaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_electrons.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlotWithRate_electrons.GetXaxis().SetNdivisions(5, 0, 0)
efficiencyPlotWithRate_electrons.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_electrons.GetXaxis().SetTitleOffset(1.2)
label_30GeV_electrons.Draw()
line_30GeV_electrons.Draw()
efficiencyPlotWithRate_electrons_legend = TLegend(0.6, 0.35, 0.9, 0.15)
efficiencyPlotWithRate_electrons_legend.SetHeader("Physical process")
efficiencyPlotWithRate_electrons_legend.AddEntry(efficiencyPlotWithRate_ff_H_WW_enuenu_1000events, "H #rightarrow WW #rightarrow e#nu_{e}e#nu_{e}", "P")
efficiencyPlotWithRate_electrons_legend.AddEntry(efficiencyPlotWithRate_ff_H_ZZ_eeee_1000events, "H #rightarrow ZZ #rightarrow eeee", "P")
efficiencyPlotWithRate_electrons_legend.AddEntry(efficiencyPlotWithRate_ff_W_enu_1000events, "W #rightarrow e#nu_{e}", "P")
efficiencyPlotWithRate_electrons_legend.AddEntry(efficiencyPlotWithRate_ff_Z_ee_1000events, "Z #rightarrow ee", "P")
efficiencyPlotWithRate_electrons_legend.Draw()
text.Draw()
canvas.Update()
canvas.Print("efficiencyPlotWithRate_electrons.svg", "svg")
canvas.Print("efficiencyPlotWithRate_electrons.png", "png")
canvas.Print("efficiencyPlotWithRate_electrons.pdf", "pdf")

efficiencyPlotWithRate_muons = TMultiGraph("efficiencyPlotWithRate_muons", "")
efficiencyPlotWithRate_muons.Add(efficiencyPlotWithRate_ff_H_WW_munumunu_1000events)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetMarkerColor(6)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetLineColor(1)
efficiencyPlotWithRate_ff_H_WW_munumunu_1000events.SetFillColor(0)
efficiencyPlotWithRate_muons.Add(efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events)
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.SetMarkerColor(2)
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.SetLineColor(1)
efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events.SetFillColor(0)
efficiencyPlotWithRate_muons.Add(efficiencyPlotWithRate_ff_W_munu_1000events)
efficiencyPlotWithRate_ff_W_munu_1000events.SetMarkerColor(3)
efficiencyPlotWithRate_ff_W_munu_1000events.SetLineColor(1)
efficiencyPlotWithRate_ff_W_munu_1000events.SetFillColor(0)
efficiencyPlotWithRate_muons.Add(efficiencyPlotWithRate_ff_Z_mumu_1000events)
efficiencyPlotWithRate_ff_Z_mumu_1000events.SetMarkerColor(4)
efficiencyPlotWithRate_ff_Z_mumu_1000events.SetLineColor(1)
efficiencyPlotWithRate_ff_Z_mumu_1000events.SetFillColor(0)
efficiencyPlotWithRate_muons.Draw("AP")
efficiencyPlotWithRate_muons.GetYaxis().SetTitle("% accepted events")
efficiencyPlotWithRate_muons.GetYaxis().SetTitleOffset(1.2)
efficiencyPlotWithRate_muons.GetYaxis().SetRangeUser(0, 1.1)
efficiencyPlotWithRate_muons.GetXaxis().SetNdivisions(5, 0, 0)
efficiencyPlotWithRate_muons.GetXaxis().SetTitle("Rate [Hz]")
efficiencyPlotWithRate_muons.GetXaxis().SetTitleOffset(1.2)
label_30GeV_muons.Draw()
line_30GeV_muons.Draw()
efficiencyPlotWithRate_muons_legend = TLegend(0.6, 0.35, 0.9, 0.15)
efficiencyPlotWithRate_muons_legend.SetHeader("Physical process")
efficiencyPlotWithRate_muons_legend.AddEntry(efficiencyPlotWithRate_ff_H_WW_munumunu_1000events, "H #rightarrow WW #rightarrow #mu#nu_{#mu}#mu#nu_{#mu}", "P")
efficiencyPlotWithRate_muons_legend.AddEntry(efficiencyPlotWithRate_ff_H_ZZ_mumumumu_1000events, "H #rightarrow ZZ #rightarrow #mu#mu#mu#mu", "P")
efficiencyPlotWithRate_muons_legend.AddEntry(efficiencyPlotWithRate_ff_W_munu_1000events, "W #rightarrow #mu#nu_{#mu}", "P")
efficiencyPlotWithRate_muons_legend.AddEntry(efficiencyPlotWithRate_ff_Z_mumu_1000events, "Z #rightarrow #mu#mu", "P")
efficiencyPlotWithRate_muons_legend.Draw()
text.Draw()
canvas.Update()
canvas.Print("efficiencyPlotWithRate_muons.svg", "svg")
canvas.Print("efficiencyPlotWithRate_muons.png", "png")
canvas.Print("efficiencyPlotWithRate_muons.pdf", "pdf")