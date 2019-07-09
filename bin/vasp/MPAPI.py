# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 21:31:58 2017

@author: clian
"""



from pymatgen.matproj.rest import MPRester
#from pymatgen.phasediagram.pdmaker import PhaseDiagram
#from pymatgen.phasediagram.plotter import PDPlotter

#This initializes the REST adaptor. Put your own API key in.
a = MPRester("0aUWdnPklbFXw2zT")

entries = a.get_entries_in_chemsys(['Pb', 'Ti', 'O'])


print entries