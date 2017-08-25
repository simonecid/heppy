from heppy.framework.analyzer import Analyzer
from heppy.particles.fcc.particle import Particle
from heppy.particles.fcc.jet import Jet
from heppy.particles.fcc.vertex import Vertex 
from heppy.particles.fcc.met import Met
import heppy.configuration

from heppy.particles.TriggerObject import TriggerObject


import math

class MissingCollection(Exception):
  pass

class CMSMatchingReader(Analyzer):
  '''Reads events in FCC EDM format, and creates lists of objects adapted to an
  analysis in python.

  Configuration: 
  ----------------------
  
  Example: 
  
  from heppy.analyzers.triggerrates.CMSMatchingReader import CMSMatchingReader
  source = cfg.Analyzer(
    CMSMatchingReader,
  )  
  Those keys must be defined in the component
  * gen_object generator level object name
  * trigger_object:  trigger level object name
  
  Name of the collection of trigger objects
  
  You can find out about the names of the collections by opening
  the root file with root, and by printing the events TTree.

  Creates: 
  - event.gen_objects: generator-level object
  - event.trigger_objects: trigger objects  
  '''
  
  def process(self, event):

    gen_object = TriggerObject()
    trigger_object = TriggerObject()
    tree = event.input
    if hasattr(self.cfg_comp, "gen_object"):
#      gen_object.id = getattr(tree, self.cfg_comp.gen_object + "_id")
      gen_object._pt = getattr(tree, self.cfg_comp.gen_object + "_pt")
      gen_object._eta = getattr(tree, self.cfg_comp.gen_object + "_eta")
      gen_object._phi = getattr(tree, self.cfg_comp.gen_object + "_phi")
      event.gen_objects = [gen_object]
    if hasattr(self.cfg_comp, "trigger_object"):
#      trigger_object.id = getattr(tree, self.cfg_comp.trigger_object + "_id")
      trigger_object._pt = getattr(tree, self.cfg_comp.trigger_object + "_pt")
      trigger_object._eta = getattr(tree, self.cfg_comp.trigger_object + "_eta")
      trigger_object._phi = getattr(tree, self.cfg_comp.trigger_object + "_phi")
      trigger_object.match = gen_object
      trigger_object.deltaR2 = tree.deltaR2
      event.trigger_objects = [trigger_object]