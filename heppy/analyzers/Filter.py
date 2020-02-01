'''Select objects'''

from heppy.framework.analyzer import Analyzer
import collections

class Filter(Analyzer):
    '''
    Stops the workflow is the filter function does not return true.
    Filter function receives the event object and must return a boolean.

    Example:
    
    from heppy.analyzers.Filter import Filter
    def has_muons(event):
      #Returns true if the event has a muon
      return len(event.muons) > 0

    leptons = cfg.Analyzer(
      Filter,
      'sel_muons',
      filter_func = has_muons
    )

        * filter_func : a function object.
    IMPORTANT NOTE: lambda statements should not be used, as they
    do not work in multiprocessing mode. looking for a solution...
    
    '''

    def process(self, event):
        return self.cfg_ana.filter_func(event)
