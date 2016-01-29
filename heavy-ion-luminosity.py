__author__ = 'jacob'
import ROOT
import numpy as np
import os
from root_numpy import root2array, root2rec, tree2rec

# Look at r284484 data

filename = os.path.join("data", "r284484.root")

# Convert a TTree in a ROOT file into a NumPy structured array
arr = root2array(filename)

for element in arr.dtype.names:
    print(element)
    print("\n")
# The TTree name is always optional if there is only one TTree in the file

# Convert a TTree in a ROOT file into a NumPy record array
rec = root2rec(filename)

# Get the TTree from the ROOT file
rfile = ROOT.TFile(filename)
