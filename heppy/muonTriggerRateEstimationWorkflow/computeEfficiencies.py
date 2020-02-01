from ROOT import TFile
from ROOT import TH1F
from ROOT import TCanvas
from ROOT import TChain
from numpy import zeros
from numpy import float32
import argparse
import ast
from bisect import bisect_right

def computeEfficiencies(**kwargs):
  chainGenObj = TChain (kwargs["GenObjTree"])
  chainGenObj.Add(kwargs["GenObjFileFolder"]+"/*.root")

  chainL1TObjGenObj = TChain(kwargs["MatchTree"])
  chainL1TObjGenObj.Add(kwargs["MatchFileFolder"]+"/*.root")

  bins = ast.literal_eval(kwargs["binning"])
  detectorEta = float(kwargs["eta"])
  quality = int(kwargs["quality"])
  barrelEta = float(kwargs["barrelEta"])
  minPtInBarrel = float(kwargs["minPtInBarrel"])
  minPtInEndcap = float(kwargs["minPtInEndcap"])
  deltaR2Matching = float(kwargs["deltaR2Matching"])
  deltaEtaMatching = float(kwargs["deltaEtaMatching"])
  
  conversion_factors = []

  numberOfGenObject = zeros(len(bins), float32)
  numberOfMatchedObject = zeros(len(bins), float32)
  conversion_factors = zeros(len(bins), float32)

  nEntries = chainGenObj.GetEntries()
  for entryIndex in xrange(0, nEntries):
    if entryIndex % 1000 == 0:
      print entryIndex, "/", nEntries
    chainGenObj.GetEntry(entryIndex)
    genObj_pt = getattr(chainGenObj, "genParticle_pt", getattr(chainGenObj, "genMuon_pt", None))
    genObj_eta = getattr(chainGenObj, "genParticle_eta", getattr(chainGenObj, "genMuon_eta", None))
    isGoodMuon = False
    if ((abs(genObj_eta) < barrelEta) and (genObj_pt > minPtInBarrel)):
      isGoodMuon = True
    # If not in barrel check if it is in the endcap acceptance
    elif ((abs(genObj_eta) >= barrelEta) and (abs(genObj_eta) < detectorEta) and (genObj_pt > minPtInEndcap)): 
      isGoodMuon = True
    if not isGoodMuon: continue
    # Looking for the correct bin
    binNumber = bisect_right(bins, genObj_pt) - 1
    if binNumber < 0:
      print "Entry lost in underflow!" 
      continue
    numberOfGenObject[binNumber] += 1
  
  nEntries = chainL1TObjGenObj.GetEntries()
  for entryIndex in xrange(0, nEntries):
    if entryIndex % 1000 == 0:
      print entryIndex, "/", nEntries
    chainL1TObjGenObj.GetEntry(entryIndex)
    genObj_pt = getattr(chainL1TObjGenObj, "genParticle_pt", getattr(chainL1TObjGenObj, "genMuon_pt", None))
    genObj_eta = getattr(chainL1TObjGenObj, "genParticle_eta", getattr(chainL1TObjGenObj, "genMuon_eta", None))
    l1tMuon_eta = chainL1TObjGenObj.l1tMuon_eta
    deltaR2 = chainL1TObjGenObj.deltaR2
    #Checking if the gen and l1t objects are enough close
    if (deltaR2 > deltaR2Matching) and (abs(genObj_eta - l1tMuon_eta) < deltaEtaMatching):
      continue
    # There are two different pt threshold based on the muon eta
    # If in barrel and the momentum is higher than the threshold, muon is good
    isGoodMuon = False
    
    if (genObj_pt < 0): # Rejecting non-matches
      continue
      
    if ((abs(genObj_eta) < barrelEta) and (genObj_pt > minPtInBarrel)):
      isGoodMuon = True
    # If not in barrel check if it is in the endcap acceptance
    elif ((abs(genObj_eta) >= barrelEta) and (abs(genObj_eta) < detectorEta) and (genObj_pt > minPtInEndcap)): 
      isGoodMuon = True
    if not isGoodMuon: continue

    l1tMuon_qual = chainL1TObjGenObj.l1tMuon_qual
    # Looking for the correct bin
    binNumber = bisect_right(bins, genObj_pt) - 1
    if l1tMuon_qual < quality : 
      continue
    if binNumber < 0:
      print "Entry lost in underflow!" 
      continue
    numberOfMatchedObject[binNumber] += 1

  return numberOfMatchedObject, numberOfGenObject

if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  parser.add_argument('--GenObjTree', type=str)
  parser.add_argument('--GenObjFileFolder', type=str)
  parser.add_argument('--MatchTree', type=str)
  parser.add_argument('--MatchFileFolder', type=str)
  parser.add_argument('--binning', type=str)
  parser.add_argument('--eta', type=float)
  parser.add_argument('--quality', type=int)
  parser.add_argument('--barrelEta', type=float)
  parser.add_argument('--minPtInBarrel', type=float)
  parser.add_argument('--minPtInEndcap', type=float)
  parser.add_argument('--deltaR2Matching', type=float)
  parser.add_argument('--deltaEtaMatching', type=float)


  args = parser.parse_args()

  accepted, total = computeEfficiencies(
    GenObjTree = args.GenObjTree,
    GenObjFileFolder = args.GenObjFileFolder,
    MatchTree = args.MatchTree,
    MatchFileFolder = args.MatchFileFolder,
    binning = args.binning,
    eta = args.eta,
    quality = args.quality,
    barrelEta = args.barrelEta,
    minPtInBarrel = args.minPtInBarrel,
    minPtInEndcap = args.minPtInEndcap,
    deltaR2Matching=args.deltaR2Matching,
    deltaEtaMatching=args.deltaEtaMatching,
  )
  factors = accepted/total
  print "Conversion factors are", factors
