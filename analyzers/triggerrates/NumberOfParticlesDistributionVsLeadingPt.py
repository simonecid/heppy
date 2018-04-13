'''Plots the distribution of the number of particles in a certain event'''

from heppy.framework.analyzer import Analyzer
from ROOT import TH1F
import collections
from ROOT import TCanvas, TFile
from array import array


class NumberOfParticlesDistributionVsLeadingPt(Analyzer):
  '''Plots the average number of objects in a certain events as a function of the leading object of that event

  Example::
  
  tfile_service_1 = cfg.Service(
    TFileService,
    'tfile1',
    fname='histograms.root',
    option='recreate'
  )

  numberOfParticlesDistribution = cfg.Analyzer(
    NumberOfParticlesDistributionVsLeadingPt,
    file_label = 'tfile1',
    histo_name = 'numberOfChargedGenParticlesVsPt',
    histo_title = 'Number of charged generated particles',
    bins = [0, 10, 20, 30, 50, 100],
    objects_to_count = 'gen_jets',
    leading_objects = 'gen_jets',
  )

  * file_label: (Facultative) Name of a TFileService. If specified, the histogram will be saved in that root file, otherwise it will be saved in a <histo_name>.png and <histo_name>.root file .

  * histo_name: Name of the histogram.

  * histo_title: Title of the histogram.

  * min: Minimum of the histogram

  * max: Maximum of the histogram

  * nbins: Number of bins
  
  * objects_to_count: collection whose multiplicity we are interested in
  
  * leading_objects: collection whose leading object must be found

  '''

  def beginLoop(self, setup):
    super(NumberOfParticlesDistributionVsLeadingPt, self).beginLoop(setup)
    self.hasTFileService = hasattr(self.cfg_ana, "file_label")
    if self.hasTFileService:
      servname = '_'.join(['heppy.framework.services.tfile.TFileService',
                          self.cfg_ana.file_label
                      ])
      tfileservice = setup.services[servname]
      self.rootfile = tfileservice.file
    else:
      self.rootfile = TFile('/'.join([self.dirName,
                                      self.cfg_ana.histo_name,
                                      '.root']),
                            'recreate')
      

    binsArray = array("f", self.cfg_ana.bins)
    self.histogram = TH1F(self.cfg_ana.histo_name, self.cfg_ana.histo_title, len(binsArray)-1, binsArray)
    self.numberOfEventsHistogram = TH1F(self.cfg_ana.histo_name+"_nevents", self.cfg_ana.histo_title, len(binsArray)-1, binsArray)
      
  def process(self, event):
    '''event must contain
    
    * self.cfg_ana.input_objects: collection of objects to be selected
      These objects must be usable by the filtering function
      self.cfg_ana.trigger_func.
    '''

    collection_to_count = getattr(event, self.cfg_ana.objects_to_count)
    numberOfParticlesInEvent = len(collection_to_count)
    collection_with_leading = getattr(event, self.cfg_ana.objects_to_count)

    maximumPt = float("-inf")

    if isinstance(collection_with_leading, collections.Mapping):
      for key, val in collection_with_leading.iteritems():
        if val.pt() > maximumPt:
          maximumPt = val.pt()
          leadingObject = val
    else:
      for obj in collection_with_leading:
        if obj.pt() > maximumPt:
          maximumPt = obj.pt()
          leadingObject = obj

    if maximumPt > float("-inf"):
      self.histogram.Fill(leadingObject.pt(), numberOfParticlesInEvent)
      self.numberOfEventsHistogram.Fill(leadingObject.pt())

       
  
  def write(self, setup):
    self.rootfile.cd()
    self.histogram.Write()
    