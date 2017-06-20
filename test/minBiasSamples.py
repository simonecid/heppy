import heppy.framework.config as cfg

MBtest = cfg.MCComponent(
  '_MBtest',
  files = ["../FCCSW/minimumBias_10000evts.root"]
)

MinBiasDistribution_100TeV_DelphesFCC_FCCJets = cfg.MCComponent(
  'MinBiasDistribution_100TeV_DelphesFCC_FCCJets',
  files = [
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.0.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.10.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.11.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.12.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.13.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.14.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.15.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.16.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.17.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.18.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.19.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.1.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.2.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.3.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.4.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.5.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.6.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.7.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.8.root",
    "/hdfs/FCC-hh/minBias/events_MinimumBiasGeneration_25kevents_1684753.9.root"
  ],
  xSection = 80, #mb
  nGenEvents = 500000
)

MinBiasDistribution_13TeV_DelphesFCC_FCCJets = cfg.MCComponent(
  'MinBiasDistribution_13TeV_DelphesFCC_FCCJets',
  files = [
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.0.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.10.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.11.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.12.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.13.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.14.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.15.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.16.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.17.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.18.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.19.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.1.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.2.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.3.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.4.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.5.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.6.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.7.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.8.root",
    "/hdfs/FCC-hh/minBias_13TeV/events_MinimumBiasGeneration_25kevents_13TeV_2274254.9.root"
  ],
  xSection = 56.7, #mb
  nGenEvents = 500000
)

MinBiasDistribution_13TeV_DelphesCMS_CMSJets = cfg.MCComponent(
  'MinBiasDistribution_13TeV_DelphesCMS_CMSJets',
  files = [
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.0.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.10.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.11.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.12.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.13.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.14.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.15.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.16.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.17.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.18.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.19.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.1.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.2.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.3.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.4.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.5.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.6.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.7.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.8.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesCMS/events_MinimumBiasGeneration_25kevents_13TeV_DelphesCMS_2274953.9.root",
  ],
  xSection = 56.7, #mb
  nGenEvents = 500000
)

MinBiasDistribution_13TeV_DelphesFCC_CMSJets = cfg.MCComponent(
  'MinBiasDistribution_13TeV_DelphesFCC_CMSJets',
  files = [
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.0.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.10.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.11.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.12.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.13.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.14.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.15.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.16.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.17.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.18.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.19.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.1.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.2.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.3.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.4.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.5.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.6.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.7.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.8.root",
    "/hdfs/FCC-hh/minBias_13TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_13TeV_DelphesFCC_CMSJets_2276635.9.root",
  ],
  xSection = 56.7, #mb
  nGenEvents = 500000
)

MinBiasDistribution_100TeV_DelphesFCC_CMSJets  = cfg.MCComponent(
  'MinBiasDistribution_100TeV_DelphesFCC_CMSJets',
  files = [
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.0.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.10.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.11.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.12.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.13.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.14.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.15.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.16.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.17.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.18.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.19.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.1.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.2.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.3.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.4.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.5.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.6.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.7.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.8.root",
    "/hdfs/FCC-hh/minBias_100TeV_DelphesFCC_CMSJets/events_MinimumBiasGeneration_25kevents_100TeV_DelphesFCC_CMSJets_2282065.9.root",
  ],
  xSection = 80, #mb
  nGenEvents = 500000
)

# Max 4 jobs
MBtest.splitFactor = len(MBtest.files) if len(MBtest.files) < 4 else 4
MinBiasDistribution_100TeV_DelphesFCC_FCCJets.splitFactor = len(MinBiasDistribution_100TeV_DelphesFCC_FCCJets.files) if len(MinBiasDistribution_100TeV_DelphesFCC_FCCJets.files) < 4 else 4
MinBiasDistribution_13TeV_DelphesFCC_FCCJets.splitFactor = len(MinBiasDistribution_13TeV_DelphesFCC_FCCJets.files) if len(MinBiasDistribution_13TeV_DelphesFCC_FCCJets.files) < 4 else 4
MinBiasDistribution_13TeV_DelphesCMS_CMSJets.splitFactor = len(MinBiasDistribution_13TeV_DelphesCMS_CMSJets.files) if len(MinBiasDistribution_13TeV_DelphesCMS_CMSJets.files) < 4 else 4
MinBiasDistribution_13TeV_DelphesFCC_CMSJets.splitFactor = len(MinBiasDistribution_13TeV_DelphesFCC_CMSJets.files) if len(MinBiasDistribution_13TeV_DelphesFCC_CMSJets.files) < 4 else 4
MinBiasDistribution_100TeV_DelphesFCC_CMSJets.splitFactor = len(MinBiasDistribution_100TeV_DelphesFCC_CMSJets.files) if len(MinBiasDistribution_100TeV_DelphesFCC_CMSJets.files) < 4 else 4