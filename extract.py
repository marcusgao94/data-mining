import tarfile
import os
path = '../data/'
years = os.listdir(path)
for year in years:
    p = os.path.join(path, year)
    print year
    tgzs = os.listdir(p)
    for tgz in tgzs:
        if tgz.endswith('.tgz'):
            filepath = os.path.join(p, tgz)
            tar = tarfile.open(filepath)
            tar.extractall(p)
            os.remove(filepath)
            print filepath