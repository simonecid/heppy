'''Generic histogrammer that takes a particle type and quantity and plots the higher one in the event'''

from heppy.framework.analyzer import Analyzer
from ROOT import TH1F
import collections
from ROOT import TCanvas
from ROOT import TFile

class LeadingQuantityHistogrammer(Analyzer):
  '''Generic histogrammer that takes a particle type and quantity and plots the higher one in the event
  
  Example::
  
    tfile_service_1 = cfg.Service(
        TFileService,
        'tfile1',
        fname='histograms.root',
        option='recreate'
      )

    def pt (ptc):
      return ptc.pt()

    histogrammer = cfg.Analyzer(
      LeadingQuantityHistogrammer,
      file_label = 'tfile1',
      histo_name = 'jetPtDistribution',
      histo_title = 'Leading jet transverse momentum distribution',
      min = 0,
      max = 300,
      nbins = 100,
      input_objects = 'jets',
      value_func = pt,
      key_func = pt
    )

    * file_label: (Facultative) Name of a TFileService. If specified, the histogram will be saved in that root file, otherwise it will be saved in a <histo_name>.png and <histo_name>.root file .
    * histo_name: Name of the histogram.
    * histo_title: Title of the histogram.
    * min: Minimum of the histogram
    * max: MaximumKey of the histogram
    * nbins: Number of bins
    * input_objects : the input collection.
    * value_func : function that returns the value to store in the histogram
    * key_func : function that returns the value used to determine the leading object (typically pt for the trigger)
  
  '''

  def beginLoop(self, setup):
    super(LeadingQuantityHistogrammer, self).beginLoop(setup)
    self.hasTFileService = hasattr(self.cfg_ana, "file_label")
    if self.hasTFileService:
      servname = '_'.join(['heppy.framework.services.tfile.TFileService',
                          self.cfg_ana.file_label
                      ])
      tfileservice = setup.services[servname]
      self.rootfile = tfileservice.file
    else:
      self.rootfile = TFile('/'.join([self.dirName,
                                      self.cfg_ana.histo_name + '.root']),
                            'recreate')
      
    self.histogram = TH1F(self.cfg_ana.histo_name, self.cfg_ana.histo_title, self.cfg_ana.nbins, self.cfg_ana.min, self.cfg_ana.max)
      
  def process(self, event):
    '''event must contain
    
    * self.cfg_ana.input_objects: collection of objects to be selected
       These objects must be usable by the filtering function
       self.cfg_ana.trigger_func.
    '''

    maximumKey = float("-inf")
    maximumValue = 0

    input_collection = getattr(event, self.cfg_ana.input_objects)
    if isinstance(input_collection, collections.Mapping):
      for key, val in input_collection.iteritems():
        if self.cfg_ana.key_func(val) > maximumKey:
          maximumKey = self.cfg_ana.key_func(val)
          maximumValue = self.cfg_ana.value_func(val)
    else:
      for obj in input_collection:
        if self.cfg_ana.key_func(obj) > maximumKey:
          maximumKey = self.cfg_ana.key_func(obj)
          maximumValue = self.cfg_ana.value_func(obj)

    if maximumKey > float("-inf"):
      self.histogram.Fill(maximumValue)

  def write(self, setup):
    self.rootfile.cd()
    #self.histogram.Write()
    c1 = TCanvas ("c1", "c1", 600, 600)
    c1.SetGridx()
    c1.SetGridy()
    self.histogram.GetXaxis().SetTitleOffset(1.2)
    self.histogram.GetYaxis().SetTitleOffset(1.2)
    self.histogram.SetMarkerStyle(21)
    self.histogram.SetMarkerColor(4)
    self.histogram.SetLineColor(1)
    self.histogram.Write()
    if hasattr(self.cfg_ana, "log_y"):
      c1.SetLogy(self.cfg_ana.log_y)
    self.histogram.Draw("")
    if hasattr(self.cfg_ana, "x_label"):
      self.histogram.GetXaxis().SetTitle(self.cfg_ana.x_label)
    if hasattr(self.cfg_ana, "y_label"):
      self.histogram.GetYaxis().SetTitle(self.cfg_ana.y_label)
    c1.Update()
    c1.Print("/".join([self.dirName, self.cfg_ana.histo_name + ".svg"]), "svg")
    c1.Print("/".join([self.dirName, self.cfg_ana.histo_name + ".root"]), "root")