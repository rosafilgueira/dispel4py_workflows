from dispel4py.core import GenericPE
from dispel4py.workflow_graph import WorkflowGraph
from dispel4py.base import BasePE, IterativePE, GenericPE, create_iterative_chain

import numpy as np
import time
import os, shutil
import traceback
from tc_cross_correlation.xcorr import xcorrf, xcorrf_noFFT
from  distutils.dir_util  import create_tree as mkadir
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.backends
from obspy import read
import codecs, json
import pickle

ROOT_DIR = './tc_cross_correlation/OUTPUT/'
starttime='2015-04-06T06:00:00.000'

class Product(GenericPE):
    def __init__(self):
        GenericPE.__init__(self)
        self._add_output('output', tuple_type=['counter1', 'counter2', 'station1', 'station2'])
    def process(self, inputs):
        store = []
        for dir in os.listdir(ROOT_DIR + 'DATA/'+ starttime):
            for f in os.listdir(ROOT_DIR+'/DATA/'+ starttime +'/'+ dir):
               file=ROOT_DIR+'DATA/'+ starttime + '/'+ dir+'/'+f
               self.log("open file %s" % file)
               str1_array= np.load(file)
               str1 = pickle.dumps(str1_array)
               index = len(store)
               for i in range(index):
                  self.write('output',[i, index, store[i], str1])                                                                                                 
               store.append(str1)                                                                                                                                 
                                                                                                                                                                  
                                                                                                                                                                  
class Xcorr(GenericPE):                                                                                                                                           
    def __init__(self):                                                                                                                                           
        GenericPE.__init__(self)                                                                                                                                  
        self._add_input ('input')                                                                                                                                 
        self._add_output('output', tuple_type=['counter1','counter2', 'xcorr'])                                                                                   
    def process(self, inputs):                                                                                                                                    
        str1=pickle.loads(inputs['input'][2])                                                                                                                     
        str2=pickle.loads(inputs['input'][3])                                                                                                                     
        try:                                                                                                                                                      
            xcorr1 = xcorrf_noFFT(str1, str2, 5000)                                                                                                               
            xcorr1_pickle = pickle.dumps(xcorr1)                                                                                                                  
            self.write('output',[inputs['input'][0], inputs['input'][1], xcorr1_pickle])                                                                          
        except:                                                                                                                                                   
            self.log('error in %s_%s xcorr' % (inputs['input'][0], inputs['input'][1]))                                                                           
            self.log(traceback.format_exc())                                                                                                                      
                                                                                                                                                                  
class StreamToFile(GenericPE):                                                                                                                                    
    def __init__(self):                                                                                                                                           
        GenericPE.__init__(self)                                                                                                                                  
        self._add_input ('input')                                                                                                                                 
    def _process(self, inputs):                                                                                                                                   
        try:                                                                                                                                                      
            self.log('wrote xcorr (%s, %s)' % (inputs['input'][0], inputs['input'][1]))                                                                           
        except:                                                                                                                                                   
            self.log(traceback.format_exc())                                                                                                                      
                                                                                                                                                                  
class Plot(GenericPE):                                                                                                                                            
    def __init__(self):                                                                                                                                           
        GenericPE.__init__(self)                                                                                                                                  
        self._add_input ('input')                                                                                                                                 
    def process(self, inputs):                                                                                                                                    
        try:                                                                                                                                                      
            self.log('plot xcorr (%s, %s)' % (inputs['input'][0], inputs['input'][1]))                                                                            
        except:                                                                                                                                                   
            self.log(traceback.format_exc())                                                                                                                      
                                                                                                                                                                  
                                                                                                                                                                  
                                                                                                                                                                  
product=Product()                                                                                                                                                 
xcorr=Xcorr()                                                                                                                                                     
store_xcorr = StreamToFile()                                                                                                                                      
plot = Plot()                                                                                                                                                     
graph = WorkflowGraph()                                                                                                                                           
                                                                                                                                                                  
graph.connect(product, 'output', xcorr, 'input')                                                                                                                  
graph.connect(xcorr, 'output', store_xcorr, 'input')                                                                                                              
graph.connect(xcorr, 'output', plot, 'input')  
