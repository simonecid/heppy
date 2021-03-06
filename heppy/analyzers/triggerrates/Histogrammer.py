'''Generic histogrammer that takes a particle type and quantity and plots it'''

from heppy.framework.analyzer import Analyzer
from ROOT import TH1F
import collections
from ROOT import TCanvas
from ROOT import TFile
from array import array

class Histogrammer(Analyzer):
  '''Generic histogrammer that takes a particle type and quantity and plots it.
  
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
      Histogrammer,
      file_label = 'tfile1',
      histo_name = 'jetPtDistribution',
      histo_title = 'Jet transverse momentum distribution',
      min = 0,
      max = 300,
      nbins = 100,
      input_objects = 'jets',
      value_func = pt,
      x_label = "pt [GeV]",
      y_label = "\# events"
    )

    --- OR ---

    histogrammer = cfg.Analyzer(
      Histogrammer,
      file_label = 'tfile1',
      histo_name = 'jetPtDistribution',
      histo_title = 'Jet transverse momentum distribution',
      bins = [0, 10, 20, 30, 50, 100],
      input_objects = 'jets',
      value_func = pt,
      x_label = "pt [GeV]",
      y_label = "\# events"
    )

    * file_label: (Facultative) Name of a TFileService. If specified, the histogram will be saved in that root file, otherwise it will be saved in a <histo_name>.png and <histo_name>.root file .
    * histo_name: Name of the histogram.
    * histo_title: Title of the histogram.
    * min: Minimum of the histogram
    * max: Maximum of the histogram
    * nbins: Number of bins
    * input_objects : the input collection.
    * value_func : function that returns the value to store in the histogram. If it returns None, it will not be stored
    * log_y: True or False, sets log scale on y axis (False by default)
    * x_label (y_label): X-axis (Y- axis) label
  
  '''

  def beginLoop(self, setup):
    super(Histogrammer, self).beginLoop(setup)
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
      
    bins = getattr(self.cfg_ana, "bins", None)
    if bins is None:
      self.histogram = TH1F(self.cfg_ana.histo_name, self.cfg_ana.histo_title, self.cfg_ana.nbins, self.cfg_ana.min, self.cfg_ana.max)
    else: 
      binsArray = array("f", bins)
      self.histogram = TH1F(self.cfg_ana.histo_name, self.cfg_ana.histo_title, len(binsArray)-1, binsArray)
      
  def process(self, event):
    '''event must contain
    
    * self.cfg_ana.input_objects: collection of objects to be selected
       These objects must be usable by the filtering function
       self.cfg_ana.trigger_func.
    '''
    input_collection = getattr(event, self.cfg_ana.input_objects)
    if isinstance(input_collection, collections.Mapping):
      for key, val in input_collection.iteritems():
        value = self.cfg_ana.value_func(val)
        if value is not None:
          self.histogram.Fill(value)
    else:
      for obj in input_collection:
        value = self.cfg_ana.value_func(obj)
        if value is not None:
          self.histogram.Fill(value)

  def write(self, setup):
    self.rootfile.cd()
    self.histogram.Write()
    c1 = TCanvas ("c1", "c1", 600, 600)
    c1.SetGridx()
    c1.SetGridy()
    self.histogram.GetXaxis().SetTitleOffset(1.2)
    self.histogram.GetYaxis().SetTitleOffset(1.2)
    self.histogram.SetMarkerStyle(21)
    self.histogram.SetMarkerColor(4)
    self.histogram.SetLineColor(1)
    if hasattr(self.cfg_ana, "log_y"):
      c1.SetLogy(self.cfg_ana.log_y)
    self.histogram.Draw("PE")
    if hasattr(self.cfg_ana, "x_label"):
      self.histogram.GetXaxis().SetTitle(self.cfg_ana.x_label)
    if hasattr(self.cfg_ana, "y_label"):
      self.histogram.GetYaxis().SetTitle(self.cfg_ana.y_label)
    c1.Update()
    c1.Print("/".join([self.dirName, self.cfg_ana.histo_name + ".svg"]), "svg")
    c1.Print("/".join([self.dirName, self.cfg_ana.histo_name + ".png"]), "png")
    c1.Print("/".join([self.dirName, self.cfg_ana.histo_name + ".root"]), "root")
    
