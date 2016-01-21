__author__ = 'Jacob Bieker'
import ROOT
import numpy as np
from rootpy.plotting import Canvas, Graph
from rootpy.plotting.style import get_style, set_style
from rootpy.interactive import wait
import rootpy.plotting.root2matplotlib as rplt
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import os
import glob


# Functions to graph luminosity data
def luminosity_vs_time(timing_list, luminosity_list, style):
    # Set ROOT graph style
    set_style(str(style))

    # create graph
    graph = Graph(len(timing_list))
    for i, (xx, yy) in enumerate(zip(timing_list, luminosity_list)):
        graph.SetPoint(i, xx, yy)

        # set visual attributes
    graph.linecolor = 'blue'
    graph.markercolor = 'blue'
    graph.xaxis.SetTitle("Time")
    graph.yaxis.SetTitle("Luminosity")
    graph.xaxis.SetRangeUser(min(timing_list), max(timing_list))
    graph.yaxis.SetRangeUser(min(luminosity_list), max(luminosity_list))

    # plot with ROOT
    canvas = Canvas()
    graph.Draw("APL")

    label = ROOT.TText(0.4, 0.8, "ROOT")
    label.SetTextFont(43)
    label.SetTextSize(25)
    label.SetNDC()
    label.Draw()
    canvas.Modified()
    canvas.Update()

# Go through each directory of luminosity data

# ATLAS 4557 Data
atlas_4557_data = glob.iglob(os.path.join("data", "4557", "4557_lumi_*_ATLAS.txt"))

atlas_timing = []
atlas_luminosity = []
cms_timing = []
cms_luminosity = []

for atlas_file in atlas_4557_data:
    with open(atlas_file, 'r') as data:
        print("Opened " + str(atlas_file) + "\n")
        for line in data:
            event_data = line.split(" ")
            if int(event_data[1]) == 1: # Check if ATLAS (=1) or CMS (=5)
                atlas_timing.append(int(event_data[0])) # Add timing data to array
                atlas_luminosity.append(event_data[2]) # Add instantaneous luminosity to array
            elif int(event_data[1]) == 5:
                cms_timing.append(int(event_data[0]))
                cms_luminosity.append(int(event_data[2]))