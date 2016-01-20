__author__ = 'Jacob Bieker'
#import rootpy as ROOT
import os
import glob

# Go through each directory of luminosity data

# ATLAS 4557 Data
atlas_4557_data = glob.iglob(os.path.join("data", "4557", "4557_lumi_*_ATLAS.txt"))

atlas_timing = {}
cms_timing = {}

for atlas_file in atlas_4557_data:
    with open(atlas_file, 'r') as data:
        print("Opened " + str(atlas_file) + "\n")
        for line in data:
            event_data = line.split(" ")
            if int(event_data[1]) == 1: # Check if ATLAS (=1) or CMS (=5)
                atlas_timing[int(event_data[0])] = event_data[2] # Add instantaneous luminosity to the dictionary
            elif int(event_data[1]) == 5:
                cms_timing[int(event_data[0])] = event_data[2]
