__author__ = 'Jacob Bieker'
#import rootpy as ROOT
import os
import re
import glob
# Go through each directory of luminosity data

atlas_4557_data = glob.iglob(os.path.join("data", "4557", "4557_lumi_*_ATLAS.txt"))
