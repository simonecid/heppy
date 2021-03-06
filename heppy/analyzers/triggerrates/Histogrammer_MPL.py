'''Generic histogrammer_MPL that takes a particle type and quantity and plots it using matplotlib'''

from heppy.framework.analyzer import Analyzer
import collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle

class Histogrammer_MPL(Analyzer):
  '''Generic histogrammer that takes a particle type and quantity and plots it using matplotlib.

  Histogram is saved in .png and in .pickle.
  Bins and relative contents are saved in a separate pickle file.
  
  Example::
  
    tfile_service_1 = cfg.Service(
        TFileService,
        'tfile1',
        fname='histograms.root',
        option='recreate'
      )

    def pt (ptc):
      return ptc.pt()

    histogrammer_MPL = cfg.Analyzer(
      Histogrammer_MPL,
      histo_name = 'jetPtDistribution',
      histo_title = 'Jet transverse momentum distribution',
      min = 0,
      max = 300,
      nbins = 100,
      input_objects = 'jets',
      value_func = pt,
      x_label = "pt [GeV]",
      y_label = "# events"
    )

    * histo_name: Name of the histogram.
    * histo_title: Title of the histogram.
    * min: Minimum of the histogram
    * max: Maximum of the histogram
    * nbins: Number of bins
    * input_objects : the input collection.
    * value_func : function that returns the value to store in the histogram. If it returns None, it will not be stored
    * log_y: True or False, sets log scale on y axis (False by default)
    * x_label: x-axis label
    * y_label: y-axis label
  
  '''

  def beginLoop(self, setup):
    super(Histogrammer_MPL, self).beginLoop(setup)

    '''Window for the histogram'''
    self.histogramCanvas = plt.figure()
    '''Plot object for the histogram'''
    self.histogramPlot = self.histogramCanvas.add_subplot(1, 1, 1)
    '''Histogram data container'''
    self.histogramData = []
      
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
        if value != None:
          self.histogramData.append(value)
    else:
      for obj in input_collection:
        value = self.cfg_ana.value_func(obj)
        if value != None:
          self.histogramData.append(value)

  def write(self, setup):
    
    binContents, bins, patches = self.histogramPlot.hist(
                                                         self.histogramData, 
                                                         bins = self.cfg_ana.nbins,
                                                         histtype="step",
                                                         range =(self.cfg_ana.min, self.cfg_ana.max)
                                                        )

    histogramContent = [bins, binContents]
    
    self.histogramPlot.set_title(self.cfg_ana.histo_title)
    self.histogramPlot.grid(b=True)
    self.histogramPlot.minorticks_on()

    if hasattr(self.cfg_ana, "x_label"):
      self.histogramPlot.set_xlabel(self.cfg_ana.x_label)
    if hasattr(self.cfg_ana, "y_label"):
      self.histogramPlot.set_ylabel(self.cfg_ana.y_label)
    if hasattr(self.cfg_ana, "log_y"):
      self.histogramPlot.set_yscale("log")

    pickle.dump(self.histogramCanvas, file('/'.join([self.dirName,
                                      self.cfg_ana.histo_name + '_figure.pickle']), 'wb'))
    pickle.dump(histogramContent, file('/'.join([self.dirName,
                                      self.cfg_ana.histo_name + '_histogramContent.pickle']), 'wb'))
    self.histogramCanvas.savefig('/'.join([self.dirName,
                                      self.cfg_ana.histo_name + '.png']), format="png")