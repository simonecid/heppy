from ROOT import TFile
from ROOT import TH1I
from ROOT import TH1F
from ROOT import TCanvas
from ROOT import TLegend

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

canvas = TCanvas("canvas", "canvas", 1024, 1024)
canvas.SetGridx()
canvas.SetGridy()

# ======================================
# ========= BUILDING THE PLOTS =========
# ======================================

# Electrons in HH to WW
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_H_WW_enuenu_1000events = TH1F(
                                               "efficiencyPlot_ff_H_WW_enuenu_1000events",
                                               "Efficiency ff_H_WW_enuenu_1000events",
                                               delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetNbinsX(),
                                               delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetXaxis().GetXmin(),
                                               delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetXaxis().GetXmax()
                                             )
numberOfEntries_ff_H_WW_enuenu_1000events = delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetEntries()
efficiencyPlot_ff_H_WW_enuenu_1000events.SetBinContent(1, numberOfEntries_ff_H_WW_enuenu_1000events)
for binNumber_ff_H_WW_enuenu_1000events in xrange(2, efficiencyPlot_ff_H_WW_enuenu_1000events.GetNbinsX() + 1):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_H_WW_enuenu_1000events.SetBinContent(
                                                        binNumber_ff_H_WW_enuenu_1000events,
                                                        efficiencyPlot_ff_H_WW_enuenu_1000events.GetBinContent(binNumber_ff_H_WW_enuenu_1000events - 1) - delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetBinContent(binNumber_ff_H_WW_enuenu_1000events - 1)
                                                      )
# Normalise to 1
efficiencyPlot_ff_H_WW_enuenu_1000events.Scale(1/numberOfEntries_ff_H_WW_enuenu_1000events)
efficiencyPlot_ff_H_WW_enuenu_1000events.SetXTitle("Threshold [GeV]")
efficiencyPlot_ff_H_WW_enuenu_1000events.SetYTitle("Efficiency")
efficiencyPlot_ff_H_WW_enuenu_1000events.Draw("HIST")
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_H_WW_enuenu_1000events.svg", "svg")

# Muons in HH to WW
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_H_WW_munumunu_1000events = TH1F(
                                               "efficiencyPlot_ff_H_WW_munumunu_1000events",
                                               "Efficiency ff_H_WW_munumunu_1000events",
                                               delphesSim_ff_H_WW_munumunu_1000events.muonLeadingRecoPtDistribution.GetNbinsX(),
                                               delphesSim_ff_H_WW_munumunu_1000events.muonLeadingRecoPtDistribution.GetXaxis().GetXmin(),
                                               delphesSim_ff_H_WW_munumunu_1000events.muonLeadingRecoPtDistribution.GetXaxis().GetXmax()
                                             )
numberOfEntries_ff_H_WW_munumunu_1000events = delphesSim_ff_H_WW_munumunu_1000events.muonLeadingRecoPtDistribution.GetEntries()
efficiencyPlot_ff_H_WW_munumunu_1000events.SetBinContent(1, numberOfEntries_ff_H_WW_munumunu_1000events)
for binNumber_ff_H_WW_munumunu_1000events in xrange(2, efficiencyPlot_ff_H_WW_munumunu_1000events.GetNbinsX() + 1):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_H_WW_munumunu_1000events.SetBinContent(
                                                        binNumber_ff_H_WW_munumunu_1000events,
                                                        efficiencyPlot_ff_H_WW_munumunu_1000events.GetBinContent(binNumber_ff_H_WW_munumunu_1000events - 1) - delphesSim_ff_H_WW_munumunu_1000events.muonLeadingRecoPtDistribution.GetBinContent(binNumber_ff_H_WW_munumunu_1000events - 1)
                                                      )
# Normalise to 1
efficiencyPlot_ff_H_WW_munumunu_1000events.Scale(1/numberOfEntries_ff_H_WW_munumunu_1000events)
efficiencyPlot_ff_H_WW_munumunu_1000events.SetXTitle("Threshold [GeV]")
efficiencyPlot_ff_H_WW_munumunu_1000events.SetYTitle("Efficiency")
efficiencyPlot_ff_H_WW_munumunu_1000events.Draw("HIST")
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_H_WW_munumunu_1000events.svg", "svg")

# Electrons in HH to ZZ
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_H_ZZ_eeee_1000events = TH1F(
                                               "efficiencyPlot_ff_H_ZZ_eeee_1000events",
                                               "Efficiency ff_H_ZZ_eeee_1000events",
                                               delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetNbinsX(),
                                               delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetXaxis().GetXmin(),
                                               delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetXaxis().GetXmax()
                                             )
numberOfEntries_ff_H_ZZ_eeee_1000events = delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetEntries()
efficiencyPlot_ff_H_ZZ_eeee_1000events.SetBinContent(1, numberOfEntries_ff_H_ZZ_eeee_1000events)
for binNumber_ff_H_ZZ_eeee_1000events in xrange(2, efficiencyPlot_ff_H_ZZ_eeee_1000events.GetNbinsX() + 1):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_H_ZZ_eeee_1000events.SetBinContent(
                                                        binNumber_ff_H_ZZ_eeee_1000events,
                                                        efficiencyPlot_ff_H_ZZ_eeee_1000events.GetBinContent(binNumber_ff_H_ZZ_eeee_1000events - 1) - delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetBinContent(binNumber_ff_H_ZZ_eeee_1000events - 1)
                                                      )
# Normalise to 1
efficiencyPlot_ff_H_ZZ_eeee_1000events.Scale(1/numberOfEntries_ff_H_ZZ_eeee_1000events)
efficiencyPlot_ff_H_ZZ_eeee_1000events.SetXTitle("Threshold [GeV]")
efficiencyPlot_ff_H_ZZ_eeee_1000events.SetYTitle("Efficiency")
efficiencyPlot_ff_H_ZZ_eeee_1000events.Draw("HIST")
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_H_ZZ_eeee_1000events.svg", "svg")

# Muons in HH to ZZ
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_H_ZZ_mumumumu_1000events = TH1F(
                                               "efficiencyPlot_ff_H_ZZ_mumumumu_1000events",
                                               "Efficiency ff_H_ZZ_mumumumu_1000events",
                                               delphesSim_ff_H_ZZ_mumumumu_1000events.muonLeadingRecoPtDistribution.GetNbinsX(),
                                               delphesSim_ff_H_ZZ_mumumumu_1000events.muonLeadingRecoPtDistribution.GetXaxis().GetXmin(),
                                               delphesSim_ff_H_ZZ_mumumumu_1000events.muonLeadingRecoPtDistribution.GetXaxis().GetXmax()
                                             )
numberOfEntries_ff_H_ZZ_mumumumu_1000events = delphesSim_ff_H_ZZ_mumumumu_1000events.muonLeadingRecoPtDistribution.GetEntries()
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetBinContent(1, numberOfEntries_ff_H_ZZ_mumumumu_1000events)
for binNumber_ff_H_ZZ_mumumumu_1000events in xrange(2, efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetNbinsX() + 1):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetBinContent(
                                                        binNumber_ff_H_ZZ_mumumumu_1000events,
                                                        efficiencyPlot_ff_H_ZZ_mumumumu_1000events.GetBinContent(binNumber_ff_H_ZZ_mumumumu_1000events - 1) - delphesSim_ff_H_ZZ_mumumumu_1000events.muonLeadingRecoPtDistribution.GetBinContent(binNumber_ff_H_ZZ_mumumumu_1000events - 1)
                                                      )
# Normalise to 1
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.Scale(1/numberOfEntries_ff_H_ZZ_mumumumu_1000events)
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetXTitle("Threshold [GeV]")
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.SetYTitle("Efficiency")
efficiencyPlot_ff_H_ZZ_mumumumu_1000events.Draw("HIST")
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_H_ZZ_mumumumu_1000events.svg", "svg")

# Electrons in W production
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_W_enu_1000events = TH1F(
                                               "efficiencyPlot_ff_W_enu_1000events",
                                               "Efficiency ff_W_enu_1000events",
                                               delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetNbinsX(),
                                               delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetXaxis().GetXmin(),
                                               delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetXaxis().GetXmax()
                                             )
numberOfEntries_ff_W_enu_1000events = delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetEntries()
efficiencyPlot_ff_W_enu_1000events.SetBinContent(1, numberOfEntries_ff_W_enu_1000events)
for binNumber_ff_W_enu_1000events in xrange(2, efficiencyPlot_ff_W_enu_1000events.GetNbinsX() + 1):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_W_enu_1000events.SetBinContent(
                                                        binNumber_ff_W_enu_1000events,
                                                        efficiencyPlot_ff_W_enu_1000events.GetBinContent(binNumber_ff_W_enu_1000events - 1) - delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetBinContent(binNumber_ff_W_enu_1000events - 1)
                                                      )
# Normalise to 1
efficiencyPlot_ff_W_enu_1000events.Scale(1/numberOfEntries_ff_W_enu_1000events)
efficiencyPlot_ff_W_enu_1000events.SetXTitle("Threshold [GeV]")
efficiencyPlot_ff_W_enu_1000events.SetYTitle("Efficiency")
efficiencyPlot_ff_W_enu_1000events.Draw("HIST")
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_W_enu_1000events.svg", "svg")

# Muons in W production
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_W_munu_1000events = TH1F(
                                               "efficiencyPlot_ff_W_munu_1000events",
                                               "Efficiency ff_W_munu_1000events",
                                               delphesSim_ff_W_munu_1000events.muonLeadingRecoPtDistribution.GetNbinsX(),
                                               delphesSim_ff_W_munu_1000events.muonLeadingRecoPtDistribution.GetXaxis().GetXmin(),
                                               delphesSim_ff_W_munu_1000events.muonLeadingRecoPtDistribution.GetXaxis().GetXmax()
                                             )
numberOfEntries_ff_W_munu_1000events = delphesSim_ff_W_munu_1000events.muonLeadingRecoPtDistribution.GetEntries()
efficiencyPlot_ff_W_munu_1000events.SetBinContent(1, numberOfEntries_ff_W_munu_1000events)
for binNumber_ff_W_munu_1000events in xrange(2, efficiencyPlot_ff_W_munu_1000events.GetNbinsX() + 1):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_W_munu_1000events.SetBinContent(
                                                        binNumber_ff_W_munu_1000events,
                                                        efficiencyPlot_ff_W_munu_1000events.GetBinContent(binNumber_ff_W_munu_1000events - 1) - delphesSim_ff_W_munu_1000events.muonLeadingRecoPtDistribution.GetBinContent(binNumber_ff_W_munu_1000events - 1)
                                                      )
# Normalise to 1
efficiencyPlot_ff_W_munu_1000events.Scale(1/numberOfEntries_ff_W_munu_1000events)
efficiencyPlot_ff_W_munu_1000events.SetXTitle("Threshold [GeV]")
efficiencyPlot_ff_W_munu_1000events.SetYTitle("Efficiency")
efficiencyPlot_ff_W_munu_1000events.Draw("HIST")
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_W_munu_1000events.svg", "svg")

# Electrons in Z production
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_Z_ee_1000events = TH1F(
                                               "efficiencyPlot_ff_Z_ee_1000events",
                                               "Efficiency ff_Z_ee_1000events",
                                               delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetNbinsX(),
                                               delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetXaxis().GetXmin(),
                                               delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetXaxis().GetXmax()
                                             )
numberOfEntries_ff_Z_ee_1000events = delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetEntries()
efficiencyPlot_ff_Z_ee_1000events.SetBinContent(1, numberOfEntries_ff_Z_ee_1000events)
for binNumber_ff_Z_ee_1000events in xrange(2, efficiencyPlot_ff_Z_ee_1000events.GetNbinsX() + 1):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_Z_ee_1000events.SetBinContent(
                                                        binNumber_ff_Z_ee_1000events,
                                                        efficiencyPlot_ff_Z_ee_1000events.GetBinContent(binNumber_ff_Z_ee_1000events - 1) - delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetBinContent(binNumber_ff_Z_ee_1000events - 1)
                                                      )
# Normalise to 1
efficiencyPlot_ff_Z_ee_1000events.Scale(1/numberOfEntries_ff_Z_ee_1000events)
efficiencyPlot_ff_Z_ee_1000events.SetXTitle("Threshold [GeV]")
efficiencyPlot_ff_Z_ee_1000events.SetYTitle("Efficiency")
efficiencyPlot_ff_Z_ee_1000events.Draw("HIST")
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_Z_ee_1000events.svg", "svg")

# Muons in Z production
# Building a TH1F with the same binning properties as the leadingPt distribution
efficiencyPlot_ff_Z_mumu_1000events = TH1F(
                                               "efficiencyPlot_ff_Z_mumu_1000events",
                                               "Efficiency ff_Z_mumu_1000events",
                                               delphesSim_ff_Z_mumu_1000events.muonLeadingRecoPtDistribution.GetNbinsX(),
                                               delphesSim_ff_Z_mumu_1000events.muonLeadingRecoPtDistribution.GetXaxis().GetXmin(),
                                               delphesSim_ff_Z_mumu_1000events.muonLeadingRecoPtDistribution.GetXaxis().GetXmax()
                                             )
numberOfEntries_ff_Z_mumu_1000events = delphesSim_ff_Z_mumu_1000events.muonLeadingRecoPtDistribution.GetEntries()
efficiencyPlot_ff_Z_mumu_1000events.SetBinContent(1, numberOfEntries_ff_Z_mumu_1000events)
for binNumber_ff_Z_mumu_1000events in xrange(2, efficiencyPlot_ff_Z_mumu_1000events.GetNbinsX() + 1):
  # Each bin will represent the fraction of particles with pt higher than the one of the bin
  efficiencyPlot_ff_Z_mumu_1000events.SetBinContent(
                                                        binNumber_ff_Z_mumu_1000events,
                                                        efficiencyPlot_ff_Z_mumu_1000events.GetBinContent(binNumber_ff_Z_mumu_1000events - 1) - delphesSim_ff_Z_mumu_1000events.muonLeadingRecoPtDistribution.GetBinContent(binNumber_ff_Z_mumu_1000events - 1)
                                                      )
# Normalise to 1
efficiencyPlot_ff_Z_mumu_1000events.Scale(1/numberOfEntries_ff_H_ZZ_eeee_1000events)
efficiencyPlot_ff_Z_mumu_1000events.SetXTitle("Threshold [GeV]")
efficiencyPlot_ff_Z_mumu_1000events.SetYTitle("Efficiency")
efficiencyPlot_ff_Z_mumu_1000events.Draw("HIST")
canvas.Update()
canvas.Draw()
canvas.Print("efficiencyPlot_ff_Z_mumu_1000events.svg", "svg")