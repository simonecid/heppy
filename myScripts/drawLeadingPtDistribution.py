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

delphesSim_ff_H_WW_enuenu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_H_WW_enuenu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_H_WW_munumunu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_H_WW_munumunu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_H_ZZ_eeee_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_H_ZZ_eeee_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_H_ZZ_mumumumu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_H_ZZ_mumumumu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_W_enu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_W_enu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_W_munu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_W_munu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_Z_ee_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_Z_ee_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_Z_mumu_1000events = ParticleDistributionsFromDelphes("DelphesSim_ff_Z_mumu_1000events/EWProductionAndHiggs/distributions.root")

canvas = TCanvas()
canvas.SetLogy()

# Lumi and energy info
text = TPaveText(0.5, 0.84, 0.9, 0.9, "NDC")
text.AddText("L_{inst} = 5 #times 10^{34} cm^{-2} s^{-1}   #sqrt{s} = 100 TeV")

# Plotting stuff

delphesSim_ff_H_WW_enuenu_1000events = TFile("DelphesSim_ff_H_WW_enuenu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.SetTitle("Electron leading p_{t} distribution in H #rightarrow WW #rightarrow e#nu_{e}e#nu_{e}")
delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.SetStats(0)
delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetRangeUser(0, 150)
delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetTitle("p_{t} [GeV]")
delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetYaxis().SetTitle("Number of events")
delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetTitleOffset(1.2)
delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.GetYaxis().SetTitleOffset(1.2)
delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.SetMarkerStyle(21)
delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.SetMarkerColor(4)
delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.SetLineColor(1)
delphesSim_ff_H_WW_enuenu_1000events.electronLeadingRecoPtDistribution.Draw("PE")
text.Draw()
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_H_WW_enuenu_1000events.svg", "svg")
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_H_WW_enuenu_1000events.pdf", "pdf")
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_H_WW_enuenu_1000events.png", "png")

delphesSim_ff_W_enu_1000events = TFile("DelphesSim_ff_W_enu_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.SetTitle("Electron leading p_{t} distribution in W #rightarrow e#nu_{e}")
delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.SetStats(0)
delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetRangeUser(0, 150)
delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetTitle("p_{t} [GeV]")
delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetYaxis().SetTitle("Number of events")
delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetTitleOffset(1.2)
delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.GetYaxis().SetTitleOffset(1.2)
delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.SetMarkerStyle(21)
delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.SetMarkerColor(4)
delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.SetLineColor(1)
delphesSim_ff_W_enu_1000events.electronLeadingRecoPtDistribution.Draw("PE")
text.Draw()
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_W_enu_1000events.svg", "svg")
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_W_enu_1000events.pdf", "pdf")
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_W_enu_1000events.png", "png")

delphesSim_ff_H_ZZ_eeee_1000events = TFile("DelphesSim_ff_H_ZZ_eeee_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.SetTitle("Electron leading p_{t} distribution in H #rightarrow ZZ #rightarrow eeee")
delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.SetStats(0)
delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetRangeUser(0, 150)
delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetTitle("p_{t} [GeV]")
delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetYaxis().SetTitle("Number of events")
delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetTitleOffset(1.2)
delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.GetYaxis().SetTitleOffset(1.2)
delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.SetMarkerStyle(21)
delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.SetMarkerColor(4)
delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.SetLineColor(1)
delphesSim_ff_H_ZZ_eeee_1000events.electronLeadingRecoPtDistribution.Draw("PE")
text.Draw()
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_H_ZZ_eeee_1000events.svg", "svg")
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_H_ZZ_eeee_1000events.pdf", "pdf")
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_H_ZZ_eeee_1000events.png", "png")

delphesSim_ff_Z_ee_1000events = TFile("DelphesSim_ff_Z_ee_1000events/EWProductionAndHiggs/distributions.root")
delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.SetTitle("Electron leading p_{t} distribution in Z #rightarrow ee")
delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.SetStats(0)
delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetRangeUser(0, 150)
delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetTitle("p_{t} [GeV]")
delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetYaxis().SetTitle("Number of events")
delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetXaxis().SetTitleOffset(1.2)
delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.GetYaxis().SetTitleOffset(1.2)
delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.SetMarkerStyle(21)
delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.SetMarkerColor(4)
delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.SetLineColor(1)
delphesSim_ff_Z_ee_1000events.electronLeadingRecoPtDistribution.Draw("PE")
text.Draw()
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_Z_ee_1000events.svg", "svg")
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_Z_ee_1000events.pdf", "pdf")
canvas.Print("leadingRecoPtDistribution_delphesSim_ff_Z_ee_1000events.png", "png")