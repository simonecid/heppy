'''Select objects'''

from heppy.framework.analyzer import Analyzer
import collections
from copy import deepcopy


class SetMETAsMHT(Analyzer):
    '''Sets the pt of the met as pt_sum

    Example:
    
    from heppy.analyzers.SetMETAsMHT import SetMETAsMHT
    metToMHT = cfg.Analyzer(
      SetMETAsMHT,
      'metToMHT',
      output = 'mht',
      input_objects = 'met',
      )

    * input_objects : the input collection.
        If a dictionary, the filtering function is applied to the dictionary values,
        and not to the keys.

    * output : the output collection

    * filter_func : a function object.
    IMPORTANT NOTE: lambda statements should not be used, as they
    do not work in multiprocessing mode. looking for a solution...
    
    '''

    def process(self, event):
        '''event must contain
        
        * self.cfg_ana.input_objects: collection of objects to be selected
           These objects must be usable by the filtering function
           self.cfg_ana.filter_func.
        '''
        input_collection = getattr(event, self.cfg_ana.input_objects)
        output_collection = deepcopy(input_collection)
        output_collection._tlv.SetPtEtaPhiE(output_collection.sum_et(), output_collection.eta(), output_collection.phi(), output_collection.e())        
        setattr(event, self.cfg_ana.output, output_collection)
