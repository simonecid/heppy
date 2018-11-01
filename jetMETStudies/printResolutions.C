void printResolutions() 
{

  TFile* _file_MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel = new TFile("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel_PU200_PF_PUSubtraction/genJet_l1tJet_convolutionCurves/histograms.root");
  TFile* _file_MatchAK4GenJetWithAK4JetFromPfClusters_Barrel = new TFile("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfClusters_Barrel_PU200_PF_PUSubtraction/genJet_l1tJet_convolutionCurves/histograms.root");
  TFile* _file_MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel = new TFile("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel_PU200_PF_PUSubtraction/genJet_l1tJet_convolutionCurves/histograms.root");
  TFile* _file_MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel = new TFile("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel_PU200_PF_PUSubtraction/genJet_l1tJet_convolutionCurves/histograms.root");

  TFile* _file_MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap = new TFile("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap_PU200_PF_PUSubtraction/genJet_l1tJet_convolutionCurves/histograms.root");
  TFile* _file_MatchAK4GenJetWithAK4JetFromPfClusters_Endcap = new TFile("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfClusters_Endcap_PU200_PF_PUSubtraction/genJet_l1tJet_convolutionCurves/histograms.root");
  TFile* _file_MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap = new TFile("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap_PU200_PF_PUSubtraction/genJet_l1tJet_convolutionCurves/histograms.root");
  TFile* _file_MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap = new TFile("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap_PU200_PF_PUSubtraction/genJet_l1tJet_convolutionCurves/histograms.root");

  std::vector<std::string> _histogramPrefix;
  _histogramPrefix.push_back("deltaPtDistributionBinnedInMatchedObject");
  _histogramPrefix.push_back("deltaPhiDistributionBinnedInMatchedObject");
  _histogramPrefix.push_back("deltaEtaDistributionBinnedInMatchedObject");

  std::vector<TFile*> _files;
  _files.push_back(_file_MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel);
  _files.push_back(_file_MatchAK4GenJetWithAK4JetFromPfClusters_Barrel);
  _files.push_back(_file_MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel);
  _files.push_back(_file_MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel);
  _files.push_back(_file_MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap);
  _files.push_back(_file_MatchAK4GenJetWithAK4JetFromPfClusters_Endcap);
  _files.push_back(_file_MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap);
  _files.push_back(_file_MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap);
  
  std::vector<std::string> _titles;
  _titles.push_back("AK4GenJet With AK4JetFromPfCandidates - Barrel");
  _titles.push_back("AK4GenJet With AK4JetFromPfClusters - Barrel");
  _titles.push_back("AK4GenJet With Phase1L1TJetFromPfCandidates - Barrel");
  _titles.push_back("AK4GenJet With Phase1L1TJetFromPfClusters - Barrel");
  _titles.push_back("AK4GenJet With AK4JetFromPfCandidates - Endcap");
  _titles.push_back("AK4GenJet With AK4JetFromPfClusters - Endcap");
  _titles.push_back("AK4GenJet With Phase1L1TJetFromPfCandidates - Endcap");
  _titles.push_back("AK4GenJet With Phase1L1TJetFromPfClusters - Endcap");

  std::vector<std::string> _outputFilenames;
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfClusters_Barrel");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithAK4JetFromPfClusters_Endcap");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap");

  
  for (TFile* _file: _files) {
    for (int x = 0; x < _file -> GetListOfKeys() -> GetSize(); x++) {
      //std::cout << "Normalising " << _file->GetName() << " -> " << _file -> GetListOfKeys() -> At(x) -> GetName() << std::endl;
      if (strcmp(_file -> GetListOfKeys() -> At(x) -> GetName(), "genJetL1TObjectTree") == 0) continue;
      TH1F * h = (TH1F*) _file->Get(_file -> GetListOfKeys() -> At(x) -> GetName());
      //Normalising every plot
      h -> Scale(1. / h -> GetEntries());
      h -> GetYaxis() -> SetTitle("a.u.");
    }
  }
  
  TH1F* h0;
  TH1F* h1;
  TH1F* h2;
  TH1F* h3;

  // SCALING THE PLOTS
  
  TCanvas* c1 = new TCanvas();

  //c1 -> SetLogy();

  /////////////////////////////////////////////////// 
  /////////////////////////////////////////////////// 
  /////////////// COMPARISON PLOTS ////////////////// 
  /////////////////////////////////////////////////// 
  ///////////////////////////////////////////////////

  for (const std::string & _prefix: _histogramPrefix) {
    for (int x = 0; x < _files.size(); x++) {
      TFile* _file = _files[x];

      std::cout << "Opening " << _file->GetName() << std::endl;

      h0 = (TH1F*) _file -> Get((_prefix + "_25_30").c_str());
      h1 = (TH1F*) _file -> Get((_prefix + "_40_45").c_str());
      h2 = (TH1F*) _file -> Get((_prefix + "_100_110").c_str());
      h3 = (TH1F*) _file -> Get((_prefix + "_175_200").c_str());

      h0 -> SetTitle(_titles[x].c_str());

      h0 -> GetYaxis() -> SetRangeUser(1e-5, 1.);

      h0 -> SetLineColor(1);
      h1 -> SetLineColor(2);
      h2 -> SetLineColor(3);
      h3 -> SetLineColor(4);

      h0 -> SetLineStyle(1);
      h1 -> SetLineStyle(1);
      h2 -> SetLineStyle(1);
      h3 -> SetLineStyle(1);

      h0->Draw("HIST ");
      h1->Draw("HIST SAME");
      h2->Draw("HIST SAME");
      h3->Draw("HIST SAME");

      TLegend* legend = new TLegend(0.1,0.7,0.48,0.9);
      legend -> AddEntry(h0, "25 < p_{t}^{gen-jet} < 30","l");
      legend -> AddEntry(h1, "40 < p_{t}^{gen-jet} < 45","l");
      legend -> AddEntry(h2, "100 < p_{t}^{gen-jet} < 110","l");
      legend -> AddEntry(h3, "175 < p_{t}^{gen-jet} < 200","l");
      legend -> Draw();

      c1->Print((_outputFilenames[x] + "_" + _prefix + ".pdf").c_str());
      c1->Print((_outputFilenames[x] + "_" + _prefix + ".png").c_str());
      delete legend;
    }
  }

  /////////////////////////////////////////////////// 
  /////////////////////////////////////////////////// 
  /////////////// BARREL VS ENDCAP PLOTS ////////////
  /////////////////////////////////////////////////// 
  /////////////////////////////////////////////////// 

  _histogramPrefix.clear();
  _histogramPrefix.push_back("deltaPtDistributionBinnedInMatchedObject");
  _histogramPrefix.push_back("deltaPhiDistributionBinnedInMatchedObject");
  _histogramPrefix.push_back("deltaEtaDistributionBinnedInMatchedObject");

  _titles.clear();
  _titles.push_back("AK4JetFromPfCandidates Barrel Vs Endcap 100 < p_{t}^{gen-jet} < 110");
  _titles.push_back("AK4JetFromPfClusters Barrel Vs Endcap 100 < p_{t}^{gen-jet} < 110");
  _titles.push_back("Phase1L1TJetFromPfCandidates Barrel Vs Endcap 100 < p_{t}^{gen-jet} < 110");
  _titles.push_back("Phase1L1TJetFromPfClusters Barrel Vs Endcap 100 < p_{t}^{gen-jet} < 110");

  _outputFilenames.clear();
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/AK4_PfCandidates_resolution_Barrel_vs_Endcap");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/AK4_PfClusters_resolution_Barrel_vs_Endcap");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/Phase1L1TJet_PfCandidates_resolution_Barrel_vs_Endcap");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/Phase1L1TJet_PfClusters_resolution_Barrel_vs_Endcap");

  for (const std::string & _prefix: _histogramPrefix) {
    for (int x = 0; x < _files.size()/2; x++) {
      
      TFile* _file0 = _files[x];
      TFile* _file1 = _files[x + (_files.size()/2)];

      h1 = (TH1F*) _file0 -> Get((_prefix + "_100_110").c_str());
      h2 = (TH1F*) _file1 -> Get((_prefix + "_100_110").c_str());

      h1 -> SetTitle(_titles[x].c_str());

      h1 -> GetYaxis() -> SetRangeUser(1e-5, 1.);

      h1 -> SetLineColor(1);
      h2 -> SetLineColor(2);

      h1 -> SetLineStyle(1);
      h2 -> SetLineStyle(1);

      h1->Draw("HIST ");
      h2->Draw("HIST SAME");

      TLegend * legend = new TLegend(0.1,0.7,0.3,0.9);
      legend -> AddEntry(h1, "Barrel","l");
      legend -> AddEntry(h2, "Endcap","l");
      legend -> Draw();
      
      c1->Print((_outputFilenames[x] + "_" + _prefix + ".pdf").c_str());
      c1->Print((_outputFilenames[x] + "_" + _prefix + ".png").c_str());
      delete legend;
    }
  }  

  /////////////////////////////////////////////////// 
  /////////////////////////////////////////////////// 
  /////////////// AK4 VS PHASE-1 PLOTS ////////////// 
  /////////////////////////////////////////////////// 
  /////////////////////////////////////////////////// 

  _files.clear();
  _files.push_back(_file_MatchAK4GenJetWithAK4JetFromPfCandidates_Barrel);
  _files.push_back(_file_MatchAK4GenJetWithAK4JetFromPfClusters_Barrel);
  _files.push_back(_file_MatchAK4GenJetWithAK4JetFromPfCandidates_Endcap);
  _files.push_back(_file_MatchAK4GenJetWithAK4JetFromPfClusters_Endcap);
  _files.push_back(_file_MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Barrel);
  _files.push_back(_file_MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Barrel);
  _files.push_back(_file_MatchAK4GenJetWithPhase1L1TJetFromPfCandidates_Endcap);
  _files.push_back(_file_MatchAK4GenJetWithPhase1L1TJetFromPfClusters_Endcap);

  _histogramPrefix.clear();
  _histogramPrefix.push_back("deltaPtDistributionBinnedInMatchedObject");
  _histogramPrefix.push_back("deltaPhiDistributionBinnedInMatchedObject");
  _histogramPrefix.push_back("deltaEtaDistributionBinnedInMatchedObject");

  _titles.clear();
  _titles.push_back("PfCandidates AK4 vs Phase-1 100 < p_{t}^{gen-jet} < 110 - Barrel");
  _titles.push_back("PfClusters AK4 vs Phase-1 100 < p_{t}^{gen-jet} < 110 - Barrel");
  _titles.push_back("PfCandidates AK4 vs Phase-1 100 < p_{t}^{gen-jet} < 110 - Endcap");
  _titles.push_back("PfClusters AK4 vs Phase-1 100 < p_{t}^{gen-jet} < 110 - Endcap");

  _outputFilenames.clear();
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/AK4_vs_Phase1_PfCandidates_resolution_Barrel");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/AK4_vs_Phase1_PfClusters_resolution_Barrel");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/AK4_vs_Phase1_PfCandidates_resolution_Endcap");
  _outputFilenames.push_back("jetMETStudies/PU200_PF_PUSubtraction/AK4_vs_Phase1_PfClusters_resolution_Endcap");

  for (const std::string & _prefix: _histogramPrefix) {
    for (int x = 0; x < _files.size()/2; x++) {
      
      TFile* _file0 = _files[x];
      TFile* _file1 = _files[x + (_files.size()/2)];

      h1 = (TH1F*) _file0 -> Get((_prefix + "_100_110").c_str());
      h2 = (TH1F*) _file1 -> Get((_prefix + "_100_110").c_str());

      h1 -> SetTitle(_titles[x].c_str());

      h1 -> GetYaxis() -> SetRangeUser(1e-5, 1.);

      h1 -> SetLineColor(1);
      h2 -> SetLineColor(2);

      h1 -> SetLineStyle(1);
      h2 -> SetLineStyle(1);

      h1->Draw("HIST ");
      h2->Draw("HIST SAME");

      TLegend * legend = new TLegend(0.1,0.7,0.3,0.9);
      legend -> AddEntry(h1, "AK4","l");
      legend -> AddEntry(h2, "Phase-1","l");
      legend -> Draw();
      
      c1->Print((_outputFilenames[x] + "_" + _prefix + ".pdf").c_str());
      c1->Print((_outputFilenames[x] + "_" + _prefix + ".png").c_str());
      delete legend;
    }
  }  

}