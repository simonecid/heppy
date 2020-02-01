'''Plots the distribution of the number of particles in a certain event'''

from heppy.framework.analyzer import Analyzer
from ROOT import TH1F
import collections
from ROOT import TCanvas, TFile

class NumberOfParticlesDistribution(Analyzer):
  '''Plots the distribution of the number of particles in a certain event

  Example::
  
  tfile_service_1 = cfg.Service(
    TFileService,
    'tfile1',
    fname='histograms.root',
    option='recreate'
  )

  numberOfParticlesDistribution = cfg.Analyzer(
    NumberOfParticlesDistribution,
    file_label = 'tfile1',
    histo_name = 'numberOfChargedGenParticles',
    histo_title = 'Number of charged generated particles',
    min = 0,
    max = 300,
    nbins = 100,
    input_objects = 'genparticles',
  )

  * file_label: (Facultative) Name of a TFileService. If specified, the histogram will be saved in that root file, otherwise it will be saved in a <histo_name>.png and <histo_name>.root file .

  * histo_name: Name of the histogram.

  * histo_title: Title of the histogram.

  * min: Minimum of the histogram

  * max: Maximum of the histogram

  * nbins: Number of bins
  
  * input_objects: the input collection. 

  '''

  def beginLoop(self, setup):
    super(NumberOfParticlesDistribution, self).beginLoop(setup)
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
      
    self.histogram = TH1F(self.cfg_ana.histo_name, self.cfg_ana.histo_title, self.cfg_ana.nbins, self.cfg_ana.min, self.cfg_ana.max)
      
  def process(self, event):
    '''event must contain
    
    * self.cfg_ana.input_objects: collection of objects to be selected
      These objects must be usable by the filtering function
      self.cfg_ana.trigger_func.
    '''
    input_collection = getattr(event, self.cfg_ana.input_objects)
    numberOfParticlesInEvent = len(input_collection)
    self.histogram.Fill(numberOfParticlesInEvent)
  
  def write(self, setup):
    self.rootfile.cd()
    self.histogram.Write()
    c1 = TCanvas ("c1", "c1", 600, 600)
    c1.SetGridx()
    c1.SetGridy()
    self.histogram.Draw("")
    c1.Update()
    c1.Print("".join([self.cfg_ana.histo_name, ".pdf"]), "pdf")
    