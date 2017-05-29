'''Print the transverse momentum of a specific particle'''

from heppy.framework.analyzer import Analyzer
import collections

class PtPrinter(Analyzer):
  '''Demonstrates how to log event variables.
  '''
  def beginLoop(self, setup):
    super(PtPrinter, self).beginLoop(setup)
    self.logger.info ("I suppose I will be called at the beginning of the event loop")
      
  def process(self, event):
    '''Process the event.
    
    The input data must contain a variable called "var1",
    which is the case of the L{test tree<heppy.utils.testtree>}. 
    '''
    #self.cfg_ana.input_objects: name of the particle I want the pt printed
    #getattr, gets the attribute which is named as the second parameter
    input_collection = getattr(event, self.cfg_ana.input_objects)
    print self.cfg_ana.input_objects, "contains", len(input_collection) , "objects" 
    #checks if input_collection is a dictionary class
    if isinstance(input_collection, collections.Mapping):
      for key, val in input_collection.iteritems():
        print "key:", key, "pt", val.pt()
    else:
      for obj in input_collection:
        print "pt", obj.pt()
        


    #'print 
                         
      
