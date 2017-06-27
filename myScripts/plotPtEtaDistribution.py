'''
  Plots pt eta distribution from ROOT file
'''

from ROOT import TFile
from ROOT import TMultiGraph
from ROOT import TGraph
from ROOT import TLegend
from ROOT import TCanvas
from ROOT import gStyle
from ROOT import TLine
from ROOT import TH2F
from array import array

import sys

gStyle.SetOptStat(0)

distributionFile = TFile("minBias_13TeV_DelphesCMS_particleDistributions/MinBiasDistribution_13TeV_DelphesCMS.root")
jetPtEtaDistribution = distributionFile.Get("jetPtEtaDistribution")

canvas = TCanvas()

jetPtEtaDistribution.Scale(1./500000.*0.05679)

jetPtEtaDistribution.GetXaxis().SetRangeUser(0, 300)
jetPtEtaDistribution.GetYaxis().SetRangeUser(-6, 6)

jetPtEtaDistribution.Draw("COLZ")

canvas.Print("jetPtEtaDistribution.png", "png")