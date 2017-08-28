from ROOT import TFile
from ROOT import TH1F
from ROOT import TCanvas
from ROOT import TChain

chainGenJet = TChain ("MatchGenJetWithL1Objects/genJetTree")
chainGenJet.Add("/hdfs/FCC-hh/l1tGenJetMatching_QCD_15_3000_NoPU_Phase1_HybridMatching_DeltaR_0.25/*")

chainL1TEGammaGenJet = TChain ("MatchGenJetWithL1Objects/matchedL1TEGammaGenJetTree")
chainL1TEGammaGenJet.Add("/hdfs/FCC-hh/l1tGenJetMatching_QCD_15_3000_NoPU_Phase1_HybridMatching_DeltaR_0.25/*")

bins = []

bins = [0, 5, 7, 9, 11, 13, 15, 18, 21, 24, 27, 30, 35, 40, 50, 60, 70, 80, 90, 100, 110, 120]
conversion_factors = []

#for x in xrange(0, 120, 10):
#  bins.append(x)

print "Bins are", bins

for x in xrange(0, len(bins) - 1):
  numberOfGenJet = float(chainGenJet.Draw("genJet_pt", "genJet_pt > " + str(bins[x]) + " && genJet_pt < " + str(bins[x+1])))
  numberOfMatchedL1TEGamma = float(chainL1TEGammaGenJet.Draw("genJet_pt", "genJet_pt > " + str(bins[x]) + " && genJet_pt < " + str(bins[x+1])))
  conversion_factor = numberOfMatchedL1TEGamma/numberOfGenJet
  print bins[x], "-", bins[x+1], numberOfMatchedL1TEGamma, "/", numberOfGenJet, "=", conversion_factor
  conversion_factors.append(conversion_factor)

print "Bins are", bins
print "Conversion factors are", conversion_factors