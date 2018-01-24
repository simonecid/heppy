from ROOT import TFile
from ROOT import TH1F
from ROOT import TCanvas
from ROOT import TChain
from numpy import zeros
from numpy import float32
import argparse
import ast
from bisect import bisect_right
from array import array
import os

def computeEfficiencies(numberOfFiles=-1, **kwargs):
  chainGenObj = TChain (kwargs["GenObjTree"])
  chainL1TObjGenObj = TChain(kwargs["MatchTree"])
  if numberOfFiles < 0:
    chainGenObj.Add(kwargs["GenObjFileFolder"]+"/*")
    chainL1TObjGenObj.Add(kwargs["MatchFileFolder"]+"/*")
  if numberOfFiles >= 0:
    genObjFiles = os.listdir(kwargs["GenObjFileFolder"])
    matchFiles = os.listdir(kwargs["MatchFileFolder"])
    if numberOfFiles > len(matchFiles):
      numberOfFiles = len(matchFiles)
    
    for x in xrange(0, numberOfFiles):
      chainGenObj.Add(kwargs["GenObjFileFolder"] + "/" + genObjFiles[x])
      chainL1TObjGenObj.Add(kwargs["MatchFileFolder"] + "/" + matchFiles[x])

  bins = ast.literal_eval(kwargs["binning"])
  detectorEta = float(kwargs["eta"])
  quality = int(kwargs["quality"])
  barrelEta = float(kwargs["barrelEta"])
  endcapEta = float(kwargs["endcapEta"])
  minPtInBarrel = float(kwargs["minPtInBarrel"])
  minPtInEndcap = float(kwargs["minPtInEndcap"])
  minPtInForward = float(kwargs["minPtInForward"])
  deltaR2Matching = float(kwargs["deltaR2Matching"])
  
  conversion_factors = []

  numberOfGenObject = zeros(len(bins), float32)
  numberOfMatchedObject = zeros(len(bins), float32)
  conversion_factors = zeros(len(bins), float32)

  nEntries = chainGenObj.GetEntries()

  chainGenObj.GetEntry(0)
  isLeadingGenJet = hasattr("leadingGenJet_pt", chainGenObj)

  for entryIndex in xrange(0, nEntries):
    if entryIndex % 1000 == 0:
      print entryIndex, "/", nEntries
    chainGenObj.GetEntry(entryIndex)
    if isLeadingGenJet:
      genObj_pt = chainGenObj.leadingGenJet_pt
      genObj_eta = chainGenObj.leadingGenJet_eta
    else:
      genObj_pt = chainGenObj.genJet_pt
      genObj_eta = chainGenObj.genJet_eta
    isGoodMuon = False
    if ((abs(genObj_eta) < barrelEta) and (genObj_pt > minPtInBarrel)):
      isGoodMuon = True
    # If not in barrel check if it is in the endcap acceptance
    elif ((abs(genObj_eta) >= barrelEta) and (abs(genObj_eta) < endcapEta) and (genObj_pt > minPtInEndcap)): 
      isGoodMuon = True
    # check if is in forward
    elif ((abs(genObj_eta) >= endcapEta) and (abs(genObj_eta) < detectorEta) and (genObj_pt > minPtInForward)): 
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
    if isLeadingGenJet:
      genObj_pt = chainL1TObjGenObj.leadingGenJet_pt
      genObj_eta = chainL1TObjGenObj.leadingGenJet_eta
    else:
      genObj_pt = chainL1TObjGenObj.genJet_pt
      genObj_eta = chainL1TObjGenObj.genJet_eta
    deltaR2 = chainL1TObjGenObj.deltaR2

    #Checking if the gen and l1t objects are enough close
    if (deltaR2 > deltaR2Matching): continue
    # There are two different pt threshold based on the muon eta
    # If in barrel and the momentum is higher than the threshold, muon is good

    isGoodMuon = False
    if ((abs(genObj_eta) < barrelEta) and (genObj_pt > minPtInBarrel)):
      isGoodMuon = True
    # If not in barrel check if it is in the endcap acceptance
    elif ((abs(genObj_eta) >= barrelEta) and (abs(genObj_eta) < endcapEta) and (genObj_pt > minPtInEndcap)): 
      isGoodMuon = True
      # check if is in forward
    elif ((abs(genObj_eta) >= endcapEta) and (abs(genObj_eta) < detectorEta) and (genObj_pt > minPtInForward)): 
      isGoodMuon = True
    if not isGoodMuon: continue

    #l1tMuon_qual = chainL1TObjGenObj.l1tMuon_qual
    l1tMuon_qual = 0
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
  parser.add_argument('--endcapEta', type=float)
  parser.add_argument('--minPtInBarrel', type=float)
  parser.add_argument('--minPtInEndcap', type=float)
  parser.add_argument('--minPtInForward', type=float)
  parser.add_argument('--deltaR2Matching', type=float)

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
    endcapEta = args.endcapEta,
    minPtInBarrel = args.minPtInBarrel,
    minPtInEndcap = args.minPtInEndcap,
    minPtInForward = args.minPtInForward,
    deltaR2Matching = args.deltaR2Matching,
  )
  factors = accepted/total
  print "Conversion factors are", factors
