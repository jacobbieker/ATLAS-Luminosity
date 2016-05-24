from __future__ import division

__author__ = 'jacob'
import ROOT
import numpy as np
import os
import math
from root_numpy import root2array
import luminosity_plotting_routines as lp
import glob

data_files = glob.iglob(os.path.join("data", "*.root"))
data_list = list(data_files)
data_list.sort()
master_luminosity_lucid_bi = {}
master_luminosity_lucid = {}
master_luminosity_bcm_h = {}
master_luminosity_bcm_v = {}
master_luminosity_lucid_bi_a = {}
master_luminosity_bcm_h_a = {}
master_luminosity_bcm_v_a = {}
master_luminosity_lucid_bi_c = {}
master_luminosity_bcm_h_c = {}
master_luminosity_bcm_v_c = {}
master_lumi_block_length = {}
master_status = {}
for file_name in data_list:
    detector_array = root2array(file_name)
    first_part_name = os.path.splitext(file_name)
    second_name = first_part_name[0].split("/")[1]
    display_name = second_name.split("r")[1]

    for element in detector_array.dtype.names:
        print(element)
        print("\n")

    # Get LUCID and BCM EventOR data to graph
    luminosity_block = detector_array['LBDATA_LB'].tolist()
    luminosity_block_stable = detector_array['LBDATA_stable'].tolist()
    luminosity_block_run = detector_array['LBDATA_Run'].tolist()

    start_time = detector_array['LBDATA_StartTime'].tolist()
    end_time = detector_array['LBDATA_EndTime'].tolist()

    lucid_event_or_bi = detector_array['LUCID_EVENTOR_BI'].tolist()

    lucid_event_or_bi_a = detector_array['LUCID_EVENTORA_BI'].tolist()
    lucid_event_or_bi_c = detector_array['LUCID_EVENTORC_BI'].tolist()

    lucid_event_or = detector_array['LUCID_EVENTOR_PMT'].tolist()

    lucid_event_or_a = detector_array['LUCID_EVENTORA_PMT'].tolist()
    lucid_event_or_c = detector_array['LUCID_EVENTORC_PMT'].tolist()

    bcm_h_event_or = detector_array['BCM_H_EVENTOR'].tolist()
    bcm_v_event_or = detector_array['BCM_V_EVENTOR'].tolist()

    bcm_h_event_or_a = detector_array['BCM_H_EVENTORA'].tolist()
    bcm_h_event_or_c = detector_array['BCM_H_EVENTORC'].tolist()

    bcm_v_event_or_a = detector_array['BCM_V_EVENTORA'].tolist()
    bcm_v_event_or_c = detector_array['BCM_V_EVENTORC'].tolist()


    # Timing is named Status in the root file
    status = detector_array['Status'].tolist()

    print("Length of LUCID: " + str(len(lucid_event_or_bi)))
    print(" Length of LUCID A: " + str(len(lucid_event_or_bi_a)))
    print(" Length of LUCID C: " + str(len(lucid_event_or_bi_c)))
    print(" Length of BCM H A: " + str(len(bcm_h_event_or_a)))
    print(" Length of BCM H C: " + str(len(bcm_h_event_or_c)))
    print(" Length of BCM V A: " + str(len(bcm_v_event_or_a)))
    print(" Length of BCM V C: " + str(len(bcm_v_event_or_c)))
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
    temp_lucid_bi = []
    temp_bcm_h = []
    temp_bcm_v = []
    temp_lucid_a = []
    temp_bcm_h_a = []
    temp_bcm_v_a = []
    temp_lucid_b = []
    temp_bcm_h_b = []
    temp_bcm_v_b = []

    # Go through each BCID number
    lucid_bi_sum = 0.0
    bcm_h_sum = 0.0
    bcm_v_sum = 0.0
    lucid_sum_a = 0.0
    bcm_h_sum_a = 0.0
    bcm_v_sum_a = 0.0
    lucid_sum_c = 0.0
    bcm_h_sum_c = 0.0
    bcm_v_sum_c = 0.0

    # Save each event to a list to plot later
    lucid_event_or_bi1 = [[] for _ in xrange(len(luminosity_block))]
    lucid_event_or1 = [[] for _ in xrange(len(luminosity_block))]
    bcm_v_event_or1 = [[] for _ in xrange(len(luminosity_block))]
    bcm_h_event_or1 = [[] for _ in xrange(len(luminosity_block))]
    lucid_event_or_bi1_a = [[] for _ in xrange(len(luminosity_block))]
    bcm_v_event_or1_a = [[] for _ in xrange(len(luminosity_block))]
    bcm_h_event_or1_a = [[] for _ in xrange(len(luminosity_block))]
    lucid_event_or_bi1_c = [[] for _ in xrange(len(luminosity_block))]
    bcm_v_event_or1_c = [[] for _ in xrange(len(luminosity_block))]
    bcm_h_event_or1_c = [[] for _ in xrange(len(luminosity_block))]
    block_length = [[] for _ in xrange(len(luminosity_block))]
    luminosity_ratio_lucid_h_sum = [[] for _ in xrange(len(luminosity_block))]
    luminosity_ratio_h_v_sum = [[] for _ in xrange(len(luminosity_block))]
    luminosity_ratio_lucid_v_sum = [[] for _ in xrange(len(luminosity_block))]
    luminosity_status = [[] for _ in xrange(len(luminosity_block))]
    new_luminosity_block = []
    count_bunches = 0
    for block in xrange(len(luminosity_block)):
        for bcid in xrange(3564):
            # Convert to simple luminosity plot, to try to get smooth drop off
            if luminosity_block_stable[block] > 0.0: #and status[block][bcid] > 0.0:
                if lucid_event_or_bi[block][bcid] > 0.0 and bcm_h_event_or[block][bcid] > 0.0 and bcm_v_event_or[block][bcid] > 0.0 and bcm_v_event_or_a[block][bcid] > 0.0 and bcm_v_event_or_c[block][bcid] > 0.0 and bcm_h_event_or_a[block][bcid] > 0.0 and bcm_h_event_or_c[block][bcid] > 0.0 and lucid_event_or_bi_c[block][bcid] > 0.0 and lucid_event_or_bi_a[block][bcid] > 0.0:
                    lucid_bi = lucid_event_or_bi[block][bcid]
                    lucid = lucid_event_or[block][bcid]
                    bcm_h = bcm_h_event_or[block][bcid]
                    bcm_v = bcm_v_event_or[block][bcid]
                    lucid_a = lucid_event_or_bi_a[block][bcid]
                    bcm_h_a = bcm_h_event_or_a[block][bcid]
                    bcm_v_a = bcm_v_event_or_a[block][bcid]
                    lucid_c = lucid_event_or_bi_c[block][bcid]
                    bcm_h_c = bcm_h_event_or_c[block][bcid]
                    bcm_v_c = bcm_v_event_or_c[block][bcid]
                    status_lum = status[block][bcid]
                    # Save the event to the list
                    lucid_event_or1[block].append(lucid)
                    lucid_event_or_bi1[block].append(lucid_bi)
                    bcm_h_event_or1[block].append(bcm_h)
                    bcm_v_event_or1[block].append(bcm_v)
                    lucid_event_or_bi1_a[block].append(lucid_a)
                    bcm_h_event_or1_a[block].append(bcm_h_a)
                    bcm_v_event_or1_a[block].append(bcm_v_a)
                    lucid_event_or_bi1_c[block].append(lucid_c)
                    bcm_h_event_or1_c[block].append(bcm_h_c)
                    bcm_v_event_or1_c[block].append(bcm_v_c)
                    luminosity_status[block].append(status_lum)
                    block_length1 = end_time[block] - start_time[block]
                    block_length[block].append(block_length1)
                    if status[block][bcid] > 0.0:
                        count_bunches += 1
                        #print(luminosity_status[block][bcid-1])
                        # Add as the negative log of 1 - rate, as that should be linear to luminosity
                        #lucid_sum += -math.log(1 - lucid[0])
                        #bcm_h_sum += -math.log(1 - bcm_h[0])
                        #bcm_v_sum += -math.log(1 - bcm_v[0])
            # Print out if the blocks are zero
            #if lucid_sum != 0.0 or bcm_h_sum != 0.0 or bcm_v_sum != 0.0:
             #   luminosity_ratio_lucid_h = lucid_sum / bcm_h_sum
              #  luminosity_ratio_lucid_v = lucid_sum / bcm_v_sum
               # luminosity_ratio_h_v = bcm_h_sum / bcm_v_sum
                #luminosity_ratio_lucid_h_sum[block].append(luminosity_ratio_lucid_h)
                #l#uminosity_ratio_lucid_v_sum[block].append(luminosity_ratio_lucid_v)
                #luminosity_ratio_h_v_sum[block].append(luminosity_ratio_h_v)
                #if status[block][bcid] > 0.0:
                 #   new_luminosity_block.append(block)
        count_bunches = 0

    # Add to master ones for plotting later
    master_luminosity_lucid_bi[display_name] = lucid_event_or_bi1
    master_luminosity_lucid[display_name] = lucid_event_or1
    master_luminosity_bcm_h[display_name] = bcm_h_event_or1
    master_luminosity_bcm_v[display_name] = bcm_v_event_or1
    master_luminosity_lucid_bi_a[display_name] = lucid_event_or_bi1_a
    master_luminosity_bcm_h_a[display_name] = bcm_h_event_or1_a
    master_luminosity_bcm_v_a[display_name] = bcm_v_event_or1_a
    master_luminosity_lucid_bi_c[display_name] = lucid_event_or_bi1_c
    master_luminosity_bcm_h_c[display_name] = bcm_h_event_or1_c
    master_luminosity_bcm_v_c[display_name] = bcm_v_event_or1_c
    master_lumi_block_length[display_name] = block_length
    master_status[display_name] = luminosity_status

# list of runs to subtract background on (currently just subtracting the previous not stable BCID
background_list = ["286282"]
print"Made it to Background list"

lp.plot_all_luminosity(master_luminosity_lucid_bi, master_lumi_block_length, bcid_status=master_status,
                       background_list=background_list,
                       style='ATLAS', name='LUCID BI EVENTOR', integrated=True, vs_data=[master_luminosity_bcm_v,
                                                                                         master_luminosity_bcm_h])

    # Actually plot the luminosity ratios
   # luminosity_plotting.plot_raw_detector_vs_detector(lucid_event_or_bi1, bcm_v_event_or1, 'ATLAS', str(display_name) + ' LUCID vs BCM V')
    #luminosity_plotting.plot_luminosity_log(lucid_event_or_bi1, 'ATLAS', display_name)
    #luminosity_plotting.plot_percent_luminosity_ratio_sum(lucid_event_or_bi1, bcm_v_event_or1,
     #                                                 'ATLAS', display_name)
    #luminosity_plotting.plot_bcid_percent_luminosity_ratio(lucid_event_or_bi1, bcm_v_event_or1,
     #                                                     'ATLAS', display_name)
'''luminosity_plotting.plot_normalized_luminosity_ratio(lucid_event_or_bi1, bcm_v_event_or1,
                                                         'ATLAS', display_name)
    luminosity_plotting.plot_luminosity_ratio(lucid_event_or_bi1, bcm_v_event_or1,
                                              'ATLAS', display_name)'''
'''
lp.plot_percent_luminosity_ratio(lucid_event_or1, bcm_h_event_or1, new_luminosity_block,
                                             'ATLAS', os.path.splitext(file_name)[0])
'''
'''
    luminosity_plotting.plot_normalized_luminosity_ratio(lucid_event_or_bi1, bcm_h_event_or1, new_luminosity_block,
                                                         'ATLAS', os.path.splitext(file_name)[0])
    luminosity_plotting.plot_luminosity_ratio(lucid_event_or_bi1, bcm_h_event_or1, new_luminosity_block,
                                              'ATLAS', os.path.splitext(file_name)[0])

    luminosity_plotting.plot_percent_luminosity_ratio(bcm_h_event_or1, bcm_v_event_or1, new_luminosity_block,
                                                      'ATLAS', os.path.splitext(file_name)[0])
    luminosity_plotting.plot_normalized_luminosity_ratio(bcm_h_event_or1, bcm_v_event_or1, new_luminosity_block,
                                                         'ATLAS', os.path.splitext(file_name)[0])
    luminosity_plotting.plot_luminosity_ratio(bcm_h_event_or1, bcm_v_event_or1, new_luminosity_block,
                                             'ATLAS', os.path.splitext(file_name)[0])
'''


# Plotting methods for plotting all the runs

lp.plot_all_luminosity_block_ratio(master_luminosity_lucid_bi, master_luminosity_lucid,
                                                    background_list, master_status,
                                                    'ATLAS',
                                                    'LUCID / LUCID BI')
'''
luminosity_plotting.plot_all_luminosity_block_ratio(master_luminosity_lucid_bi_a, master_luminosity_bcm_v_a,
                                                    background_list, master_status, 'ATLAS',
                                                    'LUCID BI A / BCM V A')

luminosity_plotting.plot_all_luminosity_block_ratio(master_luminosity_lucid_bi_c, master_luminosity_bcm_h_c,
                                                    background_list, master_status,'ATLAS',
                                                    'LUCID BI C/ BCM H C')
luminosity_plotting.plot_all_luminosity_block_ratio(master_luminosity_lucid_bi_c, master_luminosity_bcm_v_c,
                                                    background_list, master_status, 'ATLAS',
                                                    'LUCID BI C/ BCM V C')

luminosity_plotting.plot_all_luminosity_block_ratio(master_luminosity_lucid_bi_a, master_luminosity_bcm_h_a,
                                                    background_list, master_status, 'ATLAS',
                                                    'LUCID BI A/ BCM H A')
luminosity_plotting.plot_all_luminosity_block_ratio(master_luminosity_lucid_bi_a, master_luminosity_lucid_bi_c,
                                                    background_list, master_status, 'ATLAS',
                                                    'LUCID BI A/ LUCID BI C')

luminosity_plotting.plot_all_luminosity_block_ratio(master_luminosity_bcm_h_a, master_luminosity_bcm_h_c,
                                                    background_list, master_status, 'ATLAS',
                                                    'BCM H A / BCM H C')
luminosity_plotting.plot_all_luminosity_block_ratio(master_luminosity_bcm_v_a, master_luminosity_bcm_v_c,
                                                    background_list, master_status, 'ATLAS',
                                                    'BCM V A / BCM V C')
luminosity_plotting.plot_multiple_all_luminosity_block_ratio(master_luminosity_lucid_bi, master_luminosity_bcm_v,
                                                             master_luminosity_bcm_h, background_list, master_status,
                                                             'ATLAS', 'LUCID BI /BCM V & LUCID BI / BCM H')

luminosity_plotting.plot_all_integrated_luminosity(master_luminosity_lucid_bi, master_luminosity_bcm_v,
                                                   master_luminosity_bcm_h,
                                                   master_lumi_block_length, master_status, background_list, 'ATLAS',
                                                   'LUCID BI / BCM V LUCID BI / BCM H Integrated Ratio')
'''
