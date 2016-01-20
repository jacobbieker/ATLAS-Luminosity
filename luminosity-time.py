__author__ = 'Jacob Bieker'
#import rootpy as ROOT
import os
import glob

# Go through each directory of luminosity data

# ATLAS 4557 Data
atlas_4557_data = glob.iglob(os.path.join("data", "4557", "4557_lumi_*_ATLAS.txt"))

for atlas_file in atlas_4557_data:
    with open(atlas_file, 'r') as data:
        print("Opened " + str(atlas_file) + "\n")
