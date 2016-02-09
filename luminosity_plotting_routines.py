from __future__ import division

__author__ = 'jacob'
import ROOT
from rootpy.plotting import Canvas, Graph
from rootpy.plotting.style import get_style, set_style
from rootpy.interactive import wait
import math


def plot_luminosity_ratio(detector_one_data, detector_two_data, luminosity_blocks, style):
    '''

    :param detector_one_data: Data from one detector type, such as ATLAS' LUCID, in a list of lists, every entry is one
    luminsoity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_two_data
    :param detector_two_data: Data from another detector type, such as ATLAS' LUCID, in a list of lists, every entry is
    one luminosity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_one_data
    :param luminosity_blocks: A list of luminosity blocks
    :param style: The ROOT style for the graph, generally 'ATLAS'
    :return: ROOT plots of the ratio of luminosities over the luminosity
    '''
    # Set ROOT graph style
    set_style(str(style))


    # Get ratio of the detectors
    luminosity_ratio = []
    for block in range(len(detector_one_data)):
        for bcid in range(len(detector_one_data[block])):
            ratio = -math.log(1 - detector_one_data[block][bcid]) / -math.log(1 - detector_two_data[block][bcid])
            luminosity_ratio.append(ratio)

    # create graph
    graph = Graph(len(luminosity_blocks))
    for i, (xx, yy) in enumerate(zip(luminosity_blocks, luminosity_ratio)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity")
    graph.xaxis.SetRangeUser(min(luminosity_blocks), max(luminosity_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    wait(True)


def plot_normalized_luminosity_ratio(detector_one_data, detector_two_data, luminosity_blocks, style):
    '''

    :param detector_one_data: Data from one detector type, such as ATLAS' LUCID, in a list of lists, every entry is one
    luminsoity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_two_data
    :param detector_two_data: Data from another detector type, such as ATLAS' LUCID, in a list of lists, every entry is
    one luminosity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_one_data
    :param luminosity_blocks: A list of luminosity blocks
    :param style: The ROOT style for the graph, generally 'ATLAS'
    :return: ROOT plots of the ratio of luminosities over the luminosity, normalized to one
    '''
    # Set ROOT graph style
    set_style(str(style))


    # Get ratio of the detectors
    luminosity_ratio = []
    for block in range(len(detector_one_data)):
        for bcid in range(len(detector_one_data[block])):
            detector_one_point = detector_one_data[block][bcid]
            detector_two_point = detector_two_data[block][bcid]
            # Print out if the blocks are zero
            if detector_one_point != 0.0 or detector_two_point != 0.0:
                luminosity_ratio_lucid_h = lucid_sum / bcm_h_sum
                luminosity_ratio_lucid_v = lucid_sum / bcm_v_sum
                luminosity_ratio_h_v = bcm_h_sum / bcm_v_sum
                luminosity_ratio_lucid_h_sum[block].append(luminosity_ratio_lucid_h)
                luminosity_ratio_lucid_v_sum[block].append(luminosity_ratio_lucid_v)
                luminosity_ratio_h_v_sum[block].append(luminosity_ratio_h_v)
                ratio = -math.log(1 - detector_one_data[block][bcid]) / -math.log(1 - detector_two_data[block][bcid])
                luminosity_ratio.append(ratio)

    # create graph
    graph = Graph(len(luminosity_blocks))
    for i, (xx, yy) in enumerate(zip(luminosity_blocks, luminosity_ratio)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity")
    graph.xaxis.SetRangeUser(min(luminosity_blocks), max(luminosity_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    wait(True)


# Functions to graph luminosity data
def luminosity_vs_time(timing_list, luminosity_list, style):
    '''

    :param timing_list: Python list containing the timing data
    :param luminosity_list: Python list containing the luminosity data
    :param style: ROOT style in string, such as 'ATLAS'
    :return:
    '''
    # Set ROOT graph style
    set_style(str(style))

    # create graph
    graph = Graph(len(timing_list))
    for i, (xx, yy) in enumerate(zip(timing_list, luminosity_list)):
        graph.SetPoint(i, xx, yy)

        # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Time")
    graph.yaxis.SetTitle("Luminosity")
    graph.xaxis.SetRangeUser(min(timing_list), max(timing_list))
    graph.yaxis.SetRangeUser(1, max(luminosity_list))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    wait(True)
