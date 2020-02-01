'''Generic AddToSetup that takes a particle type and quantity and plots it'''

from heppy.framework.analyzer import Analyzer
from ROOT import TH1F
import collections
from ROOT import TCanvas
from ROOT import TFile

class AddToSetup(Analyzer):
  '''Add a property to setup. Used for output purposes.
  
  Example::
      
    myObject = lambda a: 0
    myObject.aProperty = "lol"

    addToSetup = cfg.Analyzer(
      AddToSetup,
      'addToSetup',
      name = "myOutput",
      value = myObject,
    )

    * name: name of the property to add to the setup object
    * value: value to set to the "name" property in setup
  
  '''

  def beginLoop(self, setup):
    super(AddToSetup, self).beginLoop(setup)
      
  def process(self, event):
    pass

  def write(self, setup):
    setattr(setup, self.cfg_ana.name, self.cfg_ana.value)
    
