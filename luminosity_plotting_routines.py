from __future__ import division

__author__ = 'jacob'
import ROOT
from rootpy.plotting import Canvas, Graph
from rootpy.plotting.style import get_style, set_style
from rootpy.interactive import wait
import math


def plot_luminosity_ratio(detector_one_data, detector_two_data, style, run_name):
    '''

    :param detector_one_data: Data from one detector type, such as ATLAS' LUCID, in a list of lists, every entry is one
    luminsoity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_two_data
    :param detector_two_data: Data from another detector type, such as ATLAS' LUCID, in a list of lists, every entry is
    one luminosity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_one_data
    :param style: The ROOT style for the graph, generally 'ATLAS'
    :return: ROOT plots of the ratio of luminosities over the luminosity
    '''
    # Set ROOT graph style
    set_style(str(style))

    print("Number of Luminosity Blocks included: " + str(len(detector_one_data)))
    # Get ratio of the detectors
    luminosity_ratio = []
    lumi_blocks = []
    for block in range(len(detector_one_data)):
        for bcid in range(len(detector_one_data[block])):
            detector_one_point = detector_one_data[block][bcid]
            detector_two_point = detector_two_data[block][bcid]
            # Check if the blocks are zero
            if detector_one_point != 0.0 and detector_two_point != 0.0:
                ratio = -math.log(1 - detector_one_point) / -math.log(1 - detector_two_point)
                luminosity_ratio.append(ratio)
                lumi_blocks.append(block)

    # create graph
    graph = Graph(len(lumi_blocks), title=run_name)
    for i, (xx, yy) in enumerate(zip(lumi_blocks, luminosity_ratio)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Ratio]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    label = ROOT.TText(0.8, 0.9, str(run_name))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)


def plot_normalized_luminosity_ratio(detector_one_data, detector_two_data, style, run_name):
    '''

    :param detector_one_data: Data from one detector type, such as ATLAS' LUCID, in a list of lists, every entry is one
    luminsoity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_two_data
    :param detector_two_data: Data from another detector type, such as ATLAS' LUCID, in a list of lists, every entry is
    one luminosity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_one_data
    :param style: The ROOT style for the graph, generally 'ATLAS'
    :return: ROOT plots of the ratio of luminosities over the luminosity, normalized to one
    '''

    # Set ROOT graph style
    set_style(str(style))

    print("Number of Luminosity Blocks included: " + str(len(detector_one_data)))

    # Get ratio of the detectors
    luminosity_ratio = []
    lumi_blocks = []
    for block in range(len(detector_one_data)):
        for bcid in range(len(detector_one_data[block])):
            detector_one_point = detector_one_data[block][bcid]
            detector_two_point = detector_two_data[block][bcid]
            # Check if the blocks are zero
            if detector_one_point != 0.0 and detector_two_point != 0.0:
                ratio = -math.log(1 - detector_one_point) / -math.log(1 - detector_two_point)
                luminosity_ratio.append(ratio)
                lumi_blocks.append(block)

    # Normalize the ratios
    def normalize(x, x_min, x_max):
        top = x - x_min
        bottom = x_max - x_min
        return top / bottom

    max_ratio = max(luminosity_ratio)
    min_ratio = min(luminosity_ratio)
    print("Max ratio: " + str(max_ratio))
    print("Min Ratio: " + str(min_ratio))
    for ratio_entry in range(len(luminosity_ratio)):
        luminosity_ratio[ratio_entry] = normalize(luminosity_ratio[ratio_entry], x_max=max_ratio, x_min=min_ratio)

    # create graph
    graph = Graph(len(lumi_blocks), title=run_name)
    for i, (xx, yy) in enumerate(zip(lumi_blocks, luminosity_ratio)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Normalized Ratio]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    label = ROOT.TText(0.8, 0.9, str(run_name))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)


def plot_percent_luminosity_ratio(detector_one_data, detector_two_data, style, run_name):
    '''

    :param detector_one_data: Data from one detector type, such as ATLAS' LUCID, in a list of lists, every entry is one
    luminsoity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_two_data
    :param detector_two_data: Data from another detector type, such as ATLAS' LUCID, in a list of lists, every entry is
    one luminosity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_one_data
    :param style: The ROOT style for the graph, generally 'ATLAS'
    :return: ROOT plots of the ratio of luminosities over the luminosity, as percetnage difference from first data point
    '''
    # Set ROOT graph style
    set_style(str(style))

    print("Number of Luminosity Blocks included: " + str(len(detector_one_data)))
    # Get ratio of the detectors
    luminosity_ratio = []
    lumi_blocks = []
    for block in range(len(detector_one_data)):
        for bcid in range(len(detector_one_data[block])):
            detector_one_point = detector_one_data[block][bcid]
            detector_two_point = detector_two_data[block][bcid]
            # Check if the blocks are zero
            if detector_one_point != 0.0 and detector_two_point != 0.0:
                ratio = -math.log(1 - detector_one_point) / -math.log(1 - detector_two_point)
                luminosity_ratio.append(ratio)
                lumi_blocks.append(block)

    # Get percentage difference based off the first block and BCID
    first_point = luminosity_ratio[0]

    for index in range(len(luminosity_ratio)):
        luminosity_ratio[index] = (luminosity_ratio[index] / first_point) - 1

    # create graph
    graph = Graph(len(lumi_blocks), title=run_name)
    for i, (xx, yy) in enumerate(zip(lumi_blocks, luminosity_ratio)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Percent Ratio]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    label = ROOT.TText(0.8, 0.9, str(run_name))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)


def plot_luminosity_log(detector_one_data, style, run_name):
    '''

    :param detector_one_data: Data from one detector type, such as ATLAS' LUCID, in a list of lists, every entry is one
    luminosity block, with the luminosity block being a list of BCID data
    :param style: The ROOT style for the graph, generally 'ATLAS'
    :return: ROOT plots of the ratio of luminosities over the luminosity, as percetnage difference from first data point
    '''
    # Set ROOT graph style
    set_style(str(style))

    print("Number of Luminosity Blocks included: " + str(len(detector_one_data)))
    # Get ratio of the detectors
    luminosity_ratio = []
    lumi_blocks = []
    for block in range(len(detector_one_data)):
        for bcid in range(len(detector_one_data[block])):
            detector_one_point = detector_one_data[block][bcid]
            # Check if the blocks are zero
            if detector_one_point != 0.0:
                ratio = -math.log(1 - detector_one_point)
                luminosity_ratio.append(ratio)
                lumi_blocks.append(block)

    # create graph
    graph = Graph(len(lumi_blocks), title=run_name)
    for i, (xx, yy) in enumerate(zip(lumi_blocks, luminosity_ratio)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Single Detector]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    label = ROOT.TText(0.8, 0.9, str(run_name))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)


# Functions to graph luminosity data
def luminosity_vs_time(timing_list, luminosity_list, style, run_name):
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
    graph.yaxis.SetRangeUser(min(luminosity_list), max(luminosity_list))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    label = ROOT.TText(0.8, 0.9, str(run_name))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)


# Functions to graph luminosity data
def luminosity_block_log_time(luminosity_list, style):
    '''

    :param timing_list: Python list containing the timing data
    :param luminosity_list: Python list containing the luminosity data
    :param style: ROOT style in string, such as 'ATLAS'
    :return: Graph of the luminosity over a single block
    '''
    # Set ROOT graph style
    set_style(str(style))

    luminosity_ratio = []
    for bcid in range(len(luminosity_list)):
        detector_one_point = luminosity_list[bcid]
        # Check if the blocks are zero
        if detector_one_point != 0.0:
            ratio = -math.log(1 - detector_one_point)
            luminosity_ratio.append(ratio)

    # create graph
    graph = Graph(len(luminosity_ratio))
    for i, (xx, yy) in enumerate(zip(range(len(luminosity_ratio)), luminosity_ratio)):
        graph.SetPoint(i, xx, yy)

        # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Time")
    graph.yaxis.SetTitle("-Ln(1 - Rate) [Single Detector]")
    graph.xaxis.SetRangeUser(0, 3564)
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    wait(True)
