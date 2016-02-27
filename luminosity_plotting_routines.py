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


def plot_percent_luminosity_ratio_sum(detector_one_data, detector_two_data, style, run_name):
    '''

    :param detector_one_data: Data from one detector type, such as ATLAS' LUCID, in a list of lists, every entry is one
    luminsoity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_two_data
    :param detector_two_data: Data from another detector type, such as ATLAS' LUCID, in a list of lists, every entry is
    one luminosity block, with the luminosity block being a list of BCID data, assumed to be same
    length as detector_one_data
    :param style: The ROOT style for the graph, generally 'ATLAS'
    :return: ROOT plots of the ratio of luminosity sums over the luminosity, as percentage difference from first data point
    '''
    # Set ROOT graph style
    set_style(str(style))

    print("Number of Luminosity Blocks included: " + str(len(detector_one_data)))

    # Get average value of the rate for each luminosity block
    temp_detector_one = [[] for _ in xrange(len(detector_one_data))]
    temp_detector_two = [[] for _ in xrange(len(detector_one_data))]
    for block in range(len(detector_one_data)):
        detector_one_avg = 0
        one_count = 0
        detector_two_avg = 0
        two_count = 0
        for bcid in range(len(detector_one_data[block])):
            detector_one_point = detector_one_data[block][bcid]
            detector_two_point = detector_two_data[block][bcid]
            detector_one_avg += detector_one_point
            one_count += 1
            detector_two_avg += detector_two_point
            two_count += 1
        if one_count != 0:
            detector_one_avg = detector_one_avg / one_count
            detector_two_avg = detector_two_avg / two_count
            temp_detector_one[block].append(detector_one_avg)
            temp_detector_two[block].append(detector_two_avg)

    # Reassign temp to the original lists
    detector_one_data = temp_detector_one
    detector_two_data = temp_detector_two

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

    # Delete last point, when the beams are being shut down and there are massive spikes
    luminosity_ratio = luminosity_ratio[:-1]
    lumi_blocks = lumi_blocks[:-1]
    # create graph
    graph = Graph(len(lumi_blocks), title=run_name)
    for i, (xx, yy) in enumerate(zip(lumi_blocks, luminosity_ratio)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Average Percent Ratio]")
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


# Functions to graph BCID events
def plot_bcid_percent_luminosity_ratio(detector_one_data, detector_two_data, style, run_name):
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
    for bcid in range(len(detector_one_data[0])):
        detector_one_point = detector_one_data[0][bcid]
        detector_two_point = detector_two_data[0][bcid]
        # Check if the blocks are zero
        if detector_one_point != 0.0 and detector_two_point != 0.0:
            ratio = -math.log(1 - detector_one_point) / -math.log(1 - detector_two_point)
            luminosity_ratio.append(ratio)
            lumi_blocks.append(bcid)

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
    graph.xaxis.SetTitle("BCID")
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


# Functions with all the runs
def plot_all_luminosity_block_ratio(all_detector_one_data, all_detector_two_data, style, names):
    # Set ROOT graph style
    set_style(str(style))
    print(names)
    names_true = []
    names_true = names
    print(names_true)
    names_true.sort()
    print(names_true)
    print("Number of Runs included: " + str(len(all_detector_one_data)))

    # Get average value of the rate for each luminosity block
    temp_detector_one = [[] for _ in xrange(len(all_detector_one_data))]
    temp_detector_two = [[] for _ in xrange(len(all_detector_one_data))]
    for run in range(len(all_detector_one_data)):
        block_count = 0
        temp_detector_one[run] = [[] for _ in xrange(len(all_detector_one_data[run]))]
        temp_detector_two[run] = [[] for _ in xrange(len(all_detector_one_data[run]))]
        for block in range(len(all_detector_one_data[run]) - 1):
            block_count += 1
            detector_one_avg = 0
            one_count = 0
            detector_two_avg = 0
            two_count = 0
            for bcid in range(len(all_detector_one_data[run][block])):
                detector_one_point = all_detector_one_data[run][block][bcid]
                detector_two_point = all_detector_two_data[run][block][bcid]
                detector_one_avg += detector_one_point
                one_count += 1
                detector_two_avg += detector_two_point
                two_count += 1
            if one_count != 0:
                detector_one_avg = detector_one_avg / one_count
                detector_two_avg = detector_two_avg / two_count
                temp_detector_one[run][block_count - 1].append(detector_one_avg)
                temp_detector_two[run][block_count - 1].append(detector_two_avg)
        # Remove the last luminosity block from each run, the one that generally spikes
        temp_detector_one[run] = temp_detector_one[run][:-1]
        temp_detector_two[run] = temp_detector_two[run][:-1]
    # Reassign temp to the original lists
    all_detector_two_data = temp_detector_two
    print(names)
    print(all_detector_one_data)
    all_detector_one_data = [x for (y,x) in sorted(zip(names,temp_detector_one), key=lambda pair: pair[0])]
    print(all_detector_one_data)
    print(names)
    all_detector_two_data = [x for (y,x) in sorted(zip(names,temp_detector_two), key=lambda pair: pair[0])]
    # Get ratio of the detectors
    luminosity_ratio = []
    lumi_blocks = []
    block_count1 = 0
    for run in range(len(all_detector_one_data)):
        for block in range(len(all_detector_one_data[run])):
            block_count1 += 1
            for bcid in range(len(all_detector_one_data[run][block])):
                detector_one_point = all_detector_one_data[run][block][bcid]
                detector_two_point = all_detector_two_data[run][block][bcid]
                # Check if the blocks are zero
                if detector_one_point != 0.0 and detector_two_point != 0.0:
                    ratio = -math.log(1 - detector_one_point) / -math.log(1 - detector_two_point)
                    luminosity_ratio.append(ratio)
                    lumi_blocks.append(block_count1)

    # Get percentage difference based off the first block and BCID
    first_point = luminosity_ratio[0]

    for index in range(len(luminosity_ratio)):
        luminosity_ratio[index] = (luminosity_ratio[index] / first_point) - 1

    # create graph
    graph = Graph(len(lumi_blocks))
    for i, (xx, yy) in enumerate(zip(lumi_blocks, luminosity_ratio)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Average Percent Ratio]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(-0.3, 1)

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    label = ROOT.TText(0.8, 0.9, str("All Runs"))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)


def plot_raw_detector_vs_detector(detector_one_data, detector_two_data, style, name):
    # Set ROOT graph style
    set_style(str(style))
    detector_one_list = []
    detector_two_list = []
    for block in range(len(detector_one_data)):
        for bcid in range(len(detector_one_data[block])):
            detector_one_list.append(detector_one_data[block][bcid])
            detector_two_list.append(detector_two_data[block][bcid])
    # create graph
    graph = Graph(len(detector_one_list))
    for i, (xx, yy) in enumerate(zip(detector_one_list, detector_two_list)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("BCM V [Raw Rate]")
    graph.yaxis.SetTitle("LUCID BI [Raw Rate]")
    graph.xaxis.SetRangeUser(0, 1)
    graph.yaxis.SetRangeUser(0, 1)

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    label = ROOT.TText(0.6, 0.9, str(name))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)


def plot_detector_vs_detector_ratio(detector_one_data, detector_two_data, style, name):
    # Set ROOT graph style
    set_style(str(style))
    detector_one_list = []
    detector_two_list = []
    lumi_blocks = []
    for block in range(len(detector_one_data)):
        for bcid in range(len(detector_one_data[block])):
            detector_one_list.append(detector_one_data[block][bcid])
            detector_two_list.append(detector_two_data[block][bcid])


    # create graph
    graph = Graph(len(detector_one_list))
    for i, (xx, yy) in enumerate(zip(detector_one_list, detector_two_list)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.linecolor = 'white'  # Hides the lines at this time
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("BCM V")
    graph.yaxis.SetTitle("LUCID BI")
    graph.xaxis.SetRangeUser(min(detector_two_list), max(detector_two_list))
    graph.yaxis.SetRangeUser(min(detector_one_list), max(detector_one_list))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")
    label = ROOT.TText(0.8, 0.9, str(name))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)