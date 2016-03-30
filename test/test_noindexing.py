import unittest
import shutil
import os 
from simple_example_noindexing_cfg import config
from heppy.utils.testtree import create_tree, remove_tree
from heppy.framework.looper import Looper
from ROOT import TFile

import logging
logging.getLogger().setLevel(logging.ERROR)

class TestNoIndexing(unittest.TestCase):

    def setUp(self):
        self.fname = create_tree()
        rootfile = TFile(self.fname)
        self.nevents = rootfile.Get('test_tree').GetEntries()

    def test_all_events_processed(self):
        outdir = 'Out_test_all_events_processed'
        if os.path.isdir(outdir):
            shutil.rmtree(outdir)
        loop = Looper( outdir, config,
                       nEvents=None,
                       nPrint=0,
                       timeReport=True)
        loop.loop()
        loop.write()
        logfile = open('/'.join([outdir, 'log.txt']))
        nev_processed = None
        for line in logfile:
            if line.startswith('number of events processed:'):
                nev_processed = int(line.split(':')[1])
        self.assertEqual(nev_processed, self.nevents)
        # checking the looper itself.
        self.assertEqual(loop.nEvProcessed, self.nevents)

    def test_skip(self):
        outdir = 'Out_test_skip'
        if os.path.isdir(outdir):
            shutil.rmtree(outdir)
        first = 10 
        loop = Looper( outdir, config,
                       nEvents=None,
                       firstEvent=first,
                       nPrint=0,
                       timeReport=True)
        loop.loop()
        loop.write()
        # input file has 200 entries
        # we skip 10 entries, so we process 190.
        self.assertEqual(loop.nEvProcessed, self.nevents-first)

    def test_process_event(self):
        '''Test that indeed, calling loop.process(iev) raises
        TypeError if the events backend does not support indexing. 
        '''
        outdir = 'Out_test_process_event'
        if os.path.isdir(outdir):
            shutil.rmtree(outdir)
        loop = Looper( outdir, config,
                       nEvents=None,
                       nPrint=0,
                       timeReport=True)
        self.assertRaises(TypeError, loop.process, 10)
        
       
if __name__ == '__main__':

    unittest.main()
