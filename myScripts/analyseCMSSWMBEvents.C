#include "TH1F.h"
#include "TTree.h"
#include "TFile.h"

int analyseCMSSWMBEvents(){
  TChain * genJetNoNuTreeCMSSW = new TChain("SaveGenLevelInfo/genJetNoNuTree");
  TChain * leadingGenJetNoNuTreeCMSSW = new TChain("SaveGenLevelInfo/leadingGenJetNoNuTree");
  TChain * genMuonTreeCMSSW = new TChain("SaveGenLevelInfo/genMuonTree");
  TChain * leadingGenMuonTreeCMSSW = new TChain("SaveGenLevelInfo/leadingGenMuonTree");
  TChain * numberOfGenJetNoNuInEventTreeCMSSW = new TChain("SaveGenLevelInfo/numberOfGenJetNoNuInEventTree");
  TChain * numberOfGenMuonInEventTreeCMSSW = new TChain("SaveGenLevelInfo/numberOfGenMuonInEventTree");

  TChain * genJetNoNuTreeDelphes = new TChain("jetTree");
  genJetNoNuTreeDelphes -> Add("_MinBias_CMSSWTune/MinimumBias_100TeV_GenParticles_full_CMSSWTune_WPropagation_1MEvents/distributions.root");
  TChain * genMuonTreeDelphes = new TChain("muonTree");
  genMuonTreeDelphes -> Add("_MinBias_CMSSWTune/MinimumBias_100TeV_GenParticles_full_CMSSWTune_WPropagation_1MEvents/distributions.root");

  genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.96.root");
//  genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.97.root");
//  genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.98.root");
//  genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.99.root");
//  genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.9.root");
//  genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570599.93.root");
//  genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570601.79.root");
//  genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570602.0.root");
//  genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570603.3.root");
//  genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570604.4.root");
//  genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570606.86.root");

  genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.96.root");
//  genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.97.root");
//  genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.98.root");
//  genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.99.root");
//  genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.9.root");
//  genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570599.93.root");
//  genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570601.79.root");
//  genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570602.0.root");
//  genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570603.3.root");
//  genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570604.4.root");
//  genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570606.86.root");

  leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.96.root");
//  leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.97.root");
//  leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.98.root");
//  leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.99.root");
//  leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.9.root");
//  leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570599.93.root");
//  leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570601.79.root");
//  leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570602.0.root");
//  leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570603.3.root");
//  leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570604.4.root");
//  leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570606.86.root");

  leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.96.root");
//  leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.97.root");
//  leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.98.root");
//  leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.99.root");
//  leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.9.root");
//  leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570599.93.root");
//  leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570601.79.root");
//  leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570602.0.root");
//  leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570603.3.root");
//  leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570604.4.root");
//  leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570606.86.root");

  numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.96.root");
//  numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.97.root");
//  numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.98.root");
//  numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.99.root");
//  numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.9.root");
//  numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570599.93.root");
//  numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570601.79.root");
//  numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570602.0.root");
//  numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570603.3.root");
//  numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570604.4.root");
//  numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570606.86.root");

  numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.96.root");
//  numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.97.root");
//  numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.98.root");
//  numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.99.root");
//  numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.9.root");
//  numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570599.93.root");
//  numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570601.79.root");
//  numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570602.0.root");
//  numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570603.3.root");
//  numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570604.4.root");
//  numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570606.86.root");


  //genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //genJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  //genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //genMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  //leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //leadingGenJetNoNuTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  //leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //leadingGenMuonTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  //numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //numberOfGenJetNoNuInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  //numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //numberOfGenMuonInEventTreeCMSSW -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");


  //TFile *delphesPlots = new TFile("_MinBias_CMSSWTune/MinimumBias_14TeV_GenParticles_full_CMSSWTune_WPropagation/distributions.root");
  TFile *delphesPlots = new TFile("_MinBias_CMSSWTune/MinimumBias_100TeV_GenParticles_full_CMSSWTune_WPropagation_1MEvents/distributions.root");
  //  
  //TH1F* genJetPtDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genJetPtDistribution"));
  //TH1F* genJetPtDistribution_CMSSW = static_cast<TH1F*>(genJetPtDistribution_Delphes -> Clone("genJetPtDistribution_CMSSW"));
  //
  TH1F* genJetLeadingPtDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genJetLeadingPtDistribution"));
  TH1F* genJetLeadingPtDistribution_CMSSW = static_cast<TH1F*>(genJetLeadingPtDistribution_Delphes -> Clone("genJetLeadingPtDistribution_CMSSW"));
  //
  //TH1F* genJetEtaDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genJetEtaDistribution"));
  //TH1F* genJetEtaDistribution_CMSSW = static_cast<TH1F*>(genJetEtaDistribution_Delphes -> Clone("genJetEtaDistribution_CMSSW"));
  //
  TH1F* genJetLeadingEtaDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genJetLeadingEtaDistribution"));
  TH1F* genJetLeadingEtaDistribution_CMSSW = static_cast<TH1F*>(genJetLeadingEtaDistribution_Delphes -> Clone("genJetLeadingEtaDistribution_CMSSW"));
  
  TH1F* numberOfGenJetsInEventDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("numberOfGenJetsInEventDistribution"));
  TH1F* numberOfGenJetsInEventDistribution_CMSSW = static_cast<TH1F*>(numberOfGenJetsInEventDistribution_Delphes -> Clone("numberOfGenJetsInEventDistribution_CMSSW"));
  //
  //TH1F* genMuonPtDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genMuonPtDistribution"));
  //TH1F* genMuonPtDistribution_CMSSW = static_cast<TH1F*>(genMuonPtDistribution_Delphes -> Clone("genMuonPtDistribution_CMSSW"));
  //
  TH1F* genMuonLeadingPtDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genMuonLeadingPtDistribution"));
  TH1F* genMuonLeadingPtDistribution_CMSSW = static_cast<TH1F*>(genMuonLeadingPtDistribution_Delphes -> Clone("genMuonLeadingPtDistribution_CMSSW"));
  //
  //TH1F* genMuonEtaDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genMuonEtaDistribution"));
  //TH1F* genMuonEtaDistribution_CMSSW = static_cast<TH1F*>(genMuonEtaDistribution_Delphes -> Clone("genMuonEtaDistribution_CMSSW"));
  //
  TH1F* genMuonLeadingEtaDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genMuonLeadingEtaDistribution"));
  TH1F* genMuonLeadingEtaDistribution_CMSSW = static_cast<TH1F*>(genMuonLeadingEtaDistribution_Delphes -> Clone("genMuonLeadingEtaDistribution_CMSSW"));

  TH1F* numberOfGenMuonsInEventDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("numberOfGenMuonsInEventDistribution"));
  TH1F* numberOfGenMuonsInEventDistribution_CMSSW = static_cast<TH1F*>(numberOfGenMuonsInEventDistribution_Delphes -> Clone("numberOfGenMuonsInEventDistribution_CMSSW"));
  
  TH1F* genJetPtDistribution_Delphes = new TH1F("genJetPtDistribution_Delphes", "Gen Jet p_{t} distribution", 500, 0, 500);
  TH1F* genJetPtDistribution_CMSSW = new TH1F("genJetPtDistribution_CMSSW", "Gen Jet p_{t} distribution", 500, 0, 500);
  
  TH1F* genJetEtaDistribution_Delphes = new TH1F("genJetEtaDistribution_Delphes", "Gen jet #eta distribution", 100, -10, 10);
  TH1F* genJetEtaDistribution_CMSSW = new TH1F("genJetEtaDistribution_CMSSW", "Gen jet #eta distribution", 100, -10, 10);
  
  TH1F* genMuonPtDistribution_Delphes = new TH1F("genMuonPtDistribution_Delphes", "Gen muon p_{t} distribution", 500, 0, 500);
  TH1F* genMuonPtDistribution_CMSSW = new TH1F("genMuonPtDistribution_CMSSW", "Gen muon p_{t} distribution", 500, 0, 500);
  
  TH1F* genMuonEtaDistribution_Delphes = new TH1F("genMuonEtaDistribution_Delphes", "Gen muon #eta distribution", 100, -10, 10);
  TH1F* genMuonEtaDistribution_CMSSW = new TH1F("genMuonEtaDistribution_CMSSW", "Gen muon #eta distribution", 100, -10, 10);

  genJetPtDistribution_CMSSW -> Reset();
  std::cout << "genJet_pt >> genJetPtDistribution_CMSSW" << std::endl;
  genJetNoNuTreeCMSSW -> Draw("genJet_pt >> genJetPtDistribution_CMSSW", "", "goff");
  genJetNoNuTreeDelphes -> Draw("gen_jets_pt >> genJetPtDistribution_Delphes", "", "goff");
  genJetLeadingPtDistribution_CMSSW -> Reset();
  std::cout << "genJet_pt >> genJetLeadingPtDistribution_CMSSW" << std::endl;
  leadingGenJetNoNuTreeCMSSW -> Draw("genJet_pt >> genJetLeadingPtDistribution_CMSSW", "", "goff");
  genJetEtaDistribution_CMSSW -> Reset();
  std::cout << "genJet_eta >> genJetEtaDistribution_CMSSW" << std::endl;
  genJetNoNuTreeCMSSW -> Draw("genJet_eta >> genJetEtaDistribution_CMSSW", "", "goff");
  genJetNoNuTreeDelphes -> Draw("gen_jets_eta >> genJetEtaDistribution_Delphes", "", "goff");
  genJetLeadingEtaDistribution_CMSSW -> Reset();
  std::cout << "genJet_eta >> genJetLeadingEtaDistribution_CMSSW" << std::endl;
  leadingGenJetNoNuTreeCMSSW -> Draw("genJet_eta >> genJetLeadingEtaDistribution_CMSSW", "", "goff");
  numberOfGenJetsInEventDistribution_CMSSW -> Reset();
  std::cout << "numberOfGenJetInEvent >> numberOfGenJetsInEventDistribution_CMSSW" << std::endl;
  numberOfGenJetNoNuInEventTreeCMSSW -> Draw("numberOfGenJetInEvent >> numberOfGenJetsInEventDistribution_CMSSW", "", "goff");
  genMuonPtDistribution_CMSSW -> Reset();
  std::cout << "genMuon_pt >> genMuonPtDistribution_CMSSW" << std::endl;
  genMuonTreeCMSSW -> Draw("genMuon_pt >> genMuonPtDistribution_CMSSW", "", "goff");
  genMuonTreeDelphes -> Draw("muons_pt >> genMuonPtDistribution_Delphes", "", "goff");
  genMuonLeadingPtDistribution_CMSSW -> Reset();
  std::cout << "genMuon_pt >> genMuonLeadingPtDistribution_CMSSW" << std::endl;
  leadingGenMuonTreeCMSSW -> Draw("genMuon_pt >> genMuonLeadingPtDistribution_CMSSW", "", "goff");
  genMuonEtaDistribution_CMSSW -> Reset();
  std::cout << "genMuon_eta >> genMuonEtaDistribution_CMSSW" << std::endl;
  genMuonTreeCMSSW -> Draw("genMuon_eta >> genMuonEtaDistribution_CMSSW", "", "goff");
  genMuonTreeDelphes -> Draw("muons_eta >> genMuonEtaDistribution_Delphes", "", "goff");
  genMuonLeadingEtaDistribution_CMSSW -> Reset();
  std::cout << "genMuon_eta >> genMuonLeadingEtaDistribution_CMSSW" << std::endl;
  leadingGenMuonTreeCMSSW -> Draw("genMuon_eta >> genMuonLeadingEtaDistribution_CMSSW", "", "goff");
  numberOfGenMuonsInEventDistribution_CMSSW -> Reset();
  std::cout << "numberOfGenMuonInEvent >> numberOfGenMuonsInEventDistribution_CMSSW" << std::endl;
  numberOfGenMuonInEventTreeCMSSW -> Draw("numberOfGenMuonInEvent >> numberOfGenMuonsInEventDistribution_CMSSW", "", "goff");

  TFile *cmsswPlots = new TFile("_MinBias_CMSSWTune/distributions_fromcmssw_14TeV_1Mevents.root", "RECREATE");  
  cmsswPlots -> cd();
  genJetPtDistribution_CMSSW -> Write();
  genJetLeadingPtDistribution_CMSSW -> Write();
  genJetEtaDistribution_CMSSW -> Write();
  genJetLeadingEtaDistribution_CMSSW -> Write();
  numberOfGenJetsInEventDistribution_CMSSW -> Write();
  genMuonPtDistribution_CMSSW -> Write();
  genMuonLeadingPtDistribution_CMSSW -> Write();
  genMuonEtaDistribution_CMSSW -> Write();
  genMuonLeadingEtaDistribution_CMSSW -> Write();
  numberOfGenMuonsInEventDistribution_CMSSW -> Write();
  genJetPtDistribution_CMSSW -> SetDirectory(0);
  genJetLeadingPtDistribution_CMSSW -> SetDirectory(0);
  genJetEtaDistribution_CMSSW -> SetDirectory(0);
  genJetLeadingEtaDistribution_CMSSW -> SetDirectory(0);
  numberOfGenJetsInEventDistribution_CMSSW -> SetDirectory(0);
  genMuonPtDistribution_CMSSW -> SetDirectory(0);
  genMuonLeadingPtDistribution_CMSSW -> SetDirectory(0);
  genMuonEtaDistribution_CMSSW -> SetDirectory(0);
  genMuonLeadingEtaDistribution_CMSSW -> SetDirectory(0);
  numberOfGenMuonsInEventDistribution_CMSSW -> SetDirectory(0);
  cmsswPlots -> Close();

  TFile *delphesPlots_Save = new TFile("_MinBias_CMSSWTune/distributions_fromdelphes_100TeV_1Mevents.root", "RECREATE");  
  delphesPlots_Save -> cd();
  genJetPtDistribution_Delphes -> Write();
  genJetEtaDistribution_Delphes -> Write();
  genMuonPtDistribution_Delphes -> Write();
  genMuonEtaDistribution_Delphes -> Write();
  genJetLeadingPtDistribution_Delphes -> Write();
  genJetLeadingEtaDistribution_Delphes -> Write();
  numberOfGenJetsInEventDistribution_Delphes -> Write();
  genMuonLeadingPtDistribution_Delphes -> Write();
  genMuonLeadingEtaDistribution_Delphes -> Write();
  numberOfGenMuonsInEventDistribution_Delphes -> Write();
  genJetPtDistribution_Delphes -> SetDirectory(0);
  genJetEtaDistribution_Delphes -> SetDirectory(0);
  genMuonPtDistribution_Delphes -> SetDirectory(0);
  genMuonEtaDistribution_Delphes -> SetDirectory(0);
  delphesPlots_Save -> Close();

  TFile *normalisedPlots = new TFile("_MinBias_CMSSWTune/distributions_normalised.root", "RECREATE");    
  normalisedPlots->cd();
  genJetPtDistribution_CMSSW -> Scale(1./genJetPtDistribution_CMSSW -> GetEntries());
  genJetPtDistribution_CMSSW -> Write();
  genJetLeadingPtDistribution_CMSSW -> Scale(1./genJetLeadingPtDistribution_CMSSW -> GetEntries());
  genJetLeadingPtDistribution_CMSSW -> Write();
  genJetEtaDistribution_CMSSW -> Scale(1./genJetEtaDistribution_CMSSW -> GetEntries());
  genJetEtaDistribution_CMSSW -> Write();
  genJetLeadingEtaDistribution_CMSSW -> Scale(1./genJetLeadingEtaDistribution_CMSSW -> GetEntries());
  genJetLeadingEtaDistribution_CMSSW -> Write();
  numberOfGenJetsInEventDistribution_CMSSW -> Scale(1./numberOfGenJetsInEventDistribution_CMSSW -> GetEntries());
  numberOfGenJetsInEventDistribution_CMSSW -> Write();
  genMuonPtDistribution_CMSSW -> Scale(1./genMuonPtDistribution_CMSSW -> GetEntries());
  genMuonPtDistribution_CMSSW -> Write();
  genMuonLeadingPtDistribution_CMSSW -> Scale(1./genMuonLeadingPtDistribution_CMSSW -> GetEntries());
  genMuonLeadingPtDistribution_CMSSW -> Write();
  genMuonEtaDistribution_CMSSW -> Scale(1./genMuonEtaDistribution_CMSSW -> GetEntries());
  genMuonEtaDistribution_CMSSW -> Write();
  genMuonLeadingEtaDistribution_CMSSW -> Scale(1./genMuonLeadingEtaDistribution_CMSSW -> GetEntries());
  genMuonLeadingEtaDistribution_CMSSW -> Write();
  numberOfGenMuonsInEventDistribution_CMSSW -> Scale(1./numberOfGenMuonsInEventDistribution_CMSSW -> GetEntries());
  numberOfGenMuonsInEventDistribution_CMSSW -> Write();
  genJetPtDistribution_Delphes -> Scale(1./genJetPtDistribution_Delphes -> GetEntries());
  genJetPtDistribution_Delphes -> Write();
  genJetLeadingPtDistribution_Delphes -> Scale(1./genJetLeadingPtDistribution_Delphes -> GetEntries());
  genJetLeadingPtDistribution_Delphes -> Write();
  genJetEtaDistribution_Delphes -> Scale(1./genJetEtaDistribution_Delphes -> GetEntries());
  genJetEtaDistribution_Delphes -> Write();
  genJetLeadingEtaDistribution_Delphes -> Scale(1./genJetLeadingEtaDistribution_Delphes -> GetEntries());
  genJetLeadingEtaDistribution_Delphes -> Write();
  numberOfGenJetsInEventDistribution_Delphes -> Scale(1./numberOfGenJetsInEventDistribution_Delphes -> GetEntries());
  numberOfGenJetsInEventDistribution_Delphes -> Write();
  genMuonPtDistribution_Delphes -> Scale(1./genMuonPtDistribution_Delphes -> GetEntries());
  genMuonPtDistribution_Delphes -> Write();
  genMuonLeadingPtDistribution_Delphes -> Scale(1./genMuonLeadingPtDistribution_Delphes -> GetEntries());
  genMuonLeadingPtDistribution_Delphes -> Write();
  genMuonEtaDistribution_Delphes -> Scale(1./genMuonEtaDistribution_Delphes -> GetEntries());
  genMuonEtaDistribution_Delphes -> Write();
  genMuonLeadingEtaDistribution_Delphes -> Scale(1./genMuonLeadingEtaDistribution_Delphes -> GetEntries());
  genMuonLeadingEtaDistribution_Delphes -> Write();
  numberOfGenMuonsInEventDistribution_Delphes -> Scale(1./numberOfGenMuonsInEventDistribution_Delphes -> GetEntries());
  numberOfGenMuonsInEventDistribution_Delphes -> Write();
  normalisedPlots->Close();


  return 0;
}