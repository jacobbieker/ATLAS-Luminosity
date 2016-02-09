from __future__ import division

__author__ = 'jacob'
import ROOT
import numpy as np
import os
import math
from root_numpy import root2array
import luminosity_plotting_routines as luminosity_plotting
import glob

data_files = glob.iglob(os.path.join("data", "*.root"))
for file_name in data_files:
    detector_array = root2array(file_name)

    # Get LUCID and BCM EventOR data to graph
    luminosity_block = detector_array['LBDATA_LB'].tolist()
    luminosity_block_stable = detector_array['LBDATA_stable'].tolist()
    luminosity_block_run = detector_array['LBDATA_Run'].tolist()

    start_time = detector_array['LBDATA_StartTime'].tolist()
    end_time = detector_array['LBDATA_EndTime'].tolist()

    lucid_event_or_bi = detector_array['LUCID_EVENTOR_BI'].tolist()

    bcm_h_event_or = detector_array['BCM_H_EVENTOR'].tolist()
    bcm_v_event_or = detector_array['BCM_V_EVENTOR'].tolist()

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

    # Each luminosity block is an array in the
    # Slice the data to ignore certain datasets because of physical reasons
    temp_lucid = []
    temp_bcm_h = []
    temp_bcm_v = []

    # Go through each BCID number
    lucid_sum = 0.0
    bcm_h_sum = 0.0
    bcm_v_sum = 0.0

    # Save each event to a list to plot later
    lucid_event_or_bi1 = [[] for _ in xrange(len(luminosity_block))]
    bcm_v_event_or1 = [[] for _ in xrange(len(luminosity_block))]
    bcm_h_event_or1 = [[] for _ in xrange(len(luminosity_block))]
    luminosity_ratio_lucid_h_sum = [[] for _ in xrange(len(luminosity_block))]
    luminosity_ratio_h_v_sum = [[] for _ in xrange(len(luminosity_block))]
    luminosity_ratio_lucid_v_sum = [[] for _ in xrange(len(luminosity_block))]
    new_luminosity_block = []

    for block in range(len(luminosity_block)):
        for bcid in range(3564):
            if luminosity_block_stable[block] > 0.0 and status[block] > 0.0:
                if lucid_event_or_bi[block][bcid] > 0.0 and bcm_h_event_or[block][bcid] > 0.0 and bcm_v_event_or[block][bcid] > 0.0:
                    lucid = lucid_event_or_bi[block][bcid]
                    bcm_h = bcm_h_event_or[block][bcid]
                    bcm_v = bcm_v_event_or[block][bcid]
                    # Save the event to the list
                    lucid_event_or_bi1[block].append(lucid)
                    bcm_h_event_or1[block].append(bcm_h)
                    bcm_v_event_or1[block].append(bcm_v)
                    # Add as the negative log of 1 - rate, as that should be linear to luminosity
                    lucid_sum += -math.log(1 - lucid)
                    bcm_h_sum += -math.log(1 - bcm_h)
                    bcm_v_sum += -math.log(1 - bcm_v)
        # Print out if the blocks are zero
        if lucid_sum != 0.0 or bcm_h_sum != 0.0 or bcm_v_sum != 0.0:
            luminosity_ratio_lucid_h = lucid_sum / bcm_h_sum
            luminosity_ratio_lucid_v = lucid_sum / bcm_v_sum
            luminosity_ratio_h_v = bcm_h_sum / bcm_v_sum
            luminosity_ratio_lucid_h_sum[block].append(luminosity_ratio_lucid_h)
            luminosity_ratio_lucid_v_sum[block].append(luminosity_ratio_lucid_v)
            luminosity_ratio_h_v_sum[block].append(luminosity_ratio_h_v)
            new_luminosity_block.append(block)

    # Actually plot the luminosity ratios
    luminosity_plotting.plot_normalized_luminosity_ratio(lucid_event_or_bi1, bcm_v_event_or1, new_luminosity_block, 'ATLAS')

    luminosity_plotting.plot_normalized_luminosity_ratio(lucid_event_or_bi1, bcm_h_event_or1, new_luminosity_block, 'ATLAS')

    luminosity_plotting.plot_normalized_luminosity_ratio(bcm_h_event_or1, bcm_v_event_or1, new_luminosity_block, 'ATLAS')