from __future__ import division

__author__ = 'jacob'
import ROOT
from rootpy.plotting import Canvas, Graph
from rootpy.plotting.style import get_style, set_style
from rootpy.interactive import wait
import math
import copy


def convert_to_raw_luminosity(f_rev, sigma_vis, mu_vis):
    converted = f_rev / sigma_vis
    converted *= mu_vis
    return converted


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

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Ratio]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("AP")
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

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Normalized Ratio]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("AP")
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

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Percent Ratio]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("AP")
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

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Average Percent Ratio]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("AP")
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

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Single Detector]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("AP")
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

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Time")
    graph.yaxis.SetTitle("Luminosity")
    graph.xaxis.SetRangeUser(min(timing_list), max(timing_list))
    graph.yaxis.SetRangeUser(min(luminosity_list), max(luminosity_list))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("AP")
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

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Time")
    graph.yaxis.SetTitle("-Ln(1 - Rate) [Single Detector]")
    graph.xaxis.SetRangeUser(0, 3564)
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("AP")
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

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("BCID")
    graph.yaxis.SetTitle("Luminosity [Percent Ratio]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("AP")
    label = ROOT.TText(0.8, 0.9, str(run_name))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)


# Functions with all the runs
def plot_all_luminosity_block_ratio(all_detector_one_data, all_detector_two_data, background_list, status_data, style, name):
    '''

    :param all_detector_one_data: A dictionary of the run name to a list of lists of luminosity blocks
    :param all_detector_two_data: A dictionary of the run name to a list of lists of luminosity blocks
    :param style: a string corresponding to a ROOT graphing style, e.g. 'ATLAS'
    :return: Plot of all the detector data on a graph chronologically according to run number
    '''
    # Set ROOT graph style
    set_style(str(style))

    # Get average value of the rate for each luminosity block
    temp_detector_one = copy.deepcopy(all_detector_one_data)
    temp_detector_two = copy.deepcopy(all_detector_two_data)
    # print(sorted(all_detector_one_data.keys()))
    for run in sorted(all_detector_one_data.keys()):
        block_count = 0
        print"Starting run", run
        for block in range(len(all_detector_one_data.get(run)) - 1):
            del temp_detector_one.get(run)[block][:]
            del temp_detector_two.get(run)[block][:]
            block_count += 1
            detector_one_avg = 0
            one_count = 0
            detector_two_avg = 0
            two_count = 0
            for bcid in range(len(all_detector_one_data.get(run)[block])):
                # Gets the previous BCID luminosity to subtract as the background
                if run in background_list:
                    if status_data.get(run)[block][bcid - 1] <= 0.0:
                        detector_one_point_background = all_detector_one_data.get(run)[block][bcid - 1]
                        detector_two_point_background = all_detector_two_data.get(run)[block][bcid - 1]
                        print("BCID [N-1] Stability: " + str(status_data.get(run)[block][bcid - 1]))
                    else:
                        print("No empty BCID to subtract background from")
                    if all_detector_one_data.get(run)[block][bcid] < 1 and all_detector_two_data.get(run)[block][bcid] < 1:
                        print("BCID [N] Stability: " + str(status_data.get(run)[block][bcid]))
                        detector_one_point = -math.log(1 - all_detector_one_data.get(run)[block][bcid]) \
                                             + math.log(1 - detector_one_point_background)
                        print("Detector 1 Point: " + str(detector_one_point))
                        detector_two_point = -math.log(1 - all_detector_two_data.get(run)[block][bcid]) \
                                             + math.log(1 - detector_two_point_background)
                        print("Detector 2 Point: " + str(detector_two_point))
                        detector_one_avg += detector_one_point
                        one_count += 1
                        detector_two_avg += detector_two_point
                        two_count += 1
                else:
                    #print("         RUN:     " + str(run) + "                    END")
                    #print(all_detector_one_data.get(run)[block][bcid])
                    # Checking if the status is stable
                    if 1 > all_detector_one_data.get(run)[block][bcid] > 0.0 and 1 > all_detector_two_data.get(run)[block][bcid] > 0.0\
                            and status_data.get(run)[block][bcid] > 0.0:
                        #print("Value of Block, BCID: " + str(block) + " " + str(bcid) + " " + str(all_detector_one_data.get(run)[block][bcid]))
                        detector_one_point = -math.log(1 - all_detector_one_data.get(run)[block][bcid])
                        detector_two_point = -math.log(1 - all_detector_two_data.get(run)[block][bcid])
                        detector_one_avg += detector_one_point
                        one_count += 1
                        detector_two_avg += detector_two_point
                        two_count += 1
            if one_count != 0:
                detector_one_avg = detector_one_avg / one_count
                detector_two_avg = detector_two_avg / two_count
                if run == "286282":
                    print("One Average: " + str(detector_one_avg))
                temp_detector_one.get(run)[block_count - 1].append(detector_one_avg)
                temp_detector_two.get(run)[block_count - 1].append(detector_two_avg)
        # Remove the last luminosity block from each run, the one that generally spikes
        temp_detector_one[run] = temp_detector_one[run][:-10]
        temp_detector_two[run] = temp_detector_two[run][:-10]
    # Reassign temp to the original lists
    all_detector_one_data = temp_detector_one
    all_detector_two_data = temp_detector_two

    # Get ratio of the detectors
    luminosity_ratio = []
    lumi_blocks = []
    block_count1 = 0
    for run in sorted(all_detector_one_data.keys()):
        for block in range(len(all_detector_one_data.get(run))):
            block_count1 += 1
            for bcid in range(len(all_detector_one_data.get(run)[block])):
                detector_one_point = all_detector_one_data.get(run)[block][bcid]
                detector_two_point = all_detector_two_data.get(run)[block][bcid]
                # Check if the blocks are zero
                if detector_one_point != 0.0 or detector_two_point != 0.0:
                    ratio = detector_one_point / detector_two_point
                    luminosity_ratio.append(ratio)
                    lumi_blocks.append(block_count1)
                else:
                    print("Run", str(run), " Block:", str(block), "One:", str(detector_one_point),
                          "Two:", str(detector_two_point))

    print("Length lumi_blocks: " + str(len(lumi_blocks)))
    print("length lumi_ratio: " + str((len(luminosity_ratio))))

    # Get percentage difference based off the first block and BCID
    first_point = luminosity_ratio[0]

    for index in range(len(luminosity_ratio)):
        luminosity_ratio[index] = 100 * ((luminosity_ratio[index] / first_point) - 1)

    # create graph
    graph = Graph(len(lumi_blocks))
    for i, (xx, yy) in enumerate(zip(lumi_blocks, luminosity_ratio)):
        #print (xx, yy)
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Average Percent Ratio]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))
    # graph.yaxis.SetRangeUser(-15, 15)

    # plot with ROOT
    canvas = Canvas()

    graph.Draw("AP")
    # Draw lines for different runs
    run_length = 0
    for run in sorted(all_detector_one_data.keys()):
        #print("Length of Run " + str(run) + ": " + str(len(all_detector_one_data.get(run))))
        run_length += len(all_detector_one_data.get(run))
        line = ROOT.TLine(run_length, min(luminosity_ratio),
                          run_length, max(luminosity_ratio))
        line.Draw()
        line_label = ROOT.TText(run_length - 30, max(luminosity_ratio) - 1.5, str(run))
        line_label.SetTextAngle(90)
        line_label.SetTextSize(18)
        line_label.SetTextFont(43)
        line_label.Draw()
    label = ROOT.TText(0.7, 0.8, str(name))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)


def plot_multiple_all_luminosity_block_ratio(all_detector_one_data, all_detector_two_data, all_detector_three_data,
                                             background_list, style, name):
    '''

    :param all_detector_one_data: A dictionary of the run name to a list of lists of luminosity blocks
    :param all_detector_two_data: A dictionary of the run name to a list of lists of luminosity blocks
    :param style: a string corresponding to a ROOT graphing style, e.g. 'ATLAS'
    :return: Plot of all the detector data on a graph chronologically according to run number
    '''
    # Set ROOT graph style
    set_style(str(style))

    # Get average value of the rate for each luminosity block
    temp_detector_one = copy.deepcopy(all_detector_one_data)
    temp_detector_two = copy.deepcopy(all_detector_two_data)
    temp_detector_three = copy.deepcopy(all_detector_three_data)
    print(sorted(all_detector_one_data.keys()))
    for run in sorted(all_detector_one_data.keys()):
        block_count = 0
        for block in range(len(all_detector_one_data.get(run)) - 1):
            del temp_detector_one.get(run)[block][:]
            del temp_detector_two.get(run)[block][:]
            del temp_detector_three.get(run)[block][:]
            block_count += 1
            detector_one_avg = 0
            one_count = 0
            detector_two_avg = 0
            two_count = 0
            detector_three_avg = 0
            three_count = 0
            for bcid in range(len(all_detector_one_data.get(run)[block])):
                # Gets the previous BCID luminosity to subtract as the background
                if run == "286282":
                    detector_one_point_background = all_detector_one_data.get(run)[block][bcid - 1]
                    detector_two_point_background = all_detector_two_data.get(run)[block][bcid - 1]
                    detector_three_point_background = all_detector_three_data.get(run)[block][bcid - 1]
                    print("BCID [N-1]: " + str(detector_one_point_background))
                    print("BCID [N]: " + str(all_detector_one_data.get(run)[block][bcid]))
                    detector_one_point = -math.log(1 - all_detector_one_data.get(run)[block][bcid]) \
                                         + math.log(1 - detector_one_point_background)
                    detector_three_point = -math.log(1 - all_detector_three_data.get(run)[block][bcid]) \
                                           + math.log(1 - detector_three_point_background)
                    print("Detector 1 Point: " + str(detector_one_point))
                    detector_two_point = -math.log(1 - all_detector_two_data.get(run)[block][bcid]) \
                                         + math.log(1 - detector_two_point_background)
                    detector_one_avg += detector_one_point
                    one_count += 1
                    detector_two_avg += detector_two_point
                    two_count += 1
                    detector_three_avg += detector_three_point
                    three_count += 1
                else:
                    detector_one_point = -math.log(1 - all_detector_one_data.get(run)[block][bcid])
                    detector_two_point = -math.log(1 - all_detector_two_data.get(run)[block][bcid])
                    detector_three_point = -math.log(1 - all_detector_three_data.get(run)[block][bcid])
                    detector_one_avg += detector_one_point
                    one_count += 1
                    detector_two_avg += detector_two_point
                    two_count += 1
                    detector_three_avg += detector_three_point
                    three_count += 1
            if one_count != 0:
                detector_one_avg = detector_one_avg / one_count
                detector_two_avg = detector_two_avg / two_count
                detector_three_avg = detector_three_avg / three_count
                temp_detector_one.get(run)[block_count - 1].append(detector_one_avg)
                temp_detector_two.get(run)[block_count - 1].append(detector_two_avg)
                temp_detector_three.get(run)[block_count - 1].append(detector_three_avg)
        # Remove the last luminosity block from each run, the one that generally spikes
        temp_detector_one[run] = temp_detector_one[run][:-10]
        temp_detector_two[run] = temp_detector_two[run][:-10]
        temp_detector_three[run] = temp_detector_three[run][:-10]
    # Reassign temp to the original lists
    all_detector_one_data = temp_detector_one
    all_detector_two_data = temp_detector_two
    all_detector_three_data = temp_detector_three

    # Get ratio of the detectors 1 and 2
    luminosity_ratio = []
    lumi_blocks = []
    block_count1 = 0
    for run in sorted(all_detector_one_data.keys()):
        for block in range(len(all_detector_one_data.get(run))):
            block_count1 += 1
            for bcid in range(len(all_detector_one_data.get(run)[block])):
                detector_one_point = all_detector_one_data.get(run)[block][bcid]
                detector_two_point = all_detector_two_data.get(run)[block][bcid]
                # Check if the blocks are zero
                if detector_one_point != 0.0 and detector_two_point != 0.0:
                    ratio = detector_one_point / detector_two_point
                    luminosity_ratio.append(ratio)
                    lumi_blocks.append(block_count1)

    # Get ratio of the detectors 1 and 3
    luminosity_ratio_1 = []
    lumi_blocks_1 = []
    block_count2 = 0
    for run in sorted(all_detector_one_data.keys()):
        for block in range(len(all_detector_one_data.get(run))):
            block_count2 += 1
            for bcid in range(len(all_detector_one_data.get(run)[block])):
                detector_one_point = all_detector_one_data.get(run)[block][bcid]
                detector_three_point = all_detector_three_data.get(run)[block][bcid]
                # Check if the blocks are zero
                if detector_one_point != 0.0 and detector_three_point != 0.0:
                    ratio = detector_one_point / detector_three_point
                    luminosity_ratio_1.append(ratio)
                    lumi_blocks_1.append(block_count2)

    # Get percentage difference based off the first block and BCID
    first_point = luminosity_ratio[0]
    first_point_1 = luminosity_ratio_1[0]

    for index in range(len(luminosity_ratio)):
        luminosity_ratio[index] = 100 * ((luminosity_ratio[index] / first_point) - 1)

    for index in range(len(luminosity_ratio_1)):
        luminosity_ratio_1[index] = 100 * ((luminosity_ratio_1[index] / first_point_1) - 1)

    # create graph
    graph = Graph(len(lumi_blocks))
    for i, (xx, yy) in enumerate(zip(lumi_blocks, luminosity_ratio)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Luminosity Block")
    graph.yaxis.SetTitle("Luminosity [Average Percent Ratio]")
    graph.xaxis.SetRangeUser(min(lumi_blocks), max(lumi_blocks))
    graph.yaxis.SetRangeUser(min(luminosity_ratio), max(luminosity_ratio))

    # plot with ROOT
    canvas = Canvas()

    graph.Draw("AP")
    canvas.Update()

    # add points from detectors 1 and 3
    # create graph
    graph1 = Graph(len(lumi_blocks_1))
    for i, (xx, yy) in enumerate(zip(lumi_blocks_1, luminosity_ratio_1)):
        graph1.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph1.linecolor = 'white'  # Hides the lines at this time
    graph1.markercolor = 'red'
    # graph1.xaxis.SetRangeUser(min(lumi_blocks_1), max(lumi_blocks_1))
    # graph1.yaxis.SetRangeUser(min(luminosity_ratio_1), max(luminosity_ratio_1))

    graph1.Draw("P")
    canvas.Update()
    # Draw lines for different runs
    run_length = 0
    for run in sorted(all_detector_one_data.keys()):
        run_length += len(all_detector_one_data.get(run))
        line = ROOT.TLine(run_length, min(luminosity_ratio),
                          run_length, max(luminosity_ratio))
        line.Draw()
        line_label = ROOT.TText(run_length - 30, max(luminosity_ratio) - 1.5, str(run))
        line_label.SetTextAngle(90)
        line_label.SetTextSize(18)
        line_label.SetTextFont(43)
        line_label.Draw()
    label = ROOT.TText(0.7, 0.8, str(name))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)


def plot_all_integrated_luminosity(all_detector_one_data, all_detector_two_data, all_detector_three_data, block_length,
                                   bcid_status, background_list, style, name):
    '''
    Take all the luminosity ratio for each luminosity block and multiply by the time to get the integrated luminosity
    :param all_detector_one_data: A dictionary of the run name to a list of lists of luminosity blocks
    :param all_detector_two_data: A dictionary of the run name to a list of lists of luminosity blocks
    :param block_length: A dictionary the same length as the detector arrays containing the luminosity block length (time)
    :param style: a string corresponding to a ROOT graphing style, e.g. 'ATLAS'
    :return: Plot of all the detector data on a graph chronologically according to run number
    '''
    # Set ROOT graph style
    set_style(str(style))

    # Get average value of the rate for each luminosity block
    temp_detector_one = copy.deepcopy(all_detector_one_data)
    temp_detector_two = copy.deepcopy(all_detector_two_data)
    temp_detector_three = copy.deepcopy(all_detector_three_data)
    print(sorted(all_detector_one_data.keys()))
    for run in sorted(all_detector_one_data.keys()):
        block_count = 0
        for block in range(len(all_detector_one_data.get(run)) - 1):
            del temp_detector_one.get(run)[block][:]
            del temp_detector_two.get(run)[block][:]
            del temp_detector_three.get(run)[block][:]
            block_count += 1
            detector_one_avg = 0
            one_count = 0
            detector_two_avg = 0
            two_count = 0
            detector_three_avg = 0
            three_count = 0
            for bcid in range(len(all_detector_one_data.get(run)[block])):
                # Gets the previous BCID luminosity to subtract as the background
                if run in background_list:
                    if bcid_status.get(run)[block][bcid - 1] == 0:
                        detector_one_point_background = all_detector_one_data.get(run)[block][bcid - 1]
                        detector_two_point_background = all_detector_two_data.get(run)[block][bcid - 1]
                        detector_three_point_background = all_detector_three_data.get(run)[block][bcid - 1]
                        print("BCID [N-1] Stability: " + str(bcid_status.get(run)[block][bcid - 1]))
                        print("BCID [N] Stability: " + str(bcid_status.get(run)[block][bcid]))
                        detector_one_point = -math.log(1 - all_detector_one_data.get(run)[block][bcid]) \
                                             + math.log(1 - detector_one_point_background)
                        print("Detector 1 Point: " + str(detector_one_point))
                        detector_two_point = -math.log(1 - all_detector_two_data.get(run)[block][bcid]) \
                                             + math.log(1 - detector_two_point_background)
                        print("Detector 2 Point: " + str(detector_two_point))
                        detector_three_point = -math.log(1 - all_detector_three_data.get(run)[block][bcid]) \
                                               + math.log(1 - detector_three_point_background)
                        detector_one_avg += detector_one_point
                        one_count += 1
                        detector_two_avg += detector_two_point
                        two_count += 1
                        detector_three_avg += detector_three_point
                        three_count += 1
                    else:
                        print("No empty BCID to subtract background from")
                        '''
                        print("BCID [N] Stability: " + str(bcid_status.get(run)[block][bcid]))
                        detector_one_point = -math.log(1 - all_detector_one_data.get(run)[block][bcid]) #\
                                             #+ math.log(1 - detector_one_point_background)
                        print("Detector 1 Point: " + str(detector_one_point))
                        detector_two_point = -math.log(1 - all_detector_two_data.get(run)[block][bcid]) #\
                                             #+ math.log(1 - detector_two_point_background)
                        print("Detector 2 Point: " + str(detector_two_point))
                        detector_three_point = -math.log(1 - all_detector_three_data.get(run)[block][bcid]) #\
                                               #+ math.log(1 - detector_three_point_background)
                        detector_one_avg += detector_one_point
                        one_count += 1
                        detector_two_avg += detector_two_point
                        two_count += 1
                        detector_three_avg += detector_three_point
                        three_count += 1
                        '''
                if bcid_status.get(run)[block][bcid] > 0.0:
                    detector_one_point = -math.log(1 - all_detector_one_data.get(run)[block][bcid])
                    detector_two_point = -math.log(1 - all_detector_two_data.get(run)[block][bcid])
                    detector_three_point = -math.log(1 - all_detector_three_data.get(run)[block][bcid])
                    detector_one_avg += detector_one_point
                    one_count += 1
                    detector_two_avg += detector_two_point
                    two_count += 1
                    detector_three_avg += detector_three_point
                    three_count += 1
            if one_count != 0:
                detector_one_avg = detector_one_avg / one_count
                detector_two_avg = detector_two_avg / two_count
                detector_three_avg = detector_three_avg / three_count
                temp_detector_one.get(run)[block_count - 1].append(detector_one_avg)
                temp_detector_two.get(run)[block_count - 1].append(detector_two_avg)
                temp_detector_three.get(run)[block_count - 1].append(detector_three_avg)
        # Remove the last luminosity block from each run, the one that generally spikes
        temp_detector_one[run] = temp_detector_one[run][:-10]
        temp_detector_two[run] = temp_detector_two[run][:-10]
        temp_detector_three[run] = temp_detector_three[run][:-10]
    # Reassign temp to the original lists
    all_detector_one_data = temp_detector_one
    all_detector_two_data = temp_detector_two
    all_detector_three_data = temp_detector_three

    # Get integrated luminosity of the detectors
    integrated_luminosity_one = []
    integrated_luminosity_two = []
    integrated_luminosity_three = []
    luminosity_ratio_two = []
    luminosity_ratio_three = []
    lumi_blocks = []
    block_count1 = 0
    lumi_total = 0
    lumi_total_two = 0
    lumi_total_three = 0
    # To keep track of how long each run actually is when plotting
    run_length_dict = {}
    for run in sorted(all_detector_one_data.keys()):
        run_length_dict[run] = 0
        for block in range(len(all_detector_one_data.get(run))):
            block_count1 += 1
            for bcid in range(len(all_detector_one_data.get(run)[block])):
                detector_one_point = all_detector_one_data.get(run)[block][bcid]
                detector_two_point = all_detector_two_data.get(run)[block][bcid]
                detector_three_point = all_detector_three_data.get(run)[block][bcid]
                if detector_one_point != 0.0 and detector_two_point != 0.0 and detector_three_point != 0.0:
                    # Use conversion factor
                    converted_point_one = convert_to_raw_luminosity(11.245, 20.8, detector_one_point)
                    converted_point_two = convert_to_raw_luminosity(11.245, 20.8, detector_two_point)
                    converted_point_three = convert_to_raw_luminosity(11.245, 20.8, detector_three_point)
                    ratio_one_two = converted_point_one / converted_point_two
                    ratio_one_three = converted_point_one / converted_point_three
                    luminosity_ratio_two.append(ratio_one_two)
                    luminosity_ratio_three.append(ratio_one_three)
                    length = block_length.get(run)[block][bcid]
                    lumi_total += converted_point_one * length
                    lumi_total_two += converted_point_two * length
                    lumi_total_three += converted_point_three * length
                    integrated_luminosity_one.append(lumi_total)
                    integrated_luminosity_two.append(lumi_total_two)
                    integrated_luminosity_three.append(lumi_total_three)
                    lumi_blocks.append(block_count1)
                    run_length_dict[run] += 1

    # Get percentage difference based off the first block and BCID
    first_point = luminosity_ratio_two[0]
    first_point_three = luminosity_ratio_three[0]

    for index in range(len(integrated_luminosity_one)):
        luminosity_ratio_two[index] = 100 * ((luminosity_ratio_two[index] / first_point) - 1)
        luminosity_ratio_three[index] = 100 * ((luminosity_ratio_three[index] / first_point) - 1)

    # create graph
    graph = Graph(len(integrated_luminosity_one))
    for i, (xx, yy) in enumerate(zip(integrated_luminosity_one, luminosity_ratio_two)):
        graph.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    # Set temp list for the min and max functions
    luminosity_ratio = luminosity_ratio_two + luminosity_ratio_three
    integrated_luminosity = integrated_luminosity_one

    graph.markercolor = 'blue'
    graph.yaxis.SetTitle("Luminosity Ratio [Percent]")
    graph.xaxis.SetTitle("Luminosity [Integrated]")
    graph.yaxis.SetRangeUser(min(luminosity_ratio),
                             max(luminosity_ratio))
    graph.xaxis.SetRangeUser(min(integrated_luminosity),
                             max(integrated_luminosity))

    # plot with ROOT
    canvas = Canvas()

    graph.Draw("AP")
    canvas.Update()

    # add points from detectors 1 and 3
    # create graph
    graph1 = Graph(len(integrated_luminosity_one))
    for i, (xx, yy) in enumerate(zip(integrated_luminosity_one, luminosity_ratio_three)):
        graph1.SetPoint(i, float(xx), float(yy))

    # set visual attributes

    graph1.linecolor = 'white'  # Hides the lines at this time
    graph1.markercolor = 'red'

    graph1.Draw("P")
    canvas.Update()
    # Draw lines for different runs
    run_length = 0
    total_length = 0
    num_run = 0
    print"Integrated Luminosity length: ",len(integrated_luminosity)
    for run in sorted(all_detector_one_data.keys()):
        print str(run)
        total_length += run_length_dict[run]
        print"Total Length: ",total_length
        run_length = integrated_luminosity_one[total_length - 1]
        print"Run Length", run_length
        line = ROOT.TLine(run_length, min(luminosity_ratio),
                          run_length, max(luminosity_ratio))
        line.Draw()
        line_label = ROOT.TText(run_length - 30, max(luminosity_ratio) - 1.5, str(run))
        line_label.SetTextAngle(90)
        line_label.SetTextSize(18)
        line_label.SetTextFont(43)
        line_label.Draw()
    label = ROOT.TText(0.7, 0.9, str(name))
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

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("BCM V [Raw Rate]")
    graph.yaxis.SetTitle("LUCID BI [Raw Rate]")
    graph.xaxis.SetRangeUser(0, 1)
    graph.yaxis.SetRangeUser(0, 1)

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("AP")
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

    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("BCM V")
    graph.yaxis.SetTitle("LUCID BI")
    graph.xaxis.SetRangeUser(min(detector_two_list), max(detector_two_list))
    graph.yaxis.SetRangeUser(min(detector_one_list), max(detector_one_list))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("AP")
    label = ROOT.TText(0.8, 0.9, str(name))
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()
    wait(True)
