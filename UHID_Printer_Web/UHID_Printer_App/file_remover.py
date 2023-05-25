import os
import glob

files = glob.glob('/pdf/*')
for f in files:
    print(f)
    os.remove(f)