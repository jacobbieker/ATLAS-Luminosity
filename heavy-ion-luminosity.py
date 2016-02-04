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

# Slice the data to remove runs that have zeros at either detector or are too short
detector_subset = detector_array[['LBDATA_StartTime', 'LBDATA_EndTime', 'LUCID_EVENTOR_BI', 'BCM_H_EVENTOR',
                                  'BCM_V_EVENTOR', 'Status']]

# Get LUCID and BCM EventOR data to graph

start_time = detector_array['LBDATA_StartTime'].tolist()
end_time = detector_array['LBDATA_EndTime'].tolist()

lucid_event_or_bi = detector_array['LUCID_EVENTOR_BI'][0].tolist()

bcm_h_event_or = detector_array['BCM_H_EVENTOR'][0].tolist()
bcm_v_event_or = detector_array['BCM_V_EVENTOR'][0].tolist()

# Timing is named Status in the root file
timing = detector_array['Status'].tolist()

print("Length of LUCID: " + str(len(lucid_event_or_bi)))
print(" Length of BCM H: " + str(len(bcm_h_event_or)))
print(" Length of BCM V: " + str(len(bcm_v_event_or)))
print(" Length of Start: " + str(len(start_time)))
print(" Length of End: " + str(len(end_time)))
print(" Length of Timing: " + str(len(timing)))
# Slice the data to ignore certain datasets because of physical reasons
temp_lucid = []
temp_bcm_h = []
temp_bcm_v = []
for index in range(len(lucid_event_or_bi)):
    # Go through and eliminate entries where the detector value is zero, so that no divide by zero
    if lucid_event_or_bi[index] != 0.0 and bcm_h_event_or[index] != 0.0 and bcm_v_event_or[index] != 0.0:
        # Delete the values for the other detectors and timing for events that have zero
        temp_lucid.append(lucid_event_or_bi[index])
        temp_bcm_h.append(bcm_h_event_or[index])
        temp_bcm_v.append(bcm_v_event_or[index])
        #del start_time[index]
        #del end_time[index]
        #del timing[index]

# Reset to previous arrays
lucid_event_or_bi = temp_lucid
bcm_h_event_or = temp_bcm_h
bcm_v_event_or = temp_bcm_v
print("Length of LUCID: " + str(len(lucid_event_or_bi)))
print(" Length of BCM H: " + str(len(bcm_h_event_or)))
print(" Length of BCM V: " + str(len(bcm_v_event_or)))
print(" Length of Start: " + str(len(start_time)))
print(" Length of End: " + str(len(end_time)))
print(" Length of Timing: " + str(len(timing)))
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
        graph.SetPoint(i, float(xx), float(yy))

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