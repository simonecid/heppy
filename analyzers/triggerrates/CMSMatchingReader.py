from heppy.framework.analyzer import Analyzer
from heppy.particles.particle import Particle
from heppy.particles.fcc.jet import Jet
from heppy.particles.fcc.vertex import Vertex 
from heppy.particles.fcc.met import Met
import heppy.configuration
from ROOT import TLorentzVector


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

    gen_object = Particle()
    trigger_object = Particle()
    tree = event.input
    if hasattr(self.cfg_comp, "gen_object"):
#      gen_object.id = getattr(tree, self.cfg_comp.gen_object + "_id")
      if hasattr(tree, self.cfg_comp.gen_object):
        gen_object_pt = getattr(tree, self.cfg_comp.gen_object)
        gen_object_eta = 0
        gen_object_phi = 0
      else: 
        gen_object_pt = getattr(tree, self.cfg_comp.gen_object + "_pt")
        gen_object_eta = getattr(tree, self.cfg_comp.gen_object + "_eta")
        gen_object_phi = getattr(tree, self.cfg_comp.gen_object + "_phi")
      gen_object = Particle()
      gen_object._tlv = TLorentzVector()
      gen_object._pid = 0
      gen_object._charge = 0
      gen_object._status = 1
      gen_object._tlv.SetPtEtaPhiE(gen_object_pt, gen_object_eta, gen_object_phi, 0)
      event.gen_objects = [gen_object]
    if hasattr(self.cfg_comp, "trigger_object"):
      if hasattr(tree, self.cfg_comp.gen_object):
        trigger_object_pt = getattr(tree, self.cfg_comp.trigger_object, None)
        trigger_object_eta = 0
        trigger_object_phi = 0
      else: 
        trigger_object_pt = getattr(tree, self.cfg_comp.trigger_object + "_pt", None)
        trigger_object_eta = getattr(tree, self.cfg_comp.trigger_object + "_eta", None)
        trigger_object_phi = getattr(tree, self.cfg_comp.trigger_object + "_phi", None)
#      trigger_object.id = getattr(tree, self.cfg_comp.trigger_object + "_id")
      if trigger_object_pt is not None:
        trigger_object = Particle()
        trigger_object._tlv = TLorentzVector()
        trigger_object._pid = 0
        trigger_object._charge = 0
        trigger_object._status = 1
        trigger_object._tlv.SetPtEtaPhiE(trigger_object_pt, trigger_object_eta, trigger_object_phi, 0)
        trigger_object.match = gen_object
        gen_object.match = trigger_object
        trigger_object.deltaR2 = getattr(tree, "deltaR2", None)
        trigger_object.quality = getattr(tree, "l1tMuon_qual", 0)
        if trigger_object.deltaR2 is None: trigger_object.deltaR2 = tree.dr**2
        event.trigger_objects = [trigger_object]
      else:
        event.trigger_objects = []
        self.cfg_comp.trigger_object = "NoObject"  
    else:
      event.trigger_objects = []
      self.cfg_comp.trigger_object = "NoObject"