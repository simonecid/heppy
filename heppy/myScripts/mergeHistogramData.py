import pickle

files = [
  "minBias_500kevents/MinBiasDistribution_Chunk0/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk1/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk10/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk11/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk12/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk13/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk14/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk15/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk16/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk17/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk18/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk19/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk2/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk3/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk4/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk5/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk6/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk7/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk8/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle",
  "minBias_500kevents/MinBiasDistribution_Chunk9/heppy.analyzers.triggerrates.Histogrammer_MPL.Histogrammer_MPL_jetRecoPtDistribution/jetRecoPtDistribution_histogramContent.pickle"
]

rawHistograms = []

for fileName in files:
  rawHistograms.append(pickle.load(open(fileName, 'rb')))

bins = rawHistograms[0][0]
binContents = rawHistograms[0][1]

for x in xrange(1, len(files)):
  binContents += rawHistograms[x][1]

summedHistograms = [bins, binContents]

pickle.dump(summedHistograms, file("summedHistograms.pickle", 'wb'))