'''Analyser creating a tree containing info about two matched particles.'''

from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from ROOT import TFile
from heppy.analyzers.ntuple import *

class MatchedParticlesTreeProducer(Analyzer):
  '''Analyser creating a tree containing info about two matched particles.
  
  Example::
  
  tree = cfg.Analyzer(
    MatchedParticlesTreeProducer,
    file_label = "fileService",
    tree_name = 'matchedJetMuon',
    tree_title = 'Tree containing info about matched jet and muons'
    matched_particle_collection = 'matchedMuons'
  )
  
  The TTree is written to the file C{simple_tree.root} in the analyzer directory.
  
  * file_label: Name of a TFileService
  * tree_name: Name of the tree (Key in the output root file).
  * tree_title: Title of the tree.
  * matched_particle_collection: collection of matched particles

  '''
  def beginLoop(self, setup):
    super(MatchedParticlesTreeProducer, self).beginLoop(setup)
    
    servname = '_'.join(['heppy.framework.services.tfile.TFileService',
                             self.cfg_ana.file_label
                         ]) 
    tfileservice = setup.services[servname]
    tfileservice.file.cd()
    self.rootfile = tfileservice.file

    self.tree = Tree( self.cfg_ana.tree_name,
                      self.cfg_ana.tree_title )
    
    bookParticle(self.tree, "matchedMuon")
    bookParticle(self.tree, "matchedJet")
    var(self.tree, 'dr')

  def process(self, event):
    '''Process the event.
      
    The event must contain:
      - matched_particle_collection: collection of matched particle returned by the heppy Matcher analyzer 
        
      '''
    matched_particle_collection = getattr(event, self.cfg_ana.matched_particle_collection)
    for ptc in matched_particle_collection:
      fillParticle(self.tree, 'matchedMuon', ptc)
      fillParticle(self.tree, 'matchedJet', ptc.match)
      fill(self.tree, 'dr', ptc.dr)
      self.tree.tree.Fill()