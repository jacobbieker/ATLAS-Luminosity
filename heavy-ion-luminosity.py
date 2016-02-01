__author__ = 'jacob'
import ROOT
import numpy as np
import os
from root_numpy import root2array, root2rec, tree2rec

# Look at r284484 data

filename = os.path.join("data", "r284484.root")

# Convert a TTree in a ROOT file into a NumPy structured array
detector_array = root2array(filename)

for element in detector_array.dtype.names:
    print(element)
    print("\n")
# Get the TTree from the ROOT file
rfile = ROOT.TFile(filename)

# Get LUCID and BCM EventOR data to graph

lucid_event_or_bi = detector_array['LUCID_EVENTOR_BI']

bcm_h_event_or = detector_array['BCM_H_EVENTOR']

bcm_v_event_or = detector_array['BCM_V_EVENTOR']

