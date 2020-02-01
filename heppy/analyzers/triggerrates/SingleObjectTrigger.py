'''Filter events based on the number of objects in the input collection.'''

from heppy.framework.analyzer import Analyzer
import collections

class SingleObjectTrigger  (Analyzer):
  '''Filters events based on a trigger function passed as lambda.
  
  When an event is rejected by the SingleObjectTrigger, the analyzers
  placed after the filter in the sequence will not run. 

  Example: 

  To reject events without a jet with pt higher than 30 GeV

  def jetTrigger (jet):
      return jet.pt() > 30
      

  from heppy.analyzers.SingleObjectTrigger   import SingleObjectTrigger  
  lepton_filter = cfg.Analyzer(
    SingleObjectTrigger  ,
    'jet_trigger',
    input_objects = 'jets',
    trigger_func = jetTrigger,
  )
  
  * input_objects : the input collection.

  * trigger_func : a function object.
  IMPORTANT NOTE: lambda statements should not be used, as they
  do not work in multiprocessing mode. looking for a solution...
  
  '''

  def process(self, event):
    '''event must contain
    
    * self.cfg_ana.input_objects: collection of objects to be selected
       These objects must be usable by the filtering function
       self.cfg_ana.trigger_func.
    '''
    input_collection = getattr(event, self.cfg_ana.input_objects)
    if isinstance(input_collection, collections.Mapping):
      for key, val in input_collection.iteritems():
        if self.cfg_ana.trigger_func(val):
          return True
    else:
      for obj in input_collection:
        if self.cfg_ana.trigger_func(obj) :
          return True

    #If we still have not returned then no object satisfies the trigger condition
    return False
