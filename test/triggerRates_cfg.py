import os
import copy
import heppy.framework.config as cfg

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

comp = cfg.Component(
    'minBias',
    files = ["../FCCSW/minBiasSimulationOutput.root"]
)
selectedComponents = [comp]

from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,

    #gen_particles = 'genParticles',
    #gen_vertices = 'genVertices',

    gen_jets = 'genJets',

    jets = 'jets',
    bTags = 'bTags',
    cTags = 'cTags',
    tauTags = 'tauTags',

    electrons = 'electrons',
    electronITags = 'electronITags',

    muons = 'muons',
    muonITags = 'muonITags',

    photons = 'photons',
    met = 'met',
)

from ROOT import gSystem
gSystem.Load("libdatamodelDict")

from EventStore import EventStore as Events

from heppy.analyzers.triggerrates.PtPrinter import PtPrinter
ptPrinter = cfg.Analyzer(
    PtPrinter,
    input_objects = 'jets',
)


# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence( [
    source,
    ptPrinter  
    ] )

# comp.files.append('example_2.root')
#comp.splitFactor = len(comp.files)  # splitting the component in 2 chunks

config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)

if __name__ == '__main__':
    import sys
    from heppy.framework.looper import Looper

    def next():
        loop.process(loop.iEvent+1)

    loop = Looper( 'looper', config,
                   nEvents=100,
                   nPrint=0,
                   timeReport=True)
    loop.process(6)
    print loop.event

