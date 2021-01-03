import os
import glob

def remove_local_file(filepath='./dags/data/*.csv'):
    files = glob.glob(filepath)
    for f in files:
        os.remove(f)


