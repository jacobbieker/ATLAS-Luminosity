__author__ = 'jacob'
import tarfile
import glob
import os

atlas_filenames = glob.iglob(os.path.join("data", "atlas", "*.tgz"))
cms_filenames = glob.iglob(os.path.join("data", "cms", "*.tgz"))

for fname in atlas_filenames:
    tar = tarfile.open(fname, "r:gz")
    tar.extractall(path=os.path.join("data", "atlas"))
    tar.close()

for fname in cms_filenames:
    tar = tarfile.open(fname, "r:gz")
    tar.extractall(path=os.path.join("data", "cms"))
    tar.close()