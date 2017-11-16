'''Generic histogrammer that takes a particle type and quantity and plots it'''

from heppy.framework.analyzer import Analyzer
from ROOT import TH2F
import collections
from ROOT import TCanvas
from ROOT import TFile
from ROOT import gStyle
from array import array

class QuantityDistributionIn2D(Analyzer):
  '''
  Computes the sum of a quantity in a region defined by the binning using the input objects.
  
  Example:
  
    tfile_service_1 = cfg.Service(
        TFileService,
        'tfile1',
        fname='histograms.root',
        option='recreate'
      )

    #Binning quantities
    def phi (ptc):
      return ptc.phi()
    
    def eta (ptc):
      return eta.pt()

    #Quantity to plot
    def pt (ptc):
      return ptc.pt()

    ptDistributionin2D = cfg.Analyzer(
      QuantityDistributionIn2D,
      file_label = 'tfile1',
      histo_name = 'ptDistributionin2D',
      histo_title = 'Transverse momentum distribution in eta-phi',
      input_objects = 'charged_gen_particles',
      x_min = -10,
      x_max = 10,
      x_nbins = 200,
      x_value_func = eta,
      x_label = "pt [GeV]",
      y_min = -3.15,
      y_max = 3.15,
      y_nbins = 630,
      y_value_func = eta,
      y_label = "#eta",
      z_value_func = pt,
      z_label = "p_{t} [GeV]"
    )

    * file_label: (Facultative) Name of a TFileService. If specified, the histogram will be saved in that root file, otherwise it will be saved in a <histo_name>.png and <histo_name>.root file .
    * histo_name: Name of the histogram.
    * histo_title: Title of the histogram.
    * x_min (y_min): Minimum of the histogram in the x (y) dimension
    * x_max (y_max): Maximum of the histogram in the x (y) dimension
    * x_nbins (y_nbins): Number of bins in the x (y) dimension
    * input_objects : the input collection.
    * x_value_func (y_value_func): function that returns the x (y) value to store in the histogram. If it returns None, it will not be stored
    * log_z: True or False, sets log scale on z axis (False by default)
    * x_label (y_label) [z_label] = X-axis (y-axis) [z-axis]
  
  '''

  def beginLoop(self, setup):
    super(QuantityDistributionIn2D, self).beginLoop(setup)
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
      
    self.histogram = TH2F(self.cfg_ana.histo_name, self.cfg_ana.histo_title,
                           self.cfg_ana.x_nbins, self.cfg_ana.x_min, self.cfg_ana.x_max,
                           self.cfg_ana.y_nbins, self.cfg_ana.y_min, self.cfg_ana.y_max
                          )
      
  def process(self, event):
    '''event must contain
    
    * self.cfg_ana.input_objects: collection of objects to be selected
       These objects must be usable by the filtering function
       self.cfg_ana.trigger_func.
    '''
    input_collection = getattr(event, self.cfg_ana.input_objects)
    if isinstance(input_collection, collections.Mapping):
      for key, val in input_collection.iteritems():
        x_value = self.cfg_ana.x_value_func(val)
        y_value = self.cfg_ana.y_value_func(val)
        z_value = self.cfg_ana.z_value_func(val)
        if x_value != None and y_value != None:
          self.histogram.Fill(x_value, y_value, z_value)
    else:
      for obj in input_collection:
        x_value = self.cfg_ana.x_value_func(obj)
        y_value = self.cfg_ana.y_value_func(obj)
        z_value = self.cfg_ana.z_value_func(obj)
        if x_value != None and y_value != None:
          self.histogram.Fill(x_value, y_value, z_value)

  def write(self, setup):
    self.rootfile.cd()
    zero_array = array('i', [0])
    gStyle.SetPalette(56, zero_array)
    #self.histogram.Write()
    c1 = TCanvas ("c1", "c1", 600, 600)
    c1.SetGridx()
    c1.SetGridy()
    self.histogram.GetXaxis().SetTitleOffset(1.2)
    self.histogram.GetYaxis().SetTitleOffset(1.2)
    if hasattr(self.cfg_ana, "log_z"):
      c1.SetLogz(self.cfg_ana.log_z)
    self.histogram.Draw("COLZ")
    if hasattr(self.cfg_ana, "x_label"):
      self.histogram.GetXaxis().SetTitle(self.cfg_ana.x_label)
    if hasattr(self.cfg_ana, "y_label"):
      self.histogram.GetYaxis().SetTitle(self.cfg_ana.y_label)
    self.histogram.Write()
    c1.Write()
    c1.Update()
    c1.Print("/".join([self.dirName, self.cfg_ana.histo_name + ".png"]), "png")
    c1.Print("/".join([self.dirName, self.cfg_ana.histo_name + ".root"]), "root")