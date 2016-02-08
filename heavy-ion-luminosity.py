__author__ = 'jacob'
import ROOT
import numpy as np
from rootpy.plotting import Canvas, Graph
from rootpy.plotting.style import get_style, set_style
from rootpy.interactive import wait
import os
import math
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
                                  'BCM_V_EVENTOR', 'Status', 'LBDATA_stable', 'LBDATA_Run', 'LBDATA_LB']]

# Get LUCID and BCM EventOR data to graph
luminosity_block = detector_array['LBDATA_LB'].tolist()
luminosity_block_stable = detector_array['LBDATA_stable'].tolist()
luminosity_block_run = detector_array['LBDATA_Run'].tolist()

start_time = detector_array['LBDATA_StartTime'].tolist()
end_time = detector_array['LBDATA_EndTime'].tolist()

lucid_event_or_bi = detector_array['LUCID_EVENTOR_BI'][0].tolist()

bcm_h_event_or = detector_array['BCM_H_EVENTOR'][0].tolist()
bcm_v_event_or = detector_array['BCM_V_EVENTOR'][0].tolist()

# Timing is named Status in the root file
status = detector_array['Status'].tolist()

print("Length of LUCID: " + str(len(lucid_event_or_bi)))
print(" Length of BCM H: " + str(len(bcm_h_event_or)))
print(" Length of BCM V: " + str(len(bcm_v_event_or)))
print(" Length of Start: " + str(len(start_time)))
print(" Length of End: " + str(len(end_time)))
print(" Length of Status: " + str(len(status)))
print(" Length of Luminosity Block Data: " + str(len(luminosity_block)))
print(" Length of LB Stable: " + str(len(luminosity_block_stable)))
print(" Length of LB Run: " + str(len(luminosity_block_stable)))
# Slice the data to ignore certain datasets because of physical reasons
temp_lucid = []
temp_bcm_h = []
temp_bcm_v = []

# Go through each BCID number
lucid_sum = 0.0
bcm_h_sum = 0.0
bcm_v_sum = 0.0


# Save each event to a list to plot later
lucid_event_or_bi1 = []
bcm_v_event_or1 = []
bcm_h_event_or1 = []
for bcid in range(3564):
    if luminosity_block_stable[bcid] != 0.0 and status[bcid] != 0.0:
        lucid = lucid_event_or_bi[bcid]
        bcm_h = bcm_h_event_or[bcid]
        bcm_v = bcm_v_event_or[bcid]
        # Save the event to the list
        lucid_event_or_bi1.append(lucid)
        bcm_h_event_or1.append(bcm_h)
        bcm_v_event_or1.append(bcm_v)
        # Add as the negative log of 1 - rate, as that should be linear to luminosity
        lucid_sum += -math.log(1 - lucid)
        bcm_h_sum += -math.log(1 - bcm_h)
        bcm_v_sum += -math.log(1 - bcm_v)

luminosity_ratio_lucid_h = lucid_sum / bcm_h_sum

luminosity_ratio_lucid_v = lucid_sum / bcm_v_sum

luminosity_ratio_h_v = bcm_h_sum / bcm_v_sum

# Old way. Left in for now while making sure above is supposed to be the way to do it
for index in range(len(lucid_event_or_bi)):
    # Go through and eliminate entries where the detector value is zero, so that no divide by zero
    if lucid_event_or_bi[index] != 0.0 and bcm_h_event_or[index] != 0.0 and bcm_v_event_or[index] != 0.0:
        # Delete the values for the other detectors and timing for events that have zero
        temp_lucid.append(lucid_event_or_bi[index])
        temp_bcm_h.append(bcm_h_event_or[index])
        temp_bcm_v.append(bcm_v_event_or[index])

# Reset to previous arrays
lucid_event_or_bi = temp_lucid
bcm_h_event_or = temp_bcm_h
bcm_v_event_or = temp_bcm_v
print("Length of LUCID: " + str(len(lucid_event_or_bi)))
print(" Length of BCM H: " + str(len(bcm_h_event_or)))
print(" Length of BCM V: " + str(len(bcm_v_event_or)))
print(" Length of Start: " + str(len(start_time)))
print(" Length of End: " + str(len(end_time)))
print(" Length of Timing: " + str(len(status)))


def plot_luminosity_ratio(detector_one_data, detector_two_data, timing, style):
    # Set ROOT graph style
    set_style(str(style))


    # Get ratio of the detectors
    luminosity_ratio = []
    for index in range(len(detector_one_data)):
        ratio = -math.log(1 - detector_one_data[index]) / -math.log(1 - detector_two_data[index])
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



#plot_luminosity_ratio(lucid_event_or_bi, bcm_h_event_or, start_time, 'ATLAS')

#plot_luminosity_ratio(lucid_event_or_bi, bcm_h_event_or, start_time, 'ATLAS')

#plot_luminosity_ratio(bcm_h_event_or, bcm_v_event_or, start_time, 'ATLAS')

plot_luminosity_ratio(lucid_event_or_bi1, bcm_v_event_or1, status, 'ATLAS')