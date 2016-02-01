__author__ = 'jacob'
import ROOT
import numpy as np
from rootpy.plotting import Canvas, Graph
from rootpy.plotting.style import get_style, set_style
from rootpy.interactive import wait
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

lucid_event_or_bi = detector_array['LUCID_EVENTOR_BI'].tolist()

bcm_h_event_or = detector_array['BCM_H_EVENTOR'].tolist()

bcm_v_event_or = detector_array['BCM_V_EVENTOR'].tolist()

# Timing is named Status in the root file
timing = detector_array['Status'].tolist()


def plot_luminosity_ratio(detector_one_data, detector_two_data, timing, style):
    # Set ROOT graph style
    set_style(str(style))

    # Get ratio of the detectors
    luminosity_ratio = []
    for index in range(len(detector_one_data)):
        ratio = detector_one_data[index] / detector_two_data[index]
        luminosity_ratio.append(ratio)


    # create graph
    graph = Graph(len(timing))
    for i, (xx, yy) in enumerate(zip(timing, luminosity_ratio)):
        graph.SetPoint(i, xx, yy)

        # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Time")
    graph.yaxis.SetTitle("Luminosity")
    graph.xaxis.SetRangeUser(min(timing), max(timing))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    wait(True)


plot_luminosity_ratio(lucid_event_or_bi, bcm_h_event_or, timing, 'ATLAS')