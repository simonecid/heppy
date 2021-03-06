�cheppy.framework.config
Config
q )�q}q(Uevents_classqcheppy.framework.chain
Chain
qUpreprocessorqNU
componentsq]qcheppy.framework.config
MCComponent
q)�q	}q
(Ufilesq]qU�/hdfs/FCC-hh/l1tMuonGenMuonMatching_SingleMu_FlatPt_8to100_QualityCut_WQualityBranch/MatchL1TMuonWithGenLevelMuons_SingleMu.rootqaUsplitFactorqKUeffCorrFactorqKU
nGenEventsqNU	tree_nameqU;MatchL1TMuonWithGenLevelMuons/matchedL1TMuonGenParticleTreeqUtrigger_objectqUl1tMuonqUintLumiqG?�      UisEmbedq�UnameqUGl1tMuonGenMuonMatching_SingleMu_FlatPt_8to100_QualityCut_WQualityBranchqUisDataq�Utriggersq]qU	addWeightqG?�      UxSectionqKUdataset_entriesqK UisMCq�U
gen_objectq UgenParticleq!ubaUservicesq"]q#cheppy.framework.config
Service
q$)�q%}q&(Uinstance_labelq'Utfile1q(Uclass_objectq)cheppy.framework.services.tfile
TFileService
q*Uverboseq+�hU2heppy.framework.services.tfile.TFileService_tfile1q,Ufnameq-Uhistograms.rootq.Uoptionq/Urecreateq0ubaUsequenceq1cheppy.framework.config
Sequence
q2)�q3(cheppy.framework.config
Analyzer
q4)�q5}q6(h'U1q7h)cheppy.analyzers.triggerrates.CMSMatchingReader
CMSMatchingReader
q8hUBheppy.analyzers.triggerrates.CMSMatchingReader.CMSMatchingReader_1q9h+�ubh4)�q:}q;(h'UkinematicCutSelectorq<h)cheppy.analyzers.Selector
Selector
q=hU6heppy.analyzers.Selector.Selector_kinematicCutSelectorq>Uinput_objectsq?Utrigger_objectsq@UoutputqAUtrigger_objects_in_detectorqBUfilter_funcqCc__cfg_to_run__
genMuInDetector
qDh+�ubh4)�qE}qF(h'UmuonQualityCutqGh)h=hU0heppy.analyzers.Selector.Selector_muonQualityCutqHh?hBhAUgood_trigger_objectsqIhCc__cfg_to_run__
qualityCut
qJh+�ubh4)�qK}qL(h'UtightRestrictionMatchSelectorqMh)h=hU?heppy.analyzers.Selector.Selector_tightRestrictionMatchSelectorqNh?hIhAUmatched_trigger_objectqOhCc__cfg_to_run__
dr2Selection
qPh+�ubh4)�qQ}qR(h'U)objectPtDistributionBinnedInMatchedObjectqSUnbinsqTK�h)cheppy.analyzers.triggerrates.MatchedObjectBinnedDistributions
MatchedObjectBinnedDistributions
qUU
file_labelqVh(Ubin_funcqWc__cfg_to_run__
pt
qXhU�heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions.MatchedObjectBinnedDistributions_objectPtDistributionBinnedInMatchedObjectqYUhisto_titleqZU8p_{t}^{L1T Muon} distribution binned in p^{Gen Muon}_{t}q[Ux_labelq\Up_{t}^{L1T Muon} [GeV]q]Uy_labelq^U# eventsq_U	plot_funcq`hXUbinningqa]qb(K G?�      G?�ffffffG?�������G?񙙙���G?�������G?�������KG@      KG@      KKG@      KKKKKKKK(K2KFKdK�K�eUmatched_collectionqchOUminqdK UmaxqeKdU
histo_nameqfhSUlog_yqg�h+�ubh4)�qh}qi(h'U;objectMatchedObjectPtRatioDistributionBinnedInMatchedObjectqjhTM h)hUhVh(hWhXhU�heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions.MatchedObjectBinnedDistributions_objectMatchedObjectPtRatioDistributionBinnedInMatchedObjectqkhZUIp_{t}^{L1T Muon}/p_{t}^{Gen Muon} distribution binned in p^{Gen Muon}_{t}qlh\U1p_{t}^{L1T Muon}/p_{t}^{' + matchedObjectName +'}qmh^h_h`c__cfg_to_run__
ptRatioWithMatched
qnhahbhchOhdK heKhfhjhg�h+�ubh4)�qo}qp(h'U*objectEtaDistributionBinnedInMatchedObjectqqhTK�h)hUhVh(hWhXhU�heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions.MatchedObjectBinnedDistributions_objectEtaDistributionBinnedInMatchedObjectqrhZU7#eta^{L1T Muon} distribution binned in p^{Gen Muon}_{t}qsh\U#etaqth^h_h`c__cfg_to_run__
eta
quhahbhchOhdJ����heK
hfhqhg�h+�ubh4)�qv}qw(h'U1matchedObjectEtaDistributionBinnedInMatchedObjectqxhTK�h)hUhVh(hWhXhU�heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions.MatchedObjectBinnedDistributions_matchedObjectEtaDistributionBinnedInMatchedObjectqyhZU7#eta^{Gen Muon} distribution binned in p^{Gen Muon}_{t}qzh\hth^h_h`c__cfg_to_run__
matchedParticleEta
q{hahbhchOhdJ����heK
hfhxhg�h+�ubh4)�q|}q}(h'U'deltaRDistributionBinnedInMatchedObjectq~hTM�h)hUhVh(hWhXhU�heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions.MatchedObjectBinnedDistributions_deltaRDistributionBinnedInMatchedObjectqhZU/#DeltaR distribution binned in p^{Gen Muon}_{t}q�h\U#DeltaRq�h^h_h`c__cfg_to_run__
deltaR
q�hahbhchOhdK heKhfh~hg�h+�ubh4)�q�}q�(h'U(deltaPtDistributionBinnedInMatchedObjectq�hTM h)hUhVh(hWhXhU�heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions.MatchedObjectBinnedDistributions_deltaPtDistributionBinnedInMatchedObjectq�hZUKp_{t}^{L1T Muon} - p_{t}^{Gen Muon} distribution binned in p^{Gen Muon}_{t}q�h\U&p_{t}^{L1T Muon} - p_{t}^{match} [GeV]q�h^h_h`c__cfg_to_run__
deltaPt
q�hahbhchOhdJ8���heK�hfh�hg�h+�ubh4)�q�}q�(h'U)deltaEtaDistributionBinnedInMatchedObjectq�hTM�h)hUhVh(hWhXhU�heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions.MatchedObjectBinnedDistributions_deltaEtaDistributionBinnedInMatchedObjectq�hZU2#Delta#eta distribution binned in p^{Gen Muon}_{t}q�h\U
#Delta#etaq�h^h_h`c__cfg_to_run__
deltaEta
q�hahbhchOhdJ����heKhfh�hg�h+�ubh4)�q�}q�(h'UobjectPtDistributionq�hTK�h)cheppy.analyzers.triggerrates.Histogrammer
Histogrammer
q�hUKheppy.analyzers.triggerrates.Histogrammer.Histogrammer_objectPtDistributionq�hZUp_{t}^{L1T Muon} distributionq�h\Up_{t}^{L1T Muon}q�h^U	\# eventsq�hVh(U
value_funcq�hXh?hOhdK heKdhfh�h+�ubh4)�q�}q�(h'UobjectQualityDistributionq�hTKh)h�hUPheppy.analyzers.triggerrates.Histogrammer.Histogrammer_objectQualityDistributionq�hZUQuality^{L1T Muon} distributionq�h\UQuality^{L1T Muon}q�h^h�hVh(h�c__cfg_to_run__
quality
q�h?hOhdK heKhfh�h+�ubh4)�q�}q�(h'UmatchedObjectPtDistributionq�hTK�h)h�hURheppy.analyzers.triggerrates.Histogrammer.Histogrammer_matchedObjectPtDistributionq�hZUp_{t}^{Gen Muon} distributionq�h\Up_{t}^{L1T Muon}q�h^h�hVh(h�c__cfg_to_run__
matchedParticlePt
q�h?hOhdK heK�hfh�h+�ubh4)�q�}q�(h'U0matchedObjectPtDistributionBinnedInMatchedObjectq�hTK�h)hUhVh(hWhXhU�heppy.analyzers.triggerrates.MatchedObjectBinnedDistributions.MatchedObjectBinnedDistributions_matchedObjectPtDistributionBinnedInMatchedObjectq�hZU8p_{t}^{Gen Muon} distribution binned in p^{Gen Muon}_{t}q�h\Up_{t}^{L1T Muon} [GeV]q�h^h_h`h�hahbhchOhdK heK�hfh�hg�h+�ubh4)�q�}q�(h'U3objectPtCumulativeDistributionBinnedInMatchedObjectq�hTK�h)cheppy.analyzers.triggerrates.MatchedObjectBinnedCumulativeDistributions
MatchedObjectBinnedCumulativeDistributions
q�h`hXhWhXhU�heppy.analyzers.triggerrates.MatchedObjectBinnedCumulativeDistributions.MatchedObjectBinnedCumulativeDistributions_objectPtCumulativeDistributionBinnedInMatchedObjectq�hZUCp_{t}^{L1T Muon} cumulative distribution binned in p^{Gen Muon}_{t}q�h\Up_{t}^{L1T Muon} [GeV]q�h^h_hVh(hahbUinvertedq��hchOhdK heKdhfh�hg�h+�ube}q�bub.