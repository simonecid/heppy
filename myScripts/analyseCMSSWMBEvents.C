#include "TH1F.h"
#include "TTree.h"
#include "TFile.h"

int analyseCMSSWMBEvents(){
  TChain * genJetNoNuTree = new TChain("SaveGenLevelInfo/genJetNoNuTree");
  TChain * leadingGenJetNoNuTree = new TChain("SaveGenLevelInfo/leadingGenJetNoNuTree");
  TChain * genMuonTree = new TChain("SaveGenLevelInfo/genMuonTree");
  TChain * leadingGenMuonTree = new TChain("SaveGenLevelInfo/leadingGenMuonTree");
  TChain * numberOfGenJetNoNuInEventTree = new TChain("SaveGenLevelInfo/numberOfGenJetNoNuInEventTree");
  TChain * numberOfGenMuonInEventTree = new TChain("SaveGenLevelInfo/numberOfGenMuonInEventTree");

  genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3569173.35.root");
  genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.101.root");
  genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.102.root");
  genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.103.root");
  genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.104.root");
  genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.105.root");
  genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.106.root");
  genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.107.root");
  genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.108.root");

  genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3569173.35.root");
  genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.101.root");
  genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.102.root");
  genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.103.root");
  genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.104.root");
  genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.105.root");
  genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.106.root");
  genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.107.root");
  genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.108.root");

  leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3569173.35.root");
  leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.101.root");
  leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.102.root");
  leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.103.root");
  leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.104.root");
  leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.105.root");
  leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.106.root");
  leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.107.root");
  leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.108.root");

  leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3569173.35.root");
  leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.101.root");
  leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.102.root");
  leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.103.root");
  leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.104.root");
  leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.105.root");
  leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.106.root");
  leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.107.root");
  leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.108.root");

  numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3569173.35.root");
  numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.101.root");
  numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.102.root");
  numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.103.root");
  numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.104.root");
  numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.105.root");
  numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.106.root");
  numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.107.root");
  numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.108.root");

  numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3569173.35.root");
  numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.101.root");
  numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.102.root");
  numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.103.root");
  numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.104.root");
  numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.105.root");
  numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.106.root");
  numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.107.root");
  numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.108.root");


  //genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //genJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  //genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //genMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  //leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //leadingGenJetNoNuTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  //leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //leadingGenMuonTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  //numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //numberOfGenJetNoNuInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");
  //numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.10*.root");
  //numberOfGenMuonInEventTree -> Add("/hdfs/FCC-hh/MinBias_TuneCUETP8M1_14TeV_GenInfo/MinBias_TuneCUETP8M1_14TeV_GenInfo_3570581.100.root");


  TFile *delphesPlots = new TFile("MinimumBias_14TeV_GenParticles_full_GenDistributions/distributions_merged.root");
    
  TH1F* genJetPtDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genJetPtDistribution"));
  TH1F* genJetPtDistribution_CMSSW = static_cast<TH1F*>(genJetPtDistribution_Delphes -> Clone("genJetPtDistribution_CMSSW"));
  
  TH1F* genJetLeadingPtDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genJetLeadingPtDistribution"));
  TH1F* genJetLeadingPtDistribution_CMSSW = static_cast<TH1F*>(genJetLeadingPtDistribution_Delphes -> Clone("genJetLeadingPtDistribution_CMSSW"));
  
  TH1F* genJetEtaDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genJetEtaDistribution"));
  TH1F* genJetEtaDistribution_CMSSW = static_cast<TH1F*>(genJetEtaDistribution_Delphes -> Clone("genJetEtaDistribution_CMSSW"));
  
  TH1F* genJetLeadingEtaDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genJetLeadingEtaDistribution"));
  TH1F* genJetLeadingEtaDistribution_CMSSW = static_cast<TH1F*>(genJetLeadingEtaDistribution_Delphes -> Clone("genJetLeadingEtaDistribution_CMSSW"));
  
  TH1F* numberOfGenJetsInEventDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("numberOfGenJetsInEventDistribution"));
  TH1F* numberOfGenJetsInEventDistribution_CMSSW = static_cast<TH1F*>(numberOfGenJetsInEventDistribution_Delphes -> Clone("numberOfGenJetsInEventDistribution_CMSSW"));
  
  TH1F* genMuonPtDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genMuonPtDistribution"));
  TH1F* genMuonPtDistribution_CMSSW = static_cast<TH1F*>(genMuonPtDistribution_Delphes -> Clone("genMuonPtDistribution_CMSSW"));
  
  TH1F* genMuonLeadingPtDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genMuonLeadingPtDistribution"));
  TH1F* genMuonLeadingPtDistribution_CMSSW = static_cast<TH1F*>(genMuonLeadingPtDistribution_Delphes -> Clone("genMuonLeadingPtDistribution_CMSSW"));
  
  TH1F* genMuonEtaDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genMuonEtaDistribution"));
  TH1F* genMuonEtaDistribution_CMSSW = static_cast<TH1F*>(genMuonEtaDistribution_Delphes -> Clone("genMuonEtaDistribution_CMSSW"));
  
  TH1F* genMuonLeadingEtaDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("genMuonLeadingEtaDistribution"));
  TH1F* genMuonLeadingEtaDistribution_CMSSW = static_cast<TH1F*>(genMuonLeadingEtaDistribution_Delphes -> Clone("genMuonLeadingEtaDistribution_CMSSW"));
  
  TH1F* numberOfGenMuonsInEventDistribution_Delphes = static_cast<TH1F*>(delphesPlots -> Get("numberOfGenMuonsInEventDistribution"));
  TH1F* numberOfGenMuonsInEventDistribution_CMSSW = static_cast<TH1F*>(numberOfGenMuonsInEventDistribution_Delphes -> Clone("numberOfGenMuonsInEventDistribution_CMSSW"));

  genJetPtDistribution_CMSSW -> Reset();
  std::cout << "genJet_pt >> genJetPtDistribution_CMSSW" << std::endl;
  genJetNoNuTree -> Draw("genJet_pt >> genJetPtDistribution_CMSSW", "", "goff");
  genJetLeadingPtDistribution_CMSSW -> Reset();
  std::cout << "genJet_pt >> genJetLeadingPtDistribution_CMSSW" << std::endl;
  leadingGenJetNoNuTree -> Draw("genJet_pt >> genJetLeadingPtDistribution_CMSSW", "", "goff");
  genJetEtaDistribution_CMSSW -> Reset();
  std::cout << "genJet_eta >> genJetEtaDistribution_CMSSW" << std::endl;
  genJetNoNuTree -> Draw("genJet_eta >> genJetEtaDistribution_CMSSW", "", "goff");
  genJetLeadingEtaDistribution_CMSSW -> Reset();
  std::cout << "genJet_eta >> genJetLeadingEtaDistribution_CMSSW" << std::endl;
  leadingGenJetNoNuTree -> Draw("genJet_eta >> genJetLeadingEtaDistribution_CMSSW", "", "goff");
  numberOfGenJetsInEventDistribution_CMSSW -> Reset();
  std::cout << "numberOfGenJetInEvent >> numberOfGenJetsInEventDistribution_CMSSW" << std::endl;
  numberOfGenJetNoNuInEventTree -> Draw("numberOfGenJetInEvent >> numberOfGenJetsInEventDistribution_CMSSW", "", "goff");
  genMuonPtDistribution_CMSSW -> Reset();
  std::cout << "genMuon_pt >> genMuonPtDistribution_CMSSW" << std::endl;
  genMuonTree -> Draw("genMuon_pt >> genMuonPtDistribution_CMSSW", "", "goff");
  genMuonLeadingPtDistribution_CMSSW -> Reset();
  std::cout << "genMuon_pt >> genMuonLeadingPtDistribution_CMSSW" << std::endl;
  leadingGenMuonTree -> Draw("genMuon_pt >> genMuonLeadingPtDistribution_CMSSW", "", "goff");
  genMuonEtaDistribution_CMSSW -> Reset();
  std::cout << "genMuon_eta >> genMuonEtaDistribution_CMSSW" << std::endl;
  genMuonTree -> Draw("genMuon_eta >> genMuonEtaDistribution_CMSSW", "", "goff");
  genMuonLeadingEtaDistribution_CMSSW -> Reset();
  std::cout << "genMuon_eta >> genMuonLeadingEtaDistribution_CMSSW" << std::endl;
  leadingGenMuonTree -> Draw("genMuon_eta >> genMuonLeadingEtaDistribution_CMSSW", "", "goff");
  numberOfGenMuonsInEventDistribution_CMSSW -> Reset();
  std::cout << "numberOfGenMuonInEvent >> numberOfGenMuonsInEventDistribution_CMSSW" << std::endl;
  numberOfGenMuonInEventTree -> Draw("numberOfGenMuonInEvent >> numberOfGenMuonsInEventDistribution_CMSSW", "", "goff");

  TFile *cmsswPlots = new TFile("MinimumBias_14TeV_GenParticles_full_GenDistributions/distributions_fromcmssw.root", "RECREATE");  
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

  TFile *normalisedPlots = new TFile("MinimumBias_14TeV_GenParticles_full_GenDistributions/distributions_normalised.root", "RECREATE");    
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