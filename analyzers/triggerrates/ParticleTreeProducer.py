'''Analyser creating a tree containing info about a particle`.'''

from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile
from heppy.analyzers.ntuple import *

class ParticleTreeProducer(Analyzer):
  '''Analyser creating a tree containing info about a particle`.
  
  Example::
  
  tree = cfg.Analyzer(
    ParticleTreeProducer,
    file_label = "fileService",
    tree_name = 'jets',
    tree_title = 'Tree containing info about jets',
    collection = "jets"
  )
  
  The TTree is written to the file C{simple_tree.root} in the analyzer directory.
  
  * file_label: Name of a TFileService
  * tree_name: Name of the tree (Key in the output root file).
  * tree_title: Title of the tree.
  * collection: Particle collection

  '''
  def beginLoop(self, setup):
    super(ParticleTreeProducer, self).beginLoop(setup)
    
    servname = '_'.join(['heppy.framework.services.tfile.TFileService',
                             self.cfg_ana.file_label
                         ]) 
    tfileservice = setup.services[servname]
    tfileservice.file.cd()
    self.rootfile = tfileservice.file

    self.tree = Tree( self.cfg_ana.tree_name,
                      self.cfg_ana.tree_title )
    
    bookParticle(self.tree, self.cfg_ana.collection)

  def process(self, event):
    '''Process the event.
      
    The event must contain:
      - collection: collection of particles
        
      '''
    collection = getattr(event, self.cfg_ana.collection)
    for ptc in collection:
      fillParticle(self.tree, self.cfg_ana.collection, ptc)
      self.tree.tree.Fill()
